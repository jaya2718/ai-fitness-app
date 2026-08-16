# AI Fitness App — Python (Flask) Setup Guide

## Quick Setup

### 1. Clone / Download
```bash
cd "AI FITNESS APP"
```

### 2. Create a Virtual Environment
```bash
python -m venv venv

# Activate:
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and fill in:
# SECRET_KEY=some-random-secret-string
# GEMINI_API_KEY=your-google-gemini-api-key
```

### 5. Get a Gemini API Key (Free)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy it into your `.env` file as `GEMINI_API_KEY=...`

### 6. Run the App
```bash
python run.py
```

Open your browser at: **http://localhost:5000**

---

## Project Structure

```
AI FITNESS APP/
├── run.py                    # App entry point
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Example env file
└── app/
    ├── __init__.py           # Flask app factory
    ├── models.py             # Database models (User, WorkoutPlan, DietPlan)
    ├── ai_engine.py          # Google Gemini AI integration
    ├── forms.py              # WTForms form definitions
    ├── routes/
    │   ├── auth.py           # Register, Login, Logout
    │   ├── main.py           # Home, Dashboard
    │   ├── workout.py        # Workout plan generation & viewing
    │   ├── diet.py           # Diet plan generation & viewing
    │   └── profile.py        # Profile setup & editing
    └── templates/
        ├── base.html         # Base template with navbar & layout
        ├── auth/
        │   ├── register.html
        │   └── login.html
        ├── main/
        │   ├── index.html    # Landing page
        │   └── dashboard.html
        ├── profile/
        │   └── setup.html
        ├── workout/
        │   ├── view.html
        │   └── history.html
        └── diet/
            ├── view.html
            └── history.html
```

---

## Features

### 🤖 AI-Powered Plans
- Uses **Google Gemini 1.5 Flash** to generate plans
- 7-day personalized **workout routines** with sets, reps, rest periods
- 7-day **meal plans** with full recipes, macros, and cost estimates

### 🌍 Cultural Sensitivity
- Supports: Indian, Western, Mediterranean, Asian, Middle Eastern, Latin, African cuisines
- Respects diet types: Vegetarian, Vegan, Non-Vegetarian, Pescatarian, Keto, Gluten-Free

### 💰 Budget-Friendly
- Meal plans generated within your daily food budget
- Cost estimates per meal
- Budget shopping tips included

### 🏠 Any Equipment
- Bodyweight-only plans for students with no equipment
- Home basic / full setup plans
- Full gym plans for gym-goers

### 📊 Smart Calculations
- Automatic BMR & TDEE calculation
- Calorie targets adjusted for goal (weight loss: -400 kcal, muscle gain: +300 kcal)
- Macronutrient breakdown

---

## Tech Stack
- **Backend**: Python + Flask
- **Database**: SQLite (via SQLAlchemy ORM)
- **Auth**: Flask-Login + Werkzeug password hashing
- **Forms**: Flask-WTF + WTForms validation
- **AI**: Google Generative AI (Gemini 1.5 Flash)
- **Frontend**: Jinja2 templates, vanilla CSS, vanilla JS
- **Design**: Dark-themed, modern glass-morphism UI
