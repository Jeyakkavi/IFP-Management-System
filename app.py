from flask import Flask, abort, render_template, redirect, send_file, url_for, request, flash, get_flashed_messages,send_from_directory
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'mshshmhsetajdhnbjhs'  # Change this to a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
migrate = Migrate(app, db)






app.config['upload_directory'] = r"C:\Users\Kavi2\OneDrive\Pictures\projlast\uploads"
# Mock user data - replace this with your actual user authentication mechanism



# Models

class Project(db.Model):
    __tablename__ = 'project'
    pid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    fid = db.Column(db.Integer, db.ForeignKey('faculty.fid'), index=True)
    faculty = db.relationship('Faculty', backref=db.backref('projects', lazy=True))
    students = db.relationship('Student', secondary='project_student', backref=db.backref('projects', lazy='joined'))
    amount_sanctioned = db.Column(db.Float, index=True)
    start_date = db.Column(db.Date, index=True)
    end_date = db.Column(db.Date)
    duration = db.Column(db.Integer, index=True)  # in months
    domain = db.Column(db.String(100), index=True)
    sanction_copy = db.Column(db.String(100))  # Assuming file path
    academic_year = db.Column(db.String(20), index=True)
    items_approved = db.Column(db.String, nullable=True)
    

class Student(db.Model):
    __tablename__ = 'student'
    regno = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=True)
    name = db.Column(db.String(100), index=True)
    year = db.Column(db.Integer, index=True)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    fid = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), index=True)

class ProjectStudent(db.Model):
    __tablename__ = 'project_student'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer, db.ForeignKey('project.pid'))
    regno = db.Column(db.String(20), db.ForeignKey('student.regno'))


class Task(db.Model):
    __tablename__ = 'task'
    tid = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.pid'))
    description = db.Column(db.String(255), nullable=True)
    project = db.relationship('Project', backref='tasks')

