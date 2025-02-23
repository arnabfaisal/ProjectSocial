Social Media Application
A simple Django-based social media platform that allows users to create, read, update, and delete posts. Users can share text content and images while maintaining their own profiles.



erDiagram
    User ||--o{ Post : creates
    User {
        string username
        string email
        string password
        datetime date_joined
    }
    Post {
        int id
        string content
        string image
        datetime created_at
        datetime updated_at
        int user_id FK
    }


Features

User Authentication

User registration with email
Login/logout functionality
Password protection


Post Management

Create new posts with text and optional images
View all posts on the homepage
View personal posts on profile page
Edit and delete own posts
Image upload support


User Interface

Responsive navigation bar
Bootstrap-based clean design
Flash messages for user feedback
Mobile-friendly layout



Test Credentials
Regular Users

Username: testuser1
Password: test1234
Username: testuser2
Password: test1234

Admin User

Username: admin
Password: admin

git clone <repository-url>
cd social_media
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

run requirements.txt
pip install -r requirements.txt

Technical Details

Framework: Django 4.2
Database: SQLite (default)
Frontend: Bootstrap 5
Image Handling: Django ImageField with Pillow
Authentication: Django's built-in authentication system