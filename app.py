from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from datetime import datetime
from statistics import mean, median
from dotenv import load_dotenv

# Monkeypatch: ensure gotrue/http client accepts a `proxy` kwarg.
# Some versions of the Supabase/gotrue libraries pass `proxy=` into
# their internal http client constructor but httpx.Client does not
# accept `proxy` as a keyword. This causes a TypeError when deployed
# to some environments (e.g. Render) where installed package versions
# differ. The patch below defines a compatible SyncClient and injects
# it into gotrue before importing Supabase.
# try:
#     from httpx import Client as HTTPXClient
#     import gotrue.http_clients as _gotrue_http_clients

#     class _PatchedSyncClient(HTTPXClient):
#         def __init__(self, *args, proxy=None, **kwargs):
#             # map a `proxy` kwarg to httpx `proxies`
#             if proxy is not None:
#                 kwargs.setdefault("proxies", {"all": proxy})
#             super().__init__(*args, **kwargs)

#         def aclose(self) -> None:
#             self.close()

#     # Inject the patched client into gotrue module so subsequent imports use it
#     _gotrue_http_clients.SyncClient = _PatchedSyncClient
# except Exception:
#     # If monkeypatching fails for any reason, continue and let import-time
#     # errors surface when creating the Supabase client.
#     pass

from supabase import create_client

load_dotenv()

app = Flask(__name__)

supabase = create_client(
    os.getenv('VITE_SUPABASE_URL'),
    os.getenv('VITE_SUPABASE_ANON_KEY')
)

def calculate_grade_letter(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def calculate_gpa(grades):
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    if not grades:
        return 0.0
    total_points = sum(grade_points.get(g['grade_letter'], 0) for g in grades)
    return round(total_points / len(grades), 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def students():
    response = supabase.table('students').select('*').order('name').execute()
    return render_template('students.html', students=response.data)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'enrollment_date': request.form.get('enrollment_date', datetime.now().date().isoformat())
        }
        supabase.table('students').insert(data).execute()
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/courses')
def courses():
    response = supabase.table('courses').select('*').order('code').execute()
    return render_template('courses.html', courses=response.data)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'code': request.form['code'],
            'credits': int(request.form['credits'])
        }
        supabase.table('courses').insert(data).execute()
        return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/grades')
def grades():
    response = supabase.table('grades').select('*, students(*), courses(*)').order('created_at', desc=True).execute()
    return render_template('grades.html', grades=response.data)

@app.route('/grades/add', methods=['GET', 'POST'])
def add_grade():
    if request.method == 'POST':
        score = float(request.form['score'])
        data = {
            'student_id': request.form['student_id'],
            'course_id': request.form['course_id'],
            'score': score,
            'grade_letter': calculate_grade_letter(score),
            'semester': request.form['semester'],
            'year': int(request.form['year'])
        }
        supabase.table('grades').insert(data).execute()
        return redirect(url_for('grades'))

    students = supabase.table('students').select('*').order('name').execute()
    courses = supabase.table('courses').select('*').order('code').execute()
    return render_template('add_grade.html', students=students.data, courses=courses.data)

@app.route('/student/<student_id>/performance')
def student_performance(student_id):
    student = supabase.table('students').select('*').eq('id', student_id).single().execute()
    grades_response = supabase.table('grades').select('*, courses(*)').eq('student_id', student_id).execute()

    grades = grades_response.data

    if not grades:
        analytics = {
            'total_courses': 0,
            'average_score': 0,
            'gpa': 0.0,
            'highest_score': 0,
            'lowest_score': 0,
            'median_score': 0
        }
    else:
        scores = [g['score'] for g in grades]
        analytics = {
            'total_courses': len(grades),
            'average_score': round(mean(scores), 2),
            'gpa': calculate_gpa(grades),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'median_score': round(median(scores), 2)
        }

    return render_template('student_performance.html',
                         student=student.data,
                         grades=grades,
                         analytics=analytics)

@app.route('/analytics')
def analytics():
    students = supabase.table('students').select('*').execute()
    grades = supabase.table('grades').select('*').execute()
    courses = supabase.table('courses').select('*').execute()

    total_students = len(students.data)
    total_courses = len(courses.data)
    total_grades = len(grades.data)

    if grades.data:
        all_scores = [g['score'] for g in grades.data]
        overall_average = round(mean(all_scores), 2)

        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for g in grades.data:
            grade_distribution[g['grade_letter']] += 1
    else:
        overall_average = 0
        grade_distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}

    stats = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_grades': total_grades,
        'overall_average': overall_average,
        'grade_distribution': grade_distribution
    }

    return render_template('analytics.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
