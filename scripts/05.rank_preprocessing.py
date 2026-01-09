import pandas as pd

# 1. 데이터 로드
df = pd.read_csv('final_integrated_data.csv')

# 2. '기존 응원 팀'의 빈 값을 처리하여 그룹화 오류 방지
df_temp = df.copy()
df_temp['기존 응원 팀'] = df_temp['기존 응원 팀'].fillna('None')

# 3. 질문 블록 ID 생성
group_cols = ['사용자 유형', '기존 응원 팀', '질문']
df['question_id'] = (df_temp[group_cols] != df_temp[group_cols].shift()).any(axis=1).cumsum()

# 4. 재랭킹 함수 수정
def rerank_by_league(group):
    # confidence(내림차순) -> 매칭 스코어(내림차순) 순으로 정렬
    group = group.sort_values(by=['llm_confidence', '매칭 스코어'], ascending=[False, False])
    
    # 기본적으로 1, 2, 3... 순위 부여
    group['llm_rank'] = range(1, len(group) + 1)
    
    # 추가 수정: llm_confidence가 0인 경우 llm_rank를 0으로 변경
    group.loc[group['llm_confidence'] == 0, 'llm_rank'] = 0
    
    return group

# 5. 질문별 & 리그별 그룹화 및 재랭킹 적용
df_final = df.groupby(['question_id', '추천 리그'], group_keys=False).apply(rerank_by_league)

# 6. 원본 질문 순서 보존 및 정렬
df_final = df_final.sort_values(by=['question_id', '추천 리그', 'llm_rank']).drop(columns=['question_id'])

# 7. 최종 결과 저장
df_final.to_csv('final_data.csv', index=False)