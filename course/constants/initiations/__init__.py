'''
DEFINIG THE ARTIFACTS DIRECTORY
'''
SOURCE_FILE:str='Notebooks\Datasets\online_courses_updated.csv'
ARTIFACT_DIR_NAME:str='Course_Artifact'

'''
DATA INGESTION
'''
DATA_INGESTION_FILE_NAME:str='data_ingestion'
INGESTED_COURSE_DB:str='course.db'
DATA_INGESTION_TABLE_NAME:str='course_data_table'


'''
DATA VALIDATION
'''
DATA_VALIDATION_FOLDER_NAME:str='data_validation'

DATA_VALIDATION_FILE_NAME:str='validation_report.txt'

'''
DATA TRANSFORMATION
'''
DATA_TRANSFORMATION_FILE_NAME:str='data_transformation'

'''
DATA TRANFORMATION : POPULARITY BASED RECOMMENDATION
'''
POPULARITY_BASED_FILTERING_FILE_NAME:str='popularity_based_filtering'
POPULARITY_BASED_FILTERING_DB_NAME:str='popular_courses.db'
POPULARITY_BASED_FILETERING_TABLE_NAME:str='popular_course_table'
THRESHOLD_VALUE:float=0.80
POPULARITY_COLUMNS_UI:list=['course_name', 'instructor', 'course_duration_hours', 'certification_offered', 'difficulty_level', 'course_price', 'study_material_available', 'course_images', 'instructor_images', 'average_rating']


'''
DATA TRANSFORMATION : THRESHOLD VALUE (FOR MAKING THE RENDER FASTER)
'''
THRESHOLD_DATA_FILE_NAME:str='threshold_filtered_data'
THRESHOLD_DATABASE:str='threshold_data.db'
THRESHOLD_TABLE_NAME:str='threshold_data_table'

'''
MODEL TRAINER : DEEP LEARNING 
'''
MODEL_TRAINER_FILE_NAME:str='model_trainer'
MODEL_CONTAINER_FILE_NAME:str='model_containers'
SUPPORTING_DATABASES_FILE_NAME:str='supporting_databases'

### CONTENTS OF MODEL_CONTAINER_FILE_NAME
## FILE FOR SAVING DIFFERENT MODELS
MODEL_ENCODERS_FILE_NAME:str='encoder_container'
MODEL_SCALER_FILE_NAME:str='scalers_container'
FINAL_MODEL_FILE_NAME:str='final_model_container'

## ENCODERS REQUIRED
COURSE_ENCODER:str='course_le.pkl'
INSTRUCTOR_ENCODER:str='instructor_le.pkl'
DIFFICULTY_LEVEL_ENCODER:str='difficulty_le.pkl'

## SCALER REQUIRED
NUMERICAL_SCALER:str='min_max_scaler.pkl'

## FINAL DEEP-LEARNING MODEL_NAME:
DEEP_LEARNING_MODEL_NAME:str='final_model.h5'

### CONTENT OF SUPPORTING_DATABASE_FILE_NAME
TRAINED_DATABASE_NAME:str='training_df.db'

## embedding layer
COURSE_EMBEDDING_CONTAINER_NAME:str='embeddings'
COURSE_EMBEDDING_FILE_NAME:str='course_embeddings.npy'

## NUMERICAL COLUMN FOR THE MODEL TRAINING
NUM_COL_FOR_TRAINING: list = ['course_duration_hours', 'rating', 'feedback_score', 'course_price', 'enrollment_numbers', 'time_spent_hours','previous_courses_taken']