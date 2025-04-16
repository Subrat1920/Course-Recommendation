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
THRESHOLD_DATABASE:str='threshold_data.db'
THRESHOLD_VALUE:float=0.80
POPULARITY_COLUMNS_UI:list=['course_name', 'instructor', 'course_duration_hours', 'certification_offered', 'difficulty_level', 'course_price', 'study_material_available', 'course_images', 'instructor_images', 'average_rating']

'''
DATA TRANSFORMATION : MODEL BASED RECOMMENDATION
'''

