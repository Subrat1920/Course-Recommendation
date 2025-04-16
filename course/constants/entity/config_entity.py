import os, sys
from course.constants.initiations import *

class DataIngestionConfig:
    def __init__(self):
        self.artifact_dir:str = ARTIFACT_DIR_NAME
        self.data_ingestion_file_name:str = os.path.join(self.artifact_dir, DATA_INGESTION_FILE_NAME)
        self.data_ingestion_db:str = os.path.join(self.data_ingestion_file_name, INGESTED_COURSE_DB)
        self.data_source:str = SOURCE_FILE
        self.ingestion_table:str = DATA_INGESTION_TABLE_NAME


class DataTransformationConfig:
    def __init__(self):
        self.artifact = ARTIFACT_DIR_NAME
        self.data_transformation_file_name = os.path.join(self.artifact, DATA_TRANSFORMATION_FILE_NAME)
        self.popularity_based_filtering_file_name = os.path.join(self.data_transformation_file_name, POPULARITY_BASED_FILTERING_FILE_NAME)
        self.popularity_based_filtering_db_name = os.path.join(self.popularity_based_filtering_file_name, POPULARITY_BASED_FILTERING_DB_NAME)
        self.popularity_columns_ui:list = POPULARITY_COLUMNS_UI
        self.threshold_value:float = THRESHOLD_VALUE
        self.popular_table_name:str = POPULARITY_BASED_FILETERING_TABLE_NAME

