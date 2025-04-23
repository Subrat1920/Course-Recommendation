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
        '''
        POPULARITY BASED FILTERING ARTIFACTS
        '''
        self.artifact = ARTIFACT_DIR_NAME
        self.data_transformation_file_name = os.path.join(self.artifact, DATA_TRANSFORMATION_FILE_NAME)
        self.popularity_based_filtering_file_name = os.path.join(self.data_transformation_file_name, POPULARITY_BASED_FILTERING_FILE_NAME)
        self.popularity_based_filtering_db_name = os.path.join(self.popularity_based_filtering_file_name, POPULARITY_BASED_FILTERING_DB_NAME)
        self.popularity_columns_ui:list = POPULARITY_COLUMNS_UI
        self.threshold_value:float = THRESHOLD_VALUE
        self.popular_table_name:str = POPULARITY_BASED_FILETERING_TABLE_NAME

        '''
        THRESHOLD FILTERED DATA
        '''
        self.data_transformation_file_name:str=os.path.join(self.artifact, DATA_TRANSFORMATION_FILE_NAME)   ## transformation file name
        self.threshold_data_file_name:str = os.path.join(self.data_transformation_file_name, THRESHOLD_DATA_FILE_NAME)  ## threshold file name
        self.threshold_database_name: str = os.path.join(self.threshold_data_file_name, THRESHOLD_DATABASE)   ## database name
        self.threshold_table_name:str = THRESHOLD_TABLE_NAME  ## table name


class ModelTrainerConfig:
    def __init__(self):
       ## initiating model training artifact
       self.artifact:str=ARTIFACT_DIR_NAME
       self.model_trainer_path:str=os.path.join(self.artifact, MODEL_CONTAINER_FILE_NAME)

       ## initiating model container artifact
       self.model_container_path:str=os.path.join(self.model_trainer_path, MODEL_CONTAINER_FILE_NAME)

       ## initiating encoders_container_artifact
       self.model_encoder_container_path:str=os.path.join(self.model_container_path, MODEL_ENCODERS_FILE_NAME)

       ## initiating encoders
       self.course_encoder_file:str=os.path.join(self.model_encoder_container_path, COURSE_ENCODER)
       
       self.instructor_encoder_file:str=os.path.join(self.model_encoder_container_path, INSTRUCTOR_ENCODER)

       self.difficulty_level_encoder_file:str=os.path.join(self.model_encoder_container_path, DIFFICULTY_LEVEL_ENCODER)

       ## initiating scaler_container_artifact
       self.model_scaler_container_path:str=os.path.join(self.model_container_path, MODEL_SCALER_FILE_NAME)
       ## initiating scaler
       self.numerical_scaler:str=os.path.join(self.model_scaler_container_path, NUMERICAL_SCALER)

       ## initiating final_model_container_artifact
       self.final_model_container_path:str=os.path.join(self.model_container_path, FINAL_MODEL_FILE_NAME)
       ## initiating final_model
       self.final_model:str=os.path.join(self.final_model_container_path, DEEP_LEARNING_MODEL_NAME)

       ## initiating supporting data frame artifact
       self.supporting_database_container:str=os.path.join(self.model_trainer_path, SUPPORTING_DATABASES_FILE_NAME)

       ## initiating training database file name
       self.training_database_path:str=os.path.join(self.supporting_database_container, TRAINED_DATABASE_NAME)

       ## initiating embedding layers artifact
       self.embedding_layer_folder_path:str=os.path.join(self.model_container_path, COURSE_EMBEDDING_CONTAINER_NAME)

       self.embedding_layer_path:str=os.path.join(self.embedding_layer_folder_path, COURSE_EMBEDDING_FILE_NAME)



        
