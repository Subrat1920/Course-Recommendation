import pandas as pd
import numpy as np
import os, sys, sqlite3
from course.exception.exception import RecommenderException, error_message_details
from course.logger.logging import logging
from sklearn.metrics.pairwise import cosine_similarity


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




def get_recommendations(original_dataframe, trained_dataframe, course_embeddings, course_name, instructor_name, top_n=6):
    try:
        # Extract index of the course
        course_idx = trained_dataframe[
            (original_dataframe['course_name'] == course_name) &
            (original_dataframe['instructor'] == instructor_name)
        ].index

        if len(course_idx) == 0:
            return "Course not found."

        course_idx = course_idx[0]  # Make sure course_idx is an integer, not a list

        # Ensure course_embeddings is a NumPy array and course_idx is a valid index
        input_vec = course_embeddings[course_idx].reshape(1, -1)

        # Calculate similarity
        sims = cosine_similarity(input_vec, course_embeddings).flatten()

        # Get similar courses (excluding the input course)
        similar_idxs = np.argsort(sims)[::-1]
        similar_idxs = [i for i in similar_idxs if i != course_idx][:top_n]

        # Get final recommended courses
        final_df = original_dataframe.iloc[similar_idxs][['course_name', 'instructor', 'rating', 'course_images', 'instructor_images']].reset_index()
        final_df = final_df.drop(columns=['index'])
        
        return final_df

    except Exception as e:
        logging.error('Error in get_recommendation---> util.py')
        raise RecommenderException(e, sys)
    

