from flask import Flask, render_template, url_for, request
import os, sys, sqlite3
from urllib.parse import unquote

## loading util contents
from course.utils.utils import read_db

## loading the artifacts
from course.constants.entity.config_entity import DataTransformationConfig

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

@app.route('/top_rated_courses', methods=['POST','GET'])
def show_top_rated_courses():
    return render_template('top_rated_courses.html')

@app.route('/frequently_bought_courses', methods=['POST','GET'])
def show_frequently_bought_courses():
    return render_template('frequently_bought.html')

@app.route('/help_desk', methods=['POST','GET'])
def show_help():
    return render_template('help.html')

@app.route('/course_detail', methods=['GET'])
def course_detail():
    course_name = request.args.get('name')
    instructor = request.args.get('instructor')

    # For now, just render a placeholder page
    return f"<h1>Details for {course_name} by {instructor} will be shown here.</h1>"


@app.route('/instructor/courses')
def view_courses_by_instructor():
    instructor_name = request.args.get('instructor_name', '')
    instructor_name = unquote(instructor_name)

    # Load data from DB
    data_transformation_config = DataTransformationConfig()
    threshold_df = read_db(
        data_transformation_config.threshold_database_name,
        data_transformation_config.threshold_table_name
    )

    # Filter for instructor
    instructor_courses = threshold_df[threshold_df['instructor'] == instructor_name]

    # Drop duplicate course names to avoid redundancy
    unique_courses = instructor_courses.drop_duplicates(subset=['course_name'])

    # Calculate top-rated courses based on mean rating
    top_courses = (
        unique_courses
        .groupby(['course_name','course_images','course_duration_hours', 'certification_offered', 'difficulty_level', 'rating', 'enrollment_numbers', 'course_price','study_material_available'], as_index=False)['rating']
        .mean()
        .sort_values(by='rating', ascending=False).head(15)
    )

    # Convert to dictionary list for rendering
    courses = top_courses.to_dict(orient='records')

    return render_template(
        'courses_by_instructor.html',
        instructor_name=instructor_name,
        courses=courses
    )

if __name__=='__main__':
    app.run(debug=True)


['course_duration_hours', 'certification_offered', 'difficulty_level', 'rating', 'enrollment_numbers', 'course_price','study_material_available']