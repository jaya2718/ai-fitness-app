from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.forms import ProfileForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/setup', methods=['GET', 'POST'])
@login_required
def setup():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.height_cm = form.height_cm.data
        current_user.weight_kg = form.weight_kg.data
        current_user.goal = form.goal.data
        current_user.fitness_level = form.fitness_level.data
        current_user.activity_level = form.activity_level.data
        current_user.diet_type = form.diet_type.data
        current_user.food_culture = form.food_culture.data
        current_user.allergies = form.allergies.data
        current_user.budget_per_day = form.budget_per_day.data
        current_user.available_equipment = form.available_equipment.data
        current_user.workout_days_per_week = form.workout_days_per_week.data
        current_user.workout_duration_min = form.workout_duration_min.data
        current_user.health_conditions = form.health_conditions.data
        db.session.commit()
        flash('Profile saved! Your AI plans are ready to generate. 🚀', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('profile/setup.html', form=form)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.age = form.age.data
        current_user.gender = form.gender.data
        current_user.height_cm = form.height_cm.data
        current_user.weight_kg = form.weight_kg.data
        current_user.goal = form.goal.data
        current_user.fitness_level = form.fitness_level.data
        current_user.activity_level = form.activity_level.data
        current_user.diet_type = form.diet_type.data
        current_user.food_culture = form.food_culture.data
        current_user.allergies = form.allergies.data
        current_user.budget_per_day = form.budget_per_day.data
        current_user.available_equipment = form.available_equipment.data
        current_user.workout_days_per_week = form.workout_days_per_week.data
        current_user.workout_duration_min = form.workout_duration_min.data
        current_user.health_conditions = form.health_conditions.data
        db.session.commit()
        flash('Profile updated! Regenerate your plans for fresh recommendations. 🔄', 'success')
        return redirect(url_for('main.dashboard'))
    return render_template('profile/setup.html', form=form, editing=True)
