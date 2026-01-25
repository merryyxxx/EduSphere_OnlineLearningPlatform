"""
EduSphere - Complete Flask Application (Single File Version)
All configurations, models, forms, and routes in one file
"""

# ==================== IMPORTS ====================
import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

# ==================== FLASK APP INITIALIZATION ====================
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'edusphere-secret-key-2024-dev'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://root:@localhost/edusphere_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['COURSES_PER_PAGE'] = 9
app.config['USERS_PER_PAGE'] = 10

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# ==================== DATABASE MODELS ====================

class User(UserMixin, db.Model):
    """User model for students, instructors, and admins"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')
    bio = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses_taught = db.relationship('Course', backref='instructor', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('Enrollment', backref='student', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='reviewer', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Category(db.Model):
    """Category model for course classification"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    courses = db.relationship('Course', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Course(db.Model):
    """Course model for educational content"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    duration = db.Column(db.String(50), nullable=True)
    level = db.Column(db.String(20), nullable=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def get_enrollment_count(self):
        """Get number of students enrolled"""
        return len(self.enrollments)
    
    def get_average_rating(self):
        """Calculate average rating from reviews"""
        if not self.reviews:
            return 0
        return sum(review.rating for review in self.reviews) / len(self.reviews)
    
    def __repr__(self):
        return f'<Course {self.title}>'


class Enrollment(db.Model):
    """Enrollment model for student-course relationship"""
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)
    
    def __repr__(self):
        return f'<Enrollment User:{self.user_id} Course:{self.course_id}>'


class Review(db.Model):
    """Review model for course ratings and feedback"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_review'),)
    
    def __repr__(self):
        return f'<Review User:{self.user_id} Course:{self.course_id} Rating:{self.rating}>'

# ==================== FORMS ====================

class RegistrationForm(FlaskForm):
    """User registration form"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=3, max=100, message='Name must be between 3 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    role = SelectField('Register as', choices=[
        ('student', 'Student'),
        ('instructor', 'Instructor')
    ], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_email(self, email):
        """Check if email already exists"""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')


class LoginForm(FlaskForm):
    """User login form"""
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    submit = SubmitField('Login')


class CourseForm(FlaskForm):
    """Course creation and editing form"""
    title = StringField('Course Title', validators=[
        DataRequired(message='Title is required'),
        Length(min=5, max=200, message='Title must be between 5 and 200 characters')
    ])
    description = TextAreaField('Course Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=20, message='Description must be at least 20 characters')
    ])
    price = FloatField('Price (USD)', validators=[
        DataRequired(message='Price is required'),
        NumberRange(min=0, message='Price cannot be negative')
    ])
    duration = StringField('Duration', validators=[
        DataRequired(message='Duration is required'),
        Length(max=50)
    ])
    level = SelectField('Level', choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced')
    ], validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[
        DataRequired(message='Please select a category')
    ])
    submit = SubmitField('Save Course')


class ProfileForm(FlaskForm):
    """User profile update form"""
    name = StringField('Full Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=3, max=100)
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    bio = TextAreaField('Bio', validators=[
        Length(max=500, message='Bio cannot exceed 500 characters')
    ])
    submit = SubmitField('Update Profile')

# ==================== UTILITY FUNCTIONS ====================

def role_required(*roles):
    """Decorator to restrict access based on user role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def format_currency(amount):
    """Format number as USD currency"""
    return f"${amount:,.2f}"

def format_date(date):
    """Format datetime object to readable string"""
    if date:
        return date.strftime('%B %d, %Y')
    return 'N/A'

# ==================== FLASK-LOGIN SETUP ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Template filters
@app.template_filter('currency')
def currency_filter(amount):
    return format_currency(amount)

