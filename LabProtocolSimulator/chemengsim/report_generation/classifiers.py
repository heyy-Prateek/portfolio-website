"""
Classifiers Report Generation Module
==================================

Module for generating reports for Single Cone Classifier and Thickener experiments.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .report_generator import ReportGenerator
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_separation_efficiency(data, total_coal_mass=30):
    """Calculate separation efficiency for single cone classifier"""
    # Copy original data
    results = data.copy()
    
    # Convert all values to numeric
    for col in results.columns:
        if col not in ['Time of collection (min)', 'Coal Size (micron)']:
            results[col] = pd.to_numeric(results[col], errors='coerce')
    
    # Calculate separation efficiency
    results['Separation Efficiency'] = results['Weight of coal obtained (g)'] / total_coal_mass
    
    return results

def calculate_thickener_concentration(data, calibration_data):
    """Calculate concentrations for thickener using calibration curve"""
    # Copy original data
    results = data.copy()
    
    # Convert all values to numeric
    for col in results.columns:
        if col != 'Time (min)':
            results[col] = pd.to_numeric(results[col], errors='coerce')
    
    # Calculate densities
    vessel_wt = 13  # g
    sample_volume = 50  # mL
    
    for point in ['bottom', '1', '2', '3', 'top']:
        col_name = f'Sample weight (g) W{point}'
        density_col = f'ρ{point}'
        conc_col = f'Conc{point}'
        
        if point == 'bottom':
            w_col = 'Wbottom'
        elif point == 'top':
            w_col = 'Wtop'
        else:
            w_col = f'W{point}'
        
        # Calculate density
        results[density_col] = (results[w_col] - vessel_wt) / sample_volume
        
        # Determine concentration from calibration data
        # For simplicity, we'll use a linear interpolation
        # In a real-world scenario, you'd use the actual calibration curve
        results[conc_col] = results[density_col].apply(
            lambda x: get_concentration_from_density(x, calibration_data)
        )
    
    return results

def get_concentration_from_density(density, calibration_data):
    """Get concentration from density using calibration data"""
    # Simple linear calibration model (example)
    # density = m * concentration + b
    m = 0.12  # example slope
    b = 1.0   # example intercept
    
    # Calculate concentration
    concentration = (density - b) / m
    
    # Ensure non-negative values
    return max(0, concentration)

def generate_classifier_plots(results):
    """Generate plots for single cone classifier experiment"""
    # Flow rate vs separation efficiency
    flow_rates = pd.to_numeric(results['Water flow rate (LPM)'], errors='coerce')
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=flow_rates,
        y=results['Separation Efficiency'],
        mode='lines+markers',
        name='Separation Efficiency'
    ))
    
    fig.update_layout(
        title='Effect of Flow Rate on Separation Efficiency',
        xaxis_title='Water Flow Rate (LPM)',
        yaxis_title='Separation Efficiency',
        template='plotly_white'
    )
    
    return fig

def generate_thickener_plots(results):
    """Generate plots for thickener experiment"""
    # Create subplots
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('Time vs Concentration', 'Height vs Concentration'))
    
    # Plot 1: Time vs Concentration
    times = results['Time (min)']
    for point in ['bottom', '1', '2', '3', 'top']:
        conc_col = f'Conc{point}'
        
        label = 'Bottom' if point == 'bottom' else 'Top' if point == 'top' else f'Point {point}'
        
        fig.add_trace(
            go.Scatter(
                x=times,
                y=results[conc_col],
                mode='lines+markers',
                name=label
            ),
            row=1, col=1
        )
    
    # Plot 2: Height vs Concentration
    # For a specific time point (e.g., t=5 min)
    time_point = 5  # minutes
    time_data = results[results['Time (min)'] == time_point]
    
    if not time_data.empty:
        # Heights for the different sampling points (in mm)
        heights = [0, 65, 155, 230, 370]  # Bottom, Point 3, Point 2, Point 1, Top
        concentrations = [
            time_data['Concbottom'].values[0],
            time_data['Conc3'].values[0],
            time_data['Conc2'].values[0],
            time_data['Conc1'].values[0],
            time_data['Conctop'].values[0]
        ]
        
        fig.add_trace(
            go.Scatter(
                x=heights,
                y=concentrations,
                mode='lines+markers',
                name=f'Time = {time_point} min'
            ),
            row=1, col=2
        )
    
    fig.update_layout(
        title='Thickener Concentration Analysis',
        template='plotly_white',
        height=500,
        width=900
    )
    
    fig.update_xaxes(title_text='Time (min)', row=1, col=1)
    fig.update_yaxes(title_text='Concentration (%)', row=1, col=1)
    
    fig.update_xaxes(title_text='Height (mm)', row=1, col=2)
    fig.update_yaxes(title_text='Concentration (%)', row=1, col=2)
    
    return fig

def generate_matplotlib_plots(results, experiment_type):
    """Generate matplotlib plots for document embedding"""
    if experiment_type == 'classifier':
        # Flow rate vs separation efficiency
        flow_rates = pd.to_numeric(results['Water flow rate (LPM)'], errors='coerce')
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(flow_rates, results['Separation Efficiency'], 'o-', color='blue')
        ax.set_xlabel('Water Flow Rate (LPM)')
        ax.set_ylabel('Separation Efficiency')
        ax.set_title('Effect of Flow Rate on Separation Efficiency')
        ax.grid(True)
        
        return fig
    
    elif experiment_type == 'thickener':
        # Create two plots
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        
        # Plot 1: Time vs Concentration
        times = results['Time (min)']
        for point in ['bottom', '1', '2', '3', 'top']:
            conc_col = f'Conc{point}'
            
            label = 'Bottom' if point == 'bottom' else 'Top' if point == 'top' else f'Point {point}'
            
            ax1.plot(times, results[conc_col], 'o-', label=label)
        
        ax1.set_xlabel('Time (min)')
        ax1.set_ylabel('Concentration (%)')
        ax1.set_title('Effect of Time on Concentration')
        ax1.legend()
        ax1.grid(True)
        
        # Plot 2: Height vs Concentration
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        
        # For a specific time point (e.g., t=5 min)
        time_point = 5  # minutes
        time_data = results[results['Time (min)'] == time_point]
        
        if not time_data.empty:
            # Heights for the different sampling points (in mm)
            heights = [0, 65, 155, 230, 370]  # Bottom, Point 3, Point 2, Point 1, Top
            concentrations = [
                time_data['Concbottom'].values[0],
                time_data['Conc3'].values[0],
                time_data['Conc2'].values[0],
                time_data['Conc1'].values[0],
                time_data['Conctop'].values[0]
            ]
            
            ax2.plot(heights, concentrations, 'o-', color='red')
            ax2.set_xlabel('Height (mm)')
            ax2.set_ylabel('Concentration (%)')
            ax2.set_title(f'Effect of Height on Concentration (Time = {time_point} min)')
            ax2.grid(True)
        
        return fig1, fig2

def create_classifier_form():
    """Create input form for single cone classifier experiment"""
    st.title("Single Cone Classifier Experiment")
    
    st.markdown("""
    ## Experiment: Single Cone Classifier
    
    Enter the observation data from your single cone classifier experiment. The system will calculate:
    - Separation efficiency for a mixture of coal and sand particles
    - Generate a graph showing the relationship between flow rate and separation efficiency
    """)
    
    # Constants section
    st.subheader("Constants")
    col1, col2 = st.columns(2)
    with col1:
        sand_density = st.number_input("Density of sand (g/cm³)", value=1.4, format="%.2f")
    with col2:
        coal_density = st.number_input("Density of coal (g/cm³)", value=0.65, format="%.2f")
    
    total_coal = st.number_input("Total coal used (g)", value=30, format="%.1f")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="classifier_student_name")
    student_id = st.text_input("Your ID", key="classifier_student_id")
    
    # Observation data
    st.subheader("Observation Data")
    st.markdown("Enter the observations from your experiment:")
    
    # Initialize or get session state
    if 'classifier_data' not in st.session_state:
        # Default empty dataframe with 3 rows
        st.session_state.classifier_data = pd.DataFrame({
            'Set No': ['1', '2', '3'],
            'Water flow rate (LPM)': ['10', '15', '20'],
            'Time of collection (min)': ['10', '10', '10'],
            'Coal Size (micron)': ['600', '600', '600'],
            'Weight of coal obtained (g)': ['', '', '']
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state.classifier_data,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state.classifier_data = edited_df
    
    generate_report = st.button("Generate Report", key="classifier_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        required_cols = ['Weight of coal obtained (g)']
        
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
            results = calculate_separation_efficiency(edited_df, total_coal)
            
            # Create interactive plotly plot for display
            fig = generate_classifier_plots(results)
            
            # Create matplotlib plot for document
            doc_fig = generate_matplotlib_plots(results, 'classifier')
            
            # Display results
            st.subheader("Results")
            st.dataframe(results[['Set No', 'Water flow rate (LPM)', 'Separation Efficiency']])
            
            # Display plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("cone_classifier", "Single Cone Classifier Experiment")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "To study the characteristics of a single cone classifier"
            objectives = [
                "To determine the separation efficiency for a mixture of coal and sand particles for a different flow rate of water"
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.document.add_heading("Observations", level=1)
            
            # Add constants
            constants_para = report.document.add_paragraph()
            constants_para.add_run(f"Density of sand = {sand_density} g/cm³\n").bold = True
            constants_para.add_run(f"Density of coal = {coal_density} g/cm³").bold = True
            
            # Add observation table
            report.document.add_heading("Table 1 Observations", level=2)
            report.add_observation_table(edited_df, "")
            
            # Add sample calculations
            report.document.add_heading("Sample Calculations", level=1)
            
            # Sample calculation text
            sample_calc = (
                f"Efficiency = Weight of coal obtained / Total coal used\n\n"
                f"For Set 1:\n"
                f"Efficiency = {edited_df.iloc[0]['Weight of coal obtained (g)']} / {total_coal} = {results.iloc[0]['Separation Efficiency']:.4f}"
            )
            report.document.add_paragraph(sample_calc)
            
            # Add results
            report.document.add_heading("Results and Discussions", level=1)
            
            # Add results table
            report.document.add_heading("Table 2 Results", level=2)
            report.add_results_table(results[['Set No', 'Water flow rate (LPM)', 'Separation Efficiency']], "")
            
            # Add figure
            report.document.add_paragraph()
            report.add_graph(doc_fig, "Figure 1")
            
            # Add discussion
            discussion = [
                "From the graph, it can be seen that with increase in flow rate the separation efficiency increases, which means that at higher flow rates it is easy to separate the two components of the mixture at higher flow rates.",
                "At higher flow rates the settling velocity of sand particles decreases, however, the coal particles are carried by the flow faster thus enabling better separation."
            ]
            report.add_discussion(discussion)
            
            # Add conclusion
            conclusion = [
                "The separation efficiency is a good measure of the performance of cone classifier. The separation efficiency increases with an increase in the flow rate of water."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def create_thickener_form():
    """Create input form for thickener experiment"""
    st.title("Thickener Experiment")
    
    st.markdown("""
    ## Experiment: Thickener
    
    Enter the observation data from your thickener experiment. The system will calculate:
    - Concentration of product at different heights
    - Generate graphs showing time vs. concentration and height vs. concentration
    """)
    
    # Constants section
    st.subheader("Constants")
    vessel_wt = st.number_input("Vessel weight (g)", value=13, format="%.1f")
    sample_collected = st.number_input("Sample Collected (mL)", value=50, format="%.1f")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="thickener_student_name")
    student_id = st.text_input("Your ID", key="thickener_student_id")
    
    # Observation data
    st.subheader("Observation Data")
    st.markdown("Enter the observations from your experiment:")
    
    # Initialize or get session state
    if 'thickener_data' not in st.session_state:
        # Default empty dataframe with 3 rows
        st.session_state.thickener_data = pd.DataFrame({
            'S. No': ['1', '2', '3'],
            'Time (min)': ['0', '5', '10'],
            'Wbottom': ['66', '66', '67'],
            'W1': ['65', '65', '66'],
            'W2': ['64', '65', '65'],
            'W3': ['64', '64', '65'],
            'Wtop': ['63', '63', '63']
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state.thickener_data,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state.thickener_data = edited_df
    
    # Calibration data (simplified)
    st.subheader("Calibration Chart")
    
    # Create dummy calibration data
    density_values = [1.00, 1.02, 1.04, 1.06, 1.08]
    concentration_values = [1.0, 1.75, 4.4, 5.8, 7.4]
    
    calibration_data = pd.DataFrame({
        'Density (g/cm³)': density_values,
        'Concentration (%)': concentration_values
    })
    
    st.dataframe(calibration_data)
    
    # Create simple calibration plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=density_values,
        y=concentration_values,
        mode='lines+markers',
        name='Calibration Curve'
    ))
    
    fig.update_layout(
        title='Calibration Chart',
        xaxis_title='Density (g/cm³)',
        yaxis_title='Concentration (%)',
        template='plotly_white'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    generate_report = st.button("Generate Report", key="thickener_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        required_cols = ['Wbottom', 'W1', 'W2', 'W3', 'Wtop']
        
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
            results = calculate_thickener_concentration(edited_df, calibration_data)
            
            # Create interactive plotly plot for display
            fig = generate_thickener_plots(results)
            
            # Create matplotlib plots for document
            doc_fig1, doc_fig2 = generate_matplotlib_plots(results, 'thickener')
            
            # Display results in two tables
            st.subheader("Calculated Densities")
            density_results = results[['S. No', 'Time (min)', 'ρbottom', 'ρ1', 'ρ2', 'ρ3', 'ρtop']]
            st.dataframe(density_results)
            
            st.subheader("Calculated Concentrations")
            conc_results = results[['S. No', 'Time (min)', 'Concbottom', 'Conc1', 'Conc2', 'Conc3', 'Conctop']]
            st.dataframe(conc_results)
            
            # Display plots
            st.plotly_chart(fig, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("thickener", "Thickener Experiment")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "To study the working principle of continuous type thickener"
            objectives = [
                "To determine the concentration of product obtained at the different height of sampling point",
                "Plot the curve for:",
                "- Time vs Concentration",
                "- Height of Sampling point vs Concentration"
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.document.add_heading("Observations", level=1)
            
            # Add constants
            constants_para = report.document.add_paragraph()
            constants_para.add_run(f"Vessel wt. = {vessel_wt}g\n").bold = True
            constants_para.add_run(f"Sample Collected = {sample_collected} mL").bold = True
            
            # Add observation table
            report.document.add_heading("Table 3 Observations", level=2)
            report.add_observation_table(edited_df, "")
            
            # Add sample calculations
            report.document.add_heading("Sample Calculations", level=1)
            report.document.add_paragraph("Performing Sample Calculations for Reading 2, i.e., Time = 5 min.")
            
            # Sample calculation text
            sample_calc = (
                f"First, the density of the sample obtained from each point is calculated, and then the concentration of the sample (in %) is determined by the use of the calibration chart provided for the experiment.\n\n"
                f"For Sample Obtained from the bottom:\n"
                f"ρbottom = (Wbottom - Vessel Weight) / Sample Volume\n"
                f"ρbottom = ({results.iloc[1]['Wbottom']} - {vessel_wt}) / {sample_collected} = {results.iloc[1]['ρbottom']:.2f} g/cm³\n\n"
                f"For Sample Obtained from the Sampling Point 1:\n"
                f"ρ1 = (W1 - Vessel Weight) / Sample Volume\n"
                f"ρ1 = ({results.iloc[1]['W1']} - {vessel_wt}) / {sample_collected} = {results.iloc[1]['ρ1']:.2f} g/cm³\n\n"
                f"For Sample Obtained from the Sampling Point 2:\n"
                f"ρ2 = (W2 - Vessel Weight) / Sample Volume\n"
                f"ρ2 = ({results.iloc[1]['W2']} - {vessel_wt}) / {sample_collected} = {results.iloc[1]['ρ2']:.2f} g/cm³\n\n"
                f"For Sample Obtained from the Sampling Point 3:\n"
                f"ρ3 = (W3 - Vessel Weight) / Sample Volume\n"
                f"ρ3 = ({results.iloc[1]['W3']} - {vessel_wt}) / {sample_collected} = {results.iloc[1]['ρ3']:.2f} g/cm³\n\n"
                f"For Sample Obtained from the top:\n"
                f"ρtop = (Wtop - Vessel Weight) / Sample Volume\n"
                f"ρtop = ({results.iloc[1]['Wtop']} - {vessel_wt}) / {sample_collected} = {results.iloc[1]['ρtop']:.2f} g/cm³"
            )
            report.document.add_paragraph(sample_calc)
            
            # Add results
            report.document.add_heading("Results and Discussions", level=1)
            
            # Add density results table
            report.document.add_heading("Table 4 Results", level=2)
            report.add_results_table(density_results, "")
            
            # Add calibration chart section
            report.document.add_heading("Calibration Chart:", level=2)
            
            # Create simplified calibration chart
            calib_fig, calib_ax = plt.subplots(figsize=(8, 5))
            calib_ax.plot(calibration_data['Density (g/cm³)'], calibration_data['Concentration (%)'], 'o-')
            calib_ax.set_xlabel('Density (g/cm³)')
            calib_ax.set_ylabel('Concentration (%)')
            calib_ax.set_title('Calibration Chart')
            calib_ax.grid(True)
            
            report.add_graph(calib_fig, "Figure 2")
            
            # Add concentration results based on calibration curve
            report.document.add_heading("Table 5 Concentration using a calibration chart", level=2)
            report.add_results_table(conc_results, "")
            
            # Add time vs concentration figure
            report.add_graph(doc_fig1, "Figure 3")
            
            # Add discussion for time vs concentration
            time_discussion = [
                "From the graph, it can be seen that as the time increases the concentration at all points(except at the top) increases. This is because as the time proceeds more particles settle down thus increasing concentration. At the top, the concentration remains constant because the particles are already settled down below that level."
            ]
            report.document.add_paragraph(time_discussion[0])
            
            # Add height vs concentration figure
            report.add_graph(doc_fig2, "Figure 4")
            
            # Add discussion for height vs concentration
            height_discussion = [
                "From the graph, it can be seen that with an increase in height, the concentration of product obtained also increases. It is because more particles are settling down at lower levels. There is one deflection point where the concentration decreases after increasing, it may be because of experimental error."
            ]
            report.document.add_paragraph(height_discussion[0])
            
            # Add conclusion
            conclusion = [
                "With the increase in height, the concentration of product increases.",
                "With the increase in time, the concentration of product also increases."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def app():
    """Main function to run the classifiers report generation app"""
    st.title("Classifiers Experiments")
    
    # Create tabs for the two classifiers experiments
    tab1, tab2 = st.tabs(["Single Cone Classifier", "Thickener"])
    
    with tab1:
        create_classifier_form()
    
    with tab2:
        create_thickener_form()

def main():
    """Entry point for the classifiers module when called from main.py"""
    app()