# ARMC
AI-based android malicious app detection

[ARMC.ipynb](https://github.com/ykeunsong/ARMC/blob/main/ARMC.ipynb) : executable code

[ARMC_train.ipynb](https://github.com/ykeunsong/ARMC/blob/main/ARMC_train.ipynb) : training code

## Introduction
1. Malicious app trend research
* review of papers, classification of malicious apps 
* Malicious app classification omitted → Focus on feature extraction and classifier production rather than malicious app trend analysis and classification

2. Extract features from apps
* Static analysis: APK build user signature, required authority, used API list, application string set, execution command set, execution file byte distribution, execution file image, etc.
* Dynamic analysis: Permissions required during actual operation, network access, network traffic, web requests, file access, actually executed commands (requires hooking)

3. Creating a Malicious Code Classifier Using the Extracted Features
* SVM, Random Forest, XGBoost, DNN
* CNN+DNN (for binary image)
* RNNs, etc. (instruction set) : Future work

### Feature extraction
* After decompressing the APK, separate the code part (DEX) and the configuration file (Manifest.xml)
* Parsing API information from the extracted DEX file: Extracting only APIs mainly used by malicious apps
* Extraction of permissions required by the configuration file: Extraction of all permissions and permissions mainly used by malicious apps
* DEX file size and entropy calculation
* DEX file binary → Convert to image

* CNN+DNN: DEX binary image classification results (logit function, degree of malicious/normal) are used as features of the classifier

### Classifier
* Random Forest: Can train complex datasets, and tuning is simple
* XGBoost: Like RF, ensemble method, generally more powerful than RF, but difficult to tune
* DNN: comparison with existing methods, 2-layer, 3-layer comparison
* SVM: the traditional way

* Voting for 4 classifiers after learning more than 4 classifiers
* Avoid overfitting by actively using ensemble methods (RF, XGB, voting) and implementing model complexity regulation (l1, l2 and dropout in DNN)

## Dataset analysis
* 6,000 data for training (4,000 normal, 2,000 malicious) 2000 data for submission
* Excluding 2 apps without CRC errors and DEX files from malicious learning data, 5,998 were used
* String analysis related to malicious apps → Excluded from feature due to few apps including them

* Permissions list: Overall permission vs malicious app-related permission performance comparison, the latter is superior
* Excluding features lacking in correlation with correct answers in the API list and permission list → 110

### Dataset analysis(1)
* DEX file entropy analysis: measure the degree of disorder in bytes of the file → different file formats have different entropy
* DEX File Size Analysis: Windows Malicious File → Small Size
![image](https://user-images.githubusercontent.com/119989103/206964763-4c508291-7d24-4bf4-a76f-9dbba226001f.png)
![image](https://user-images.githubusercontent.com/119989103/206964775-7704c604-79ac-46de-91c0-94504eea2aef.png)


source : https://www.kennethghartman.com/shannon-entropy-of-file-formats/

### Dataset analysis(2)
* Comparison of entropy and file size after extraction: Malicious apps (top) are smaller in size and normal apps have more diverse entropy distribution (bottom)

![image](https://user-images.githubusercontent.com/119989103/206964901-426ea56c-7ddf-48d2-9ddd-26820ede6cf5.png)

![image](https://user-images.githubusercontent.com/119989103/206964911-091f794f-0cc8-454d-996d-9de6cf08dcf0.png)

### Dataset analysis(3)
* DEX Binary File Image: Known to show good performance in family classification of Android apps

![image](https://user-images.githubusercontent.com/119989103/206964974-a2090e2d-398e-43dc-b7dd-9d364fdefd05.png)


source : TonTon Hsien-De Huang, “R2-D2: ColoR -inspired Convolutional NeuRal Network(CNN)-based AndroiD malware Detections”, 2018

Normal application

![image](https://user-images.githubusercontent.com/119989103/206964985-895d84e7-b84d-4d2e-b27e-bafa80343ef8.png)

Malicious application : Unusual black space inside the file

![image](https://user-images.githubusercontent.com/119989103/206964997-c9df431a-594c-4a92-b5c3-e3d1ae120961.png)

## Program structure
* The earlier test data set was used as a feature using CNN+DNN, and the entropy and file size extraction part was also implemented separately.

![image](https://user-images.githubusercontent.com/119989103/206965139-6f6b929c-a6ba-452a-9a5b-3691f5b428c7.png)

### DNN (3-layer)
* Comparison of 3 layers and 2 layers
* Implemented as a low-level API with TensorFlow
* Initially, it was designed to have 110 input values, 3 Fully Connected Layers [FC], and 2 output values with 90 nodes each. Finally, it was designed to have 2 FC layers and 200 nodes each.
* Dropout and L1 and L2 rules were applied to avoid overfitting

![image](https://user-images.githubusercontent.com/119989103/206965233-10a7d7ce-cf83-4dfe-bfc1-fce66206fe56.png)

## Traditional Classifier
* XGB: Conduct grid search (max_depth=9, learning_rate=0.01, objective=’binary:logistic’, booster=’gbtree’, n_estimators=2000)
* RF: prior trial and error, estimator=200
* SVM: C value and gamma value of 1000 and 0.001, respectively

* Voting machine: 2 or more malicious out of 4

* RF and SVM are trial and error without grid search

## Execution result
* 10-Fold
* DNN modeling experiments
![image](https://user-images.githubusercontent.com/119989103/206965774-a3166494-7c64-4f13-a307-f6cfc92b5fed.png)

* XGB grid navigation

>Best parameters set found on development set:
>{'booster': 'gbtree', 'learning_rate': 0.01, 'max_depth': 8, 'n_estimators': 2000, 'nthread': 4}
>Grid scores on development set:
>0.987 (+/-0.002) for {'booster': 'gbtree', 'learning_rate': 0.05, 'max_depth': 7, 'n_estimators': 2000, 'nthread': 4}
>0.987 (+/-0.001) for {'booster': 'gbtree', 'learning_rate': 0.05, 'max_depth': 8, 'n_estimators': 2000, 'nthread': 4}

## Correlation between correct answers and predicted values by classifier
* Correlation analysis of predicted values by classifier for experimental results
![image](https://user-images.githubusercontent.com/119989103/206966289-dd769fa9-3cbf-499b-ac8c-67431f7d520c.png)

* Low correlation between SVM and other classifiers
* If the correlation is low, it is advantageous to use a voting machine: Build a voting machine

## Final evaluation
* Preliminary Competition : ***95.7%***

||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|191|18|
|Test-Bengin|8|382|

* Final competition(1st, add imaged DEX classifier) : ***95.99%***

||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|192|17|
|Test-Bengin|7|383|

* Final competition(2nd, add 2,000 dataset) : ***96.9%***

||Answer-Malware|Answer-Benign|
|------|---|---|
|Test-Malware|266|18|
|Test-Bengin|7|508|
