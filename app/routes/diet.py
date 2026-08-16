from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import DietPlan
from app.ai_engine import generate_diet_plan
import json

diet_bp = Blueprint('diet', __name__, url_prefix='/diet')


@diet_bp.route('/generate')
@login_required
def generate():
    if not current_user.age:
        flash('Please complete your profile first.', 'warning')
        return redirect(url_for('profile.setup'))

    flash('Generating your personalized meal plan with AI... ⏳', 'info')
    plan_data, target_calories, error = generate_diet_plan(current_user)

    if error:
        flash(f'Error generating plan: {error}', 'danger')
        return redirect(url_for('main.dashboard'))

    # Deactivate old plans
    DietPlan.query.filter_by(user_id=current_user.id).update({'is_active': False})
    db.session.commit()

    new_plan = DietPlan(
        user_id=current_user.id,
        title=plan_data.get('plan_title', 'My Meal Plan'),
        plan_data=json.dumps(plan_data),
        daily_calories=target_calories,
        is_active=True
    )
    db.session.add(new_plan)
    db.session.commit()

    flash('Meal plan generated successfully! 🥗', 'success')
    return redirect(url_for('diet.view', plan_id=new_plan.id))


@diet_bp.route('/view/<int:plan_id>')
@login_required
def view(plan_id):
    plan = DietPlan.query.filter_by(id=plan_id, user_id=current_user.id).first_or_404()
    plan_data = json.loads(plan.plan_data)
    return render_template('diet/view.html', plan=plan, plan_data=plan_data)


@diet_bp.route('/history')
@login_required
def history():
    plans = DietPlan.query.filter_by(user_id=current_user.id)\
        .order_by(DietPlan.created_at.desc()).all()
    return render_template('diet/history.html', plans=plans)
