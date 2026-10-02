# 🤖 AI-Powered Customer Support Intelligence Platform

An AI-powered customer support platform designed to manage, classify, prioritize, and analyze customer support tickets using Machine Learning and NLP.

The platform provides REST APIs with FastAPI, stores data in PostgreSQL, and offers an interactive Streamlit dashboard for customers and support agents.

---

## 🚀 Features

- 🎫 Customer ticket creation and management
- 🤖 Automatic ticket category classification
- ⚡ Rule-based ticket priority detection
- 👤 Customer and agent management
- 🔐 JWT-based authentication
- 📊 Ticket analytics and dashboard
- ⭐ Customer feedback and ratings
- 🗄️ PostgreSQL database integration
- 🧪 API and unit testing with Pytest
- 🐳 Docker support
- 📚 Automatic API documentation with Swagger

---

## 🏗️ System Architecture

```text
Customer / Agent
       ↓
Streamlit Dashboard
       ↓
FastAPI REST API
       ↓
 ┌───────────────┐
 │               │
 ↓               ↓
ML Classifier   Priority Detection
 │               │
 └───────┬───────┘
         ↓
    PostgreSQL
