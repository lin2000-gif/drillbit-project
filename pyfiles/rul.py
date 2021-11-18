import joblib
import numpy as np

def calcRUL(data_comp,final_cluster):
    loaded_rf = joblib.load("./NNmodel/rul_model.joblib")

    data=np.concatenate((data_comp,[(4-final_cluster)/4]),axis=0).reshape(1,-1)

    predicted_rul=loaded_rf.predict(data)[0]

    print("RUL HERE!!!")
    print(predicted_rul)
    return predicted_rul