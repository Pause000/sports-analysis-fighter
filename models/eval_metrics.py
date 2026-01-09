import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import ndcg_score

def calculate_mean_ndcg(df, preds_col):
    """
    제공된 데이터프레임에서 질문(query)별로 NDCG를 계산하여 평균을 냅니다.
    기존 코드의 계산 로직을 그대로 함수화했습니다.
    """
    return np.mean([
        ndcg_score([sub["relevance"]], [sub[preds_col]]) 
        for _, sub in df.groupby("query") if len(sub) > 1
    ])

def plot_feature_importance(model, features, title):
    """
    최종 모델의 피처 중요도를 시각화합니다.
    """
    plt.figure(figsize=(12, 8))
    feat_imp = pd.Series(model.feature_importances_, index=features).sort_values(ascending=False)
    sns.barplot(x=feat_imp, y=feat_imp.index, palette='viridis')
    plt.title(title)
    plt.show()