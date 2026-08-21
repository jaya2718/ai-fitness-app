from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app.models import WorkoutPlan, DietPlan, ProgressLog
from app.ai_engine import get_fitness_tip

main_bp = Blueprint('main', __name__)


@main_bp.route('/ping')
def ping():
    return jsonify({'status': 'ok'}), 200


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.age:
        return redirect(url_for('profile.setup'))

    latest_workout = WorkoutPlan.query.filter_by(
        user_id=current_user.id, is_active=True
    ).order_by(WorkoutPlan.created_at.desc()).first()

    latest_diet = DietPlan.query.filter_by(
        user_id=current_user.id, is_active=True
    ).order_by(DietPlan.created_at.desc()).first()

    tip = get_fitness_tip(current_user)

    return render_template('main/dashboard.html',
                           user=current_user,
                           workout_plan=latest_workout,
                           diet_plan=latest_diet,
                           tip=tip)
