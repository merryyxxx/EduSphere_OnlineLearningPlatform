# EduSphere - Online Learning Platform

![EduSphere Banner](static/images/banner.png)

## 📚 Project Overview

**EduSphere** is a comprehensive full-stack online learning management system built with Python Flask, SQLAlchemy, and Bootstrap 5. It connects students, instructors, and administrators in a seamless educational environment with course management, enrollment tracking, and role-based access control.

**Project Type:** Academic Assignment - Web Technology (BIT233)  
**Institution:** Texas College of Management & IT  
**Submitted By:** Merry Subedi (LC00017003482)  
**Academic Year:** 2024  
**Submission Date:** January 26, 2026

---

## 🌟 Key Features

### For Students
- ✅ Browse and search courses
- ✅ Enroll in courses
- ✅ Track learning progress
- ✅ Manage course enrollments
- ✅ View personalized dashboard
- ✅ Update profile information

### For Instructors
- ✅ Create and manage courses
- ✅ Edit course details
- ✅ View enrolled students
- ✅ Track course performance
- ✅ Instructor-specific dashboard
- ✅ CRUD operations on own courses

### For Administrators
- ✅ Complete user management
- ✅ Category management
- ✅ Platform statistics overview
- ✅ System-wide course management
- ✅ User role assignment
- ✅ Comprehensive admin panel

### Technical Features
- ✅ Role-based access control (Student, Instructor, Admin)
- ✅ Secure authentication with password hashing
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ RESTful architecture
- ✅ Flash messaging system
- ✅ Search and filter functionality
- ✅ Form validation (client and server-side)
- ✅ Protected routes with decorators
- ✅ Database relationships (One-to-Many, Many-to-Many)

---

## 🛠️ Technology Stack

### Backend
- **Python 3.10+**
- **Flask 2.3.0** - Web framework
- **Flask-SQLAlchemy 3.0.0** - ORM for database operations
- **Flask-Login 0.6.2** - User session management
- **Werkzeug 2.3.0** - Password hashing and security
- **SQLite/MySQL** - Database

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Flexbox and Grid
- **Bootstrap 5.3.0** - Responsive framework
- **JavaScript ES6+** - Client-side interactivity
- **jQuery 3.7.0** - DOM manipulation
- **Bootstrap Icons** - Icon library
- **Google Fonts** - Typography (Poppins, Inter)

### Development Tools
- **VS Code** - IDE
- **Git/GitHub** - Version control
- **Figma** - UI/UX design
- **DB Browser for SQLite** - Database management
- **Chrome DevTools** - Testing and debugging

---

## 📁 Project Structure

```
EDUSPHERE/
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── images/                # Image assets
│   └── js/
│       └── script.js          # Client-side JavaScript
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Homepage
│   ├── courses.html           # Course listing page
│   ├── course_details.html    # Individual course page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── student_dashboard.html # Student dashboard
│   ├── instructor_dashboard.html # Instructor dashboard
│   ├── admin_panel.html       # Admin panel
│   ├── course_form.html       # Create/Edit course form
│   ├── profile.html           # User profile page
│   └── 404.html               # Error page
├── app.py                     # Main Flask application
├── models.py                  # Database models (if separated)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 💾 Database Schema

### Users Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(100) | Not Null |
| email | String(120) | Unique, Not Null |
| password_hash | String(255) | Not Null |
| role | String(20) | Default: 'student' |
| bio | Text | Nullable |
| created_at | DateTime | Default: Now |

### Courses Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| title | String(200) | Not Null |
| description | Text | Not Null |
| price | Float | Not Null |
| duration | String(50) | Nullable |
| level | String(20) | Nullable |
| instructor_id | Integer | Foreign Key → users.id |
| category_id | Integer | Foreign Key → categories.id |
| created_at | DateTime | Default: Now |

### Categories Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(100) | Unique, Not Null |
| description | Text | Nullable |
| created_at | DateTime | Default: Now |

### Enrollments Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key → users.id |
| course_id | Integer | Foreign Key → courses.id |
| progress | Integer | Default: 0 |
| completed | Boolean | Default: False |
| enrolled_at | DateTime | Default: Now |

**Unique Constraint:** (user_id, course_id) - Prevents duplicate enrollments

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning repository)
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the Repository**
```bash
git clone https://github.com/merryyxxx/EduSphere_OnlineLearningPlatform.git
cd EduSphere_OnlineLearningPlatform
```

2. **Create Virtual Environment**
```bash
# Create virtual environment
python -m venv backend_flask

# Activate virtual environment
# On Windows:
backend_flask\Scripts\activate

# On macOS/Linux:
source backend_flask/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize Database**
```bash
# Initialize database tables
python app.py init_db

# Seed database with sample data
python app.py seed_db
```

5. **Run the Application**
```bash
python app.py
```

6. **Access the Application**
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 👥 Default User Accounts

### Admin Account
- **Email:** admin@edusphere.com
- **Password:** Admin@123
- **Access:** Full system control, user management, statistics

