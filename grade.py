import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = 'https://canvas.kth.se/api/v1'
COURSE_ID = '41678' # EN2720 Ethical Hacking


def get(url):
    """Fetch data from the provided URL."""
    response = requests.get(
        url,
        headers={'Authorization': f'Bearer {API_KEY}'},
        timeout=10
    ) 
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
    """
    total_points = 0
    earned_points = 0

    for assignment in assignments:
        total_points += assignment['points_possible']
        submission_url = f"{BASE_URL}/courses/{COURSE_ID}/assignments/{assignment['id']}/submissions/self"
        submission = get(submission_url)
        if 'score' in submission:
            earned_points += submission['score']

    return (earned_points / total_points) * 100 if total_points else 0


assignments = get_all_assignments()
grade = calculate_grade(assignments)

print(f'My grade for the Ethical Hacking course is: {grade}%')
