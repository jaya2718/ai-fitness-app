from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SelectField, IntegerField,
                     FloatField, TextAreaField, SubmitField, BooleanField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                 NumberRange, Optional, ValidationError)
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=80)
    ])
    email = StringField('Email', validators=[
        DataRequired(), Email(), Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(min=6, message='Password must be at least 6 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another.')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ProfileForm(FlaskForm):
    age = IntegerField('Age', validators=[
        DataRequired(), NumberRange(min=13, max=100, message='Age must be between 13 and 100')
    ])
    gender = SelectField('Gender', validators=[DataRequired()], choices=[
        ('', 'Select Gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other / Prefer not to say')
    ])
    height_cm = FloatField('Height (cm)', validators=[
        DataRequired(), NumberRange(min=100, max=250)
    ])
    weight_kg = FloatField('Weight (kg)', validators=[
        DataRequired(), NumberRange(min=30, max=300)
    ])
    goal = SelectField('Fitness Goal', validators=[DataRequired()], choices=[
        ('', 'Select Goal'),
        ('weight_loss', '🔥 Weight Loss'),
        ('muscle_gain', '💪 Muscle Gain / Body Building'),
        ('maintenance', '⚖️ Maintain Current Weight'),
        ('endurance', '🏃 Improve Endurance / Stamina'),
        ('flexibility', '🧘 Flexibility & Wellness')
    ])
    fitness_level = SelectField('Current Fitness Level', validators=[DataRequired()], choices=[
        ('', 'Select Level'),
        ('beginner', '🌱 Beginner (0–6 months)'),
        ('intermediate', '🌿 Intermediate (6 months – 2 years)'),
        ('advanced', '🌳 Advanced (2+ years)')
    ])
    activity_level = SelectField('Daily Activity Level', validators=[DataRequired()], choices=[
        ('', 'Select Activity Level'),
        ('sedentary', '🪑 Sedentary (desk job, little movement)'),
        ('light', '🚶 Lightly Active (light exercise 1-3 days/week)'),
        ('moderate', '🚴 Moderately Active (moderate exercise 3-5 days/week)'),
        ('active', '🏋️ Very Active (hard exercise 6-7 days/week)'),
        ('very_active', '⚡ Extra Active (athlete / physical job)')
    ])
    diet_type = SelectField('Diet Type', validators=[DataRequired()], choices=[
        ('', 'Select Diet Type'),
        ('non-vegetarian', '🍗 Non-Vegetarian'),
        ('vegetarian', '🥗 Vegetarian'),
        ('vegan', '🌱 Vegan'),
        ('pescatarian', '🐟 Pescatarian (fish only)'),
        ('keto', '🥑 Keto'),
        ('gluten-free', '🌾 Gluten-Free')
    ])
    food_culture = SelectField('Food Culture / Cuisine', validators=[DataRequired()], choices=[
        ('', 'Select Food Culture'),
        ('indian', '🇮🇳 Indian'),
        ('western', '🍔 Western / American'),
        ('mediterranean', '🫒 Mediterranean'),
        ('asian', '🍜 Asian / East Asian'),
        ('middle_eastern', '🧆 Middle Eastern'),
        ('latin', '🌮 Latin American'),
        ('african', '🌍 African'),
        ('mixed', '🌐 Mixed / No Preference')
    ])
    allergies = StringField('Food Allergies / Intolerances', validators=[Optional()],
                            description='e.g., nuts, gluten, dairy, shellfish (leave blank if none)')
    budget_per_day = FloatField('Daily Food Budget (USD)', validators=[
        DataRequired(), NumberRange(min=1, max=100)
    ])
    available_equipment = SelectField('Available Equipment', validators=[DataRequired()], choices=[
        ('', 'Select Equipment'),
        ('no_equipment', '🏠 No Equipment (bodyweight only)'),
        ('home_basic', '🏋️ Home – Basic (dumbbells, resistance bands)'),
        ('home_full', '🏠 Home – Full Setup (pull-up bar, bench, etc.)'),
        ('gym', '🏟️ Full Gym Access')
    ])
    workout_days_per_week = SelectField('Workout Days Per Week', validators=[DataRequired()],
                                        choices=[(str(i), f'{i} days') for i in range(2, 8)],
                                        coerce=int)
    workout_duration_min = SelectField('Session Duration', validators=[DataRequired()],
                                       choices=[
                                           ('20', '20 minutes'),
                                           ('30', '30 minutes'),
                                           ('45', '45 minutes'),
                                           ('60', '60 minutes'),
                                           ('90', '90 minutes')
                                       ], coerce=int)
    health_conditions = TextAreaField('Health Conditions / Injuries',
                                       validators=[Optional()],
                                       description='e.g., knee injury, back pain, asthma (leave blank if none)')
    submit = SubmitField('Save Profile & Generate Plans')
