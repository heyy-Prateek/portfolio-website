import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy import optimize
from utils import set_plot_style

# Set consistent style for plots
set_plot_style()

def app():
    st.title("Experiment 3: Isothermal CSTR (Continuous Stirred Tank Reactor)")
    
    st.markdown("""
    ## Objective
    Study of a non-catalytic homogeneous reaction in a Continuous Stirred Tank Reactor (CSTR).
    
    ## Aim
    To determine the steady-state conversion and concentration profiles in a CSTR for a given reaction.
    
    ## Types of CSTR
    1. CSTR with Jacket Heating
    2. CSTR with Coil Heating
    
    ## Chemical Reaction
    NaOH + CH₃COOC₂H₅ → CH₃COONa + C₂H₅OH
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        A Continuous Stirred Tank Reactor (CSTR) is a vessel where perfect mixing is assumed, resulting in uniform concentration throughout the reactor. The key characteristics of a CSTR are:
        
        1. The exit stream has the same composition as the fluid within the reactor
        2. The reactor operates at steady state
        3. There is perfect mixing inside the reactor
        
        The material balance for a CSTR at steady state is:
        
        $$F_{A0} - F_A + r_A V = 0$$
        
        Where:
        - $F_{A0}$ = molar feed rate of component A
        - $F_A$ = molar exit rate of component A
        - $r_A$ = rate of reaction of component A per unit volume
        - $V$ = volume of the reactor
        
        In terms of conversion ($X$), the equation becomes:
        
        $$V = \\frac{F_{A0} X}{-r_A}$$
        
        For a second-order reaction $A + B \\rightarrow C + D$, the rate equation is:
        
        $$r_A = kC_A C_B$$
        
        For the case of equal initial concentrations ($C_{A0} = C_{B0}$), the CSTR design equation is:
        
        $$\\tau = \\frac{X}{k C_{A0} (1-X)^2}$$
        
        Where:
        - $\\tau$ = residence time ($V/v_0$)
        - $X$ = fractional conversion
        - $k$ = reaction rate constant
        - $C_{A0}$ = initial concentration of A
        
        For the case of different initial concentrations, the equation becomes more complex.
        """)
    
    # Choose CSTR type
    cstr_type = st.radio("Select CSTR Type:", ["Jacket Heating", "Coil Heating"])
    
    # Input parameters
    st.sidebar.header("Reactor Parameters")
    
    # Feed parameters
    feed_flow_rate = st.sidebar.number_input("Feed flow rate (L/min)", 
                                          min_value=0.1, max_value=10.0, value=2.0, step=0.1)
    
    feed_conc_naoh = st.sidebar.number_input("NaOH concentration in feed (mol/L)", 
                                           min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    
    feed_conc_ea = st.sidebar.number_input("Ethyl Acetate concentration in feed (mol/L)", 
                                         min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    
    # Reactor parameters
    reactor_volume = st.sidebar.number_input("Reactor volume (L)", 
                                          min_value=1.0, max_value=100.0, value=20.0, step=1.0)
    
    temperature = st.sidebar.slider("Reaction Temperature (°C)", 25, 60, 35, 1)
    
    # Heating parameters
    if cstr_type == "Jacket Heating":
        coolant_temp = st.sidebar.slider("Jacket Coolant Temperature (°C)", 10, 80, 25, 1)
        overall_heat_transfer = st.sidebar.number_input("Overall Heat Transfer Coefficient (W/m²·K)", 
                                                     min_value=10.0, max_value=1000.0, value=200.0, step=10.0)
        jacket_area = st.sidebar.number_input("Jacket Heat Transfer Area (m²)", 
                                            min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    else:  # Coil Heating
        coolant_temp = st.sidebar.slider("Coil Coolant Temperature (°C)", 10, 80, 25, 1)
        overall_heat_transfer = st.sidebar.number_input("Overall Heat Transfer Coefficient (W/m²·K)", 
                                                      min_value=10.0, max_value=1000.0, value=300.0, step=10.0)
        coil_area = st.sidebar.number_input("Coil Heat Transfer Area (m²)", 
                                          min_value=0.1, max_value=10.0, value=0.5, step=0.1)
        coil_length = st.sidebar.number_input("Coil Length (m)", 
                                            min_value=1.0, max_value=20.0, value=5.0, step=0.5)
    
    # Calculate residence time
    residence_time = reactor_volume / feed_flow_rate  # minutes
    
    # Calculated parameters
    temp_kelvin = temperature + 273.15
    
    # Define rate constants for different temperatures (based on experimental data)
    # Values based on the saponification reaction of ethyl acetate
    k_ref = 0.11  # L/(mol·min) at 35°C
    E_R = 4500    # E/R value in Kelvin
    
    # Calculate rate constant using Arrhenius equation
    k = k_ref * np.exp(E_R * (1/308.15 - 1/temp_kelvin))  # 308.15 K = 35°C (reference temperature)
    
    # Calculate steady-state conversion and concentrations
    if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
        # Equal initial concentrations case
        # For a second-order reaction with equal initial concentrations
        # Solve X from: τ = X / (k * C_A0 * (1-X)²)
        
        def equal_conc_equation(X):
            return residence_time - X / (k * feed_conc_naoh * (1-X)**2)
        
        # Initial guess
        X_guess = 0.5
        
        # Solve the equation
        X_solution = fsolve(equal_conc_equation, X_guess)[0]
        
        # Clamp to valid range
        X_solution = max(0.0, min(1.0, X_solution))
        
        # Calculate exit concentrations
        exit_conc_naoh = feed_conc_naoh * (1 - X_solution)
        exit_conc_ea = feed_conc_ea * (1 - X_solution)
        exit_conc_products = feed_conc_naoh * X_solution
        
    else:
        # Different initial concentrations case
        # For a second-order reaction with different initial concentrations
        M = feed_conc_ea / feed_conc_naoh  # ratio of feed concentrations
        
        def diff_conc_equation(X):
            return residence_time - (1 / (k * feed_conc_naoh)) * np.log((M - X) / (M * (1 - X))) / (M - 1)
        
        # Initial guess
        X_guess = 0.5
        
        # Solve the equation
        try:
            X_solution = fsolve(diff_conc_equation, X_guess)[0]
            
            # Clamp to valid range
            X_solution = max(0.0, min(1.0, X_solution))
            
        except:
            # Fallback calculation if solver fails
            X_solution = 1.0 / (1.0 + 1.0 / (k * feed_conc_naoh * residence_time))
        
        # Calculate exit concentrations
        exit_conc_naoh = feed_conc_naoh * (1 - X_solution)
        exit_conc_ea = feed_conc_ea - feed_conc_naoh * X_solution
        exit_conc_products = feed_conc_naoh * X_solution
    
    # Heat generation from reaction
    # Saponification heat of reaction (approximation)
    heat_of_reaction = -55000  # J/mol (exothermic)
    
    # Rate of heat generation
    heat_generation = -heat_of_reaction * feed_conc_naoh * feed_flow_rate * X_solution  # J/min
    
    # Heat transfer analysis
    if cstr_type == "Jacket Heating":
        heat_transfer_area = jacket_area
    else:  # Coil Heating
        heat_transfer_area = coil_area
    
    # Heat transfer rate
    heat_transfer = overall_heat_transfer * heat_transfer_area * (temperature - coolant_temp) / 60  # J/min
    
    # Create data for steady-state operation
    operating_time = np.linspace(0, 60, 100)  # minutes
    
    # For plotting stability around steady state (small perturbations)
    perturbation = 0.1  # 10% perturbation
    conc_naoh = np.ones_like(operating_time) * exit_conc_naoh
    conc_naoh[:10] = exit_conc_naoh * (1 + perturbation)  # Initial perturbation
    
    # Simple damped response to show stability
    for i in range(10, len(operating_time)):
        conc_naoh[i] = exit_conc_naoh + (conc_naoh[i-1] - exit_conc_naoh) * np.exp(-0.2)
    
    # Conversion profile
    conversion = (feed_conc_naoh - conc_naoh) / feed_conc_naoh * 100
    
    # Create dataframe
    df = pd.DataFrame({
        'Time (minutes)': operating_time,
        'NaOH Concentration (mol/L)': conc_naoh,
        'Conversion (%)': conversion
    })
    
    # Main results section
    st.header("Steady-State Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Reaction rate constant (k):** {k:.6f} L/(mol·min) at {temperature}°C")
        st.write(f"**Residence time (τ):** {residence_time:.2f} minutes")
        st.write(f"**Steady-state conversion:** {X_solution*100:.2f}%")
    
    with col2:
        st.write(f"**Exit NaOH concentration:** {exit_conc_naoh:.6f} mol/L")
        st.write(f"**Exit Ethyl Acetate concentration:** {exit_conc_ea:.6f} mol/L")
        st.write(f"**Exit Products concentration:** {exit_conc_products:.6f} mol/L")
    
    # Heat transfer analysis section
    st.subheader("Heat Transfer Analysis")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.write(f"**Heat of reaction:** {heat_of_reaction:.1f} J/mol")
        st.write(f"**Heat generation rate:** {heat_generation:.1f} J/min")
    
    with col4:
        st.write(f"**Heat transfer rate:** {heat_transfer:.1f} J/min")
        heat_balance = heat_generation - heat_transfer
        st.write(f"**Heat balance:** {heat_balance:.1f} J/min")
        
        if abs(heat_balance) < 100:
            st.success("Reactor is close to thermal equilibrium")
        elif heat_balance > 0:
            st.warning("Reactor is generating more heat than removing - temperature will rise")
        else:
            st.info("Reactor is removing more heat than generating - temperature will drop")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["CSTR Stability", "Conversion Analysis", "Residence Time Effect"])
    
    with tab1:
        # Stability plot
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        ax.plot(operating_time, conc_naoh, 'b-', label='NaOH Concentration')
        ax.axhline(y=exit_conc_naoh, color='r', linestyle='--', label='Steady-state Concentration')
        ax.set_xlabel('Time (minutes)')
        ax.set_ylabel('NaOH Concentration (mol/L)')
        ax.set_title('CSTR Stability - Response to Perturbation (NaOH Concentration in mol/L vs. Time in minutes)')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
        
        st.write("""
        The graph above shows the stability of the CSTR. A small perturbation in the concentration is 
        applied at the beginning, and the system returns to the steady-state value, demonstrating 
        that the CSTR is a self-regulating system.
        """)
    
    with tab2:
        # Conversion analysis
        # Calculate conversion for different residence times
        residence_times = np.linspace(0.1, residence_time*2, 100)
        conversions = []
        
        for rt in residence_times:
            if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
                # Equal initial concentrations
                X = rt * k * feed_conc_naoh / (1 + rt * k * feed_conc_naoh)
            else:
                # Different initial concentrations - simplified approach
                M = feed_conc_ea / feed_conc_naoh
                
                # Approximate solution
                if M > 1:
                    X = 1 - np.exp(-k * feed_conc_naoh * rt)
                else:
                    X = 1 - np.exp(-k * feed_conc_ea * rt)
            
            conversions.append(X * 100)  # Convert to percentage
        
        fig2, ax2 = plt.subplots(figsize=(10, 6), dpi=100)
        ax2.plot(residence_times, conversions, 'g-')
        ax2.axvline(x=residence_time, color='r', linestyle='--', label=f'Current τ = {residence_time:.2f} min')
        ax2.axhline(y=X_solution*100, color='b', linestyle='--', label=f'Current X = {X_solution*100:.2f}%')
        ax2.set_xlabel('Residence Time (minutes)')
        ax2.set_ylabel('Conversion (%)')
        ax2.set_title('Effect of Residence Time on Conversion')
        ax2.grid(True, alpha=0.3)
        ax2.legend(frameon=True, fancybox=True, shadow=True)
        fig2.tight_layout()
        st.pyplot(fig2)
    
    with tab3:
        # Residence time effect on exit concentrations
        exit_naoh = []
        exit_ea = []
        exit_prod = []
        
        for rt in residence_times:
            if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
                # Equal initial concentrations
                X = rt * k * feed_conc_naoh / (1 + rt * k * feed_conc_naoh)
            else:
                # Different initial concentrations - simplified approach
                M = feed_conc_ea / feed_conc_naoh
                
                # Approximate solution
                if M > 1:
                    X = 1 - np.exp(-k * feed_conc_naoh * rt)
                else:
                    X = 1 - np.exp(-k * feed_conc_ea * rt)
            
            exit_naoh.append(feed_conc_naoh * (1 - X))
            exit_ea.append(feed_conc_ea - feed_conc_naoh * X if feed_conc_ea > feed_conc_naoh * X else 0)
            exit_prod.append(feed_conc_naoh * X)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6), dpi=100)
        ax3.plot(residence_times, exit_naoh, 'b-', label='NaOH')
        ax3.plot(residence_times, exit_ea, 'r-', label='Ethyl Acetate')
        ax3.plot(residence_times, exit_prod, 'g-', label='Products')
        ax3.axvline(x=residence_time, color='k', linestyle='--', label=f'Current τ = {residence_time:.2f} min')
        ax3.set_xlabel('Residence Time (minutes)')
        ax3.set_ylabel('Exit Concentration (mol/L)')
        ax3.set_title('Effect of Residence Time on Exit Concentrations')
        ax3.grid(True, alpha=0.3)
        ax3.legend(frameon=True, fancybox=True, shadow=True)
        fig3.tight_layout()
        st.pyplot(fig3)
    
    # CSTR Schematic
    with st.expander("CSTR Schematic"):
        if cstr_type == "Jacket Heating":
            st.markdown("""
            ### CSTR with Jacket Heating
            
            ```
                 Feed
                  ↓
                ┌─────┐
                │     │
                │  R  │ ← Jacket Coolant In
                │     │
                └─────┘
                  ↓    → Jacket Coolant Out
                Product
            ```
            
            In jacket heating, a fluid circulates through a jacket surrounding the reactor. This provides heat transfer through the reactor wall.
            """)
        else:
            st.markdown("""
            ### CSTR with Coil Heating
            
            ```
                 Feed
                  ↓
                ┌─────┐
                │  ╭╮ │
                │  │  │ ← Coil Coolant In
                │  ╰╯ │
                └─────┘
                  ↓    → Coil Coolant Out
                Product
            ```
            
            In coil heating, a coiled tube runs through the reactor. The coolant flows through this tube, providing internal heat exchange.
            """)
        
        st.write("""
        #### CSTR Characteristics:
        - Well-mixed reactor - concentration is uniform throughout
        - Exit stream has same composition as reactor contents
        - Often used for liquid-phase reactions
        - Simple to operate and control
        - Can handle slurries and viscous materials
        - Lower conversion per unit volume compared to plug flow reactors
        """)
