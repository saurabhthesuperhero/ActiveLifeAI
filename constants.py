# Constants for Clarifai API
import os

CLARIFAI_PAT = os.environ.get("CLARIFAI_PAT")
USER_ID = "openai"
APP_ID = "chat-completion"
MODEL_ID = 'openai-gpt-4-vision'
MODEL_VERSION_ID = '266df29bc09843e0aee9b7bf723c03c2'


# Exercise Prompt Template
def get_exercise_prompt(bmi, gender, goals):
    return f"""
    Based on the user's BMI ({bmi}),gender ({gender} and goals ({goals} provide a personalized bodyweight exercise routine that is:
    - Safe and effective for their current fitness level (if known).
    - Engaging and enjoyable to prevent boredom.
    - Designed to target major muscle groups (upper body, lower body, core).
    - Includes clear instructions and variations for different difficulty levels.
    - Consider user preferences for specific exercises or areas of focus (if available).
    NOTE: DO ALWAYS PROVIDE FULL WORKOUT MINIMUM and LONGER RESPONSE
    Example response:

    Given the user's BMI of {bmi},
     Your Body Falls in 'Overweight' Category which is Not good.
     So 
     here's a 30-minute bodyweight exercise routine that combines cardio, strength training, and core work:


    Warm-up (5 minutes):
    - Jumping jacks (30 seconds)
    - High knees (30 seconds)
    - Butt kicks (30 seconds)
    - Arm circles (forward and backward, 10 each)

    Cardio (10 minutes):
    - Jumping squats (30 seconds, rest 15 seconds) x 3 sets
    - Mountain climbers (30 seconds, rest 15 seconds) x 3 sets
    - Burpees (modified if needed, 20 seconds, rest 20 seconds) x 2 sets

    Strength Training (10 minutes):
    - Push-ups (modified on knees if needed, 10 reps) x 3 sets
    - Squats (bodyweight or modified with chair, 12 reps) x 3 sets
    - Lunges (10 reps per leg) x 3 sets
    - Plank (30 seconds) x 3 sets

    Cool-down (5 minutes):
    - Arm stretches (15 seconds each)
    - Leg stretches (15 seconds each)
    - Hamstring stretches (30 seconds each)

    Remember to listen to your body and modify exercises as needed. Gradually increase intensity or duration as you get fitter.
    """


def get_diet_prompt(age, preferred_food_style, favorite_dishes, gender, goals):
    return f"""
    Based on the user's age ({age}), gender ({gender}), preferred food style ({preferred_food_style}), favorite dishes ({favorite_dishes}), and health goals ({', '.join(goals)}), provide a personalized and healthy diet plan that addresses those goals effectively.
    """
