import os
import json
from dotenv import load_dotenv

load_dotenv()

def get_model():
    import google.generativeai as genai
    genai.configure(api_key=os.getenv('GEMINI_API_KEY', ''))
    return genai.GenerativeModel('models/gemini-1.5-flash')


def generate_workout_plan(user):
    """Generate a personalized weekly workout plan using Gemini AI."""

    equipment = user.available_equipment or 'no equipment'
    conditions = user.health_conditions or 'none'
    allergies = user.allergies or 'none'

    prompt = f"""You are an expert certified fitness trainer. Create a DETAILED 7-day personalized workout plan for a student with the following profile:

PROFILE:
- Age: {user.age} years
- Gender: {user.gender}
- Height: {user.height_cm} cm | Weight: {user.weight_kg} kg
- BMI: {user.bmi()} ({user.bmi_category()})
- Fitness Goal: {user.goal}
- Fitness Level: {user.fitness_level}
- Activity Level: {user.activity_level}
- Available Equipment: {equipment}
- Workout Days Per Week: {user.workout_days_per_week}
- Session Duration: {user.workout_duration_min} minutes per session
- Health Conditions: {conditions}

REQUIREMENTS:
1. Make it practical for a STUDENT with limited time and budget
2. Account for available equipment: {equipment}
3. Include warm-up and cool-down for each day
4. Provide exact sets, reps, and rest periods
5. Include modifications for beginners if needed
6. Mark rest days clearly

Return ONLY valid JSON in this exact format:
{{
  "plan_title": "string",
  "goal": "string",
  "weekly_overview": "string",
  "tips": ["tip1", "tip2", "tip3"],
  "days": [
    {{
      "day": "Monday",
      "day_type": "workout" or "rest",
      "focus": "e.g. Upper Body / Cardio / Rest",
      "duration_min": 45,
      "warm_up": [
        {{"exercise": "name", "duration": "5 min", "description": "how to do it"}}
      ],
      "main_workout": [
        {{
          "exercise": "name",
          "sets": 3,
          "reps": "12-15",
          "rest": "60 sec",
          "muscle_group": "chest",
          "description": "proper form description",
          "modification": "easier version"
        }}
      ],
      "cool_down": [
        {{"exercise": "name", "duration": "2 min", "description": "how to do it"}}
      ],
      "notes": "any special notes for this day"
    }}
  ]
}}"""

    try:
        model = get_model()
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Extract JSON from markdown code blocks if present
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        plan = json.loads(text)
        return plan, None
    except json.JSONDecodeError as e:
        return None, f"Failed to parse AI response: {str(e)}"
    except Exception as e:
        return None, f"AI generation error: {str(e)}"


