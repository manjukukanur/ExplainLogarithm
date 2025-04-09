import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Add utils to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logarithm_utils import generate_quiz_question

st.set_page_config(
    page_title="Logarithm Quiz",
    page_icon="📝",
    layout="wide"
)

st.title("Test Your Logarithm Knowledge")

st.markdown("""
This quiz will test your understanding of logarithms, their properties, and applications.
Challenge yourself with questions covering the concepts you've learned throughout this application.
""")

st.markdown("---")

# Initialize session state variables if they don't exist
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'questions' not in st.session_state:
    st.session_state.questions = []

if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None

if 'answered' not in st.session_state:
    st.session_state.answered = False

if 'show_explanation' not in st.session_state:
    st.session_state.show_explanation = False

# Start Quiz button
if not st.session_state.quiz_started:
    st.markdown("""
    ### Quiz Instructions
    
    - This quiz consists of 10 questions about logarithms
    - Each question has 4 possible answers
    - Select your answer and click "Submit"
    - After submitting, you'll see if your answer was correct
    - You can view an explanation for each question
    - Your final score will be shown at the end of the quiz
    
    Choose a difficulty level to begin:
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Easy", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.difficulty = "easy"
            # Generate 10 questions
            st.session_state.questions = [generate_quiz_question("easy") for _ in range(10)]
            st.rerun()
    
    with col2:
        if st.button("Medium", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.difficulty = "medium"
            # Generate 10 questions
            st.session_state.questions = [generate_quiz_question("medium") for _ in range(10)]
            st.rerun()
    
    with col3:
        if st.button("Hard", use_container_width=True):
            st.session_state.quiz_started = True
            st.session_state.difficulty = "hard"
            # Generate 10 questions
            st.session_state.questions = [generate_quiz_question("hard") for _ in range(10)]
            st.rerun()
    
    # Display a fun logarithm fact
    st.markdown("---")
    
    logarithm_facts = [
        "The word 'logarithm' comes from the Greek words 'logos' (ratio) and 'arithmos' (number).",
        "Logarithms were invented in the early 17th century by John Napier as a calculation aid.",
        "Before electronic calculators, logarithm tables were used to perform complex calculations.",
        "The Richter scale for measuring earthquakes is a logarithmic scale.",
        "Every logarithmic function passes through the point (1, 0).",
        "The natural logarithm (base e) is especially useful in calculus and growth/decay problems.",
        "The pH scale is a negative logarithmic scale of hydrogen ion concentration.",
        "In computer science, logarithms help analyze the efficiency of algorithms.",
        "Musical intervals are based on logarithmic frequency ratios.",
        "Human perception of sound and light intensity follows a logarithmic pattern.",
        "The Decibel (dB) scale for sound intensity is logarithmic."
    ]
    
    st.info(f"**Fun Logarithm Fact:** {random.choice(logarithm_facts)}")

# Display the quiz
else:
    # Create a progress bar
    progress = st.progress((st.session_state.current_question) / len(st.session_state.questions))
    
    # Display current question number and score
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}**")
    with col2:
        st.markdown(f"**Score: {st.session_state.score}/{st.session_state.current_question}**" if st.session_state.current_question > 0 else "**Score: 0/0**")
    
    # Get current question
    current_q = st.session_state.questions[st.session_state.current_question]
    
    # Display the question
    st.markdown(f"### {current_q['question']}")
    
    # Display the options
    if not st.session_state.answered:
        option_selected = st.radio(
            "Select your answer:",
            current_q['options'],
            key=f"q{st.session_state.current_question}"
        )
        
        # Store the selected option index
        st.session_state.selected_answer = current_q['options'].index(option_selected)
        
        # Submit button
        if st.button("Submit Answer"):
            st.session_state.answered = True
            
            # Check if answer is correct
            if st.session_state.selected_answer == current_q['correct_index']:
                st.session_state.score += 1
            
            st.rerun()
    
    else:  # After answering
        # Display all options with correct/incorrect highlighting
        for i, option in enumerate(current_q['options']):
            if i == current_q['correct_index']:
                st.success(f"✓ {option}")
            elif i == st.session_state.selected_answer:
                st.error(f"✗ {option}")
            else:
                st.markdown(f"  {option}")
        
        # Display if the answer was correct or not
        if st.session_state.selected_answer == current_q['correct_index']:
            st.success("Correct! Well done!")
        else:
            st.error("Incorrect. The correct answer is highlighted above.")
        
        # Show/Hide explanation button
        if st.button("Show Explanation" if not st.session_state.show_explanation else "Hide Explanation"):
            st.session_state.show_explanation = not st.session_state.show_explanation
            st.rerun()
        
        # Display explanation if requested
        if st.session_state.show_explanation:
            st.info(current_q['explanation'])
        
        # Next question button
        if st.session_state.current_question < len(st.session_state.questions) - 1:
            if st.button("Next Question"):
                st.session_state.current_question += 1
                st.session_state.answered = False
                st.session_state.show_explanation = False
                st.rerun()
        else:
            # If this is the last question, show a finish button
            if st.button("Finish Quiz"):
                st.session_state.quiz_completed = True
                st.rerun()

# Quiz completion screen
if st.session_state.get('quiz_completed', False):
    st.markdown("## Quiz Complete!")
    
    # Calculate final score and percentage
    final_score = st.session_state.score
    total_questions = len(st.session_state.questions)
    percentage = (final_score / total_questions) * 100
    
    # Display results
    st.markdown(f"### Your final score: {final_score}/{total_questions} ({percentage:.1f}%)")
    
    # Performance assessment
    if percentage >= 90:
        st.success("Excellent! You have a strong understanding of logarithms!")
    elif percentage >= 70:
        st.success("Good job! You understand most logarithm concepts.")
    elif percentage >= 50:
        st.warning("You've got the basics, but might want to review some concepts.")
    else:
        st.error("You might need to revisit the earlier sections to strengthen your understanding.")
    
    # Create a bar chart of results
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['Correct', 'Incorrect'],
        y=[final_score, total_questions - final_score],
        marker_color=['green', 'red']
    ))
    
    fig.update_layout(
        title="Quiz Results",
        xaxis_title="Answer Type",
        yaxis_title="Number of Questions",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Suggestions for further study
    st.markdown("""
    ### Where to go from here
    
    Based on your results, here are some suggestions:
    
    - **Review the sections** in this application to strengthen your understanding
    - **Try the interactive calculators** to practice working with logarithms
    - **Apply logarithms** to solve problems in your field of interest
    - **Explore advanced topics** like logarithmic differentiation and integration
    """)
    
    # Restart Quiz button
    if st.button("Take Another Quiz"):
        # Reset all quiz state
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.session_state.show_explanation = False
        st.session_state.quiz_completed = False
        st.rerun()
    
    # Return to home button
    if st.button("Return to Home"):
        st.session_state.quiz_started = False
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.questions = []
        st.session_state.selected_answer = None
        st.session_state.answered = False
        st.session_state.show_explanation = False
        st.session_state.quiz_completed = False
        st.switch_page("app.py")  # This will redirect to the home page

else:
    # Show a "Quit Quiz" button if quiz is in progress but not completed
    if st.session_state.quiz_started and not st.session_state.get('quiz_completed', False):
        if st.button("Quit Quiz"):
            st.session_state.quiz_started = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.questions = []
            st.session_state.selected_answer = None
            st.session_state.answered = False
            st.session_state.show_explanation = False
            st.rerun()
