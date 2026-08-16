from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import WorkoutPlan
from app.ai_engine import generate_workout_plan
import json

workout_bp = Blueprint('workout', __name__, url_prefix='/workout')


@workout_bp.route('/generate')
@login_required
def generate():
    if not current_user.age:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.setup'))

    flash('Generating your personalized workout plan with AI... ⏳', 'info')
    plan_data, error = generate_workout_plan(current_user)

    if error:
        flash(f'Error generating plan: {error}', 'danger')
        return redirect(url_for('main.dashboard'))

    # Deactivate old plans
    WorkoutPlan.query.filter_by(user_id=current_user.id).update({'is_active': False})
    db.session.commit()

    new_plan = WorkoutPlan(
        user_id=current_user.id,
        title=plan_data.get('plan_title', 'My Workout Plan'),
        plan_data=json.dumps(plan_data),
        is_active=True
    )
    db.session.add(new_plan)
    db.session.commit()

    flash('Workout plan generated successfully! 🎉', 'success')
    return redirect(url_for('workout.view', plan_id=new_plan.id))


@workout_bp.route('/view/<int:plan_id>')
@login_required
def view(plan_id):
    plan = WorkoutPlan.query.filter_by(id=plan_id, user_id=current_user.id).first_or_404()
    plan_data = json.loads(plan.plan_data)
    return render_template('workout/view.html', plan=plan, plan_data=plan_data)


@workout_bp.route('/history')
@login_required
def history():
    plans = WorkoutPlan.query.filter_by(user_id=current_user.id)\
        .order_by(WorkoutPlan.created_at.desc()).all()
    return render_template('workout/history.html', plans=plans)
