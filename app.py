from flask import Flask, render_template, url_for, request
import os, sys, sqlite3
from urllib.parse import unquote
import joblib
import numpy as np

## loading util contents
from course.utils.utils import read_db, get_recommendations

## loading the artifacts
from course.constants.entity.config_entity import DataTransformationConfig, ModelTrainerConfig

## supporters
from course.exception.exception import RecommenderException, error_message_details
from course.logger.front_end_logger import logging


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_popular_courses', methods=['GET','POST'])
def recommend_popular_courses():
    try:
        logging.info('Popularity Based Filtering initiated')
        data_transformation_config = DataTransformationConfig()
        popularity_based_filtering_db_name = data_transformation_config.popularity_based_filtering_db_name
        popularity_based_filtering_table_name = data_transformation_config.popular_table_name
        popular_courses = read_db(popularity_based_filtering_db_name, popularity_based_filtering_table_name)
        popular_courses = popular_courses.head(15)
        logging.info('Succesfully read the database from ingested database')

        return render_template('popular_courses.html', courses=popular_courses.to_dict(orient='records'))
    
    except Exception as e:
        logging.error(error_message_details(e, sys))
        raise RecommenderException(e, sys)

@app.route('/top_educators', methods=['POST','GET'])
def show_top_educators():
    try:
            data_transformation_config = DataTransformationConfig()
            threshold_db_name = data_transformation_config.threshold_database_name
            threshold_table_name = data_transformation_config.threshold_table_name
            
            threshold_df = read_db(threshold_db_name, threshold_table_name)
            
            top_instructors = (threshold_df.groupby(['instructor', 'instructor_images'])
                            .agg({'rating': 'mean', 'feedback_score': 'mean'})
                            .sort_values(by=['rating', 'feedback_score'], 
                                        ascending=[False, False])
                            .reset_index()
                            .head(15)) 
            
            return render_template('top_educators.html', instructors=top_instructors.to_dict('records'))
    
    except Exception as e:
        logging.error(f"Error in show_top_educators: {str(e)}")


@app.route('/frequently_bought_courses', methods=['POST','GET'])
def show_frequently_bought_courses():
    try:
        data_transformation_config = DataTransformationConfig()
        thrreshold_db_name = data_transformation_config.threshold_database_name
        threshold_table_name = data_transformation_config.threshold_table_name
        df = read_db(thrreshold_db_name, threshold_table_name)
        frequently_brought_courses = df.groupby(['course_name', 'course_images', 'rating', 'instructor', 'instructor_images'])['enrollment_numbers'].max().sort_values(ascending=False).reset_index().head(15)
        return render_template('frequently_bought.html', courses=frequently_brought_courses.to_dict(orient='records'))
    except Exception as e:
        raise RecommenderException(e, sys)
    

@app.route('/help_desk', methods=['POST','GET'])
def show_help():
    return render_template('help.html')

@app.route('/course_detail', methods=['GET'])
def course_detail():
    try:
        # Extract parameters first
        course_name = request.args.get('name')
        instructor_name = request.args.get('instructor')

        # Load configs
        model_trainer_config = ModelTrainerConfig()
        trained_database_path = model_trainer_config.training_database_path
        trained_dataframe_table_name = 'training_db_table'

        # Load trained DataFrame
        trained_dataframe = read_db(trained_database_path, trained_dataframe_table_name)

        # Load embeddings
        course_embeddings = np.load(model_trainer_config.embedding_layer_path)  # Example

        # Load threshold/original DataFrame
        data_transformation_config = DataTransformationConfig()
        threshold_db_name = data_transformation_config.threshold_database_name
        threshold_table_name = data_transformation_config.threshold_table_name
        threshold_df = read_db(threshold_db_name, threshold_table_name)

        # Get recommendations
        recommends = get_recommendations(
            original_dataframe=threshold_df,
            trained_dataframe=trained_dataframe,
            course_embeddings=course_embeddings,
            course_name=course_name,
            instructor_name=instructor_name,
            top_n=6
        )
        print(f'Course Name: {course_name}\nInstructor Name : {instructor_name}')
        print(recommends[['course_name', 'instructor']])

        # Get main course data
        df = threshold_df.loc[
            (threshold_df['course_name'] == course_name) &
            (threshold_df['instructor'] == instructor_name)
        ].drop_duplicates(subset=['course_name', 'instructor'])

        if df.empty:
            return "Course not found", 404

        course_data = df.iloc[0]

        return render_template(
            'course_details_with_recommendation.html',
            course_name=course_data['course_name'],
            instructor_name=course_data['instructor'],
            course_image=course_data['course_images'],
            instructor_image=course_data['instructor_images'],
            rating=course_data['rating'],
            enrollment_numbers=course_data['enrollment_numbers'],
            course_duration=course_data['course_duration_hours'],
            recommendations=recommends.to_dict('records')  # Pass to template
        )
    
    except Exception as e:
        logging.error(f"Error in course_detail: {str(e)}")
        raise RecommenderException(e, sys)




@app.route('/contact')
def contact():
    return render_template('contacts.html')


@app.route('/instructor/courses')
def view_courses_by_instructor():
    instructor_name = request.args.get('instructor_name', '')
    instructor_name = unquote(instructor_name)
    data_transformation_config = DataTransformationConfig()
    threshold_df = read_db(
        data_transformation_config.threshold_database_name,
        data_transformation_config.threshold_table_name
    )
    instructor_courses = threshold_df[threshold_df['instructor'] == instructor_name]
    unique_courses = instructor_courses.drop_duplicates(subset=['course_name'])
    top_courses = (
        unique_courses
        .groupby(['course_name','course_images','course_duration_hours', 'certification_offered', 'difficulty_level', 'rating', 'enrollment_numbers', 'course_price','study_material_available'], as_index=False)['rating']
        .mean()
        .sort_values(by='rating', ascending=False).head(15)
    )
    courses = top_courses.to_dict(orient='records')
    return render_template(
        'courses_by_instructor.html',
        instructor_name=instructor_name,
        courses=courses
    )


if __name__=='__main__':
    app.run(debug=True)


