Yesterday 5:11 PM
me dashboard esa krna chahta hu ki cusstomer jab ticket likhe to use sare verity ko tivket ki slide open ho jaye aur wo isme se select kar le
tume select ticket type ka slider bna diya wo to shi kyi but muje cusstomer message ka bhi slider chahiye jime diff type k mess ho slider m bas select krna ho
Pasted code(6).py
Python
isme add ka do aur new dashoard codeee generate
ye error kyo show kar rha ha
this project can use 2 page compress in ine page
is link ko convert int live demo clickable in word
is project ka complelete url kha se nikale to add on reume
ye aa rha ah
is setting ki bat kar rhe ho
esa koi option nhi ha
isme kha ha
isme kha ha setting
isme
done sucssfull deploy
new user bna rha hu to not found kyo bta rha ha
Pasted code(8).py
Python
y ha
Pasted code(9).py
Python
ho gya complete 
ab my ticket error 
dubara login kra but error
bhai 2 option ha
invalid
password nhi aa rha ha
ab complete huaa next step

Haan bhai 👍 agar Execute kar diya hai aur 200 OK aa gaya hai, ab next step live Agent Login test hai.

Step 1 — Streamlit app kholo

Login page par:

Email:    livesupportagent@gmail.com
Password: LiveAgent@123

Phir Login click karo.

Step 2 — Expected

Login successful hone par Agent Dashboard open hona chahiye.

Wahan ideally:

👨‍💼 Agent Dashboard
🎫 Tickets
📊 Analytics
Agent ID / assigned tickets

dikhne chahiye.

Agar Invalid email or password aaye

Tab kuch change mat karna — mujhe error ka screenshot bhejna.

Agar Agent Dashboard open ho jaye

Uska screenshot bhejo. Phir next step:

Ticket ID 1 → Agent ko assign → status IN_PROGRESS → resolve → customer feedback

test karenge.

ye compleete ho gya na project 

Haan bhai, core project complete ho gaya hai ✅🔥

Abhi tak humne successfully implement/test kiya hai:

🔐 Customer Sign Up/Login
👨‍💼 Agent creation + password authentication
🎫 Ticket creation
🤖 AI ticket classification
⚡ Priority detection
📋 Customer My Tickets
👨‍💼 Agent system
🗄️ PostgreSQL database
🌐 FastAPI REST API
📊 Streamlit dashboard
🐳 Docker / Docker Compose
☁️ FastAPI deployed on Render
☁️ Streamlit app deployed
🧪 Tests bhi pass hue the
🔗 GitHub repository updated

Aur humne actual deployed application ko test karke bugs bhi fix kiye hain — especially agent_id database issue aur agent authentication.

Bas ek distinction

Project functionality: ✅ Complete

Final polish / placement-ready: 🔄 Optional

Agar placement/interview ke liye use karna hai, to ab naye features add karne ke bajay final testing + README + architecture explanation + resume bullets + interview questions prepare karna zyada useful rahega.

Meri recommendation: ab project ko freeze karo; unnecessary features add mat karo. 🎯

complete readmy ready kar do 

Haan bhai 🔥 complete professional README ready kar diya hai.

Isme included hai:

Project overview
Features
AI/ML pipeline
System architecture
Tech stack
Complete project structure
API endpoints
Testing
Local setup
Docker setup
Render + Streamlit deployment
Security notes
Application workflow
Project highlights
Future improvements
Author/skills section
Download README

📄 Download README.md

GitHub me add karne ke liye

Project folder me existing README.md ko is file se replace karo, phir:

git add README.md
git commit -m "Add complete project README"
git push origin main

Iske baad GitHub repository ka README placement/resume showcase ke liye ready ho jayega. 🚀 

README.md
Document

Library
/
README.md
🤖 AI Customer Support Intelligence Platform

An end-to-end AI-powered customer support platform for managing customer
accounts, support tickets, automatic ticket classification, priority
detection, agent workflows, analytics, and customer feedback.

🚀 Live Demo
FastAPI Backend:
https://ai-customer-support-platform-tr6k.onrender.com
API Documentation:
https://ai-customer-support-platform-tr6k.onrender.com/docs
GitHub:
https://github.com/anmol7240/ai-customer-support-platform
Streamlit Dashboard: Deployed on Streamlit Community Cloud

