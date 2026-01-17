import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# 1. 데이터 통합 및 전처리
file_path = 'output_total_input.xlsx'
data = pd.read_excel(file_path, sheet_name=None)

df = None

print("데이터 로딩 중...")
for sheet_name, sheet in data.items():
    if(sheet_name == "Challenger"):
        df = sheet
        break
# ---------------------------------------------------------
# 2. 데이터 전처리
# ---------------------------------------------------------
# 승률(%)을 소수점으로 변환
df['win_rate'] = df['win_rate'].str.replace('%', '').astype(float) / 100

# 한글 폰트 설정 (그래프 깨짐 방지 - Windows 기준 'Malgun Gothic', Mac은 'AppleGothic')
plt.rc('font', family='Malgun Gothic') 
plt.rcParams['axes.unicode_minus'] = False

print("=== 데이터 미리보기 ===")
print(df.head())
print("-" * 30)

# ---------------------------------------------------------
# 3. 분석 1: 수치형 데이터 간의 상관관계 (Heatmap)
# ---------------------------------------------------------
# 수치형 컬럼만 선택
numeric_df = df[['LP', 'level', 'win', 'lose', 'games', 'win_rate']]
corr_matrix = numeric_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('수치형 변수 간 상관관계 히트맵')
plt.show()

# ---------------------------------------------------------
# 4. 분석 2: 범주형 데이터 간 연관성 (Cramer's V)
# 예: 역할군(role)과 닉네임 유형(nick_type)이 관련이 있을까?
# ---------------------------------------------------------
def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    return np.sqrt(phi2 / min(k-1, r-1))

# 예시: 역할군과 닉네임 유형의 연관성
assoc_score = cramers_v(df['position'], df['type'])
print(f"=== 범주형 연관성 분석 (Cramer's V) ===")
print(f"역할군 vs 닉네임 유형 연관성 점수: {assoc_score:.4f} (0~1 사이, 1에 가까울수록 강한 연관)")
print("-" * 30)

# ---------------------------------------------------------
# 5. 분석 3: 머신러닝(Random Forest)을 이용한 중요도 분석
# 목표: 어떤 항목이 '승률(win_rate)'에 가장 큰 영향을 주는가?
# ---------------------------------------------------------
# 범주형 데이터를 숫자로 변환 (Label Encoding)
le = LabelEncoder()
df_ml = df.copy()
cols_to_encode = ['most1', 'position', 'type'] # tier는 값이 모두 같아서 제외

for col in cols_to_encode:
    df_ml[col] = le.fit_transform(df_ml[col])

# X: 특성, y: 타겟(승률)
X = df_ml[['LP', 'level', 'win', 'lose', 'position', 'type']] 
y = df_ml['win_rate']

# 모델 학습
print("모델 생성")
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X, y)

# 중요도 시각화
print("시각화")
importances = pd.Series(rf.feature_importances_, index=X.columns)
importances = importances.sort_values(ascending=False)
print("표 생성")
plt.figure(figsize=(8, 5))
importances.plot(kind='bar', color='skyblue')
plt.title('승률(Win Rate)에 영향을 미치는 요인 중요도')
plt.ylabel('중요도 (Importance)')
plt.show()