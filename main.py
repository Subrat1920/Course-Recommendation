from course.components.data_ingestion import DataIngestion
from course.components.data_transformation.popularity_based_filtering import PopularityFiltering
from course.components.data_transformation.threshold_filtering import ThresholdDataIngestion
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging
import sys

if __name__=='__main__':
    try:
        ## initializing data ingestion
        print("Data Ingestion Initiated")
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()

        ## initiating filtered data ingestion
        print("Filtered Data Ingestion Initiated")
        threshold_data_ingestion = ThresholdDataIngestion()
        threshold_data_ingestion.initiate_threshold_filtering_data()

        ## intializing data transformation
        print('Popularity Filtering Initated')
        popularity_filtering = PopularityFiltering()
        popularity_filtering.initiate_popularity_based_filtering()

    except Exception as e:
        logging.error(error_message_details(e, sys))
        raise RecommenderException(e,sys) from e