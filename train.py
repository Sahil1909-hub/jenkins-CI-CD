from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import mlflow


data = load_breast_cancer()

df = pd.DataFrame(data.data, columns=data.feature_names)

df['target'] = data.target

X = df.drop(columns='target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

mlflow.set_experiment('Breast cancer')

with mlflow.start_run():

    n_estimators=100
    max_depth=4

    model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    sns.heatmap(cm, annot=True, fmt='d')
    plt.title('Confusion matrix')

    plt.savefig('confusion_matrix.png')

    mlflow.log_param('n_estimators', n_estimators)
    mlflow.log_param('max_depth', max_depth)
    mlflow.log_metric('accuracy', accuracy)
    mlflow.log_metric('precision', precision)
    mlflow.log_metric('f1 score', f1)
    mlflow.log_metric('roc_auc', roc_auc)
    mlflow.log_artifact('confusion_matrix.png')

    mlflow.sklearn.log_model(model, 
                             "model",
                             registered_model_name='breast-cancer-model')


with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print('Model training completed!')


