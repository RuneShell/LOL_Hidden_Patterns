import pandas as pd
import numpy as np
from jamo import h2j, j2hcj
from gensim.models import FastText
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import plotly.express as px

# 1. 데이터 통합 및 전처리
file_path = 'output.xlsx'
data = pd.read_excel(file_path, sheet_name=None)

all_nicknames = []
all_labels = []

def preprocess_nickname(text):
    if not isinstance(text, str): return []
    return list(j2hcj(h2j(text)))

print("데이터 로딩 중...")
for sheet_name, sheet in data.items():
    nicknames_in_sheet = sheet['name'].dropna().tolist()
    all_nicknames.extend(nicknames_in_sheet)
    all_labels.extend([sheet_name] * len(nicknames_in_sheet)) # 시트 이름을 라벨(랭크)로 사용

tokenized_data = [preprocess_nickname(name) for name in all_nicknames]

# 2. fastText 학습
print("fastText 학습 시작 (자모 단위)...")
model = FastText(sentences=tokenized_data, vector_size=64, window=3, min_count=1, sg=1, epochs=50)

# 3. 닉네임을 벡터로 변환
nickname_vectors = np.array([model.wv.get_mean_vector(name) for name in tokenized_data])

# 4. T-SNE 차원 축소 (시각화용)
print("T-SNE 차원 축소 중 (시간이 조금 걸릴 수 있습니다)...")
tsne = TSNE(n_components=2, random_state=42)
vectors_2d = tsne.fit_transform(nickname_vectors)

# 5. Plotly용 데이터프레임 생성
# 시각화할 때 닉네임과 랭크 정보를 함께 전달하기 위해 DF로 만듭니다.
df_vis = pd.DataFrame({
    'x': vectors_2d[:, 0],
    'y': vectors_2d[:, 1],
    'Nickname': all_nicknames,
    'Rank': all_labels
})

# 6. Plotly 인터랙티브 시각화
print("시각화 실행 중...")
fig = px.scatter(
    df_vis, 
    x='x', 
    y='y', 
    color='Rank',           # 랭크별 색상 구분
    hover_name='Nickname',  # 마우스를 올렸을 때 굵게 표시될 제목
    hover_data={'x': False, 'y': False, 'Rank': True}, # 추가 표시 정보
    title="게임 랭크별 닉네임 임베딩 클러스터 (Hover to see Name)",
    labels={'x': 'TSNE-1', 'y': 'TSNE-2'},
    template='plotly_white'
)

# 점 크기 및 투명도 조절
fig.update_traces(marker=dict(size=6, opacity=0.6))

# 그래프 출력 (브라우저가 열립니다)
fig.show()
# 코드 마지막 줄에 추가
fig.write_html("nickname_analysis.html")