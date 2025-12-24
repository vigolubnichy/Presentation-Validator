from app.ml_model import train, load
import os

def test_model_train_and_load():
    train()
    model = load()
    assert model is not None
