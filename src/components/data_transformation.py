import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
     preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")
class  DataTransformation:
    def __init__(self):
          self.data_transformation_config = DataTransformationConfig()
    
    def get_data_transformer_object(self): #this function is used to create a preprocessor object which will be used to transform the data
     try:
          numerical_features = ['reading_score', 'writing_score']
          categorical_features = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
            
          num_pipeline=Pipeline(
              steps=[
                  ("imputer",SimpleImputer(strategy="median")), #imputing the missing values with median
                  ("scaler",StandardScaler()) #scaling the data using standard scaler
              ]
          )

          cat_pipeline=Pipeline(
              steps=[
                  ("imputer",SimpleImputer(strategy="most_frequent")), #imputing the missing values with most frequent value
                  ("onehotencoder",OneHotEncoder()), #encoding the categorical features using one hot encoder
                  ("scaler",StandardScaler(with_mean=False)) #scaling the data using standard scaler
              ]
          )
          logging.info("Numerical and categorical feature transformation pipelines created")
          preprocessor=ColumnTransformer(
              [ 
                  ("num_pipeline", num_pipeline, numerical_features),
                  ("cat_pipeline", cat_pipeline, categorical_features)
              ]
          )
          return preprocessor
     except Exception as e:
          raise CustomException(e,sys)
     


    def initiate_data_transformation(self,train_path, test_path):
        try:
            train_df = pd.read_csv(train_path) #reading the train data from the csv file
            test_df = pd.read_csv(test_path) #reading the test data from the csv file
            logging.info("Read train and test data as dataframes")
            logging.info("Obtaining preprocessing object")
            preprocessor_obj = self.get_data_transformer_object() #getting the preprocessor object
            target_column_name = "math_score" #the target column name
            numerical_columns = [ 'writing_score', 'reading_score'] #the numerical columns in the data

            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name] #getting the target feature from the train data

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name] #getting the target feature from the test data    


            logging.info("Applying preprocessing object on training and testing dataframes")
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df) #fitting the preprocessor object on the train data
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df) #transforming the test data using the preprocessor object

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)] #combining the input features and target feature of the train data
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)] #combining the input features and target feature of the test data

            logging.info("Saved preprocessing object")
            #saving the preprocessor object in the artifacts folder

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path, obj = preprocessor_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)
if __name__ == "__main__":
    obj = DataTransformation()
    train_arr, test_arr, preprocessor_obj_file_path = obj.initiate_data_transformation(
        train_path=r"C:\Users\adity\mlproject\artifacts\train.csv",
        test_path=r"C:\Users\adity\mlproject\artifacts\test.csv"
    )
    





    