### Test Instructor Account
- **Email:** instructor@edusphere.com
- **Password:** Instructor@123
- **Access:** Create/manage courses, view enrollments

### Test Student Account
- **Email:** student@edusphere.com
- **Password:** Student@123
- **Access:** Browse/enroll courses, track progress

---

## 📖 User Guide

### For Students

1. **Registration**
   - Click "Register" in navigation
   - Fill in name, email, password
   - Select "Student" role
   - Submit form

2. **Browse Courses**
   - Navigate to "Courses" page
   - Use search bar for specific courses
   - Filter by category
   - Click "View Course" for details

3. **Enroll in Course**
   - View course details
   - Click "Enroll Now" button
   - Access from "My Courses" in dashboard

4. **Track Progress**
   - Go to Student Dashboard
   - View enrolled courses
   - Update progress
   - Mark courses as completed

### For Instructors

1. **Create Course**
   - Login as instructor
   - Go to Instructor Dashboard
   - Click "Create New Course"
   - Fill course details (title, description, price, duration, level, category)
   - Submit form

2. **Manage Courses**
   - View all created courses in dashboard
   - Click "Edit" to modify course
   - Click "Delete" to remove course
   - View student enrollments

3. **Update Course**
   - Click "Edit" on course card
   - Modify course information
   - Save changes

### For Administrators

1. **Access Admin Panel**
   - Login with admin credentials
   - Navigate to "Admin Panel"

2. **Manage Users**
   - View all registered users
   - Edit user roles
   - Delete users if needed
   - View user statistics

3. **Manage Categories**
   - Create new course categories
   - Edit existing categories
   - View courses per category

4. **Platform Overview**
   - View total users, courses, enrollments
   - Monitor platform activity
   - Generate reports

---

## 🎨 Design System