@app.template_filter('date')
def date_filter(date):
    return format_date(date)

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    """Home page with featured courses"""
    featured_courses = Course.query.order_by(Course.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    return render_template('index.html', courses=featured_courses, categories=categories)

@app.route('/courses')
def courses():
    """Browse all courses with search and filter"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    
    query = Course.query
    
    if search:
        query = query.filter(or_(
            Course.title.contains(search),
            Course.description.contains(search)
        ))
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    courses = query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=app.config['COURSES_PER_PAGE'], error_out=False
    )
    
    categories = Category.query.all()
    return render_template('courses.html', courses=courses, categories=categories, 
                         search=search, selected_category=category_id)

@app.route('/course/<int:course_id>')
def course_details(course_id):
    """Display single course details"""
    course = Course.query.get_or_404(course_id)
    reviews = Review.query.filter_by(course_id=course_id).order_by(Review.created_at.desc()).all()
    
    is_enrolled = False
    if current_user.is_authenticated:
        enrollment = Enrollment.query.filter_by(
            user_id=current_user.id, course_id=course_id
        ).first()
        is_enrolled = enrollment is not None
    
    return render_template('course_details.html', course=course, 
                         reviews=reviews, is_enrolled=is_enrolled)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(f'Welcome back, {user.name}!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            elif user.role == 'admin':
                return redirect(url_for('admin_panel'))
            elif user.role == 'instructor':
                return redirect(url_for('instructor_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# ==================== STUDENT ROUTES ====================

@app.route('/dashboard/student')
@login_required
@role_required('student')
def student_dashboard():
    """Student dashboard showing enrolled courses"""
    enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
    return render_template('student_dashboard.html', enrollments=enrollments)

@app.route('/enroll/<int:course_id>')
@login_required
@role_required('student')
def enroll_course(course_id):
    """Enroll student in a course"""
    course = Course.query.get_or_404(course_id)
    
    existing = Enrollment.query.filter_by(
        user_id=current_user.id, course_id=course_id
    ).first()
    
    if existing:
        flash('You are already enrolled in this course.', 'info')
    else:
        enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash(f'Successfully enrolled in {course.title}!', 'success')
    
    return redirect(url_for('student_dashboard'))

@app.route('/unenroll/<int:enrollment_id>')
@login_required
@role_required('student')
def unenroll_course(enrollment_id):
    """Unenroll from a course"""
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    
    if enrollment.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('student_dashboard'))
    
    course_title = enrollment.course.title
    db.session.delete(enrollment)
    db.session.commit()
    flash(f'Unenrolled from {course_title}.', 'info')
    return redirect(url_for('student_dashboard'))

# ==================== INSTRUCTOR ROUTES ====================

@app.route('/dashboard/instructor')
@login_required
@role_required('instructor')
def instructor_dashboard():
    """Instructor dashboard for managing courses"""
    courses = Course.query.filter_by(instructor_id=current_user.id).all()
    return render_template('instructor_dashboard.html', courses=courses)

@app.route('/course/create', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def create_course():
    """Create a new course"""
    form = CourseForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            level=form.level.data,
            category_id=form.category_id.data,
            instructor_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('instructor_dashboard'))
    
    return render_template('course_form.html', form=form, action='Create')

@app.route('/course/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
@role_required('instructor')
def edit_course(course_id):
    """Edit existing course"""
    course = Course.query.get_or_404(course_id)
    
    if course.instructor_id != current_user.id:
        flash('You can only edit your own courses.', 'danger')
        return redirect(url_for('instructor_dashboard'))
    
    form = CourseForm(obj=course)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.all()]
    
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.price = form.price.data
        course.duration = form.duration.data
        course.level = form.level.data
        course.category_id = form.category_id.data
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('instructor_dashboard'))
    
    return render_template('course_form.html', form=form, action='Edit', course=course)

@app.route('/course/delete/<int:course_id>')
@login_required
@role_required('instructor')
def delete_course(course_id):
    """Delete a course"""
    course = Course.query.get_or_404(course_id)
    
    if course.instructor_id != current_user.id:
        flash('You can only delete your own courses.', 'danger')
        return redirect(url_for('instructor_dashboard'))
    
    course_title = course.title
    db.session.delete(course)
    db.session.commit()
    flash(f'Course "{course_title}" deleted successfully.', 'success')
    return redirect(url_for('instructor_dashboard'))

# ==================== ADMIN ROUTES ====================

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    """Admin panel for managing users and categories"""
    users = User.query.all()
    categories = Category.query.all()
    courses = Course.query.all()
    
    stats = {
        'total_users': len(users),
        'total_courses': len(courses),
        'total_enrollments': Enrollment.query.count(),
        'total_categories': len(categories)
    }
    
    return render_template('admin_panel.html', users=users, categories=categories, 
                         courses=courses, stats=stats)

@app.route('/admin/category/add', methods=['POST'])
@login_required
@role_required('admin')
def add_category():
    """Add new category"""
    name = request.form.get('name')
    description = request.form.get('description')
    
    if name:
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
    else:
        flash('Category name is required.', 'danger')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/category/delete/<int:category_id>')
@login_required
@role_required('admin')
def delete_category(category_id):
    """Delete a category"""
    category = Category.query.get_or_404(category_id)
    
    if category.courses:
        flash('Cannot delete category with existing courses.', 'danger')
    else:
        db.session.delete(category)
        db.session.commit()
        flash('Category deleted successfully.', 'success')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin/user/delete/<int:user_id>')
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
    else:
        user_name = user.name
        db.session.delete(user)
        db.session.commit()
        flash(f'User "{user_name}" deleted successfully.', 'success')
    
    return redirect(url_for('admin_panel'))

# ==================== PROFILE ROUTES ====================

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('profile.html', form=form)

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500

# ==================== DATABASE INITIALIZATION ====================

def init_database():
    """Initialize the database with tables"""
    with app.app_context():
        db.create_all()
        print('✅ Database tables created successfully!')
        print('📊 Tables created: users, courses, categories, enrollments, reviews')

def seed_database():
    """Seed database with sample data"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(email='admin@edusphere.com').first()
        if existing_admin:
            print('⚠️  Admin user already exists!')
            return
        
        # Create admin user
        admin = User(name='Admin User', email='admin@edusphere.com', role='admin')
        admin.set_password('admin123')
        
        # Create sample categories
        categories = [
            Category(name='Web Development', description='Build websites and web applications'),
            Category(name='Data Science', description='Analyze and visualize data'),
            Category(name='Mobile Development', description='Create mobile apps'),
            Category(name='Design', description='UI/UX and graphic design'),
            Category(name='Business', description='Business and entrepreneurship'),
            Category(name='Marketing', description='Digital marketing strategies')
        ]
        
        db.session.add(admin)
        db.session.add_all(categories)
        db.session.commit()
        
        print('✅ Database seeded successfully!')
        print('━' * 50)
        print('📧 Admin Email: admin@edusphere.com')
        print('🔑 Admin Password: admin123')
        print('━' * 50)
        print('📂 Categories created: 6')
        print('👤 Admin user created: 1')

# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    import sys
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == 'init_db':
            print('🔧 Initializing database...')
            init_database()
            sys.exit(0)
        elif sys.argv[1] == 'seed_db':
            print('🌱 Seeding database...')
            seed_database()
            sys.exit(0)
    
    # Run Flask application
    print('━' * 50)
    print('🎓 EduSphere - Online Learning Platform')
    print('━' * 50)
    print('🚀 Starting server...')
    print('📍 URL: http://127.0.0.1:5000')
    print('━' * 50)
    app.run(debug=True)