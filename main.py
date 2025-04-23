import os
import logging
import warnings
import sys

# Suppress TensorFlow logs and warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Only show errors
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN optimizations (optional)
logging.getLogger('tensorflow').setLevel(logging.ERROR)
warnings.filterwarnings('ignore')

# Add color and styles to make the output more appealing
from termcolor import colored

# Import components
from course.components.data_ingestion import DataIngestion
from course.components.data_transformation.popularity_based_filtering import PopularityFiltering
from course.components.data_transformation.threshold_filtering import ThresholdDataIngestion
from course.components.deep_learning_model_trainer import DeepLearningTrainer
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging

if __name__ == '__main__':
    try:
        # Adding header and beautiful prints with color and indentation
        print(colored("\n========================================", 'cyan'))
        print(colored("     Edu Select Initialization Started", 'yellow'))
        print(colored("========================================\n", 'cyan'))

        # Data Ingestion
        print(colored("    --->", 'magenta'), colored("Data Ingestion Initiated", 'green'))
        data_ingestion = DataIngestion()
        data_ingestion.initiate_data_ingestion()

        # Filtered Data Ingestion
        print(colored("    --->", 'magenta'), colored("Filtered Data Ingestion Initiated", 'green'))
        threshold_data_ingestion = ThresholdDataIngestion()
        threshold_data_ingestion.initiate_threshold_filtering_data()

        # Data Transformation - Popularity Filtering
        print(colored("    --->", 'magenta'), colored("Popularity Filtering Initiated", 'green'))
        popularity_filtering = PopularityFiltering()
        popularity_filtering.initiate_popularity_based_filtering()

        # Model Training
        print(colored("    --->", 'magenta'), colored("Model Training Initialized", 'green'))
        deep_learning_trainer = DeepLearningTrainer()
        deep_learning_trainer.initiate_model_trainer()

        print(colored("\n========================================", 'cyan'))
        print(colored("     Edu Select Process Completed", 'yellow'))
        print(colored("========================================\n", 'cyan'))

    except Exception as e:
        logging.error(error_message_details(e, sys))
        raise RecommenderException(e, sys) from e