The Streamlit dashboard communicates with the deployed FastAPI backend
through REST APIs.

📌 Project Overview

Customer support teams receive a large number of tickets every day.
Manually categorizing tickets, identifying priority, tracking
resolution, and collecting customer feedback can be time-consuming.

This project provides a complete support workflow where:

Customers can register and log in.
Customers can create support tickets.
AI automatically predicts the ticket category.
A priority detection system assigns ticket priority.
Tickets are stored in PostgreSQL.
Agents can be created and authenticated.
Tickets can be tracked through their lifecycle.
Customer ratings and feedback can be recorded.
Analytics provide an overview of support activity.
A Streamlit dashboard provides an interactive interface.
✨ Key Features
🔐 Authentication
Customer registration
Customer login
Agent login
Password hashing
JWT access-token based authentication
Role information for authenticated users
🎫 Ticket Management
Create support tickets
View tickets
View customer-specific tickets
Update ticket information
Track ticket status
Store resolution notes
Store customer ratings and feedback
Agent association with tickets
🤖 AI Ticket Classification
Automatic ticket category prediction
TF-IDF text feature extraction
Logistic Regression classifier
Supports categories such as:
Account
Payment
Technical
Delivery
Refund
Security
Subscription
Other
⚡ Priority Detection

Priority is detected from ticket message content using a rule-based
system.

CRITICAL --- security/fraud related keywords
HIGH --- urgent/payment/account blocking issues
MEDIUM --- normal support requests
👨‍💼 Agent Management
Create support agents
Agent password authentication
Agent IDs linked with support tickets
Agent-oriented support workflow
📊 Analytics Dashboard
Total tickets
Open tickets
High-priority tickets
Critical-priority tickets
Ticket filtering
Customer ratings
Ticket status tracking
🗄️ Database

PostgreSQL is used as the primary relational database.

Main entities include: - Users - Customers - Agents - Tickets

🐳 Docker
Dockerized FastAPI backend
Docker Compose configuration for API and PostgreSQL
🧠 Machine Learning Pipeline

The ticket classifier uses an explainable NLP pipeline:

Customer Ticket
      ↓
TF-IDF Feature Extraction
      ↓
Unigrams + Bigrams
      ↓
Logistic Regression
      ↓
Predicted Ticket Category
Model Details
Feature Extraction: TF-IDF
N-grams: Unigrams + Bigrams
Model: Logistic Regression
Maximum Iterations: 1000
Training Data: 120 ticket examples
Categories: 8
Samples per Category: 15

The dataset is a small project dataset, so model metrics should be
interpreted as a demonstration of the ML pipeline rather than
production-level model performance.

🏗️ System Architecture
                    ┌─────────────────────┐
                    │      Customer       │
                    │  Streamlit UI       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit Cloud   │
                    │     Dashboard       │
                    └──────────┬──────────┘
                               │ REST API
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────┬───────┬──────┘
                           │       │
             ┌─────────────┘       └─────────────┐
             ▼                                   ▼
    ┌─────────────────┐                 ┌─────────────────┐
    │ ML/NLP Services │                 │ Authentication  │
    │ TF-IDF + LR     │                 │ JWT + Password  │
    └─────────────────┘                 └─────────────────┘
                           │
                           ▼
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │    Database     │
                    └─────────────────┘
🛠️ Tech Stack

Technology Purpose

Python Core programming language
FastAPI REST API backend
PostgreSQL Relational database
SQLAlchemy ORM/database interaction
Pydantic Data validation
Scikit-learn Machine learning
TF-IDF Text feature extraction
Logistic Regression Ticket classification
Pandas Data processing
NumPy Numerical computing
Streamlit Interactive dashboard
Requests API communication
Joblib Model serialization
Pytest Testing
Docker Containerization
Docker Compose Multi-container setup
Git/GitHub Version control
Render Backend deployment
Streamlit Community Cloud Dashboard deployment

📂 Project Structure
ai-customer-support-platform/
│
├── app/
│   ├── api/
│   │   ├── agents.py
│   │   └── auth.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   ├── agent.py
│   │   ├── auth.py
│   │   ├── customer.py
│   │   └── ticket.py
│   │
│   ├── services/
│   │   ├── classifier.py
│   │   └── priority.py
│   │
│   └── main.py
│
├── data/
│   └── tickets.csv
│
├── models/
│   └── ticket_classifier.joblib
│
├── tests/
│   ├── test_api.py
│   ├── test_classifier.py
│   └── test_priority.py
│
├── dashboard.py
├── train_model.py
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── requirements.txt
└── README.md
🔌 Main API Endpoints
Authentication

