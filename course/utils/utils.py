import pandas as pd
import numpy as np
import os, sys, sqlite3
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging


def read_store_csv(csv_file_path, db_path, table_name):
    try:
        df=pd.read_csv(csv_file_path)
        logging.info(f'The dataframe has {len(df.columns)}')
        with sqlite3.connect(db_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        logging.error('Error happended in read_store_csv --> utils')
        logging.warning(error_message_details(e, sys))
        raise RecommenderException(e, sys)
    
def read_csv_file(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        logging.info(f'The dataframe has {df.shape} shape')
        logging.info(f'Columns extracted ==> {df.columns.tolist()}')
        return df
    except Exception as e:
        logging.error('Error happended in read_csv_file --> utils')
        logging.warning(error_message_details(e, sys))
        raise RecommenderException(e, sys)


def load_to_db(dataframe, db_path, table_name):
    try:
        with sqlite3.connect(db_path) as conn:
            dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    except Exception as e:
        logging.error('Error happended in load_to_db --> utils')
        logging.warning(error_message_details(e, sys))
        raise RecommenderException(e, sys)
    
def read_db(db_path, table_name):
    try:
        with sqlite3.connect(db_path) as conn:
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            return df
    except Exception as e:
        logging.error('Error happended in read_db --> utils')
        logging.warning(error_message_details(e, sys))
        raise RecommenderException(e, sys)


