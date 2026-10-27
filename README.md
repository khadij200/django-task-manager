# 📋 Task Manager — Django & AI Chatbot

A web-based task management application built with **Python and Django**, featuring user authentication, task management, dashboard statistics, and an AI-powered chatbot integrated with the **Groq API**.

The application allows users to organize their daily tasks, track deadlines, monitor progress, and interact with an AI assistant in Arabic.

## Features

### User Authentication
- User registration and login.
- Protected task management pages.
- Each user can access and manage only their own tasks.

### Task Management
- Create new tasks.
- View existing tasks.
- Update task details.
- Delete tasks with confirmation.
- Set task priority and due dates.
- Track task completion status.

### Search and Filtering
- Search tasks by title.
- Filter tasks by status.

### Dashboard Statistics
- Total tasks.
- Completed tasks.
- Pending tasks.
- Overdue tasks.

### AI-Powered Chatbot
- Integration with the Groq API.
- Ask questions about existing tasks in Arabic.
- Create tasks using natural-language messages.
- Automatically extract task titles, priorities, and due dates from user requests.

## Technologies Used

| Component | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, Bootstrap, Django Templates |
| Database | SQLite |
| Authentication | Django Authentication System |
| AI Integration | Groq API |
| Environment Variables | python-dotenv |
| Version Control | Git & GitHub |

## Project Structure

```text
task-manager/
├── taskmanager/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tasks/
│   ├── migrations/
│   ├── templates/
│   │   └── tasks/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── signup.html
│   │       ├── task_list.html
│   │       ├── task_form.html
│   │       ├── task_confirm_delete.html
│   │       └── chatbot.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Prerequisites

Before running the project, install:

- Python 3 compatible with the project's Django version
- pip
- Git
- A Groq API key for the AI chatbot

## Installation and Setup

### Step 1: Clone the Repository

After publishing the project on GitHub, clone the repository using its HTTPS URL.

Navigate to the project directory:

```bash
cd task-manager
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows Command Prompt:**

```cmd
venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the location expected by the Django settings.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Replace the placeholder with your own API key.

Ensure that the Django settings load the environment variables before using the chatbot.

**Security:** Never commit API keys, passwords, or `.env` files to GitHub.

### Step 5: Apply Database Migrations

```bash
python manage.py migrate
```

This creates the necessary database tables.

### Step 6: Run the Django Server

```bash
python manage.py runserver
```

### Step 7: Open the Application

Visit:

http://127.0.0.1:8000/

Create an account, log in, and start managing your tasks.

To use the AI chatbot, configure a valid Groq API key.

## How It Works

1. A user creates an account and logs in.
2. Django authenticates the user.
3. The user can create, update, delete, search, and filter tasks.
4. Task information is stored in the SQLite database.
5. The dashboard displays task statistics.
6. The AI chatbot receives user messages and communicates with the Groq API.
7. The chatbot can answer questions about the user's tasks or create new tasks based on natural-language requests.

## Security and Privacy

- Task management views require authentication.
- Task queries are restricted to the authenticated user.
- Sensitive API keys are read from environment variables.
- The local SQLite database is excluded from Git.
- The application is intended for development and portfolio demonstration, not production deployment without additional security configuration.

## Future Improvements

- Add automated tests for task management and authentication.
- Add stronger validation for AI-generated task data.
- Add task categories and reminders.
- Add charts for task progress.
- Improve chatbot error handling.
- Deploy the application using production-ready Django settings.

## Author

**Khadija Alalawi**

Software Engineering Graduate

Developed as a full-stack software engineering portfolio project demonstrating Django development, database operations, authentication, and AI integration.