Method Endpoint Description

POST /auth/register Register customer
POST /auth/login Login user

Agents

Method Endpoint Description

GET /agents Get agents
POST /agents Create agent
GET /agents/{agent_id} Get agent

Customers

Method Endpoint Description

GET /customers Get customers
POST /customers Create customer
GET /customers/{customer_id} Get customer

Tickets

Method Endpoint Description

GET /tickets Get tickets
POST /tickets Create ticket
GET /tickets/{ticket_id} Get ticket
PUT /tickets/{ticket_id} Update ticket
DELETE /tickets/{ticket_id} Delete ticket

Analytics & ML

Method Endpoint Description

GET /analytics/tickets Ticket analytics
POST /predict-category Predict ticket category
GET /db-health Database health check
GET / API health/home

🧪 Testing

The project includes tests for:

Priority detection
Ticket classification
API functionality
Customer and ticket workflows

Run tests locally:

pytest

The test suite was verified successfully during development.

💻 Local Setup
1. Clone the repository
git clone https://github.com/anmol7240/ai-customer-support-platform.git
cd ai-customer-support-platform
2. Create virtual environment

Windows:

python -m venv venv
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Configure environment variables

Create a .env file:

DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/customer_support

Do not commit .env to GitHub.

5. Train the ML model
python train_model.py

This creates:

models/ticket_classifier.joblib
6. Start FastAPI
uvicorn app.main:app --reload

API:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs
7. Start Streamlit

In another terminal:

streamlit run dashboard.py

Dashboard:

http://localhost:8501
🐳 Docker Setup

Build the API image:

docker build -t ai-customer-support-api .

Run with Docker Compose:

docker compose up --build

Stop services:

docker compose down

The Docker Compose setup runs:

FastAPI
PostgreSQL
☁️ Deployment
Backend

The FastAPI backend is deployed on Render.

Production API:

https://ai-customer-support-platform-tr6k.onrender.com

Swagger documentation:

https://ai-customer-support-platform-tr6k.onrender.com/docs

Dashboard

The Streamlit dashboard is deployed separately and communicates with the
deployed FastAPI backend through REST APIs.

🔒 Security Notes
Passwords are stored as password hashes rather than plain text.
JWT access tokens are used for authentication.
.env is excluded from Git using .gitignore.
Database credentials should never be committed to GitHub.
Production secrets should be stored using the deployment platform's
environment-variable/secret system.
🔄 Application Workflow
Customer
   ↓
Register / Login
   ↓
Customer Dashboard
   ↓
Create Support Ticket
   ↓
FastAPI API
   ↓
AI Category Prediction
   ↓
Priority Detection
   ↓
PostgreSQL
   ↓
Agent Workflow
   ↓
Resolution
   ↓
Customer Rating & Feedback
   ↓
Analytics
🎯 Project Highlights
End-to-end AI-enabled customer support application
REST API architecture using FastAPI
PostgreSQL database integration
NLP-based ticket classification
Rule-based priority detection
Authentication and role-based workflow
Interactive Streamlit dashboard
Ticket analytics and feedback tracking
Dockerized backend
Cloud deployment
GitHub-based deployment workflow
Automated testing with Pytest
🔮 Future Improvements
Train the classifier on a larger real-world support-ticket dataset
Add precision, recall and F1-score reporting
Add semantic similarity using Sentence Transformers
Add AI-generated ticket summaries
Add suggested responses for support agents
Add email/notification integration
Add more granular role-based permissions
Add database migrations using Alembic
Add CI/CD using GitHub Actions
Add production monitoring and logging
👨‍💻 Author

Anmol Singh

B.Tech Data Science Student

Skills Demonstrated

Python · SQL · PostgreSQL · FastAPI · Scikit-learn · Pandas
· NumPy · Streamlit · Docker · REST APIs · Machine Learning ·
NLP · Git/GitHub

⭐ Project

This project demonstrates how machine learning, NLP, backend APIs,
databases, authentication, dashboards, testing, and cloud deployment can
be combined into a complete AI-powered application.