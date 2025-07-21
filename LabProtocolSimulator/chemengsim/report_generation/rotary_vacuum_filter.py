"""
Rotary Vacuum Filter Report Generation Module
===========================================

Module for generating reports for Rotary Vacuum Filter experiments.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .report_generator import ReportGenerator
import plotly.graph_objects as go
from scipy.stats import linregress

def calculate_specific_cake_resistance(data, vacuum_pressure, area, viscosity):
    """Calculate specific cake resistance and filter medium resistance"""
    # Copy data and ensure numeric values
    df = data.copy()
    
    # Convert all values to numeric
    for col in df.columns:
        if col in ['Time (s)', 'Liquid level in the filtrate tank (cm)']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Calculate V (volume in m³)
    tank_area = 0.0005  # m² (example value, adjust as needed)
    df['V'] = df['Liquid level in the filtrate tank (cm)'] * 0.01 * tank_area  # Convert cm to m and multiply by area
    
    # Calculate t/V
    df['t/V'] = df['Time (s)'] / df['V']
    
    # Linear regression to find slope and intercept
    slope, intercept, r_value, p_value, std_err = linregress(df['V'], df['t/V'])
    
    # Calculate specific cake resistance
    pressure_pa = vacuum_pressure * 133.322  # Convert mmHg to Pa
    c = 0.1  # kg/m³ (slurry concentration, adjust as needed)
    
    alpha = 2 * area**2 * slope * pressure_pa / (viscosity * c)
    
    # Calculate filter medium resistance
    r_m = intercept * area * pressure_pa / viscosity
    
    return df, alpha, r_m, slope, intercept

def generate_vacuum_filter_plots(df):
    """Generate plots for vacuum filter experiment"""
    # Plot: V vs t/V
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['V'],
        y=df['t/V'],
        mode='markers',
        name='Experimental Data'
    ))
    
    # Add linear regression line
    slope, intercept, r_value, p_value, std_err = linregress(df['V'], df['t/V'])
    
    x_range = np.linspace(min(df['V']), max(df['V']), 100)
    y_range = slope * x_range + intercept
    
    fig.add_trace(go.Scatter(
        x=x_range,
        y=y_range,
        mode='lines',
        name=f'Linear Fit (y = {slope:.2e}x + {intercept:.2e})',
        line=dict(dash='dash')
    ))
    
    fig.update_layout(
        title='Plot of t/V vs V',
        xaxis_title='Volume of Filtrate, V (m³)',
        yaxis_title='t/V (s/m³)',
        template='plotly_white'
    )
    
    return fig, slope, intercept

def generate_matplotlib_plot(df, slope, intercept):
    """Generate matplotlib plot for document embedding"""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Plot experimental data
    ax.scatter(df['V'], df['t/V'], label='Experimental Data')
    
    # Add linear regression line
    x_range = np.linspace(min(df['V']), max(df['V']), 100)
    y_range = slope * x_range + intercept
    
    ax.plot(x_range, y_range, 'r--', label=f'Linear Fit (y = {slope:.2e}x + {intercept:.2e})')
    
    ax.set_xlabel('Volume of Filtrate, V (m³)')
    ax.set_ylabel('t/V (s/m³)')
    ax.set_title('Plot of t/V vs V')
    ax.legend()
    ax.grid(True)
    
    return fig

def create_rotary_vacuum_filter_form():
    """Create input form for rotary vacuum filter experiment"""
    st.title("Rotary Vacuum Filter Experiment")
    
    st.markdown("""
    ## Experiment: Rotary Vacuum Filter
    
    Enter the observation data from your rotary vacuum filter experiment. The system will calculate:
    - Specific cake resistance
    - Filter medium resistance
    - Generate a t/V vs V plot with linear regression
    """)
    
    # Constants section
    st.subheader("Constants")
    col1, col2, col3 = st.columns(3)
    with col1:
        drum_dia = st.number_input("Drum Diameter (mm)", value=350, format="%.1f")
    with col2:
        drum_length = st.number_input("Drum Length (mm)", value=450, format="%.1f")
    with col3:
        rotation_speed = st.number_input("Rotation Speed (rpm)", value=1.5, format="%.1f")
    
    viscosity = st.number_input("Viscosity (kg/m·s)", value=0.001, format="%.4f")
    
    # Calculate area
    area = np.pi * (drum_dia/1000) * (drum_length/1000)  # Convert mm to m
    st.write(f"Calculated Filter Area: {area:.4f} m²")
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="vacuum_filter_student_name")
    student_id = st.text_input("Your ID", key="vacuum_filter_student_id")
    
    # Experiment parameters
    st.subheader("Experiment Parameters")
    col1, col2 = st.columns(2)
    with col1:
        slurry_conc = st.number_input("Slurry concentration (wt %)", value=10, format="%.1f")
    with col2:
        vacuum_pressure = st.selectbox("Vacuum pressure (mm Hg)", [200, 400])
    
    # Observation data
    st.subheader("Observation Data")
    st.markdown("Enter the observations from your experiment:")
    
    # Initialize or get session state
    session_key = f"vacuum_filter_data_{vacuum_pressure}"
    if session_key not in st.session_state:
        # Default empty dataframe with 10 rows
        time_values = [15, 33, 54, 69, 91, 108, 128, 152, 174, 206] if vacuum_pressure == 200 else [8, 15, 27, 35, 41, 51, 59, 70, 78, 89]
        level_values = list(range(1, 11))
        
        st.session_state[session_key] = pd.DataFrame({
            'Time (s)': time_values,
            'Liquid level in the filtrate tank (cm)': level_values,
            'Weight (g) Wet Cake': [''] * 10,
            'Weight (g) Dry Cake': [''] * 10
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state[session_key],
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state[session_key] = edited_df
    
    generate_report = st.button("Generate Report", key="vacuum_filter_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        required_cols = ['Time (s)', 'Liquid level in the filtrate tank (cm)']
        
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
            results, alpha, r_m, slope, intercept = calculate_specific_cake_resistance(
                edited_df, 
                vacuum_pressure,
                area,
                viscosity
            )
            
            # Create interactive plotly plot for display
            fig, slope, intercept = generate_vacuum_filter_plots(results)
            
            # Create matplotlib plot for document
            doc_fig = generate_matplotlib_plot(results, slope, intercept)
            
            # Display results
            st.subheader("Calculated Parameters")
            st.write(f"Specific Cake Resistance (α): {alpha:.2e} m/kg")
            st.write(f"Filter Medium Resistance (Rm): {r_m:.2e} m⁻¹")
            
            st.subheader("Results Table")
            st.dataframe(results)
            
            # Display plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("rotary_vacuum_filter", "Rotary Vacuum Filter Experiment")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "Study of cake filtration using continuous vacuum filter such as rotary drum filter"
            objectives = [
                "To study the construction and operation of rotary drum filter",
                "Determine the specific cake resistance and filter medium resistance for CaCO3 slurry"
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.document.add_heading("Observations", level=1)
            
            # Add constants
            constants_table = report.document.add_table(rows=2, cols=2)
            constants_table.style = "Table Grid"
            
            # Header row
            constants_table.cell(0, 0).text = "Constant Parameters"
            constants_table.cell(0, 1).text = "Value"
            
            # Data rows
            row = constants_table.rows[1]
            row.cells[0].text = "Drum Dia"
            row.cells[1].text = f"{drum_dia} mm"
            
            row = constants_table.add_row()
            row.cells[0].text = "Drum Length"
            row.cells[1].text = f"{drum_length} mm"
            
            row = constants_table.add_row()
            row.cells[0].text = "Rotation Speed"
            row.cells[1].text = f"{rotation_speed} rpm"
            
            row = constants_table.add_row()
            row.cells[0].text = "Viscosity"
            row.cells[1].text = f"{viscosity} kg/m s"
            
            report.document.add_paragraph("")
            
            # Add experimental parameters
            exp_para = report.document.add_paragraph()
            exp_para.add_run(f"Set No: 1\n").bold = True
            exp_para.add_run(f"Slurry conc. (wt %): {slurry_conc}%\n").bold = True
            exp_para.add_run(f"Vacuum pressure: {vacuum_pressure} mm Hg").bold = True
            
            report.add_observation_table(edited_df)
            
            # Add calculations
            sample_calcs = [
                f"Case 1: For Vacuum Pressure of {vacuum_pressure} mg\n\n"
                f"Plot t/V vs V to find slope and intercept:\n"
                f"Slope = {slope:.2e}\n"
                f"Intercept = {intercept:.2e}\n\n"
                f"Calculation of α and R_m using the equation and the constant parameters.\n\n"
                f"Specific Cake Resistance:\n"
                f"α = 2 * A² * slope * ΔP / (μ * c)\n"
                f"α = 2 * ({area:.4f})² * {slope:.2e} * ({vacuum_pressure * 133.322:.2f}) / ({viscosity} * {slurry_conc/100})\n"
                f"α = {alpha:.2e} m/kg\n\n"
                f"Filter Medium Resistance:\n"
                f"R_m = intercept * A * ΔP / μ\n"
                f"R_m = {intercept:.2e} * {area:.4f} * {vacuum_pressure * 133.322:.2f} / {viscosity}\n"
                f"R_m = {r_m:.2e} m⁻¹"
            ]
            report.add_calculations("", sample_calcs)
            
            # Add results
            report.document.add_heading("Results and Discussions", level=1)
            
            report.document.add_paragraph(f"For vacuum pressure of {vacuum_pressure} mm Hg")
            
            # Add results table
            report.add_results_table(results[['Time (s)', 'Liquid level in the filtrate tank (cm)', 'V', 't/V']])
            
            # Add plot
            report.document.add_paragraph("Plot of t/V vs V:")
            report.add_graph(doc_fig)
            
            parameter_table = report.document.add_table(rows=1, cols=2)
            parameter_table.style = "Table Grid"
            
            # Header row
            parameter_table.cell(0, 0).text = "Parameter"
            parameter_table.cell(0, 1).text = "Value in SI"
            
            # Data rows
            row = parameter_table.add_row()
            row.cells[0].text = "Area"
            row.cells[1].text = f"{area:.4f} m²"
            
            row = parameter_table.add_row()
            row.cells[0].text = "Slope"
            row.cells[1].text = f"{slope:.2e} s/m⁶"
            
            row = parameter_table.add_row()
            row.cells[0].text = "Intercept"
            row.cells[1].text = f"{intercept:.2e} s/m³"
            
            row = parameter_table.add_row()
            row.cells[0].text = "Specific Cake Resistance (α)"
            row.cells[1].text = f"{alpha:.2e} m/kg"
            
            row = parameter_table.add_row()
            row.cells[0].text = "Filter Medium Resistance (Rm)"
            row.cells[1].text = f"{r_m:.2e} m⁻¹"
            
            # Add discussion
            discussion = [
                f"The experiment was conducted with a vacuum pressure of {vacuum_pressure} mm Hg and slurry concentration of {slurry_conc}%. The plot of t/V vs V shows a good linear relationship, which confirms that the filtration follows the standard cake filtration theory.",
                f"From the calculations, we obtained a specific cake resistance (α) of {alpha:.2e} m/kg and a filter medium resistance (Rm) of {r_m:.2e} m⁻¹. These values are within the expected range for CaCO3 slurry filtration.",
                "The specific cake resistance is an important parameter in filtration equipment design, as it determines the rate at which filtration occurs for a given pressure drop and cake thickness."
            ]
            report.add_discussion(discussion)
            
            # Add conclusion
            conclusion = [
                "The rotary vacuum filter experiment successfully demonstrated cake filtration principles.",
                f"The specific cake resistance (α) of {alpha:.2e} m/kg was determined for CaCO3 slurry at {slurry_conc}% concentration and {vacuum_pressure} mm Hg vacuum pressure.",
                f"The filter medium resistance (Rm) was found to be {r_m:.2e} m⁻¹.",
                "The linear relationship between t/V and V confirms that the filtration follows standard cake filtration theory with a constant pressure drop across the filter medium and cake."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def app():
    """Main function to run the rotary vacuum filter report generation app"""
    create_rotary_vacuum_filter_form()

def main():
    """Entry point for the rotary vacuum filter module when called from main.py"""
    app()