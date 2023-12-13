import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity

class RegressionModel():
    def __init__(self):
        with open("./model/final_lgbm_model.pkl", 'rb') as model_file:
            self.regressor = pickle.load(model_file)
    def predict(self,form):
        newobj = [
                {
                    "year": form.year.data,
                    "transmission": form.transmission.data,
                    "mileage": form.mileage.data,
                    "fuelType": form.fuelType.data,
                    "tax": form.tax.data,
                    "mpg": form.mpg.data,
                    "engineSize": form.engineSize.data,
                    "brand": form.brand.data
                }
            ]
        data = pd.DataFrame(newobj)
        prediction = self.regressor.predict(data)
        return round(prediction[0],2)

def getRecommended(num_data,input_df):
    num_data = pd.DataFrame(num_data)
    input_df = pd.DataFrame(input_df)
    scaler = StandardScaler()
    temp_dfX = scaler.fit_transform(num_data.drop("id",axis=1)) 
    userInpX = scaler.transform(input_df) 
    similarity_scores = cosine_similarity(temp_dfX, userInpX)
    top3_indices = similarity_scores.flatten().argsort()[-3:][::-1]
    top3_rows = num_data.iloc[top3_indices]
    return top3_rows