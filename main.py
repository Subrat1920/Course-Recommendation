
import os
import logging
import warnings
import sys
from termcolor import colored

from course.components.data_ingestion import DataIngestion
from course.components.data_transformation.popularity_based_filtering import PopularityFiltering
from course.components.data_transformation.threshold_filtering import ThresholdDataIngestion
from course.components.deep_learning_model_trainer import DeepLearningTrainer
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging

# Setup once
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
logging.getLogger('tensorflow').setLevel(logging.ERROR)
warnings.filterwarnings('ignore')

def initialize_pipeline():
    try:
        print(colored("\n========================================", 'cyan'))
        print(colored("     Edu Select Initialization Started", 'yellow'))
        print(colored("========================================\n", 'cyan'))

        print(colored("    --->", 'magenta'), colored("Data Ingestion Initiated", 'green'))
        DataIngestion().initiate_data_ingestion()

        print(colored("    --->", 'magenta'), colored("Filtered Data Ingestion Initiated", 'green'))
        ThresholdDataIngestion().initiate_threshold_filtering_data()

        print(colored("    --->", 'magenta'), colored("Popularity Filtering Initiated", 'green'))
        PopularityFiltering().initiate_popularity_based_filtering()

        print(colored("    --->", 'magenta'), colored("Model Training Initialized", 'green'))
        DeepLearningTrainer().initiate_model_trainer()

        print(colored("\n========================================", 'cyan'))
        print(colored("     Edu Select Process Completed", 'yellow'))
        print(colored("========================================\n", 'cyan'))

    except Exception as e:
        logging.error(error_message_details(e, sys))
        raise RecommenderException(e, sys)
