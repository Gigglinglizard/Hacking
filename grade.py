import os
import argparse
import sys 

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://canvas.kth.se/api/v1'
COURSE_ID = '41678' # EN2720 Ethical Hacking

"""Command line functionality for more direct use."""
parser = argparse.ArgumentParser(description='API key input for Canvas grade calculator.')
parser.add_argument('--api_key', type=str, help='Canvas API key.')
args = parser.parse_args()

API_KEY = args.api_key if args.api_key else os.getenv('API_KEY')

def get(url):
    """
    Fetch data from the provided URL.
    An error is raised if the API key is invalid.
    """
    response = requests.get(
        url,
        headers={'Authorization': f'Bearer {API_KEY}'},
        timeout=10
    ) 

    if response.status_code == 401:
        raise ValueError('Invalid API key.')

    data = response.json()
    while 'next' in response.links.keys():
        response = requests.get(
            response.links['next']['url'],
            headers={'Authorization': f'Bearer {API_KEY}'},
            timeout=10  
        )
        data.extend(response.json())
    return data


def get_all_assignments():
    """
    Fetch all assignments for the course. 
    Specifically fetch 'capturing flag' assignments.
    """
    url = f'{BASE_URL}/courses/{COURSE_ID}/assignments'
    assignments = get(url)
    return [assignment for assignment in assignments if 'capturing flag' in assignment['name'].lower()]


def calculate_grade(assignments):
    """
    Calculates the grade for the course.
    Earned points are calculated by fetching score data for each assignment.
    The grade is calculated as the percentage of earned points to total points.
    A letter grade is also checked and printed depending on the percentage result.
    """
    total_points = 0
    earned_points = 0

    for assignment in assignments:
        total_points += assignment['points_possible']
        submission_url = f"{BASE_URL}/courses/{COURSE_ID}/assignments/{assignment['id']}/submissions/self"
        submission = get(submission_url)
        if 'score' in submission:
            earned_points += submission['score']

    percentage = (earned_points / total_points) * 100 if total_points else 0

    if percentage >= 90:
        letter_grade = 'A'
    elif percentage >= 70:
        letter_grade = 'B'
    elif percentage >= 50:
        letter_grade = 'C'
    elif percentage >= 30:
        letter_grade = 'D'
    elif percentage >= 20:
        letter_grade = 'E'
    else:
        letter_grade = 'F'

    return percentage, letter_grade

try:
    assignments = get_all_assignments()
except ValueError as e:
    print(e)
    sys.exit(1)

grade = calculate_grade(assignments)

print(f'Your grade for the Ethical Hacking course is: {grade[0]}% ({grade[1]})')
