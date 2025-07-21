import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import set_plot_style
from scipy.integrate import solve_ivp

# Set consistent style for plots
set_plot_style()

def app():
    st.title("Experiment 2: Isothermal Semi-batch Reactor")
    
    st.markdown("""
    ## Objective
    Study of a non-catalytic homogeneous reaction in a Semi-batch reactor.
    
    ## Aim
    To determine the concentration profiles and conversion for a given reaction in a semi-batch reactor.
    
    ## Chemical Reaction
    NaOH + CH₃COOC₂H₅ → CH₃COONa + C₂H₅OH
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        A semi-batch reactor is a hybrid of batch and continuous reactors. It allows for one or more reactants to be added continuously while no products are removed until the reaction is complete.
        
        The material balance for component A in a semi-batch reactor is given by:
        
        $$\\frac{dN_A}{dt} = F_{A0} - r_A V$$
        
        Where:
        - $N_A$ = moles of component A in the reactor
        - $F_{A0}$ = molar feed rate of component A
        - $r_A$ = rate of reaction of component A per unit volume
        - $V$ = volume of the reactor contents
        
        For the saponification reaction of ethyl acetate with sodium hydroxide, the rate equation is:
        
        $$r_A = kC_A C_B$$
        
        Where:
        - $C_A$ = concentration of NaOH
        - $C_B$ = concentration of ethyl acetate
        - $k$ = reaction rate constant
        
        In a semi-batch operation, the differential equations governing the system are:
        
        $$\\frac{dC_A}{dt} = \\frac{F_{A0}}{V} - kC_A C_B - \\frac{C_A}{V}\\frac{dV}{dt}$$
        
        $$\\frac{dC_B}{dt} = \\frac{F_{B0}}{V} - kC_A C_B - \\frac{C_B}{V}\\frac{dV}{dt}$$
        
        $$\\frac{dV}{dt} = q_0$$
        
        Where:
        - $q_0$ = volumetric feed rate
        - $F_{A0}$, $F_{B0}$ = molar feed rates of components A and B
        """)
    
    # Input parameters
    st.sidebar.header("Reaction Parameters")
    
    # Reactants initial conditions
    initial_vol_reactor = st.sidebar.number_input("Initial volume in reactor (L)", 
                                              min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    initial_conc_naoh = st.sidebar.number_input("Initial NaOH concentration in reactor (mol/L)", 
                                             min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    initial_conc_ea = st.sidebar.number_input("Initial Ethyl Acetate concentration in reactor (mol/L)", 
                                           min_value=0.0, max_value=1.0, value=0.0, step=0.001, format="%.4f")
    
    # Feed stream parameters
    feed_flow_rate = st.sidebar.number_input("Feed flow rate (L/min)", 
                                          min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    feed_conc_ea = st.sidebar.number_input("Ethyl Acetate concentration in feed (mol/L)", 
                                         min_value=0.001, max_value=1.0, value=0.05, step=0.001, format="%.4f")
    
    # Reaction parameters
    temperature = st.sidebar.slider("Reaction Temperature (°C)", 25, 60, 35, 1)
    total_time = st.sidebar.slider("Total Reaction Time (minutes)", 5, 120, 30, 5)
    
    # Calculated parameters
    temp_kelvin = temperature + 273.15
    
    # Define rate constants for different temperatures (based on experimental data)
    # Values based on the saponification reaction of ethyl acetate
    k_ref = 0.11  # L/(mol·min) at 35°C
    E_R = 4500    # E/R value in Kelvin
    
    # Calculate rate constant using Arrhenius equation
    k = k_ref * np.exp(E_R * (1/308.15 - 1/temp_kelvin))  # 308.15 K = 35°C (reference temp)
    
    # Define differential equations for semi-batch reactor
    def semi_batch_ode(t, y):
        # y[0] = C_NaOH, y[1] = C_EA, y[2] = V
        C_NaOH, C_EA, V = y
        
        # Molar feed rates
        F_EA0 = feed_flow_rate * feed_conc_ea  # mol/min of ethyl acetate
        F_NaOH0 = 0  # No NaOH in feed stream
        
        # Reaction rate per unit volume
        r = k * C_NaOH * C_EA  # mol/(L·min)
        
        # Total reaction rate
        r_total = r * V  # mol/min
        
        # Differential equations - more accurate formulation
        dC_NaOH_dt = (F_NaOH0 - r_total) / V - (C_NaOH * feed_flow_rate) / V
        dC_EA_dt = (F_EA0 - r_total) / V - (C_EA * feed_flow_rate) / V
        dV_dt = feed_flow_rate
        
        # Ensure concentrations don't go negative
        if C_NaOH < 0.0001 and dC_NaOH_dt < 0:
            dC_NaOH_dt = 0
        if C_EA < 0.0001 and dC_EA_dt < 0:
            dC_EA_dt = 0
            
        return [dC_NaOH_dt, dC_EA_dt, dV_dt]
    
    # Initial conditions
    y0 = [initial_conc_naoh, initial_conc_ea, initial_vol_reactor]
    
    # Time points
    t_span = (0, total_time)
    t_eval = np.linspace(0, total_time, 100)
    
    # Solve ODE
    solution = solve_ivp(semi_batch_ode, t_span, y0, t_eval=t_eval, method='RK45')
    
    time_points = solution.t
    conc_naoh = solution.y[0]
    conc_ea = solution.y[1]
    volume = solution.y[2]
    
    # Calculate products concentration
    # Initial amount of NaOH
    initial_naoh_moles = initial_conc_naoh * initial_vol_reactor
    
    # Current amount of NaOH
    current_naoh_moles = conc_naoh * volume
    
    # Products formed
    products_moles = initial_naoh_moles - current_naoh_moles
    conc_products = products_moles / volume
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (minutes)': time_points,
        'Volume (L)': volume,
        'NaOH Concentration (mol/L)': conc_naoh,
        'Ethyl Acetate Concentration (mol/L)': conc_ea,
        'Products Concentration (mol/L)': conc_products
    })
    
    # Calculate conversion
    df['NaOH Conversion (%)'] = (1 - (conc_naoh * volume) / initial_naoh_moles) * 100
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display current parameters
    st.write(f"**Reaction rate constant (k):** {k:.6f} L/(mol·min) at {temperature}°C")
    
    # Create tabs for different displays
    tab1, tab2, tab3, tab4 = st.tabs(["Concentration Profiles", "Conversion & Volume", "3D Visualization", "Data Table"])
    
    with tab1:
        # Concentration profile plot
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.plot(time_points, conc_naoh, 'b-', label='NaOH')
        ax.plot(time_points, conc_ea, 'r-', label='Ethyl Acetate')
        ax.plot(time_points, conc_products, 'g-', label='Products')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('Concentration (mol/L)')
        ax.set_title('Concentration Profiles (mol/L vs. Time in minutes)')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
    
    with tab2:
        # Conversion and volume plot
        fig2, ax1 = plt.subplots(figsize=(10, 6))
        
        # Conversion plot
        color = 'tab:blue'
        ax1.set_xlabel('Time (minutes)')
        ax1.set_ylabel('NaOH Conversion (%)', color=color)
        ax1.plot(time_points, df['NaOH Conversion (%)'], color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True)
        
        # Volume plot on secondary y-axis
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Reactor Volume (L)', color=color)
        ax2.plot(time_points, volume, color=color, linestyle='--')
        ax2.tick_params(axis='y', labelcolor=color)
        ax1.set_title('Conversion & Volume (Conversion % and Volume L vs. Time in minutes)')
        
        fig2.tight_layout()
        fig.tight_layout()
        st.pyplot(fig2)
    
    with tab3:
        # 3D visualization using line plots instead of surfaces to avoid triangulation issues
        from mpl_toolkits.mplot3d import Axes3D
        
        fig3 = plt.figure(figsize=(10, 8))
        ax3 = fig3.add_subplot(111, projection='3d')
        
        # Create time and volume arrays
        # Add small jitter to volume to avoid singular matrix in triangulation
        jitter = np.random.normal(0, 0.001, len(volume))
        volume_jitter = volume + jitter
        
        # Plot 3D lines
        ax3.plot(time_points, volume_jitter, conc_naoh, 'b-', linewidth=2, label='NaOH')
        ax3.plot(time_points, volume_jitter, conc_ea, 'r-', linewidth=2, label='Ethyl Acetate')
        ax3.plot(time_points, volume_jitter, conc_products, 'g-', linewidth=2, label='Products')
        
        # Add scatter points for better visibility
        ax3.scatter(time_points, volume_jitter, conc_naoh, c='blue', s=10)
        ax3.scatter(time_points, volume_jitter, conc_ea, c='red', s=10)
        ax3.scatter(time_points, volume_jitter, conc_products, c='green', s=10)
        
        # Set labels and title
        ax3.set_xlabel('Time (minutes)')
        ax3.set_ylabel('Volume (L)')
        ax3.set_zlabel('Concentration (mol/L)')
        ax3.set_title('3D Visualization of Concentration vs Time and Volume')
        ax3.legend()
        
        fig.tight_layout()
        st.pyplot(fig3)
    
    with tab4:
        # Display data table
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(time_points)-1, 20).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "semi_batch_reactor_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Parameter effect analysis
    with st.expander("Parameter Effect Analysis"):
        st.write("### Effect of Feed Flow Rate on Reactor Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            flow_rates = [0.05, 0.1, 0.2, 0.3]
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            
            for flow in flow_rates:
                # Solve ODE with different flow rate
                def semi_batch_ode_test(t, y):
                    # y[0] = C_NaOH, y[1] = C_EA, y[2] = V
                    C_NaOH, C_EA, V = y
                    
                    # Molar feed rates
                    F_EA0 = flow * feed_conc_ea  # mol/min of ethyl acetate
                    F_NaOH0 = 0  # No NaOH in feed stream
                    
                    # Reaction rate per unit volume
                    r = k * C_NaOH * C_EA  # mol/(L·min)
                    
                    # Total reaction rate
                    r_total = r * V  # mol/min
                    
                    # Differential equations - more accurate formulation
                    dC_NaOH_dt = (F_NaOH0 - r_total) / V - (C_NaOH * flow) / V
                    dC_EA_dt = (F_EA0 - r_total) / V - (C_EA * flow) / V
                    dV_dt = flow
                    
                    # Ensure concentrations don't go negative
                    if C_NaOH < 0.0001 and dC_NaOH_dt < 0:
                        dC_NaOH_dt = 0
                    if C_EA < 0.0001 and dC_EA_dt < 0:
                        dC_EA_dt = 0
                        
                    return [dC_NaOH_dt, dC_EA_dt, dV_dt]
                
                sol = solve_ivp(semi_batch_ode_test, t_span, y0, t_eval=t_eval, method='RK45')
                
                # Calculate conversion
                naoh_moles = sol.y[0] * sol.y[2]
                conversion = (1 - naoh_moles / initial_naoh_moles) * 100
                
                ax4.plot(sol.t, conversion, label=f'Flow = {flow} L/min')
            
            ax4.set_xlabel('Time (minutes)')
            ax4.set_ylabel('NaOH Conversion (%)')
            ax4.set_title('Effect of Flow Rate on Conversion')
            ax4.grid(True)
            ax4.legend()
            fig.tight_layout()
        st.pyplot(fig4)
        
        with col2:
            feed_concs = [0.02, 0.05, 0.1, 0.2]
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            
            for conc in feed_concs:
                # Solve ODE with different feed concentration
                def semi_batch_ode_test(t, y):
                    # y[0] = C_NaOH, y[1] = C_EA, y[2] = V
                    C_NaOH, C_EA, V = y
                    
                    # Molar feed rates
                    F_EA0 = feed_flow_rate * conc  # mol/min of ethyl acetate
                    F_NaOH0 = 0  # No NaOH in feed stream
                    
                    # Reaction rate per unit volume
                    r = k * C_NaOH * C_EA  # mol/(L·min)
                    
                    # Total reaction rate
                    r_total = r * V  # mol/min
                    
                    # Differential equations - more accurate formulation
                    dC_NaOH_dt = (F_NaOH0 - r_total) / V - (C_NaOH * feed_flow_rate) / V
                    dC_EA_dt = (F_EA0 - r_total) / V - (C_EA * feed_flow_rate) / V
                    dV_dt = feed_flow_rate
                    
                    # Ensure concentrations don't go negative
                    if C_NaOH < 0.0001 and dC_NaOH_dt < 0:
                        dC_NaOH_dt = 0
                    if C_EA < 0.0001 and dC_EA_dt < 0:
                        dC_EA_dt = 0
                        
                    return [dC_NaOH_dt, dC_EA_dt, dV_dt]
                
                sol = solve_ivp(semi_batch_ode_test, t_span, y0, t_eval=t_eval, method='RK45')
                
                ax5.plot(sol.t, sol.y[0], label=f'Feed EA = {conc} mol/L')
            
            ax5.set_xlabel('Time (minutes)')
            ax5.set_ylabel('NaOH Concentration (mol/L) vs. Time')
            ax5.set_title('Effect of Feed Concentration on NaOH')
            ax5.grid(True)
            ax5.legend()
            fig.tight_layout()
        st.pyplot(fig5)
