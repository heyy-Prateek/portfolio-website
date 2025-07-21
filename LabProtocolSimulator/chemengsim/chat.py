"""
Chat Module for Chemical Engineering Lab Simulator

This module provides a chat interface to answer questions about the experiments.
"""

import streamlit as st
import re

def load_experiment_info():
    """
    Load information about experiments from the knowledge base
    """
    # This dictionary contains information about each experiment
    # In a real implementation, this would be extracted from the lab manual PDF
    experiment_info = {
        "batch_reactor": {
            "name": "Isothermal Batch Reactor",
            "objective": "To determine the reaction rate constant (k) for the given saponification reaction of ethyl acetate in aqueous sodium hydroxide solution.",
            "theory": "A batch reactor is a closed system where no streams enter or leave during the reaction. The rate of reaction is defined as the change in concentration over time. For first-order reactions, -dC/dt = kC.",
            "procedure": "1. Prepare solutions of NaOH and ethyl acetate.\n2. Mix the solutions at a controlled temperature.\n3. Take samples at regular intervals.\n4. Titrate samples to determine concentration.\n5. Plot data to calculate reaction rate constant.",
            "equipment": "Glass reactor vessel, temperature control system, sampling device, titration apparatus.",
            "calculations": "For a first-order reaction: ln(C/C₀) = -kt. Plot ln(C/C₀) vs time to determine k.",
            "faqs": [
                {"question": "What is a batch reactor?", 
                 "answer": "A batch reactor is a closed vessel where reactants are loaded all at once, allowed to react for a set time, and then the products are removed all at once."},
                {"question": "Why is temperature control important?", 
                 "answer": "Temperature affects the reaction rate constant according to the Arrhenius equation. Maintaining constant temperature ensures consistent kinetic data."},
                {"question": "What is saponification?", 
                 "answer": "Saponification is the hydrolysis of an ester under basic conditions to form an alcohol and the salt of a carboxylic acid."}
            ]
        },
        "semi_batch_reactor": {
            "name": "Isothermal Semi-batch Reactor",
            "objective": "To study the effect of addition rate on reaction progress in a semi-batch reactor.",
            "theory": "Semi-batch reactors allow continuous addition of one or more reactants while no products are removed until the reaction is complete.",
            "procedure": "1. Load initial reactant into the vessel.\n2. Begin controlled addition of second reactant.\n3. Take samples at regular intervals.\n4. Analyze samples for concentration.\n5. Calculate conversion vs. time.",
            "equipment": "Reactor vessel, feed pump with flow control, temperature control system, sampling device.",
            "calculations": "Material balance accounting for feed: dN/dt = F_in - rV, where F_in is the molar feed rate.",
            "faqs": [
                {"question": "What is the advantage of a semi-batch reactor?", 
                 "answer": "Semi-batch reactors allow better control of highly exothermic reactions, improved selectivity, and management of viscous systems."},
                {"question": "How does feed rate affect conversion?", 
                 "answer": "Lower feed rates typically increase conversion by maintaining a lower concentration of the limiting reactant, which can improve selectivity for desired products."},
                {"question": "When would you choose semi-batch over batch?", 
                 "answer": "Semi-batch is preferred for highly exothermic reactions, when one reactant is volatile or hazardous, or when selectivity can be improved by controlling reactant concentration."}
            ]
        },
        "cstr": {
            "name": "Isothermal CSTR",
            "objective": "To determine the effect of residence time on conversion in a Continuous Stirred Tank Reactor.",
            "theory": "In a CSTR, perfect mixing causes the exit stream to have the same composition as the fluid within the reactor. The design equation is: V/F₀ = C₀-C/(-rₐ).",
            "procedure": "1. Set up continuous feed of reactants.\n2. Adjust flow rate to desired residence time.\n3. Wait for steady state.\n4. Sample outlet stream.\n5. Repeat for different flow rates.",
            "equipment": "CSTR vessel with stirrer, feed pumps, flow meters, temperature control system.",
            "calculations": "Conversion X = (C₀-C)/C₀. Space time τ = V/v₀.",
            "faqs": [
                {"question": "What is the difference between a CSTR and PFR?", 
                 "answer": "CSTRs have perfect mixing with uniform composition throughout. PFRs have no axial mixing with composition varying along the length."},
                {"question": "Why is a CSTR less efficient than a PFR?", 
                 "answer": "In a CSTR, reactants are immediately diluted to the final concentration, reducing reaction rate. In a PFR, concentration gradually changes, maintaining higher rates."},
                {"question": "What is residence time distribution?", 
                 "answer": "Residence time distribution describes how long different fluid elements remain in the reactor, characterizing the degree of mixing and flow behavior."}
            ]
        }
        # Additional experiments would be added here
    }
    
    # Add generic entries for experiments not specifically defined yet
    all_experiments = [
        "batch_reactor", "semi_batch_reactor", "cstr", "pfr", "crushers", 
        "filter_press", "rotary_vacuum_filter", "centrifuge_flotation", 
        "classifiers", "trommel"
    ]
    
    for exp in all_experiments:
        if exp not in experiment_info:
            experiment_info[exp] = {
                "name": exp.replace("_", " ").title(),
                "objective": f"To study the principles and operation of {exp.replace('_', ' ')}.",
                "theory": "Detailed theory is available in the lab manual.",
                "procedure": "Refer to the lab manual for detailed procedure.",
                "equipment": "Specialized equipment for this experiment.",
                "calculations": "Specific calculations depend on experimental measurements.",
                "faqs": [
                    {"question": f"What is the purpose of {exp.replace('_', ' ')}?", 
                     "answer": f"The {exp.replace('_', ' ')} experiment helps students understand the principles and applications in chemical engineering operations."}
                ]
            }
    
    return experiment_info

