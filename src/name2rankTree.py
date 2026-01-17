import pandas as pd
import numpy as np
import re
from jamo import h2j, j2hcj
from gensim.models import FastText
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

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
    # '닉네임' 컬럼 이름을 본인의 엑셀 컬럼명에 맞게 수정하세요 (예: 'Name')
    nicknames_in_sheet = sheet['name'].dropna().tolist()
    all_nicknames.extend(nicknames_in_sheet)
    all_labels.extend([sheet_name] * len(nicknames_in_sheet)) # 시트 이름을 라벨(랭크)로 사용

tokenized_data = [preprocess_nickname(name) for name in all_nicknames]

# 2. fastText 학습
print("fastText 학습 시작 (자모 단위)...")
model = FastText(sentences=tokenized_data, vector_size=64, window=3, min_count=1, sg=1, epochs=50)

# 3. 닉네임을 벡터로 변환
nickname_vectors = np.array([model.wv.get_mean_vector(name) for name in tokenized_data])




# 1. 데이터 준비 (X: 벡터, y: 랭크 라벨)
# nickname_vectors는 이전 단계에서 생성된 (9000, 64) 형태의 배열입니다.
X = nickname_vectors
y = np.array(all_labels)

# 랭크 텍스트(Challenger, Iron 등)를 숫자로 변환
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 2. 학습 데이터와 테스트 데이터 분리 (8:2 비율)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# 3. 랜덤 포레스트 모델 학습
print("머신러닝 모델 학습 중...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)

# 4. 모델 평가
y_pred = rf_model.predict(X_test)

print("\n[ 모델 평가 결과 ]")
print(f"전체 정확도(Accuracy): {accuracy_score(y_test, y_pred):.4f}")
print("\n[ 클래스별 상세 리포트 ]")
print(classification_report(y_test, y_pred, target_names=le.classes_))