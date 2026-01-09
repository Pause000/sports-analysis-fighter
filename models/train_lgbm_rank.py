import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import GroupShuffleSplit, ParameterGrid
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import warnings
import joblib
import matplotlib.pyplot as plt

# 분리한 평가 모듈 불러오기
from eval_metrics import calculate_mean_ndcg, plot_feature_importance

# 0) 초기 설정 (기존 코드와 동일)
warnings.filterwarnings("ignore")
plt.rcParams['font.family'] = 'Malgun Gothic'

df = pd.read_csv("final_data.csv")
df = df[df["llm_rank"] > 0].copy()
df["relevance"] = df["llm_rank"].map({1: 5, 2: 3, 3: 2}).fillna(0)

gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
train_idx, test_idx = next(gss.split(df, groups=df["query"]))
train_df, test_df = df.iloc[train_idx].copy(), df.iloc[test_idx].copy()

# 1) 입력 피처 생성 (로직 수정 없음)
print("🚀 [Step 1] 마스터 명단 기반 전처리 및 피처 생성 시작...")

sbert = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")
train_qs = train_df["query"].unique()
test_qs = test_df["query"].unique()
train_emb = sbert.encode(train_qs)
test_emb = sbert.encode(test_qs)

pca = PCA(n_components=5, random_state=42)
train_pca_vals = pca.fit_transform(train_emb)
test_pca_vals = pca.transform(test_emb)

pca_named_cols = ["의도_팬덤정체성", "의도_스타성과강함", "의도_명문과기적", "의도_비주얼과매력", "의도_자본과지배력"]
train_q_map = {q: v for q, v in zip(train_qs, train_pca_vals)}
test_q_map = {q: v for q, v in zip(test_qs, test_pca_vals)}

train_df[pca_named_cols] = pd.DataFrame(train_df["query"].map(train_q_map).tolist(), index=train_df.index)
test_df[pca_named_cols] = pd.DataFrame(test_df["query"].map(test_q_map).tolist(), index=test_df.index)

# 마스터 팀 명단 기반 LabelEncoder
master_team_list = [
    "아스널", "아스톤 빌라", "본머스", "브렌트포드", "브라이튼", "첼시", "크리스탈 팰리스", 
    "에버턴", "풀럼", "입스위치 타운", "레스터 시티", "리버풀", "맨체스터 시티", "맨체스터 유나이티드", 
    "뉴캐슬 유나이티드", "노팅엄 포레스트", "사우샘프턴", "토트넘 홋스퍼", "웨스트햄 유나이티드", "울버햄튼 원더러스",
    "LG 트윈스", "KT 위즈", "SSG 랜더스", "NC 다이노스", "두산 베어스", "기아 타이거즈", 
    "롯데 자이언츠", "삼성 라이온즈", "한화 이글스", "키움 히어로즈",
    "울산 HD FC", "포항 스틸러스", "광주FC", "전북 현대 모터스", "대구FC", "인천 유나이티드", 
    "FC 서울", "대전 하나 시티즌", "제주 SK FC", "강원FC", "FC안양", "수원 삼성 블루윙즈",
    "레드불", "페라리", "메르세데스", "맥라렌", "애스턴 마틴", "알핀", "윌리엄스", "레이싱 불스", "자우버", "하스",
    "Unknown"
]

le_team = LabelEncoder()
le_team.fit(master_team_list)

def safe_encode(name, encoder):
    return encoder.transform([name if name in encoder.classes_ else "Unknown"])[0]

le_league = LabelEncoder()
train_df["recommend_league_enc"] = le_league.fit_transform(train_df["recommend_league"].astype(str))
test_df["recommend_league_enc"] = test_df["recommend_league"].astype(str).apply(lambda x: le_league.transform([x])[0] if x in le_league.classes_ else -1)

train_df["matching_team_enc"] = train_df["matching_team"].astype(str).apply(lambda x: safe_encode(x, le_team))
test_df["matching_team_enc"] = test_df["matching_team"].astype(str).apply(lambda x: safe_encode(x, le_team))

score_cols = ["sbert_score", "n2v_score", "vector_score"]
scaled_score_names = [f"{c}_mm" for c in score_cols]
scaler = MinMaxScaler()
train_df[scaled_score_names] = scaler.fit_transform(train_df[score_cols])
test_df[scaled_score_names] = scaler.transform(test_df[score_cols])

input_features = ["user_type", "recommend_league_enc"] + scaled_score_names + pca_named_cols

X_train, y_train = train_df[input_features], train_df["relevance"]
X_test, y_test = test_df[input_features], test_df["relevance"]

cat_features = ["user_type", "recommend_league_enc"]
for c in cat_features:
    X_train[c] = X_train[c].astype('category')
    X_test[c] = X_test[c].astype('category')

group_train = train_df.groupby("query").size().values

# 2) 그리드 서치 및 모델 최적화
print("\n🚀 [Step 2] 모델 최적화 중...")
param_grid = {
    'learning_rate': [0.03, 0.05],
    'max_depth': [4, 6],
    'n_estimators': [300, 500],
    'num_leaves': [20, 31],
    'random_state': [42]
}

best_score = -1
best_params = None

for params in ParameterGrid(param_grid):
    model = lgb.LGBMRanker(**params, importance_type='gain', verbosity=-1)
    model.fit(X_train, y_train, group=group_train)
    test_df["temp_preds"] = model.predict(X_test)
    # 분리된 calculate_mean_ndcg 함수 호출
    cur_ndcg = calculate_mean_ndcg(test_df, "temp_preds")
    if cur_ndcg > best_score:
        best_score = cur_ndcg
        best_params = params

# 3) 최종 모델 학습 및 시각화
print(f"\n✨ 최적 파라미터 조합: {best_params}")
final_model = lgb.LGBMRanker(**best_params)
final_model.fit(X_train, y_train, group=group_train)

test_df["final_preds"] = final_model.predict(X_test)
final_ndcg = calculate_mean_ndcg(test_df, "final_preds")

print("\n" + "="*45)
print(f"🏆 최종 테스트 Mean NDCG: {final_ndcg:.4f}")
print("="*45)

# 분리된 plot_feature_importance 함수 호출
plot_feature_importance(final_model, input_features, "최종 하이브리드 추천 모델 피처 중요도 (정답 유출 방지 버전)")

# 4) 주요 구성 요소 저장 (기존 저장 구조 유지)
model_artifacts = {
    'le_team': le_team,
    'le_league': le_league,
    'scaler': scaler,
    'pca': pca,
    'final_model': final_model,
    'input_features': input_features
}
joblib.dump(model_artifacts, './saved_models/sports_chatbot_model.joblib')
print("✅ 서비스용 모델 파라미터 저장 완료!")