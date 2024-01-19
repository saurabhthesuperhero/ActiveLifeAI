import streamlit as st

import constants as const  # Importing constants
from helpers import call_clarifai_api

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
        exercise_prompt = const.get_exercise_prompt(bmi)

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
        diet_prompt = const.get_diet_prompt(age, preferred_food_style, favorite_dishes)

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
