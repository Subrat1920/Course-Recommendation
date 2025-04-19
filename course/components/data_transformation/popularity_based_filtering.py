import os, sys, sqlite3
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging
import pandas as pd

from course.constants.entity.config_entity import DataIngestionConfig, DataTransformationConfig
from course.utils.utils import read_db, load_to_db


class PopularityFiltering:
    def __init__(self):
        transformation_config = DataTransformationConfig()
        self.artifact = transformation_config.artifact
        self.data_transformation_file_name = transformation_config.data_transformation_file_name
        self.popularity_based_filtering_file_name = transformation_config.popularity_based_filtering_file_name
        self.popularity_based_filtering_db_name = transformation_config.popularity_based_filtering_db_name
        self.popularity_columns_ui:list = transformation_config.popularity_columns_ui
        self.popular_table_name:str = transformation_config.popular_table_name
        self.threshold_value:float = transformation_config.threshold_value


        ## Ingested Artifacts
        ingestion_config = DataIngestionConfig()
        self.data_ingestion_file_name:str = ingestion_config.data_ingestion_file_name
        self.data_ingestion_db_name:str = ingestion_config.data_ingestion_db
        self.table_name:str = ingestion_config.ingestion_table

        ## create the popularity based filtering folder for furhter process
        os.makedirs(self.popularity_based_filtering_file_name, exist_ok=True)

    def popularity_based_filtering(self, ingested_dataframe:pd.DataFrame):
        '''
            This function takes only the dataframe that is being ingested and filters the most rated course
            Parameters:
                    ingeste_dataframe:pd.DataFrame -> it will take only the format of dataframe
        '''
        ## get the max_enrollments and min enrollments form the dataframe for the filtering
        logging.info('Popularity Based filtering function initiated')
        logging.info(f'Shape of the dataframe {ingested_dataframe.shape}')
        max_enrollment, min_enrollment = ingested_dataframe['enrollment_numbers'].max(), ingested_dataframe['enrollment_numbers'].min()
        logging.info(f'Type of max_enrollment: {type(max_enrollment)}, value: {max_enrollment}')
        logging.info(f'Type of min_enrollment: {type(min_enrollment)}, value: {min_enrollment}')
        threshold_score = max_enrollment*self.threshold_value
        logging.info(f'Threshold is setted to {threshold_score}, with threshold_value {self.threshold_value}')
        threshold_filtered_df = ingested_dataframe[ingested_dataframe['enrollment_numbers']>=threshold_score].copy()
        logging.info(f'So, the shape of the dataframe is {threshold_filtered_df.shape}')
        ## applying the popularity based filtering
        threshold_filtered_df.loc[:, 'average_rating'] = (threshold_filtered_df.groupby(['course_name', 'instructor'])['rating'].transform('mean'))
        threshold_filtered_df = threshold_filtered_df.drop_duplicates(subset=['course_name'])

        logging.info(f'Shape of threshold_filtered_df is {threshold_filtered_df.shape}')
        popularity_df = threshold_filtered_df.sort_values('average_rating', ascending=False).reset_index().head(25)
        popularity_df = popularity_df.drop(columns=['index'])
        popularity_df = popularity_df[self.popularity_columns_ui]
        logging.info(f'Shape of popularity_df is {popularity_df.shape}')
        logging.info(f'Columns present in the popularity df found to be {popularity_df.columns.tolist()}')
        return popularity_df
    
    def initiate_popularity_based_filtering(self):
        try:
            ## read the data present in the ingested data base from ingested_data
            logging.info("="*50)
            logging.info("DATA TRANSFORMATION INITIATED")
            logging.info("-"*50)
            logging.info('Initializing reading and storing the data in the database')
            try:
                logging.info(f'Reading the data from the data base')
                df = read_db(self.data_ingestion_db_name, self.table_name)
                logging.info('Data Extraction completed from the database')
                logging.info(f'Shape of the data found to be {df.shape}')
                logging.info(f'Columns of the data found to be {df.columns.tolist()}')
                logging.info('Applying popularity filtering')
                popularity_df = self.popularity_based_filtering(df)
                logging.info(f'Columns of the popularity data found to be {popularity_df.columns.tolist()}')
                logging.info('Applied popularity filtering')
                logging.info('Loading that dataframe into the db')
                load_to_db(popularity_df, self.popularity_based_filtering_db_name, self.popular_table_name)
                logging.info('Data Loaded to the database')
            except Exception as e:
                logging.error(error_message_details(e, sys))
                raise RecommenderException(e, sys)
            logging.info('POPULARITY DATA TRANSFORMATION COMPLETED')
            logging.info("="*50)
            logging.info('\n\n')
        except Exception as e:
            logging.error(error_message_details(e,sys))
            raise RecommenderException(e, sys)


