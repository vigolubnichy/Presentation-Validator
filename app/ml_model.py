import joblib
from sklearn.linear_model import LogisticRegression

MODEL_PATH = "data/ml/model.joblib"

def train():
    X = [[1,1], [5,1], [10,3], [3,1]]
    y = [1,0,1,0]
    model = LogisticRegression()
    model.fit(X, y)
    joblib.dump(model, MODEL_PATH)

def load():
    return joblib.load(MODEL_PATH)
