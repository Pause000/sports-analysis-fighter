import pandas as pd
import json
import re
import time
import os
import unicodedata
from openai import OpenAI
from tqdm import tqdm # [추가] 진행 상황을 보기 위해 필요합니다

# ==========================================
# 1. 초기 설정 및 텍스트 정규화
# ==========================================
def normalize_nfc(text):
    if isinstance(text, str):
        return unicodedata.normalize('NFC', text)
    return text

# 데이터 로드 (원본의 모든 행과 순서를 유지합니다)
input_path = ''
df = pd.read_csv(input_path)

# 모든 텍스트 컬럼 정규화
for col in ['질문', '매칭팀', '기존 응원 팀']:
    df[col] = df[col].apply(normalize_nfc)

# LLM 평가 결과를 담을 새로운 컬럼 생성 (기본값 설정)
df['llm_confidence'] = 0.0
df['llm_rank'] = 0
df['llm_reason'] = "분석 실패 또는 신뢰도 낮음"
df['label'] = 0 # 랭킹 모델 학습용 라벨

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# ==========================================
# 2. 질문 및 리그별 순차 처리 (sort=False로 순서 보장)
# ==========================================
# 질문(시나리오) 단위로 그룹화
groups = df.groupby(['질문', '기존 응원 팀'], sort=False, dropna=False)

print(f"🚀 총 {len(groups)}개 시나리오 전수 평가 시작 (목표 행 수: {len(df)}행)")

for i, ((query, anchor), scenario_group) in enumerate(groups):
    print(f"\n분석 중 [{i+1}/{len(groups)}] : {query[:40]}...")
    
    # 시나리오 내에서 리그별로 다시 그룹화
    league_groups = scenario_group.groupby('추천 리그', sort=False)
    
    for league_name, league_data in league_groups:
        # 현재 리그에 속한 후보 팀들의 인덱스와 팀명 추출
        candidates = league_data[['매칭팀']].to_dict('records')
        team_names = [c['매칭팀'] for c in candidates]
        
        prompt = f"""
        사용자 질문: {query}
        리그: {league_name}
        후보 팀명: {', '.join(team_names)}
        
        위 팀들의 적합도를 각각 0~1 사이 점수(confidence)로 평가하고 JSON 리스트로 답변하세요.
        반드시 제공된 '팀명'을 정확하게 사용해야 합니다.
        
        예시: [{{ "team": "팀명", "confidence": 0.85, "reason": "..." }}, ...]
        """
        
        try:
            response = client.chat.completions.create(
                model="local-model",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            content = response.choices[0].message.content
            json_match = re.search(r'\[\s*\{.*\}\s*\]', content, re.DOTALL)
            
            if json_match:
                results = json.loads(json_match.group())
                # LLM 결과 반영
                for res in results:
                    target_team = normalize_nfc(res['team'])
                    # 해당 질문/리그 내에서 팀명이 일치하는 행의 인덱스를 찾아 업데이트
                    idx = league_data[league_data['매칭팀'] == target_team].index
                    if not idx.empty:
                        conf = res.get('confidence', 0)
                        df.loc[idx, 'llm_confidence'] = conf
                        df.loc[idx, 'llm_reason'] = res.get('reason', '')
                
                # 해당 리그 내에서 순위(Rank) 계산 후 업데이트
                league_indices = league_data.index
                df.loc[league_indices, 'llm_rank'] = df.loc[league_indices, 'llm_confidence'].rank(ascending=False, method='min').astype(int)
                
                print(f"   ✅ [{league_name:10}] {len(candidates)}개 팀 평가 완료")
            else:
                print(f"   ❌ [{league_name:10}] JSON 파싱 실패")
        except Exception as e:
            print(f"   ⚠️ [{league_name:10}] 서버 통신 오류: {e}")

# ==========================================
# 3. 최종 결과 저장 (입력과 동일한 순서/행수)
# ==========================================
output_path = 'final_labeled_data.csv'
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("-" * 60)
print(f"✨ 작업 완료! 입력값과 동일한 {len(df)}행의 데이터가 저장되었습니다.")
print(f"💾 파일 경로: {output_path}")