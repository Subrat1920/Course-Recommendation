import os, sys, sqlite3
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging
import pandas as pd
from course.constants.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from course.utils.utils import read_db, load_to_db


class ThresholdDataIngestion:
    def __init__(self):
        ## Ingested Artifacts
        ingestion_config = DataIngestionConfig()
        self.data_ingestion_file_name:str = ingestion_config.data_ingestion_file_name
        self.data_ingestion_db_name:str = ingestion_config.data_ingestion_db
        self.table_name:str = ingestion_config.ingestion_table

        ## Threshold Based Artifacts
        data_transformation_config=DataTransformationConfig()
        self.threshold_data_file_name:str= data_transformation_config.threshold_data_file_name

        self.threshold_database_name:str=data_transformation_config.threshold_database_name

        self.threshold_table_name:str=data_transformation_config.threshold_table_name

        self.threshold_value:float=data_transformation_config.threshold_value

        os.makedirs(self.threshold_data_file_name, exist_ok=True)

    def initiate_threshold_filtering_data(self):
            try:
                logging.info("="*50)
                logging.info("DATA FILTERED TRANSFORMATION INITIATED")
                logging.info("-"*50)
                logging.info('Initializing reading and storing the data in the database')
                ingested_dataframe = read_db(self.data_ingestion_db_name, self.table_name)
                logging.info('Data read from the database')
                logging.info(f'Shape of the data found to be {ingested_dataframe.shape}')
                logging.info(f'Columns of the data found to be {ingested_dataframe.columns.tolist()}')
                
                
                max_enrollment, min_enrollment = ingested_dataframe['enrollment_numbers'].max(), ingested_dataframe['enrollment_numbers'].min()
                logging.info(f'Type of max_enrollment: {type(max_enrollment)}, value: {max_enrollment}')
                logging.info(f'Type of min_enrollment: {type(min_enrollment)}, value: {min_enrollment}')
                threshold_score = max_enrollment*self.threshold_value
                logging.info(f'Threshold is setted to {threshold_score}, with threshold_value {self.threshold_value}')

                df = ingested_dataframe[ingested_dataframe['enrollment_numbers']>threshold_score]
                logging.info(f'Dataframe after filtering is {df.shape}')
                logging.info(f'Columns of the dataframe after filtering is {df.columns.tolist()}')

                logging.info('Storing the data in the mentioned database')
                load_to_db(df, self.threshold_database_name, self.threshold_table_name)
                logging.info('Data stored in the database')
                logging.info('DATA THRESHOLD INGESTION COMPLETED')
                logging.info("="*50)
                logging.info('\n\n')
            except Exception as e:
                logging.error(error_message_details(e, sys))
                raise RecommenderException(e, sys)