def generate_diet_plan(user):
    """Generate a personalized 7-day meal plan using Gemini AI."""

    allergies = user.allergies or 'none'
    conditions = user.health_conditions or 'none'
    budget = user.budget_per_day or 10
    culture = user.food_culture or 'mixed'
    diet_type = user.diet_type or 'non-vegetarian'

    # Calculate TDEE (Total Daily Energy Expenditure)
    if user.gender == 'male':
        bmr = 88.362 + (13.397 * (user.weight_kg or 70)) + (4.799 * (user.height_cm or 170)) - (5.677 * (user.age or 20))
    else:
        bmr = 447.593 + (9.247 * (user.weight_kg or 60)) + (3.098 * (user.height_cm or 160)) - (4.330 * (user.age or 20))

    activity_multipliers = {
        'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55,
        'active': 1.725, 'very_active': 1.9
    }
    multiplier = activity_multipliers.get(user.activity_level, 1.375)
    tdee = int(bmr * multiplier)

    if user.goal == 'weight_loss':
        target_calories = tdee - 400
    elif user.goal == 'muscle_gain':
        target_calories = tdee + 300
    else:
        target_calories = tdee

    prompt = f"""You are an expert certified nutritionist and dietitian. Create a DETAILED 7-day personalized meal plan for a student with the following profile:

PROFILE:
- Age: {user.age} years
- Gender: {user.gender}
- Height: {user.height_cm} cm | Weight: {user.weight_kg} kg
- BMI: {user.bmi()} ({user.bmi_category()})
- Fitness Goal: {user.goal}
- Diet Type: {diet_type}
- Cultural Food Preference: {culture}
- Food Allergies/Intolerances: {allergies}
- Health Conditions: {conditions}
- Daily Budget: ₹{budget} INR
- Target Daily Calories: {target_calories} kcal
- TDEE: {tdee} kcal

REQUIREMENTS:
1. Respect CULTURAL food preferences ({culture} cuisine)
2. Strictly follow diet type: {diet_type}
3. AVOID all allergens: {allergies}
4. Keep meals BUDGET-FRIENDLY (under ₹{budget}/day)
5. Include locally available, affordable ingredients
6. Provide easy student-friendly meal prep instructions
7. Include healthy snacks between meals
8. Provide grocery shopping tips

Return ONLY valid JSON in this exact format:
{{
  "plan_title": "string",
  "daily_calories": {target_calories},
  "macros": {{
    "protein_g": 150,
    "carbs_g": 200,
    "fats_g": 65
  }},
  "shopping_tips": ["tip1", "tip2"],
  "meal_prep_tips": ["tip1", "tip2"],
  "days": [
    {{
      "day": "Monday",
      "total_calories": {target_calories},
      "meals": {{
        "breakfast": {{
          "name": "meal name",
          "ingredients": ["item 1", "item 2"],
          "calories": 400,
          "protein_g": 20,
          "carbs_g": 50,
          "fats_g": 10,
          "prep_time_min": 10,
          "recipe": "brief cooking instructions",
          "estimated_cost": "₹125"
        }},
        "morning_snack": {{
          "name": "snack name",
          "ingredients": ["item 1"],
          "calories": 150,
          "protein_g": 5,
          "carbs_g": 20,
          "fats_g": 5,
          "prep_time_min": 2,
          "recipe": "instructions",
          "estimated_cost": "₹40"
        }},
        "lunch": {{
          "name": "meal name",
          "ingredients": ["item 1", "item 2"],
          "calories": 550,
          "protein_g": 30,
          "carbs_g": 60,
          "fats_g": 15,
          "prep_time_min": 20,
          "recipe": "brief cooking instructions",
          "estimated_cost": "₹210"
        }},
        "afternoon_snack": {{
          "name": "snack name",
          "ingredients": ["item 1"],
          "calories": 150,
          "protein_g": 5,
          "carbs_g": 20,
          "fats_g": 5,
          "prep_time_min": 2,
          "recipe": "instructions",
          "estimated_cost": "₹60"
        }},
        "dinner": {{
          "name": "meal name",
          "ingredients": ["item 1", "item 2"],
          "calories": 600,
          "protein_g": 35,
          "carbs_g": 65,
          "fats_g": 20,
          "prep_time_min": 25,
          "recipe": "brief cooking instructions",
          "estimated_cost": "₹250"
        }}
      }}
    }}
  ]
}}"""

    try:
        model = get_model()
        response = model.generate_content(prompt)
        text = response.text.strip()

        if '```json' in text:
            text = text.split('```json')[1].split('```')[0].strip()
        elif '```' in text:
            text = text.split('```')[1].split('```')[0].strip()

        plan = json.loads(text)
        return plan, target_calories, None
    except json.JSONDecodeError as e:
        return None, target_calories, f"Failed to parse AI response: {str(e)}"
    except Exception as e:
        return None, target_calories, f"AI generation error: {str(e)}"


def get_fitness_tip(user):
    """Get a quick personalized fitness tip."""
    prompt = f"""Give ONE short, motivational fitness or nutrition tip (2-3 sentences max) for a {user.age}-year-old {user.gender} student 
    with goal: {user.goal}, fitness level: {user.fitness_level}. Make it practical and encouraging."""

    try:
        model = get_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception:
        return "Stay consistent with your workout and nutrition plan. Small daily improvements lead to remarkable results over time!"
