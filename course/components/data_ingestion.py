import pandas as pd
import os, sys,sqlite3
from course.logger.logging import logging
from course.exception.exception import RecommenderException, error_message_details
from course.utils.utils import read_csv_file, load_to_db
from course.constants.initiations import (
    ARTIFACT_DIR_NAME, INGESTED_COURSE_DB,  DATA_INGESTION_FILE_NAME, DATA_INGESTION_TABLE_NAME, SOURCE_FILE
)

class DataIngestion:
    def __init__(self):
        self.artifact_dir:str=ARTIFACT_DIR_NAME
        self.data_ingestion_file_name:str=os.path.join(self.artifact_dir, DATA_INGESTION_FILE_NAME)
        self.data_ingestion_db:str=os.path.join(self.data_ingestion_file_name, INGESTED_COURSE_DB)
        self.data_source = SOURCE_FILE
        self.ingestion_table=DATA_INGESTION_TABLE_NAME

        os.makedirs(self.data_ingestion_file_name, exist_ok=True)
        
        
    def initiate_data_ingestion(self):
        try:
            logging.info("="*50)
            logging.info("DATA INGESTION INITIATED")
            logging.info("-"*50)
            logging.info('Initializing reading and storing the data in the database')
            try:
                logging.info(f'Reading the data from the source')
                df=read_csv_file(self.data_source)
                df=df.drop(columns=['Unnamed: 0'])
                logging.info(f'Columns in ingested dataframe ==> {df.columns.tolist()}')
                logging.info('The read_csv is successfully executed')
                logging.info('Loading the data to the database')
                load_to_db(df,self.data_ingestion_db, self.ingestion_table)
                logging.info(f'The data succesfully loaded to database {self.data_ingestion_db}')
            except Exception as e:
                logging.error(error_message_details(e, sys))
                raise RecommenderException(error_message_details(e, sys))
            logging.info('DATA INGESTION COMPLETED')
            logging.info("="*50)
            logging.info('\n\n')
        except Exception as e:
            logging.error(error_message_details(e, sys))
            raise RecommenderException(error_message_details(e, sys))
