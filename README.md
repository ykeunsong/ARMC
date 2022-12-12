# ARMC
AI-based android malicious app detection

## 방법론
1. 악성앱 동향 분석 : 논문 리뷰, 악성앱 분류 → 악성여부 점검

악성앱 분류 생략 → 악성앱 동향 분석 및 분류보다 피쳐추출 및 분류기 제작 중심

2. 앱으로부터 피쳐 추출

정적분석 : APK빌드 사용자 서명, 요구 권한, 사용 API리스트, 앱 문자열 집합, 실행명령어 집합, 실행파일 바이트 분포, 실행파일 이미지 등
동적분석 : 실제 동작하면서 요구하는 권한, 네트워크 접근여부, 네트워크 트래픽, 웹 요청, 파일 접근, 실제 실행되는 실행명령어(후킹 필요)

3. 추출한 피쳐를 이용한 악성코드 분류기 제작

SVM, Random Forest, XGBoost, DNN
CNN+DNN(바이너리 이미지)
RNN 등(명령어 집합)

### 피쳐추출

APK압축해제 후 코드부분(DEX)와 설정파일(Manifest.xml) 분리
추줄한 DEX파일에서 API정보 파싱 : 악성앱에서 주로 사용하는 API만 추출
설정파일에서 요구하는 권한 추출 : 전체 권한과 악성앱에서 주로 사용하는 권한 추출
DEX파일 크기 및 엔트로피 계산
DEX파일 바이너리 → 이미지로 변환

CNN+DNN : DEX바이너리 이미지 분류결과(logit함수, 악성/정상 정도)를 분류기의 피쳐로 사용

### 분류기

Random Forest : 복잡한 데이터셋 학습 가능, 튜닝이 간단
XGBoost : RF와 마찬가지로 앙상블 방식, 일반적으로 RF보다 강력하나 튜닝이 어려움
DNN : 기존방식과 비교, 2-layer, 3-layer 비교
SVM : 전통적인 방식

이상의 4개 분류기 학습 후 4개 분류기 투표
앙상블 방식을 적극 사용하고(RF, XGB, 투표) 모델 복잡도 규제도 실시하여(DNN에서 l1, l2 및 dropout) 오버피팅 방지

## 데이터셋 분석

학습용 데이터 6,000개(정상 4,000 악성 2,000) 제출용 데이터 2000개
악성 학습데이터에서 CRC오류 및 DEX파일이 없는 앱 2개를 제외, 5,998개 이용
악성앱과 관련된 문자열 분석 → 이를 포함한 앱이 적어 피쳐에서 제외


권한 목록 : 전체 권한 vs 악성앱 관련권한 성능 비교시 후자가 우수

API목록 및 권한목록에서 정답지와 상관관계 부족한 피쳐는 제외 → 110개

