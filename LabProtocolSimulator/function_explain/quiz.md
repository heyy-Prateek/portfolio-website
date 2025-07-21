# Quiz Feature

The Quiz feature provides assessment tools to test student knowledge of chemical engineering concepts and laboratory procedures related to each experiment. It offers immediate feedback and helps reinforce learning objectives.

## Implementation Overview

The quiz system is designed to:
1. Provide experiment-specific questions
2. Support multiple question types (multiple choice, numerical input)
3. Score responses and provide immediate feedback
4. Track progress through question sets

## Code Structure

The quiz feature is implemented in the `chemengsim/quizzes/` directory, typically with a main `quiz_module.py` file that handles the quiz interface and scoring.

```python
# Main entry point in app.py for the Quiz feature
elif view_mode == "Quiz":
    try:
        # Extract experiment name from selection
        exp_num = int(experiment.split(".")[0])
        
        # Import quiz module and run quiz
        from chemengsim.quizzes import quiz_module
        quiz_module.run_quiz(exp_names[exp_num])
    except Exception as e:
        st.error(f"Error loading quiz: {str(e)}")
        st.info("Some quizzes may still be under development.")
```

## Quiz Module Structure

The typical structure of the quiz module includes:

```python
import streamlit as st
import json
import random
import os
import pandas as pd
import numpy as np

# Dictionary or file-based quiz data structure
QUIZ_DATA = {
    "batch_reactor": [
        {
            "question": "What is the relationship between concentration and time for a first-order reaction?",
            "type": "multiple_choice",
            "options": [
                "C = C₀ - kt",
                "C = C₀e^(-kt)",
                "1/C = 1/C₀ + kt",
                "C = kt + C₀"
            ],
            "answer": 1,  # Index of correct answer (0-based)
            "explanation": "For a first-order reaction, concentration decreases exponentially with time: C = C₀e^(-kt)"
        },
        # More questions...
    ],
    # More experiments...
}

def load_quiz_data(experiment_name):
    """Load quiz data for the selected experiment"""
    # Either return from the dictionary or load from a JSON file
    if experiment_name in QUIZ_DATA:
        return QUIZ_DATA[experiment_name]
    else:
        # Attempt to load from file
        quiz_path = os.path.join("quizzes", f"{experiment_name}.json")
        try:
            with open(quiz_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

def display_multiple_choice(question_data, question_number):
    """Display a multiple choice question and get user response"""
    st.markdown(f"**Question {question_number}:** {question_data['question']}")
    
    # Create radio buttons for options
    user_answer = st.radio(
        "Select your answer:",
        question_data["options"],
        key=f"q{question_number}"
    )
    
    # Create a submit button
    submitted = st.button("Submit Answer", key=f"submit{question_number}")
    
    if submitted:
        # Check if answer is correct
        correct_option = question_data["options"][question_data["answer"]]
        if user_answer == correct_option:
            st.success("Correct! ✅")
        else:
            st.error(f"Incorrect. The correct answer is: {correct_option}")
        
        # Display explanation
        st.info(f"Explanation: {question_data['explanation']}")
    
    return submitted
        
def display_numerical(question_data, question_number):
    """Display a numerical question and get user response"""
    st.markdown(f"**Question {question_number}:** {question_data['question']}")
    
    # Create numerical input
    user_answer = st.number_input(
        "Your answer:",
        min_value=float(question_data.get("min_value", 0)),
        max_value=float(question_data.get("max_value", 1000)),
        step=float(question_data.get("step", 0.1)),
        key=f"q{question_number}"
    )
    
    # Create a submit button
    submitted = st.button("Submit Answer", key=f"submit{question_number}")
    
    if submitted:
        # Check if answer is within acceptable range
        correct_answer = question_data["answer"]
        tolerance = question_data.get("tolerance", 0.01)
        
        if abs(user_answer - correct_answer) <= tolerance:
            st.success("Correct! ✅")
        else:
            st.error(f"Incorrect. The correct answer is: {correct_answer}")
        
        # Display explanation
        st.info(f"Explanation: {question_data['explanation']}")
    
    return submitted

def run_quiz(experiment_name):
    """Main function to run the quiz for the selected experiment"""
    st.title(f"Quiz: {experiment_name.replace('_', ' ').title()}")
    
    # Load quiz questions
    questions = load_quiz_data(experiment_name)
    
    if not questions:
        st.info(f"No quiz available for {experiment_name} yet. Check back later!")
        return
    
    # Initialize session state for question index if not exists
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.answered = False
    
    # Display current question
    if st.session_state.question_index < len(questions):
        current_question = questions[st.session_state.question_index]
        
        # Display appropriate question type
        if current_question["type"] == "multiple_choice":
            submitted = display_multiple_choice(current_question, st.session_state.question_index + 1)
        elif current_question["type"] == "numerical":
            submitted = display_numerical(current_question, st.session_state.question_index + 1)
        
        # Handle next question button
        if submitted or st.session_state.answered:
            st.session_state.answered = True
            if st.button("Next Question"):
                st.session_state.question_index += 1
                st.session_state.answered = False
                st.experimental_rerun()
    else:
        # Quiz completed
        st.success(f"Quiz completed! Your score: {st.session_state.score}/{len(questions)}")
        
        # Offer to restart
        if st.button("Start Over"):
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.answered = False
            st.experimental_rerun()
```

## Question Data Structure

Questions can be stored in JSON format for easy editing:

```json
[
  {
    "question": "What is the primary purpose of a batch reactor?",
    "type": "multiple_choice",
    "options": [
      "Continuous processing of reactants",
      "Contained reaction for a fixed amount of reactants",
      "Separating products from reactants",
      "Heating reaction mixtures only"
    ],
    "answer": 1,
    "explanation": "A batch reactor processes a fixed amount of reactants for a specific reaction time, with no inflow or outflow during the reaction."
  },
  {
    "question": "Calculate the conversion in a batch reactor if initial concentration was 5.0 mol/L and final concentration is 1.2 mol/L.",
    "type": "numerical",
    "min_value": 0,
    "max_value": 1.0,
    "step": 0.01,
    "answer": 0.76,
    "tolerance": 0.01,
    "explanation": "Conversion (X) = (C₀ - C)/C₀ = (5.0 - 1.2)/5.0 = 0.76 or 76%"
  }
]
```

## Quiz State Management

The quiz feature uses Streamlit's session state to maintain quiz progress:

```python
# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.answered = False

# Update state when user submits an answer
if correct_answer:
    st.session_state.score += 1

# Move to next question
st.session_state.question_index += 1
```

## Dependencies

The Quiz feature has the following dependencies:

- **Streamlit**: For UI components and session state management
- **Python Standard Library**:
  - `json`: For loading quiz data from files
  - `random`: For question randomization
  - `os`: For file path handling
- **NumPy**: For numerical calculations in answers
- **Pandas**: For data handling (optional, depending on quiz implementation)

No additional package installations are required beyond the core scientific Python stack.

## Extending the Quiz Feature

To add new quizzes:

1. Create a new JSON file for the experiment in the `quizzes` directory
2. Add questions following the established format
3. Optionally add specialized question types for the experiment
4. Update the quiz module to support any new question types

Quiz content can be easily updated or expanded without modifying the core application logic. 