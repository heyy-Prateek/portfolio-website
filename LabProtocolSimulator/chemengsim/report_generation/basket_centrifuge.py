"""
Basket Centrifuge Report Generation Module
=========================================

Module for generating reports for Basket Centrifuge experiments.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .report_generator import ReportGenerator
import plotly.graph_objects as go

def calculate_water_retention_recovery(data):
    """Calculate water retention and recovery metrics"""
    # Calculate required values
    results = pd.DataFrame()
    
    # Copy original data
    results = data.copy()
    
    # Convert all values to numeric
    for col in results.columns:
        results[col] = pd.to_numeric(results[col], errors='coerce')
    
    # Volume of filtrate in liters
    results['Volume of filtrate(litre)'] = results['Volume of the filtrate collected (lit.)']
    
    # Calculate weight of wet cake
    results['Wt. of wet cake(g)'] = results['Weight (g) Wet Cake']
    
    # Calculate weight of dry cake
    results['Wt of dry cake(g)'] = results['Weight (g) Dry Cake']
    
    # Calculate water retention
    results['% water retention'] = (results['Wt. of wet cake(g)'] - results['Wt of dry cake(g)']) / (results['Wt. of wet cake(g)'] - results['Wt of dry cake(g)']) * 100
    
    # Calculate water recovery
    initial_water_volume = 4.5  # liters (from observations)
    results['% water recovery'] = (results['Volume of filtrate(litre)'] / initial_water_volume) * 100
    
    # Calculate water retention using water recovery
    results['% water retention using water recovery'] = 100 - results['% water recovery']
    
    return results

def generate_centrifuge_plots(results):
    """Generate plots for centrifuge experiment"""
    # Convert rpm values to numeric
    rpm_values = pd.to_numeric(results['Variac reading (rpm)'], errors='coerce')
    
    # Plot 1: RPM vs Water Recovery
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=rpm_values,
        y=results['% water recovery'],
        mode='lines+markers',
        name='Water Recovery'
    ))
    
    fig1.update_layout(
        title='Effect of Rotational Speed on Water Recovery',
        xaxis_title='Rotational Speed (RPM)',
        yaxis_title='Water Recovery (%)',
        template='plotly_white'
    )
    
    # Plot 2: RPM vs Water Retention
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=rpm_values,
        y=results['% water retention'],
        mode='lines+markers',
        name='Water Retention'
    ))
    
    fig2.update_layout(
        title='Effect of Rotational Speed on Water Retention',
        xaxis_title='Rotational Speed (RPM)',
        yaxis_title='Water Retention (%)',
        template='plotly_white'
    )
    
    return fig1, fig2

def generate_matplotlib_plots(results):
    """Generate matplotlib plots for document embedding"""
    # Convert rpm values to numeric
    rpm_values = pd.to_numeric(results['Variac reading (rpm)'], errors='coerce')
    
    # Plot 1: RPM vs Water Recovery
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    ax1.plot(rpm_values, results['% water recovery'], 'o-', color='blue')
    ax1.set_xlabel('Rotational Speed (RPM)')
    ax1.set_ylabel('Water Recovery (%)')
    ax1.set_title('Effect of Rotational Speed on Water Recovery')
    ax1.grid(True)
    
    # Plot 2: RPM vs Water Retention
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    ax2.plot(rpm_values, results['% water retention'], 'o-', color='red')
    ax2.set_xlabel('Rotational Speed (RPM)')
    ax2.set_ylabel('Water Retention (%)')
    ax2.set_title('Effect of Rotational Speed on Water Retention')
    ax2.grid(True)
    
    return fig1, fig2

def create_basket_centrifuge_form():
    """Create input form for basket centrifuge experiment"""
    st.title("Basket Centrifuge Experiment")
    
    st.markdown("""
    ## Experiment: Basket Centrifuge
    
    Enter the observation data from your basket centrifuge experiment. The system will calculate:
    - Water retention percentage
    - Water recovery percentage
    - Create graphs showing the relationship between rotational speed and these metrics
    """)
    
    # Constants section
    st.subheader("Constants")
    col1, col2, col3 = st.columns(3)
    with col1:
        water_volume = st.number_input("Volume of water (liters)", value=4.5, format="%.1f")
    with col2:
        caco3_mass = st.number_input("CaCO3 (g)", value=500, format="%.1f")
    with col3:
        pan_weight = st.number_input("Empty weight of pan (g)", value=63, format="%.1f")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="basket_centrifuge_student_name")
    student_id = st.text_input("Your ID", key="basket_centrifuge_student_id")
    
    # Observation data
    st.subheader("Observation Data")
    st.markdown("Enter the observations from your experiment:")
    
    # Initialize or get session state
    if 'centrifuge_data' not in st.session_state:
        # Default empty dataframe with 3 rows
        st.session_state.centrifuge_data = pd.DataFrame({
            'Set No': ['1', '2', '3'],
            'Variac reading (rpm)': ['50', '60', '70'],
            'Feed concentration (%)': ['10', '10', '10'],
            'Volume of the filtrate collected (lit.)': ['', '', ''],
            'Time of filtration (sec)': ['', '', ''],
            'Weight (g) Wet Cake': ['', '', ''],
            'Weight (g) Dry Cake': ['', '', '']
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state.centrifuge_data,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state.centrifuge_data = edited_df
    
    generate_report = st.button("Generate Report", key="basket_centrifuge_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        required_cols = [
            'Volume of the filtrate collected (lit.)', 
            'Weight (g) Wet Cake', 
            'Weight (g) Dry Cake'
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
            results = calculate_water_retention_recovery(edited_df)
            
            # Create interactive plotly plots for display
            fig1, fig2 = generate_centrifuge_plots(results)
            
            # Create matplotlib plots for document
            doc_fig1, doc_fig2 = generate_matplotlib_plots(results)
            
            # Display results
            st.subheader("Results")
            st.dataframe(results)
            
            # Display plots
            st.plotly_chart(fig1, use_container_width=True)
            st.plotly_chart(fig2, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("basket_centrifuge", "Basket Centrifuge Experiment")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "To study the characteristics of Basket centrifuge."
            objectives = [
                "To determine % recovery of water and % water retained by the cake for 10 wt% slurry at different speeds of rotation of basket."
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.add_observation_table(edited_df, "Observations")
            
            # Add calculations
            sample_calcs = [
                f"For Set 1:\n\n"
                f"Volume of filtrate = {edited_df.iloc[0]['Volume of the filtrate collected (lit.)']} liters\n\n"
                f"Weight of wet cake = {edited_df.iloc[0]['Weight (g) Wet Cake']} g\n\n"
                f"Weight of dry cake = {edited_df.iloc[0]['Weight (g) Dry Cake']} g\n\n"
                f"% Water retention = (Weight of wet cake - Weight of dry cake) / (Weight of wet cake - Weight of dry cake) × 100\n"
                f"% Water retention = {results.iloc[0]['% water retention']:.2f}%\n\n"
                f"% Water recovery = (Volume of filtrate / Initial water volume) × 100\n"
                f"% Water recovery = ({edited_df.iloc[0]['Volume of the filtrate collected (lit.)']} / {water_volume}) × 100 = {results.iloc[0]['% water recovery']:.2f}%\n\n"
                f"% Water retention using water recovery = 100 - % Water recovery\n"
                f"% Water retention using water recovery = 100 - {results.iloc[0]['% water recovery']:.2f} = {results.iloc[0]['% water retention using water recovery']:.2f}%"
            ]
            report.add_calculations("", sample_calcs)
            
            # Add results
            report.add_results_table(results, "Results and Discussions")
            
            # Add graphs
            report.document.add_paragraph()
            report.add_graph(doc_fig1, "Figure 1: Effect of Rotational Speed on Water Recovery")
            report.document.add_paragraph()
            report.add_graph(doc_fig2, "Figure 2: Effect of Rotational Speed on Water Retention")
            
            # Add discussion
            discussion = [
                "From the above table it is evident that the percentage retention of water using the mass of wet cake and dry cake is greater than the percentage retention of water using water recovery.",
                "This might be due to the fact that the retention calculated using the mass of wet and dry cake requires the use of a heater where the water is removed from the wet cake. The heater is limited by its efficiency and might not be able to completely remove the water from the wet cake. Thus even in the dry cake some moisture might be trapped. This led to increased retention value.",
                "The graphs show that with increase in the rotational speed of the basket centrifuge the water recovery increases and percentage retention of water in the cake formed decreases. This is intuitive and agrees with the theory suggesting that with increased rotational speed the basket centrifuge collects the same amount of filtrate at a higher water recovery percentage and lower water retention."
            ]
            report.add_discussion(discussion)
            
            # Add conclusion
            conclusion = [
                "In basket centrifuge the water recovery increases with increase in rotational speed.",
                "In basket centrifuge the water retention decreases with increase in rotational speed.",
                "Calculating the water retention by calculating the water recovery is a more accurate method as no external operation is not needed to calculate the water recovery thus reducing the error due to efficiency of heater."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def app():
    """Main function to run the basket centrifuge report generation app"""
    create_basket_centrifuge_form()

def main():
    """Entry point for the basket centrifuge module when called from main.py"""
    app()