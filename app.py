from flask import Flask, render_template, url_for, request
from course.utils.utils import read_db
import os, sys, sqlite3
from course.constants.entity.config_entity import DataTransformationConfig
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
    return render_template('top_educators.html')

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



if __name__=='__main__':
    app.run(debug=True)
