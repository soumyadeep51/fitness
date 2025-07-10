from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserInputForm, FeedbackForm, ContactForm  # Add ContactForm
import joblib
import numpy as np
import os

# Load model and encoders only once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

model = joblib.load(os.path.join(MODEL_DIR, 'fitness_model.pkl'))
le_gender = joblib.load(os.path.join(MODEL_DIR, 'gender_encoder.pkl'))
le_bmicase = joblib.load(os.path.join(MODEL_DIR, 'bmicase_encoder.pkl'))

def calculate_bmi_case(bmi):
    if bmi < 18.5:
        return 'underweight'
    elif 18.5 <= bmi < 25:
        return 'normal'
    elif 25 <= bmi < 30:
        return 'overweight'
    else:
        return 'obese'

def get_workout_plan(plan):
    plans = {
        1: """🧘 PLAN 1: Gentle Yoga & Light Movement (For Underweight or Elderly Beginners)

🗓️ Weekly Schedule:
- Monday: Morning Walk (30 mins) + Gentle Yoga Poses (Child's pose, Cat-Cow) – 3 sets each
- Tuesday: Breathing exercises (Pranayama) – 10 mins + Neck/Shoulder Rolls – 2 sets of 10 reps
- Wednesday: Walk (20 mins) + Seated Forward Fold & Butterfly Stretch – Hold 30 secs x 2
- Thursday: Rest or Light walk (15 mins)
- Friday: Seated Side Bends, Arm Circles – 2 sets of 15 reps
- Saturday: Yoga (Sun Salutation x 3 rounds)
- Sunday: Guided meditation (10 mins) + Leisure Walk (20 mins)

🕐 Daily Time: 30–45 mins
📌 Goal: Blood flow, posture, calm mind
""",
        2: """🚶 PLAN 2: Brisk Walking & Light Stretching (For Beginners or Low BMI Normal)

🗓️ Weekly Schedule:
- Monday: Brisk Walk (40 mins) + Upper Body Stretches – 2 sets of 15 reps
- Tuesday: Yoga (20 mins) + Plank (3 x 30 secs), Cat-Cow (3 sets)
- Wednesday: Walk (30 mins) + Arm Circles, Leg Swings – 2 sets of 20
- Thursday: Light Mobility + Heel-to-Toe Balance (3 sets)
- Friday: Brisk Walk (45 mins) + Hamstring & Quad Stretch – Hold 30s x 2
- Saturday: Resistance Band Rows – 2 sets of 15, Glute Bridges – 3x15
- Sunday: Leisure walk or light cycling (30 mins)

🕐 Daily Time: 45–60 mins
📌 Goal: Flexibility, light cardio, base strength
""",
        3: """🏃 PLAN 3: Cardio & Core Focus (For Mid-Age Normal BMI)

🗓️ Weekly Schedule:
- Monday: Jogging (20 mins) + Plank (3 x 30s), Crunches (3 x 15)
- Tuesday: Cycling (40 mins) + Superman Hold – 3 x 30s
- Wednesday: HIIT: Jumping Jacks (3x30), Bodyweight Squats (3x15), Lunges (3x12 each leg)
- Thursday: Yoga Flow + Cobra, Child’s Pose – Hold 30s x 2
- Friday: Stair Climbing + Core Circuit: Leg Raises (3x12), Side Planks (2x30s each)
- Saturday: Jump Rope (15 mins) + Flutter Kicks (3x20)
- Sunday: Outdoor sport or free cardio choice

🕐 Daily Time: 45–60 mins
📌 Goal: Stamina, core tightening, cardio health
""",
        4: """💪 PLAN 4: Strength Training & Mobility (For Overweight or Fit Starters)

🗓️ Weekly Schedule:
- Monday (Upper Body): Pushups (3x12), Dumbbell Shoulder Press (3x10), Bent-over Rows (3x12)
- Tuesday: Core (Russian Twists 3x20, Dead Bug 3x15) + Stretching
- Wednesday (Lower Body): Goblet Squats (3x12), Lunges (3x10/leg), Glute Bridges (3x15)
- Thursday: Yoga Flow + Foam Rolling (10 mins)
- Friday (Full Body Circuit): Kettlebell Swings (3x15), Push Press (3x10), Jump Squats (3x12)
- Saturday: Resistance Band Workout – Pull Aparts, Side Steps (3x15)
- Sunday: Walk or light movement (30 mins)

🕐 Daily Time: 60–75 mins
📌 Goal: Strength, balance, mobility
""",
        5: """🔥 PLAN 5: HIIT & Weight Training (High BMI / Intermediate)

🗓️ Weekly Schedule:
- Monday: HIIT Circuit (Burpees, Jumping Jacks, High Knees) – 4 rounds of 30s on/15s rest
  + Dumbbell Bench Press (4x10), Bent-over Row (4x12)
- Tuesday: Legs – Deadlifts (4x8), Step-ups (3x12/leg), Calf Raises (3x20)
- Wednesday: Core (Plank Hold 4x30s, Mountain Climbers 3x20), Mobility Flow
- Thursday: HIIT + Bicycle Crunches (3x20), Side Lunges (3x15)
- Friday: Full Body – Thrusters (3x12), Renegade Rows (3x10), Squat Jumps (3x12)
- Saturday: Active Recovery – Stretching + Light Cardio (30 mins)
- Sunday: Rest or foam roll (15 mins)

🕐 Daily Time: 60–75 mins
📌 Goal: Fat burn, muscle tone, intensity endurance
""",
        6: """🥋 PLAN 6: Martial Arts & Functional Training (Advanced Stamina Training)

🗓️ Weekly Schedule:
- Monday: Martial Arts Kicks (Roundhouse, Side Kick) – 3 sets of 15 + Stretch
- Tuesday: TRX Pulls, Jump Squats, Pushups – 4x10 each
- Wednesday: Shadow Boxing – 30 mins + Core (Leg Raises, Russian Twists)
- Thursday: Foam Rolling + Mobility Circuit (10 mins)
- Friday: Ladder Drills + Plyometrics (Jump Lunges, Box Jumps – 3x12)
- Saturday: Kickboxing Rounds + Combat Burpees (3 sets)
- Sunday: Long walk + deep breathwork

🕐 Daily Time: 75 mins
📌 Goal: Agility, combat readiness, stamina
""",
        7: """🏋️ PLAN 7: Powerlifting & Muscle Building (Advanced/Pro Athletes)

🗓️ Weekly Schedule:
- Monday (Chest & Triceps): Bench Press (4x8), Incline DB Press (3x10), Tricep Dips (3x12)
- Tuesday (Legs): Back Squats (4x8), Leg Press (3x10), Walking Lunges (3x12), Calf Raises (3x20)
- Wednesday (Back & Biceps): Deadlifts (4x6), Pull-Ups (3x8), Barbell Row (3x10), Bicep Curl (3x12)
- Thursday (Core + Functional): Hanging Leg Raise (3x15), Ab Wheel (3x10), Russian Twists (3x30s)
- Friday (Shoulders): Military Press (4x8), Lateral Raise (3x12), Shrugs (3x20)
- Saturday: HIIT Finisher: Burpees, Kettlebell Swings (3 rounds)
- Sunday: Rest + Deep Stretch (20 mins)

🕐 Daily Time: 90 mins
📌 Goal: Strength, aesthetics, peak performance
🍽️ Tip: Eat 1.5g protein/kg bodyweight. Focus on clean carbs and sleep 7+ hrs.
"""
    }
    return plans.get(plan, "No workout plan found.")