class Progress(db.Model):
    __tablename__ = 'progress'
    pid = db.Column(db.Integer, db.ForeignKey('project.pid'), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    fid = db.Column(db.Integer, db.ForeignKey('faculty.fid'))
    faculty = db.relationship('Faculty', backref=db.backref('progress', lazy=True))
    comment = db.Column(db.String(500))
    task_completed = db.Column(db.Integer, default=0)
    project = db.relationship('Project', backref='progress')

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from flask_login import login_required, current_user


@app.route('/admin')
@login_required
def admin_panel():
    # Render the admin panel view
    return render_template('admin_panel.html')


admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

class FacultyView(ModelView):
    column_display_pk = True  # Display primary keys in the list view
    form_columns = ['fname']  # Define which columns are editable in the form

    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        # Redirect to login page if user is not authenticated or is not admin
        return redirect(url_for('index'))


admin.add_view(FacultyView(Faculty, db.session))



login_manager = LoginManager()
login_manager.init_app(app)

# Mock users dictionary (replace with actual database queries)
users = {
    'admin': {'username': 'admin', 'password': 'ad123', 'role': 'admin'},
    'faculty': {'username': 'faculty', 'password': 'fac123', 'role': 'faculty'}
}

# User class
class User(UserMixin):
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def get_id(self):
        return self.username

# User loader function
@login_manager.user_loader
def load_user(username):
    user_data = users.get(username)
    if user_data:
        return User(user_data['username'], user_data['role'])
    return None

# Unauthorized handler
@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized access! Please log in.', 'error')
    return redirect(url_for('index'))

# Index route
@app.route('/')
def index():
    return render_template('index.html')

# Admin login route
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password == users[username]['password']:
            user = load_user(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('admin_login.html')

# Faculty login route
@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and password == users[username]['password']:
            user = load_user(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')
    return render_template('faculty_login.html')

# Example route to render the dashboard template
@app.route('/dashboard')
@login_required
def dashboard():
    user_role = current_user.role if current_user.is_authenticated else None
    print(user_role)  # Just for testing, remove in production
    return render_template('dashboard.html', user_role=user_role)

from sqlalchemy.orm.exc import NoResultFound
# Routes
# Add Project route
@app.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        title = request.form['title']
        items_approved = request.form['items_approved']
        domain = request.form['domain']
        fid = request.form['faculty']
        student_names = [name.strip() for name in request.form.get('students').split(',')]  # Split and strip student names

        amount_sanctioned = request.form['amount_sanctioned']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        duration = request.form['duration']
        academic_year = request.form['academic_year']


    

        sanction_copy = None
        if 'sanction_copy' in request.files:
            file = request.files['sanction_copy']
            if file.filename != '':
                sanction_copy = save_sanction_copy(file)
                if sanction_copy:
                    sanction_copy_path = os.path.join('uploads', sanction_copy)
                else:
                    flash('File is not in allowed files.', 'error')
                    return render_template('add_project.html', faculties=Faculty.query.all())

        # Get or create students and associate them with the project
        students = []
        for student_name in student_names:
            student = Student.query.filter_by(name=student_name).first()
            if not student:
                student = Student(name=student_name)
                db.session.add(student)
            students.append(student)

        # Create Project object and save to database
        project = Project(title=title, items_approved=items_approved, domain=domain, fid=fid, students=students, amount_sanctioned=amount_sanctioned,
                          start_date=start_date, end_date=end_date, duration=duration,
                          academic_year=academic_year,sanction_copy=sanction_copy_path)
        #project.sanction_copy = sanction_copy_path  # Store the relative file path
        db.session.add(project)
        db.session.commit()  # Commit changes to the database

        flash('Project added successfully', 'success')

        # Redirect to the View Projects page
        return redirect(url_for('dashboard'))

    # Render the Add Project form
    return render_template('add_project.html', faculties=Faculty.query.all())


#ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'pdf'}  # Set of allowed file extensions
#UPLOADS = 'uploads'

import os
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'pdf'}  # Set of allowed file extensions

def save_sanction_copy(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Define the directory to save the files (change this to your desired directory)
        upload_dir = 'uploads'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)
        return filename
    return None



UPLOADS_DIR = 'uploads'
@app.route('/download_sanction_copy/<int:pid>')
def download_sanction_copy(pid):
    # Retrieve the project by its ID
    project = Project.query.get_or_404(pid)
    
    # Check if the project has a sanction copy
    if project.sanction_copy:
        # Extract the filename from the file path
        filename = os.path.basename(project.sanction_copy)
        # Serve the file for download
        return send_from_directory(app.config['upload_directory'], filename, as_attachment=True)
    else:
        flash('Sanction copy not found for this project.', 'error')
        # Redirect to an appropriate page (e.g., project details)
        return redirect(url_for('view_projects', pid=pid))


def save_sanction_copy(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['upload_directory'], filename)
        file.save(file_path)
        return filename
    

from sqlalchemy import or_
from sqlalchemy.sql import func

@app.route('/search_projects', methods=['GET'])
def search_projects():
    search_by = request.args.get('search_by')
    keyword = request.args.get('keyword')

    if not search_by or not keyword:
        flash('Please provide both search criteria and keyword.', 'warning')
        return render_template('search_projects.html')

    try:
        if search_by == 'student':
            projects = Project.query.join(ProjectStudent).join(Student).filter(Student.name.ilike(f'%{keyword}%')).all()
        elif search_by == 'faculty':
            projects = Project.query.join(Faculty).filter(Faculty.fname.ilike(f'%{keyword}%')).all()
        elif search_by == 'amount_sanctioned':
            projects = Project.query.filter(Project.amount_sanctioned == float(keyword)).all()
        elif search_by == 'start_date':
            projects = Project.query.filter(func.DATE(Project.start_date) == keyword).all()
        elif search_by == 'duration':
            projects = Project.query.filter(Project.duration == int(keyword)).all()
        elif search_by == 'domain':
            projects = Project.query.filter(Project.domain.ilike(f'%{keyword}%')).all()
        elif search_by == 'academic_year':
            projects = Project.query.filter(Project.academic_year.ilike(f'%{keyword}%')).all()
        elif search_by == 'title':
            projects = Project.query.filter(Project.title.ilike(f'%{keyword}%')).all()
        else:
            flash('Invalid search criteria.', 'info')
            return render_template('search_project.html')
    except ValueError:
        flash('Invalid keyword format.', 'warning')
        return render_template('search_projects.html')

    if not projects:
        flash('No projects found.', 'info')
    
    return render_template('search_results.html', projects=projects)


@app.route('/search_results', methods=['GET'])
def search_results():

    search_by = request.args.get('search_by')
    keyword = request.args.get('keyword')

    flash('Please perform a search first.', 'info')
    return render_template('search_projects.html')

@app.route('/view_projectss')
def view_projectss():
    projects = Project.query.all()
    return render_template('view_projectss.html', projects=projects)


@app.route('/ongoing_projectss')
def ongoing_projectss():
    project = Project.query.all()
    #project.fid= request.form['faculty']
    # Logic to retrieve and display ongoing projects
    ongoing_projectss = Project.query.filter(Project.end_date >= datetime.now()).all()
    
    # Render the template with the ongoing projects
    return render_template('ongoing_projectss.html', ongoing_projectss=ongoing_projectss, project=project)

@app.route('/completed_projectss')
def completed_projectss():
    project = Project.query.all()
    #project.fid= request.form['faculty']
    completed_projectss = Project.query.filter(Project.end_date < datetime.now()).all()

    # Render the template with the completed projects
    return render_template('completed_projectss.html', completed_projectss=completed_projectss,project=project)


# Assuming you have a Project model defined with SQLAlchemy

@app.route('/check_paths')
def check_paths():
    projects = Project.query.all()

    for project in projects:
        print(f"Project ID: {project.title}, Sanction Copy Path: {project.sanction_copy}")

    return "Paths checked. Check your console for output."

@app.route('/progress')
@login_required
def progress():
    projects = Project.query.all()
    return render_template('progress.html', projects=projects, calculate_completion_percentage=calculate_completion_percentage)

@app.route('/task/<int:pid>')
@login_required
def task(pid):
    project = Project.query.get_or_404(pid)
    tasks = Task.query.filter_by(project_id=pid).all()
    return render_template('task.html', project=project, tasks=tasks)

@app.route('/mark_task_completed', methods=['POST'])
@login_required
def mark_task_completed():
    task_id = request.form.get('task_tid')
    task_type = request.form.get('task_type')
    task = Task.query.get_or_404(task_id)
    progress = Progress.query.filter_by(pid=task.project_id, date=date.today()).first()
    
    if not progress:
        progress = Progress(pid=task.project_id, date=date.today(), task_completed=0)
        db.session.add(progress)

    # Increment the task_completed count
    progress.task_completed += 1
    
    db.session.commit()
    return redirect(url_for('task', pid=task.project_id))

def calculate_completion_percentage(pid):
    tasks = Task.query.filter_by(project_id=pid).all()
    if not tasks:
        return 0.0
    
    total_subtasks = len(tasks) * 4  # Each task has 4 subtasks
    progress_entries = Progress.query.filter_by(pid=pid).all()
    completed_subtasks = sum(entry.task_completed for entry in progress_entries)
    
    return (completed_subtasks / total_subtasks) * 100.0

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

