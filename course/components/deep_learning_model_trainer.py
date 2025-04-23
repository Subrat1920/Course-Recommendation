import pandas as pd
import numpy as np
import os, sys, sqlite3
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dense, Concatenate, Flatten, Dropout
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from joblib import dump

from course.utils.utils import read_db
from course.logger.logging import logging
from course.exception.exception import RecommenderException, error_message_details
from course.constants.initiations import NUM_COL_FOR_TRAINING
from course.constants.entity.config_entity import ModelTrainerConfig, DataTransformationConfig


class DeepLearningTrainer:
    def __init__(self):
        model_trainer_artifact = ModelTrainerConfig()
        data_transformation_artifact = DataTransformationConfig()

        # Data Transformation Config
        self.threshold_database_name: str = data_transformation_artifact.threshold_database_name
        self.threshold_database_table: str = data_transformation_artifact.threshold_table_name

        # Encoder Paths
        self.course_encoder_path: str = model_trainer_artifact.course_encoder_file
        self.instructor_encoder_path: str = model_trainer_artifact.instructor_encoder_file
        self.difficulty_level_encoder_path: str = model_trainer_artifact.difficulty_level_encoder_file

        # Scaler Path
        self.scaler_path: str = model_trainer_artifact.numerical_scaler

        # Final Model Save Path
        self.final_dl_path: str = model_trainer_artifact.final_model

        # Embedding Output Path
        self.embedding_layer_path: str = model_trainer_artifact.embedding_layer_path

        # Numerical Columns
        self.num_cols: list = NUM_COL_FOR_TRAINING

    def model_training(self, dataframe, num_cols):
        try:
            logging.info('Model training function initialized')
            logging.info(f'Dataset shape: {dataframe.shape}')
            logging.info(f'Dataset columns: {dataframe.columns.tolist()}')

            # Encode categorical columns
            course_le = LabelEncoder()
            instructor_le = LabelEncoder()
            difficulty_le = LabelEncoder()

            dataframe['course_name_enc'] = course_le.fit_transform(dataframe['course_name'])
            dataframe['instructor_enc'] = instructor_le.fit_transform(dataframe['instructor'])
            dataframe['difficulty_enc'] = difficulty_le.fit_transform(dataframe['difficulty_level'])

            # Normalize numerical columns
            scaler = MinMaxScaler()
            dataframe[num_cols] = scaler.fit_transform(dataframe[num_cols])

            # Input splits
            X_cat = dataframe[['course_name_enc', 'instructor_enc', 'difficulty_enc']]
            X_num = dataframe[num_cols]

            # Model Inputs
            input_course = Input(shape=(1,), name='input_course')
            input_instructor = Input(shape=(1,), name='input_instructor')
            input_difficulty = Input(shape=(1,), name='input_difficulty')
            input_numeric = Input(shape=(X_num.shape[1],), name='input_numeric')

            # Embedding Layers
            emb_course = Embedding(input_dim=dataframe['course_name_enc'].nunique() + 1, output_dim=8, name='embedding_course')(input_course)
            emb_instr = Embedding(input_dim=dataframe['instructor_enc'].nunique() + 1, output_dim=8, name='embedding_instructor')(input_instructor)
            emb_diff = Embedding(input_dim=dataframe['difficulty_enc'].nunique() + 1, output_dim=4, name='embedding_difficulty')(input_difficulty)

            # Flatten Embeddings
            flat_course = Flatten()(emb_course)
            flat_instr = Flatten()(emb_instr)
            flat_diff = Flatten()(emb_diff)

            # Concatenate
            x = Concatenate(name='concat_layer')([flat_course, flat_instr, flat_diff, input_numeric])

            # Dense Layers
            x = Dense(128, activation='relu')(x)
            x = Dropout(0.3)(x)
            x = Dense(64, activation='relu')(x)
            embedding_output = Dense(32, activation='relu', name='final_embedding')(x)

            # Final Model
            model = Model(inputs=[input_course, input_instructor, input_difficulty, input_numeric], outputs=embedding_output)

            # Generate embeddings
            course_embeddings = model.predict([
                dataframe['course_name_enc'],
                dataframe['instructor_enc'],
                dataframe['difficulty_enc'],
                dataframe[num_cols]
            ], verbose=0)

            return course_embeddings, model, course_le, instructor_le, difficulty_le, scaler

        except Exception as e:
            logging.error(error_message_details(e, sys))
            raise RecommenderException(e, sys)

    def initiate_model_trainer(self):
        try:
            logging.info("=" * 50)
            logging.info("MODEL TRAINING INITIATED")
            logging.info("-" * 50)

            # Read threshold-filtered DB
            dataframe = read_db(self.threshold_database_name, self.threshold_database_table)
            num_cols = self.num_cols

            # Train model
            course_embeddings, model, course_le, instructor_le, difficulty_le, scaler = self.model_training(dataframe, num_cols)

            # Save model
            model.save(self.final_dl_path)

            # Ensure directory for embeddings exists
            embedding_dir = os.path.dirname(self.embedding_layer_path)
            if not os.path.exists(embedding_dir):
                os.makedirs(embedding_dir)

            # Save embeddings
            np.save(self.embedding_layer_path, course_embeddings)

            # Ensure encoder directory exists before saving encoders
            encoder_dir = os.path.dirname(self.course_encoder_path)
            if not os.path.exists(encoder_dir):
                os.makedirs(encoder_dir)

            # Save encoders
            dump(course_le, self.course_encoder_path)
            dump(instructor_le, self.instructor_encoder_path)
            dump(difficulty_le, self.difficulty_level_encoder_path)

            # Ensure scaler directory exists before saving scaler
            scaler_dir = os.path.dirname(self.scaler_path)
            if not os.path.exists(scaler_dir):
                os.makedirs(scaler_dir)

            # Save scaler
            dump(scaler, self.scaler_path)

            logging.info("MODEL TRAINING COMPLETED AND ARTIFACTS SAVED")
            logging.info("=" * 50)
            logging.info('\n\n')

        except Exception as e:
            logging.error(error_message_details(e, sys))
            raise RecommenderException(e, sys)


