import os
import sys
from dataclasses import dataclass

import pandas as pd
from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join("../../artifacts", "train.csv")
    test_data_path: str = os.path.join("../../artifacts", "test.csv")
    raw_data_path: str = os.path.join("../../artifacts", "raw_data.csv")


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        logging.info("Data Ingestion Initiated")

    def initiate_data_ingestion(self):
        logging.info("Data Ingestion Started")
        try:
            df = pd.read_csv('C:\\Users\\SibghatUllah\\PycharmProjects\\MarksPrediction\\notebook\\data\\students.csv')
            logging.info("Data Ingestion Completed/Read Successfully")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw Data Saved Successfully")

            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("Train Test Split Completed Successfully")
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train Test Data Saved Successfully")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation_obj = DataTransformation()
    train_array, test_array, _ = data_transformation_obj.initiate_data_transformation(train_data, test_data)

    model_trainer_obj = ModelTrainer()
    print(model_trainer_obj.initiate_model_trainer(train_array,
                                                   test_array,
                                                   ))
