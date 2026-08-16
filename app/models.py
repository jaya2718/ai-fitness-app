from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Physical profile
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)
    goal = db.Column(db.String(50))           # weight_loss, muscle_gain, maintenance, endurance
    fitness_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    activity_level = db.Column(db.String(30)) # sedentary, light, moderate, active, very_active

    # Diet preferences
    diet_type = db.Column(db.String(30))      # vegetarian, vegan, non-vegetarian, pescatarian
    food_culture = db.Column(db.String(50))   # indian, western, mediterranean, asian, etc.
    allergies = db.Column(db.String(200))
    budget_per_day = db.Column(db.Float)      # daily food budget in USD

    # Workout preferences
    available_equipment = db.Column(db.String(200))  # home, gym, no_equipment
    workout_days_per_week = db.Column(db.Integer)
    workout_duration_min = db.Column(db.Integer)
    health_conditions = db.Column(db.String(300))

    # Relationships
    workout_plans = db.relationship('WorkoutPlan', backref='user', lazy=True, cascade='all, delete-orphan')
    diet_plans = db.relationship('DietPlan', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def bmi(self):
        if self.height_cm and self.weight_kg:
            h = self.height_cm / 100
            return round(self.weight_kg / (h * h), 1)
        return None

    def bmi_category(self):
        bmi = self.bmi()
        if bmi is None:
            return 'Unknown'
        if bmi < 18.5:
            return 'Underweight'
        elif bmi < 25:
            return 'Normal'
        elif bmi < 30:
            return 'Overweight'
        return 'Obese'

    def __repr__(self):
        return f'<User {self.username}>'


class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    plan_data = db.Column(db.Text)   # JSON string of workout plan
    week_number = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<WorkoutPlan {self.title}>'


class DietPlan(db.Model):
    __tablename__ = 'diet_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    plan_data = db.Column(db.Text)   # JSON string of meal plan
    daily_calories = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<DietPlan {self.title}>'


class ProgressLog(db.Model):
    __tablename__ = 'progress_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    log_date = db.Column(db.DateTime, default=datetime.utcnow)
    weight_kg = db.Column(db.Float)
    notes = db.Column(db.Text)
    workout_completed = db.Column(db.Boolean, default=False)
    diet_followed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<ProgressLog {self.log_date}>'
