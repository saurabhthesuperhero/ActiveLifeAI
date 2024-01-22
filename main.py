import streamlit as st
import constants as const  # Importing constants
from helpers import call_clarifai_api
from fpdf import FPDF

st.set_page_config(layout="wide")  # Expands the page to full width

# Initialize session state variables
if 'exercise_routine' not in st.session_state:
    st.session_state['exercise_routine'] = None
if 'diet_routine' not in st.session_state:
    st.session_state['diet_routine'] = None

if 'gender' not in st.session_state:
    st.session_state['gender'] = None
if 'health_goals' not in st.session_state:
    st.session_state['health_goals'] = []


def generate_pdf(text, filename):
    # Create instance of FPDF class
    pdf = FPDF()
    pdf.add_page()

    # Set font: Arial, bold, 12pt
    pdf.set_font("Arial", size=12)

    # Add text
    pdf.multi_cell(0, 10, text)

    # Save the pdf with name .pdf
    pdf_file_path = f"/tmp/{filename}"
    pdf.output(pdf_file_path)

    return pdf_file_path


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
            else:
                st.write("No exercise routine available.")

    with diet_analysis_placeholder.container():
        with st.sidebar.expander("Diet Analysis"):
            if st.session_state['diet_routine']:
                st.write("Analysis of your diet routine will be shown here.\n")
                st.write(st.session_state['diet_routine'])
            else:
                st.write("No diet routine available.")

    st.sidebar.title("Download Analysis")
    download_choice = st.sidebar.radio("Choose what to download:", ['Exercise Routine', 'Diet Routine'],
                                       key='download_choice')

    if st.sidebar.button("Download Analysis", key='download_analysis'):
        if download_choice == 'Exercise Routine' and 'exercise_routine_pdf' in st.session_state:
            with open(st.session_state['exercise_routine_pdf'], "rb") as file:
                st.sidebar.download_button(label="Download Exercise Routine PDF", data=file,
                                           file_name="Exercise_Routine.pdf")

        elif download_choice == 'Diet Routine' and 'diet_routine_pdf' in st.session_state:
            with open(st.session_state['diet_routine_pdf'], "rb") as file:
                st.sidebar.download_button(label="Download Diet Plan PDF", data=file, file_name="Diet_Plan.pdf")

        else:
            st.sidebar.error("The selected routine is not available. Generate it First!")


# Streamlit UI
st.title("AI ActiveLife")

# Main horizontal split: Input Mode and Result Mode
input_mode, result_mode = st.columns([1, 2])  # Adjusted ratio for better space utilization

# Input Mode
with input_mode:
    st.header("Input Mode")
    height = st.number_input("Enter your height in meters", min_value=0.5, max_value=3.0)
    weight = st.number_input("Enter your weight in kilograms", min_value=30, max_value=250)
    age = st.number_input("Enter your age", min_value=12, max_value=100)
    preferred_food_style = st.text_input("Enter your preferred food style (e.g., Indian, Mediterranean, etc.)")
    favorite_dishes = st.text_input("Enter your favorite dishes")
    st.session_state['gender'] = st.radio(
        "Select your gender",
        ('Male', 'Female', 'Other'))

    # Health Goals Selection
    st.session_state['health_goals'] = st.multiselect(
        "Select your health goals",
        ['Healthy Living', 'Lose Weight', 'Gain Muscle', 'Improve Fitness'])

# Result Mode - Two Columns for Exercise and Diet Routines
with result_mode:
    st.header("Result Mode")
    exercise_col, diet_col = st.columns(2)

    with exercise_col:
        st.subheader("Exercise Routine")
        if st.button('Get Exercise Routine'):
            # Check if the necessary fields are filled
            if not st.session_state['gender'] or not st.session_state['health_goals']:
                st.error("Please select your gender and at least one health goal to get your exercise routine.")
            elif height and weight:
                bmi = weight / (height ** 2)
                st.write("Your BMI is:", bmi)
                # Updated to pass gender and health_goals to the function
                exercise_prompt = const.get_exercise_prompt(bmi, st.session_state['gender'],
                                                            st.session_state['health_goals'])
                with st.spinner('Generating your personalized exercise routine...'):
                    exercise_routine, error = call_clarifai_api(exercise_prompt)
                    if error:
                        st.error(error)
                    else:
                        st.session_state['exercise_routine'] = exercise_routine
                        st.session_state['exercise_routine_pdf'] = generate_pdf(exercise_routine, "Exercise_Routine.pdf")

        if st.session_state['exercise_routine']:
            with st.expander("See your Exercise Routine"):
                st.write("**Personalized Exercise Routine:**")
                st.write(st.session_state['exercise_routine'])

    with diet_col:
        st.subheader("Diet Routine")
        if st.button('Get Diet Routine'):
            # Check if the necessary fields are filled
            if not preferred_food_style or not favorite_dishes:
                st.error("Please enter your preferred food style and favorite dishes to get your diet routine.")
            else:
                # Continue with generating the diet routine
                diet_prompt = const.get_diet_prompt(age, preferred_food_style, favorite_dishes,
                                                    st.session_state['gender'], st.session_state['health_goals'])
                with st.spinner('Generating your personalized diet routine...'):
                    diet_routine, error = call_clarifai_api(diet_prompt)
                    if error:
                        st.error(error)
                    else:
                        st.session_state['diet_routine'] = diet_routine
                        st.session_state['diet_routine_pdf'] = generate_pdf(diet_routine, "Diet_Plan.pdf")

        if st.session_state['diet_routine']:
            with st.expander("See your Diet Routine"):
                st.write("**Personalized Diet Routine:**")
                st.write(st.session_state['diet_routine'])

# Sidebar
display_sidebar_routines()