### Color Palette
- **Primary Background:** Cream (#f5ead6)
- **Secondary/Text:** Navy (#3d4d65)
- **Accent:** Yellow (#ffd94d)
- **Success:** Teal (#4ecdc4)
- **Cards:** White (#ffffff)

### Typography
- **Headings:** Poppins (700-800 weight)
- **Body Text:** Inter (400-600 weight)
- **Sizes:** H1: 3.5rem, H2: 2.5rem, Body: 1rem

### UI Components
- **Border Radius:** Cards (20px), Buttons (12px)
- **Shadows:** 0 8px 24px rgba(0,0,0,0.1)
- **Spacing Scale:** 8px, 16px, 24px, 40px, 64px

### Responsive Breakpoints
- **Mobile:** 0-767px (1 column layout)
- **Tablet:** 768-1199px (2 column layout)
- **Desktop:** 1200px+ (4 column layout)

---

## 🔒 Security Features

1. **Password Security**
   - Werkzeug password hashing (PBKDF2)
   - Minimum password length validation
   - Password confirmation required

2. **Authentication**
   - Flask-Login session management
   - Protected routes with @login_required
   - Role-based access control decorators

3. **Input Validation**
   - Server-side form validation
   - Client-side JavaScript validation
   - SQL injection prevention via SQLAlchemy ORM
   - XSS protection with Jinja2 auto-escaping

4. **Session Security**
   - Secure session cookies
   - CSRF protection
   - Session timeout

---

## 🧪 Testing

### Functional Testing
All 27 core features tested and verified:
- ✅ User registration and login
- ✅ Course CRUD operations
- ✅ Enrollment management
- ✅ Progress tracking
- ✅ Search and filter
- ✅ Role-based access
- ✅ Admin operations

### Cross-Browser Compatibility
- ✅ Chrome 120+
- ✅ Firefox 121+
- ✅ Safari 17+
- ✅ Microsoft Edge 120+

### Responsive Testing
- ✅ Mobile (375px - iPhone)
- ✅ Tablet (768px - iPad)
- ✅ Desktop (1920px)
- ✅ Touch-friendly interfaces
- ✅ Responsive navigation

### Security Testing
- ✅ SQL injection prevention
- ✅ XSS protection
- ✅ CSRF tokens
- ✅ Password hashing
- ✅ Session security

---

## 📸 Screenshots

### Homepage
![Homepage Desktop](screenshots/homepage-desktop.png)
*Responsive homepage with hero section and featured courses*

### Course Listing
![Course Listing](screenshots/courses.png)
*Grid layout with search and category filters*

### Student Dashboard
![Student Dashboard](screenshots/student-dashboard.png)
*Personalized dashboard showing enrolled courses and progress*

### Instructor Dashboard
![Instructor Dashboard](screenshots/instructor-dashboard.png)
*Course management interface for instructors*

### Admin Panel
![Admin Panel](screenshots/admin-panel.png)
*Comprehensive admin control panel*

### Mobile View
![Mobile View](screenshots/mobile-view.png)
*Fully responsive mobile interface*

---

## 🚀 Deployment

### PythonAnywhere Deployment

**Live URL:** https://edusphere.pythonanywhere.com

1. **Create Account**
   - Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload Files**
   - Upload project files via Files tab
   - Or clone from GitHub

3. **Setup Virtual Environment**
```bash
mkvirtualenv --python=/usr/bin/python3.10 edusphere-env
pip install -r requirements.txt
```

4. **Configure WSGI**
   - Edit WSGI configuration file
   - Point to Flask app
   - Set working directory

5. **Environment Variables**
   - Set SECRET_KEY
   - Set DATABASE_URI
   - Configure production settings

6. **Initialize Database**
```bash
python app.py init_db
python app.py seed_db
```

7. **Reload Web App**
   - Click "Reload" button
   - Access at your PythonAnywhere URL

---

## 🐛 Troubleshooting

### Common Issues

**Database Errors**
```bash
# Re-initialize database
python app.py init_db
```

**Import Errors**
```bash
# Ensure virtual environment is activated
source backend_flask/bin/activate  # macOS/Linux
backend_flask\Scripts\activate     # Windows
```

**Login Issues**
- Clear browser cache
- Check credentials
- Verify database has seed data

**500 Internal Server Error**
- Check console logs
- Verify all dependencies installed
- Check database connection

---

## 📝 API Endpoints

### Public Routes
- `GET /` - Homepage
- `GET /courses` - Course listing
- `GET /course/<int:id>` - Course details
- `GET /about` - About page

### Authentication Routes
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Student Routes (Login Required)
- `GET /dashboard/student` - Student dashboard
- `POST /enroll/<int:course_id>` - Enroll in course
- `POST /unenroll/<int:enrollment_id>` - Unenroll from course
- `POST /update-progress/<int:enrollment_id>` - Update progress

### Instructor Routes (Login Required)
- `GET /dashboard/instructor` - Instructor dashboard
- `GET/POST /course/create` - Create course
- `GET/POST /course/edit/<int:id>` - Edit course
- `POST /course/delete/<int:id>` - Delete course

### Admin Routes (Admin Only)
- `GET /admin` - Admin panel
- `POST /admin/delete-user/<int:user_id>` - Delete user
- `POST /admin/update-role/<int:user_id>` - Update user role

---

## 🤝 Contributing

This is an academic project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for academic purposes as part of the BIT233 Web Technology course at Texas College of Management & IT.

---

## 📞 Contact

**Student:** Merry Subedi  
**LCID:** LC00017003482  
**Email:** Subedimerry123@gmail.com 
**GitHub:** [@merryyxxx](https://github.com/merryyxxx)

**Course:** BIT233 - Web Technology  
**Instructor:** Mr. Ashish Gautam (PhD Scholar)  
**Institution:** Texas College of Management & IT

---

## 🙏 Acknowledgments

- **Flask Documentation** - Comprehensive web framework guide
- **Bootstrap 5** - Responsive design framework
- **SQLAlchemy** - Database ORM
- **Stack Overflow Community** - Problem-solving assistance
- **Mr. Ashish Gautam** - Course instructor and mentor
- **Texas College of Management & IT** - Academic support

---

## 📋 Requirements.txt

```
Flask==2.3.0
Flask-SQLAlchemy==3.0.0
Flask-Login==0.6.2
Werkzeug==2.3.0
email-validator==2.0.0
```

---

## 🎯 Project Objectives Achieved

✅ **Complete Full-Stack Application** - Frontend and backend integration  
✅ **CRUD Operations** - Create, Read, Update, Delete functionality  
✅ **User Authentication** - Secure login/registration system  
✅ **Role-Based Access Control** - Three user roles implemented  
✅ **Responsive Design** - Mobile, tablet, desktop compatibility  
✅ **Database Integration** - SQLAlchemy ORM with relationships  
✅ **Modern UI/UX** - Professional design with Bootstrap 5  
✅ **Git Version Control** - 20+ meaningful commits  
✅ **Documentation** - Comprehensive README and code comments  
✅ **Deployment** - Live on PythonAnywhere  

---

## 📊 Project Statistics

- **Total Lines of Code:** 3,000+
- **HTML Templates:** 12
- **Database Tables:** 4 (Users, Courses, Categories, Enrollments)
- **Routes/Endpoints:** 20+
- **Features Implemented:** 27
- **Git Commits:** 24+
- **Development Time:** 6 weeks
- **Pages:** 8+ interconnected pages

---

## 🔮 Future Enhancements

- [ ] Payment gateway integration (Stripe/PayPal)
- [ ] Video streaming for course content
- [ ] Quiz and assessment system
- [ ] Discussion forums
- [ ] Email notifications
- [ ] Course certificates
- [ ] Mobile application (React Native)
- [ ] Advanced analytics dashboard
- [ ] Course reviews and ratings
- [ ] Wishlist functionality
- [ ] Live chat support
- [ ] Social media integration

---

**⭐ If you found this project helpful, please consider giving it a star on GitHub!**

---

*Last Updated: January 26, 2026*