### 데이터셋 분석(1)
DEX파일 엔트로피 분석 : 파일의 바이트단위의 무질서도를 측정 → 서로 다른 파일형식은 서로 다른 엔트로피를 가짐 
DEX파일크기 분석 : 윈도우 악성파일 → 작은 크기
![image](https://user-images.githubusercontent.com/119989103/206964763-4c508291-7d24-4bf4-a76f-9dbba226001f.png)
![image](https://user-images.githubusercontent.com/119989103/206964775-7704c604-79ac-46de-91c0-94504eea2aef.png)
출처 : https://www.kennethghartman.com/shannon-entropy-of-file-formats/

### 데이터셋 분석(2)
엔트로피와 파일크기 추출 후 비교 : 악성앱(우측)의 크기가 작고 정상앱이 엔트로피 분포가 보다 다양함(좌측)

![image](https://user-images.githubusercontent.com/119989103/206964901-426ea56c-7ddf-48d2-9ddd-26820ede6cf5.png)
![image](https://user-images.githubusercontent.com/119989103/206964911-091f794f-0cc8-454d-996d-9de6cf08dcf0.png)

### 데이터셋 분석(3)
DEX 바이너리 파일 이미지 : 안드로이드앱의 Family 분류에 좋은 성능을 보인다고 알려져있음

![image](https://user-images.githubusercontent.com/119989103/206964974-a2090e2d-398e-43dc-b7dd-9d364fdefd05.png)
source : TonTon Hsien-De Huang, “R2-D2: ColoR -inspired Convolutional NeuRal Network(CNN)-based AndroiD malware Detections”, 2018

Normal application
![image](https://user-images.githubusercontent.com/119989103/206964985-895d84e7-b84d-4d2e-b27e-bafa80343ef8.png)

Malicious application
![image](https://user-images.githubusercontent.com/119989103/206964997-c9df431a-594c-4a92-b5c3-e3d1ae120961.png)

## 프로그램 구성
앞부분 test data set를 CNN+DNN을 이용하여 피쳐로 사용했으며,  엔트로피와 파일크기 추출하는 부분도 별도로 구현

![image](https://user-images.githubusercontent.com/119989103/206965139-6f6b929c-a6ba-452a-9a5b-3691f5b428c7.png)

### DNN (3-layer)
층이 3개인것과 2개인것을 비교.
텐서플로우로 저수준 API로 구현. 
초기에는 110개 입력값과 3개의 Fully Connected Layer[FC]와 2개의 출력값을  각각 90개 노드를 가지는 것으로 설계를 하였으나
최종적으로 FC 2개 레이어와 각각 200개 노드를 가지는 것으로 설계하였습니다. 
과적합을 피하기 위해 Dropout과 L1, L2규제를 적용하였습니다. 

![image](https://user-images.githubusercontent.com/119989103/206965233-10a7d7ce-cf83-4dfe-bfc1-fce66206fe56.png)

## Traditional Classifier
XGB : 그리드 탐색 실시(max_depth=9, learning_rate=0.01, objective=’binary:logistic’, booster=’gbtree’, n_estimators=2000)
RF : 사전 시행착오, estimator=200
SVM : C값과 감마값 각각 1000, 0.001

투표기 : 4개 중 2개 이상 악성

파라미터값 튜닝을 위해서 그리드 탐색을 실시하였고
탐색 결과로 가장 좋은 성능을 보인 파라미터는 다음과 같다.

RF와 SVM은 그리드 탐색을 따로 하지 않고 시행차공.

## 실행결과
* 10-Fold
* DNN 모델링 실험
![image](https://user-images.githubusercontent.com/119989103/206965774-a3166494-7c64-4f13-a307-f6cfc92b5fed.png)

* XGB 그리드 탐색

>Best parameters set found on development set:
>{'booster': 'gbtree', 'learning_rate': 0.01, 'max_depth': 8, 'n_estimators': 2000, 'nthread': 4}
>Grid scores on development set:
>0.987 (+/-0.002) for {'booster': 'gbtree', 'learning_rate': 0.05, 'max_depth': 7, 'n_estimators': 2000, 'nthread': 4}
>0.987 (+/-0.001) for {'booster': 'gbtree', 'learning_rate': 0.05, 'max_depth': 8, 'n_estimators': 2000, 'nthread': 4}

## 정답지 및 분류기별 예측치 상관관계
실험결과에 대해 분류기별 예측치 상관분석
![image](https://user-images.githubusercontent.com/119989103/206966289-dd769fa9-3cbf-499b-ac8c-67431f7d520c.png)

SVM과 기타 분류기간 상관관계가 낮음
상관관계가 낮으면 투표기를 사용하는 것이 이득이기에 투표기를 제작

## 최종평가
예선 : 95.7%
||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|191|18|
|Test-Bengin|8|382|

1st 본선(add imaged DEX classifier) : 95.99%

||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|192|17|
|Test-Bengin|7|383|

2nd 본선(add 2,000 dataset) : 96.9%

||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|266|18|
|Test-Bengin|7|508|
