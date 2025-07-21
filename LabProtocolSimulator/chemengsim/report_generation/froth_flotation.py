"""
Froth Flotation Report Generation Module
=======================================

Module for generating reports for Froth Flotation experiments.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .report_generator import ReportGenerator
import plotly.graph_objects as go

def calculate_coal_recovery(data):
    """Calculate coal recovery metrics"""
    # Copy original data
    results = data.copy()
    
    # Convert all values to numeric
    for col in results.columns:
        results[col] = pd.to_numeric(results[col], errors='coerce')
    
    # Calculate final weight of coal
    results['Final wt. Of Coal(gram)'] = results['weight of coal (g)']
    
    # Calculate % recovery of coal
    initial_coal_weight = 10  # grams (from observations)
    results['% recovery of coal'] = (results['Final wt. Of Coal(gram)'] / initial_coal_weight) * 100
    
    return results

def generate_flotation_plots(results):
    """Generate plots for flotation experiment"""
    # Convert pine oil values to numeric
    pine_oil_values = pd.to_numeric(results['Pine Oil (ml)'], errors='coerce')
    
    # Plot: Pine Oil vs Coal Recovery
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pine_oil_values,
        y=results['% recovery of coal'],
        mode='lines+markers',
        name='Coal Recovery'
    ))
    
    fig.update_layout(
        title='Effect of Pine Oil Concentration on Coal Recovery',
        xaxis_title='Pine Oil Concentration (ml)',
        yaxis_title='Coal Recovery (%)',
        template='plotly_white'
    )
    
    return fig

def generate_matplotlib_plot(results):
    """Generate matplotlib plot for document embedding"""
    # Convert pine oil values to numeric
    pine_oil_values = pd.to_numeric(results['Pine Oil (ml)'], errors='coerce')
    
    # Plot: Pine Oil vs Coal Recovery
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(pine_oil_values, results['% recovery of coal'], 'o-', color='blue')
    ax.set_xlabel('Pine Oil Concentration (ml)')
    ax.set_ylabel('Coal Recovery (%)')
    ax.set_title('Effect of Pine Oil Concentration on Coal Recovery')
    ax.grid(True)
    
    return fig

def create_froth_flotation_form():
    """Create input form for froth flotation experiment"""
    st.title("Froth Flotation Experiment")
    
    st.markdown("""
    ## Experiment: Froth Flotation
    
    Enter the observation data from your froth flotation experiment. The system will calculate:
    - Coal recovery percentage
    - Create a graph showing the relationship between pine oil concentration and coal recovery
    """)
    
    # Constants section
    st.subheader("Constants")
    col1, col2, col3 = st.columns(3)
    with col1:
        coal_mass = st.number_input("Coal (g)", value=10, format="%.1f")
    with col2:
        sand_mass = st.number_input("Sand (g)", value=90, format="%.1f")
    with col3:
        detergent_volume = st.number_input("Detergent (ml)", value=15, format="%.1f")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="froth_flotation_student_name")
    student_id = st.text_input("Your ID", key="froth_flotation_student_id")
    
    # Observation data
    st.subheader("Observation Data")
    st.markdown("Enter the observations from your experiment:")
    
    # Initialize or get session state
    if 'flotation_data' not in st.session_state:
        # Default empty dataframe with 2 rows
        st.session_state.flotation_data = pd.DataFrame({
            'S. No': ['1', '2'],
            'Pine Oil (ml)': ['5', '10'],
            'Time (min)': ['10', '10'],
            'Weight of filter cloth+Particles (g)': ['', ''],
            'Dry weight of cloth (g)': ['', ''],
            'Dry weight of cloth + coal (g)': ['', ''],
            'weight of coal (g)': ['', '']
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state.flotation_data,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state.flotation_data = edited_df
    
    generate_report = st.button("Generate Report", key="froth_flotation_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        required_cols = [
            'weight of coal (g)'
        ]
        
        missing_data = False
        for col in required_cols:
            if edited_df[col].isna().any() or (edited_df[col] == '').any():
                missing_data = True
                break
        
        if missing_data:
            st.error("Please fill in all observation data before generating the report.")
            return
        
        # Generate report
        with st.spinner("Generating report..."):
            # Perform calculations
            results = calculate_coal_recovery(edited_df)
            
            # Create interactive plotly plot for display
            fig = generate_flotation_plots(results)
            
            # Create matplotlib plot for document
            doc_fig = generate_matplotlib_plot(results)
            
            # Display results
            st.subheader("Results")
            st.dataframe(results[['S. No', 'Pine Oil (ml)', 'Final wt. Of Coal(gram)', '% recovery of coal']])
            
            # Display plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("froth_flotation", "Froth Flotation Experiment")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "To study the separation performance of froth floatation using Denver Floatation cell."
            objectives = [
                "To calculate the percentage recovery of coal using Denver Floatation Cell."
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.document.add_heading("Observations and Calculations", level=1)
            
            # Add constants
            constants_para = report.document.add_paragraph()
            constants_para.add_run(f"Coal = {coal_mass} g\n").bold = True
            constants_para.add_run(f"Sand = {sand_mass} g\n").bold = True
            constants_para.add_run(f"Detergent = Fixed = {detergent_volume} ml").bold = True
            
            report.add_observation_table(edited_df)
            
            # Add calculations
            report.document.add_heading("Calculations", level=1)
            
            # Add results
            results_table = results[['S. No', 'Final wt. Of Coal(gram)', '% recovery of coal']]
            report.add_results_table(results_table, "Results and Discussions")
            
            # Add graph
            report.document.add_paragraph()
            report.add_graph(doc_fig, "Figure 1: Effect of Pine Oil Concentration on Coal Recovery")
            
            # Add discussion
            discussion = [
                "The experiment was carried out for constant collection time and varying concentration of pine oil. The above graph depicts that with increase in pine concentration the recovery increases. This might be because pine oil acts like a collector and promoter. Thus increasing the concentration of pine increases the coal carrying capacity of the air avid and water repellent particles."
            ]
            report.add_discussion(discussion)
            
            # Add conclusion
            conclusion = [
                "The Denver flotation cell is used to recover coal particles from a mixture of coal and sand particles.",
                "The recovery increases with increase in pine oil concentration in the floatation cell as the carrying capacity increases."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def app():
    """Main function to run the froth flotation report generation app"""
    create_froth_flotation_form()

def main():
    """Entry point for the froth flotation module when called from main.py"""
    app()