def find_best_answer(question, experiment_info, current_experiment):
    """
    Find the best answer to a question based on the experiment information
    """
    # Normalize the question
    question_lower = question.lower().strip()
    
    # Check FAQs first for the current experiment
    if current_experiment in experiment_info:
        for faq in experiment_info[current_experiment]["faqs"]:
            if question_similarity(question_lower, faq["question"].lower()) > 0.7:
                return faq["answer"]
    
    # Check for questions about different aspects of the experiment
    if "objective" in question_lower or "aim" in question_lower or "purpose" in question_lower:
        if current_experiment in experiment_info:
            return experiment_info[current_experiment]["objective"]
    
    elif "theory" in question_lower or "principle" in question_lower or "concept" in question_lower:
        if current_experiment in experiment_info:
            return experiment_info[current_experiment]["theory"]
    
    elif "procedure" in question_lower or "steps" in question_lower or "how to" in question_lower:
        if current_experiment in experiment_info:
            return experiment_info[current_experiment]["procedure"]
    
    elif "equipment" in question_lower or "apparatus" in question_lower:
        if current_experiment in experiment_info:
            return experiment_info[current_experiment]["equipment"]
    
    elif "calculation" in question_lower or "formula" in question_lower or "equation" in question_lower:
        if current_experiment in experiment_info:
            return experiment_info[current_experiment]["calculations"]
    
    # Search across all experiments if not found
    for exp_name, exp_data in experiment_info.items():
        if exp_name.replace("_", " ") in question_lower:
            return f"You're asking about {exp_data['name']}. {exp_data['objective']}"
    
    # Default response
    return "I don't have specific information about that. Please refer to the lab manual or ask your instructor for more details."

def question_similarity(q1, q2):
    """
    Simple similarity measure between questions (can be improved with NLP techniques)
    """
    # Convert to lowercase and tokenize by splitting on non-alphanumeric characters
    q1_tokens = set(re.findall(r'\w+', q1.lower()))
    q2_tokens = set(re.findall(r'\w+', q2.lower()))
    
    # Calculate Jaccard similarity
    if not q1_tokens or not q2_tokens:
        return 0
    
    intersection = len(q1_tokens.intersection(q2_tokens))
    union = len(q1_tokens.union(q2_tokens))
    
    return intersection / union

def handle_chat_input(question, experiment_info, current_experiment):
    """
    Process a user question and return an appropriate response
    """
    if not question:
        return "Please ask a question about the chemical engineering experiments."
    
    # Special commands
    if question.lower() == "help":
        return "You can ask questions about:\n- Experiment objectives\n- Theoretical concepts\n- Experimental procedures\n- Equipment needed\n- Calculations and formulas\n- Specific FAQs for each experiment"
    
    # Handle greetings
    greetings = ["hello", "hi", "hey", "greetings"]
    if any(greeting in question.lower() for greeting in greetings):
        return f"Hello! How can I help you with the {experiment_info[current_experiment]['name']} experiment?"
    
    # Find the best answer
    answer = find_best_answer(question, experiment_info, current_experiment)
    return answer

def chat_interface():
    """
    Main function to display the chat interface
    """
    st.title("Chemical Engineering Lab Assistant")
    
    # Get the current experiment from session state
    current_experiment = st.session_state.get('selected_experiment', 'Home')
    
    # If on Home page, show general info about all experiments
    if current_experiment == 'Home':
        exp_num = None
        current_exp_key = None
    else:
        # Extract the experiment number and key
        exp_num = int(current_experiment.split(".")[0])
        
        # Common experiment name mapping
        exp_names = [
            "",  # Home page has no number
            "batch_reactor",
            "semi_batch_reactor",
            "cstr",
            "pfr",
            "crushers",
            "filter_press",
            "rotary_vacuum_filter",
            "centrifuge_flotation",
            "classifiers",
            "trommel"
        ]
        
        current_exp_key = exp_names[exp_num]
    
    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Load experiment information
    experiment_info = load_experiment_info()
    
    # Display chat interface
    st.markdown("Ask me any questions about the chemical engineering experiments!")
    
    # Display relevant experiment information
    if current_exp_key and current_exp_key in experiment_info:
        st.subheader(f"Current Experiment: {experiment_info[current_exp_key]['name']}")
        with st.expander("Show Experiment Information"):
            st.markdown(f"**Objective:** {experiment_info[current_exp_key]['objective']}")
            st.markdown(f"**Theory:** {experiment_info[current_exp_key]['theory']}")
    
    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_question = st.text_input("Type your question here:", key="user_input")
        submit_button = st.form_submit_button("Ask")
    
    # Process input when form is submitted
    if submit_button and user_question:
        # Add user question to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Get response
        response = handle_chat_input(user_question, experiment_info, current_exp_key)
        
        # Add assistant response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Display chat history
    st.subheader("Chat History")
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Assistant:** {message['content']}")
    
    # Example questions
    with st.expander("Example Questions"):
        st.markdown("""
        - What is the objective of this experiment?
        - Explain the theory behind batch reactors
        - What equipment is needed for this experiment?
        - What calculations do I need to perform?
        - What is the procedure for this experiment?
        - Why is temperature control important?
        """)

# Main entry point for the chat module
def main():
    chat_interface()

if __name__ == "__main__":
    main() 