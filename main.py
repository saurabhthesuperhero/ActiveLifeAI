import streamlit as st
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

# Securely store API credentials
PAT = "993735bd0d62446db97ae870027e8767"
USER_ID = "openai"
APP_ID = "chat-completion"
# MODEL_ID = "GPT-4"
# MODEL_VERSION_ID = "5d7a50b44aec4a01a9c492c5a5fcf387"
MODEL_ID = "GPT-3_5-turbo"
MODEL_VERSION_ID = "4471f26b3da942dab367fe85bc0f7d21"


# Function to call Clarifai API
def call_clarifai_api(prompt):
    try:
        channel = ClarifaiChannel.get_grpc_channel()
        stub = service_pb2_grpc.V2Stub(channel)
        metadata = (('authorization', 'Key ' + PAT),)
        userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

        response = stub.PostModelOutputs(
            service_pb2.PostModelOutputsRequest(
                user_app_id=userDataObject,
                model_id=MODEL_ID,
                version_id=MODEL_VERSION_ID,
                inputs=[resources_pb2.Input(data=resources_pb2.Data(text=resources_pb2.Text(raw=prompt)))]
            ),
            metadata=metadata
        )

        if response.status.code != status_code_pb2.SUCCESS:
            return None, f"Clarifai API error: {response.status.description}"
        else:
            return response.outputs[0].data.text.raw, None
    except Exception as e:
        return None, str(e)


# Initialize session state variables
if 'exercise_routine' not in st.session_state:
    st.session_state['exercise_routine'] = None
if 'diet_routine' not in st.session_state:
    st.session_state['diet_routine'] = None

# Function to download text content as a PDF (dummy implementation)
def download_text_as_pdf(text, filename):
    st.write(f"Download {filename} as PDF")  # Replace with actual download logic

# Function to display routines in the sidebar
def display_sidebar_routines():
    # Create placeholders for the sidebar content
    exercise_analysis_placeholder = st.sidebar.empty()
    diet_analysis_placeholder = st.sidebar.empty()

    # Update the placeholders with the current session state
    with exercise_analysis_placeholder.container():
        st.sidebar.title("Analysis Summary")
        with st.sidebar.expander("Exercise Analysis"):
            if st.session_state['exercise_routine']:
                st.write("Analysis of your exercise routine will be shown here.\n")
                st.write(st.session_state['exercise_routine'])
                if st.button("Download Exercise Routine", key='download_exercise'):
                    download_text_as_pdf(st.session_state['exercise_routine'], "Exercise_Routine.pdf")
            else:
                st.write("No exercise routine available.")

    with diet_analysis_placeholder.container():
        with st.sidebar.expander("Diet Analysis"):
            if st.session_state['diet_routine']:
                st.write("Analysis of your diet routine will be shown here.\n")
                st.write(st.session_state['diet_routine'])
                if st.button("Download Diet Plan", key='download_diet'):
                    download_text_as_pdf(st.session_state['diet_routine'], "Diet_Plan.pdf")
            else:
                st.write("No diet routine available.")

# Streamlit UI
st.title("AI ActiveLife")

# Sidebar
display_sidebar_routines()


# User input for height, weight, and age
height = st.number_input("Enter your height in meters", min_value=0.5, max_value=3.0)
weight = st.number_input("Enter your weight in kilograms", min_value=30, max_value=250)
age = st.number_input("Enter your age", min_value=12, max_value=100)

# Exercise Routine Section
st.header("Exercise Routine")
exercise_routine = None
if st.button('Get Exercise Routine'):
    if height and weight:
        bmi = weight / (height ** 2)
        st.write("Your BMI is:", bmi)

        # Constructing the exercise prompt
        exercise_prompt = f"""

        Based on the user's BMI ({bmi}), provide a personalized bodyweight exercise routine that is:
        - Safe and effective for their current fitness level (if known).
        - Engaging and enjoyable to prevent boredom.
        - Designed to target major muscle groups (upper body, lower body, core).
        - Includes clear instructions and variations for different difficulty levels.
        - Consider user preferences for specific exercises or areas of focus (if available).

        Example response:

        Given the user's BMI of {bmi}, here's a 30-minute bodyweight exercise routine that combines cardio, strength training, and core work:

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
        with st.spinner('Generating your personalized exercise routine...'):
            exercise_routine, error = call_clarifai_api(exercise_prompt)
            if error:
                st.error(error)
            else:
                st.session_state['exercise_routine'] = exercise_routine

# Display exercise routine in an expander
if st.session_state['exercise_routine']:
    with st.expander("See your Exercise Routine"):
        st.write("**Personalized Exercise Routine:**")
        st.write(st.session_state['exercise_routine'])

# Diet Routine Section
st.header("Diet Routine")
diet_routine = None
preferred_food_style = st.text_input("Enter your preferred food style (e.g., Indian, Mediterranean, etc.)")
favorite_dishes = st.text_input("Enter your favorite dishes")

if st.button('Get Diet Routine'):
    if preferred_food_style and favorite_dishes:
        # Constructing the diet prompt
        diet_prompt = f"""
        Based on the user's age ({age}), preferred food style ({preferred_food_style}), and favorite dishes ({favorite_dishes}), provide a personalized and healthy diet plan.
        """
        with st.spinner('Generating your personalized diet routine...'):
            diet_routine, error = call_clarifai_api(diet_prompt)
            if error:
                st.error(error)
            else:
                st.session_state['diet_routine'] = diet_routine

# Display diet routine in an expander
if st.session_state['diet_routine']:
    with st.expander("See your Diet Routine"):
        st.write("**Personalized Diet Routine:**")
        st.write(st.session_state['diet_routine'])