from .models import WorkoutPlan

def predict_workout(request):
    result = None
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            weight = form.cleaned_data['weight']
            height_cm = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']

            height_m = height_cm / 100
            bmi = weight / (height_m ** 2)
            bmicase = calculate_bmi_case(bmi)

            # Encode categorical features
            gender_encoded = le_gender.transform([gender])[0]
            bmicase_encoded = le_bmicase.transform([bmicase])[0]

            # Prepare input
            input_data = np.array([[weight, height_cm, bmi, gender_encoded, age, bmicase_encoded]])
            plan_number = int(model.predict(input_data)[0])
            workout_text = get_workout_plan(plan_number)

            # Save to database including plan details
            workout_plan = WorkoutPlan(
                weight=weight,
                height=height_cm,
                age=age,
                gender=gender,
                plan_details=workout_text
            )
            workout_plan.save()

            result = {
                'bmi': f"{bmi:.2f}",
                'bmicase': bmicase,
                'plan_number': plan_number,
                'plan_details': workout_text
            }
    else:
        form = UserInputForm()

    return render(request, 'predict.html', {'form': form, 'result': result})

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Assuming FeedbackForm saves to a model
            return render(request, 'feedback.html', {'form': form, 'message': 'Thank you for your feedback!'})
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f"Contact Form Submission from {name}"
            from_email = email
            recipient_list = ['prasanta.work07@gmail.com']
            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False,
            )
            return render(request, 'contact.html', {'form': form, 'message': 'Thank you! Your message has been sent.'})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})