import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import create_download_link

def app():
    st.title("Experiment 1: Isothermal Batch Reactor")
    
    st.markdown("""
    ## Objective
    Study of a non-catalytic homogeneous reaction in a Batch reactor.
    
    ## Aim
    To determine the reaction rate constant (k) for the given saponification reaction of ethyl acetate
    in aqueous sodium hydroxide solution.
    
    ## Chemical Reaction
    NaOH + CH₃COOC₂H₅ → CH₃COONa + C₂H₅OH
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        A batch reactor is a closed system such that no stream enters or leaves the reactor. In
        homogeneous reactions, all reacting species remain in a single phase. The rate of reaction of any
        reaction component A is defined as:
        
        $$r_A = -\\frac{1}{V} \\frac{dN_A}{dt} = -\\frac{dC_A}{dt}$$
        
        Rate of reaction is influenced by variables like temperature, pressure, and concentration. The
        rate of reaction is a function of concentration at constant temperature, i.e., $r_A = kC_A^n$ where n is
        the order of reaction.
        
        For a first order irreversible reaction A → Product, the rate equation and its integrated form are:
        
        $$-\\frac{dC_A}{dt} = kC_A$$
        
        $$\\ln\\frac{C_A}{C_{A0}} = -kt$$
        
        For a second order irreversible reaction 2A → Product, the rate equation and its integrated form are:
        
        $$-\\frac{dC_A}{dt} = kC_A^2$$
        
        $$\\frac{1}{C_A} - \\frac{1}{C_{A0}} = kt$$
        
        The reaction rate constant is a strong function of reaction temperature following the Arrhenius equation:
        
        $$k = A \\exp\\left(-\\frac{E}{RT}\\right)$$
        
        Where:
        - A is the Arrhenius constant
        - E is the activation energy (J/g mole)
        - R is the ideal gas law constant (8.314 J/g mole K)
        - T is the absolute temperature (K)
        """)
    
    # Input parameters
    st.sidebar.header("Reaction Parameters")
    
    # Initialize variables with default values
    initial_conc_naoh = st.sidebar.number_input("Initial concentration of NaOH (mol/L)", 
                                              min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    initial_conc_ea = st.sidebar.number_input("Initial concentration of Ethyl Acetate (mol/L)", 
                                            min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    temperature = st.sidebar.slider("Reaction Temperature (°C)", 25, 60, 35, 1)
    reaction_time = st.sidebar.slider("Reaction Time (minutes)", 5, 120, 30, 5)
    
    # Convert temperature to Kelvin for rate constant calculation
    temp_kelvin = temperature + 273.15
    
    # Define rate constants for different temperatures (based on experimental data)
    # Values based on the saponification reaction of ethyl acetate
    # These are approximate values for educational purposes
    k_ref = 0.11  # L/(mol·min) at 35°C
    E_R = 4500    # E/R value in Kelvin, where E is activation energy and R is gas constant
    
    # Calculate rate constant using Arrhenius equation
    k = k_ref * np.exp(E_R * (1/308.15 - 1/temp_kelvin))  # 308.15 K = 35°C (reference temperature)
    
    # Generate time points for the simulation
    time_points = np.linspace(0, reaction_time, 100)
    
    # For equal initial concentrations, special case
    if abs(initial_conc_naoh - initial_conc_ea) < 1e-6:
        # Equal initial concentrations case
        conc_naoh = initial_conc_naoh / (1 + initial_conc_naoh * k * time_points)
        reaction_order = "Second-order (equal concentrations)"
    else:
        # Different initial concentrations
        conc_naoh = (initial_conc_naoh * initial_conc_ea * 
                     (np.exp((initial_conc_naoh - initial_conc_ea) * k * time_points) - 1)) / \
                    (initial_conc_naoh * np.exp((initial_conc_naoh - initial_conc_ea) * k * time_points) - 
                     initial_conc_ea)
        reaction_order = "Second-order (different concentrations)"
    
    # Calculate concentration of ethyl acetate, products
    conc_ea = conc_naoh - initial_conc_naoh + initial_conc_ea
    conc_products = initial_conc_naoh - conc_naoh  # Same for both products
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (minutes)': time_points,
        'NaOH Concentration (mol/L)': conc_naoh,
        'Ethyl Acetate Concentration (mol/L)': conc_ea,
        'Sodium Acetate Concentration (mol/L)': conc_products,
        'Ethanol Concentration (mol/L)': conc_products
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display current parameters
    st.write(f"**Reaction rate constant (k):** {k:.6f} L/(mol·min) at {temperature}°C")
    st.write(f"**Reaction order:** {reaction_order}")
    
    # Create conversion column for data table display
    df_display = df.copy()
    df_display['Conversion (%)'] = (1 - df_display['NaOH Concentration (mol/L)'] / initial_conc_naoh) * 100
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Concentration Profiles", "Conversion Plot", "Data Table"])
    
    with tab1:
        # Concentration profile plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(time_points, conc_naoh, 'b-', label='NaOH')
        ax.plot(time_points, conc_ea, 'r-', label='Ethyl Acetate')
        ax.plot(time_points, conc_products, 'g-', label='Products')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Concentration (mol/L)')
        ax.set_title('Concentration Profiles')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    
    with tab2:
        # Conversion plot
        conversion = (1 - conc_naoh / initial_conc_naoh) * 100
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(time_points, conversion, 'b-')
        ax2.set_xlabel('Time (minutes)')
        ax2.set_ylabel('Conversion (%)')
        ax2.set_title('Conversion vs Time')
        ax2.grid(True)
        st.pyplot(fig2)
        
        # First order kinetic test
        first_order_test = np.log(conc_naoh / initial_conc_naoh)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(time_points, first_order_test, 'r-')
        ax3.set_xlabel('Time (minutes)')
        ax3.set_ylabel('ln(CA/CA0)')
        ax3.set_title('First-Order Kinetic Test')
        ax3.grid(True)
        st.pyplot(fig3)
        
        # Second order kinetic test
        second_order_test = 1/conc_naoh - 1/initial_conc_naoh
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(time_points, second_order_test, 'g-')
        ax4.set_xlabel('Time (minutes)')
        ax4.set_ylabel('1/CA - 1/CA0')
        ax4.set_title('Second-Order Kinetic Test')
        ax4.grid(True)
        st.pyplot(fig4)
    
    with tab3:
        # Display data table with selected time points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(time_points)-1, 10).astype(int)
        st.dataframe(df_display.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df_display.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "batch_reactor_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Temperature effect analysis
    with st.expander("Temperature Effect Analysis"):
        st.write("### Effect of Temperature on Reaction Rate Constant")
        
        temperatures = [25, 30, 35, 40, 45, 50]
        temp_kelvin_array = np.array(temperatures) + 273.15
        k_values = k_ref * np.exp(E_R * (1/308.15 - 1/temp_kelvin_array))
        
        temp_df = pd.DataFrame({
            'Temperature (°C)': temperatures,
            'Temperature (K)': temp_kelvin_array,
            'Rate Constant k (L/mol·min)': k_values
        })
        
        st.dataframe(temp_df)
        
        # Arrhenius plot
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        ax5.plot(1000/temp_kelvin_array, np.log(k_values), 'ro-')
        ax5.set_xlabel('1000/T (K^-1)')
        ax5.set_ylabel('ln(k)')
        ax5.set_title('Arrhenius Plot')
        ax5.grid(True)
        
        # Calculate activation energy from slope
        slope, intercept = np.polyfit(1000/temp_kelvin_array, np.log(k_values), 1)
        ax5.plot(1000/temp_kelvin_array, slope*(1000/temp_kelvin_array) + intercept, 'b--', 
                 label=f'Slope = {slope:.2f} → E = {-slope*8.314/1000:.1f} kJ/mol')
        ax5.legend()
        
        st.pyplot(fig5)
        st.write(f"Estimated Activation Energy: {-slope*8.314/1000:.2f} kJ/mol")
