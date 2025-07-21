import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def app():
    st.title("Experiment 4: Isothermal Plug Flow Reactor (PFR)")
    
    st.markdown("""
    ## Objective
    Study of a non-catalytic homogeneous reaction in a Plug Flow Reactor (PFR).
    
    ## Aim
    To determine the conversion profile and outlet concentrations for a given reaction in a PFR.
    
    ## Types of PFR
    1. Straight Tube PFR
    2. Coiled Tube PFR
    
    ## Chemical Reaction
    NaOH + CH₃COOC₂H₅ → CH₃COONa + C₂H₅OH
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        A Plug Flow Reactor (PFR) is a tubular reactor where reactants flow continuously through the tube. The key characteristics of a PFR are:
        
        1. No mixing in the axial direction (along the flow path)
        2. Complete mixing in the radial direction (perpendicular to flow)
        3. Uniform velocity profile across the radius
        4. Steady-state operation
        
        The material balance for a PFR at steady state is given by the differential equation:
        
        $$F_{A0} \\frac{dX}{dV} = -r_A$$
        
        Where:
        - $F_{A0}$ = molar feed rate of component A
        - $X$ = conversion of component A
        - $V$ = volume of the reactor
        - $r_A$ = rate of reaction of component A per unit volume
        
        In terms of space time ($\\tau$) or residence time, the equation can be written as:
        
        $$\\frac{dX}{d\\tau} = -r_A \\frac{1}{C_{A0}}$$
        
        For a second-order reaction $A + B \\rightarrow C + D$ with equal initial concentrations ($C_{A0} = C_{B0}$), the integrated form is:
        
        $$\\tau = \\frac{1}{k C_{A0}} \\ln \\left( \\frac{1}{1-X} \\right)$$
        
        For different initial concentrations, the integrated form is more complex.
        
        The PFR generally gives higher conversions than a CSTR of the same volume for reactions with positive orders. This is because the reaction rate decreases with increasing conversion, and in a PFR, the high initial rates are fully utilized.
        """)
    
    # Choose PFR type
    pfr_type = st.radio("Select PFR Type:", ["Straight Tube", "Coiled Tube"])
    
    # Input parameters
    st.sidebar.header("Reactor Parameters")
    
    # Feed parameters
    feed_flow_rate = st.sidebar.number_input("Feed flow rate (L/min)", 
                                          min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    
    feed_conc_naoh = st.sidebar.number_input("NaOH concentration in feed (mol/L)", 
                                           min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    
    feed_conc_ea = st.sidebar.number_input("Ethyl Acetate concentration in feed (mol/L)", 
                                         min_value=0.001, max_value=1.0, value=0.01, step=0.001, format="%.4f")
    
    # Reactor parameters
    if pfr_type == "Straight Tube":
        tube_diameter = st.sidebar.number_input("Tube diameter (cm)", 
                                             min_value=0.1, max_value=10.0, value=2.0, step=0.1)
        tube_length = st.sidebar.number_input("Tube length (m)", 
                                           min_value=0.1, max_value=20.0, value=5.0, step=0.1)
    else:  # Coiled Tube
        tube_diameter = st.sidebar.number_input("Tube diameter (cm)", 
                                             min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        tube_length = st.sidebar.number_input("Tube length (m)", 
                                           min_value=0.1, max_value=20.0, value=8.0, step=0.1)
        coil_diameter = st.sidebar.number_input("Coil diameter (cm)", 
                                             min_value=5.0, max_value=50.0, value=20.0, step=1.0)
        number_of_turns = st.sidebar.number_input("Number of turns", 
                                               min_value=1, max_value=50, value=10, step=1)
    
    temperature = st.sidebar.slider("Reaction Temperature (°C)", 25, 60, 35, 1)
    
    # Calculate reactor volume
    tube_radius = tube_diameter / 2 / 100  # convert cm to m
    tube_cross_area = np.pi * tube_radius**2  # m²
    reactor_volume = tube_cross_area * tube_length * 1000  # L
    
    # Calculate residence time
    residence_time = reactor_volume / feed_flow_rate  # minutes
    
    # Calculated parameters
    temp_kelvin = temperature + 273.15
    
    # Define rate constants for different temperatures (based on experimental data)
    k_ref = 0.11  # L/(mol·min) at 35°C
    E_R = 4500    # E/R value in Kelvin
    
    # Calculate rate constant using Arrhenius equation
    k = k_ref * np.exp(E_R * (1/308.15 - 1/temp_kelvin))  # 308.15 K = 35°C (reference temperature)
    
    # Additional calculations for coiled tube
    if pfr_type == "Coiled Tube":
        # Calculate Dean number for flow characterization
        density = 1000  # kg/m³ (water approximation)
        viscosity = 0.001  # Pa·s (water approximation)
        
        # Average velocity
        velocity = feed_flow_rate / (60 * tube_cross_area)  # m/s
        
        # Reynolds number
        reynolds = density * velocity * (tube_diameter/100) / viscosity
        
        # Dean number
        dean = reynolds * np.sqrt((tube_diameter/100) / (coil_diameter/100))
        
        # Correction factor for mass transfer in coiled tubes
        # Enhances mixing due to secondary flows
        if dean < 100:
            mixing_enhancement = 1.0
        else:
            mixing_enhancement = 1.0 + 0.1 * np.log10(dean/100)
        
        # Apply enhancement to rate constant
        k = k * mixing_enhancement
    
    # PFR model differential equation
    def pfr_ode(z, X):
        # z is the dimensionless length along the reactor
        # X is the conversion
        
        if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
            # Equal initial concentrations
            rate = k * feed_conc_naoh**2 * (1 - X)**2
        else:
            # Different initial concentrations
            M = feed_conc_ea / feed_conc_naoh  # ratio of initial concentrations
            
            if feed_conc_naoh <= feed_conc_ea:
                # NaOH is limiting
                rate = k * feed_conc_naoh * (1 - X) * (feed_conc_ea - feed_conc_naoh * X)
            else:
                # Ethyl acetate is limiting
                rate = k * (feed_conc_naoh - feed_conc_ea * X) * feed_conc_ea * (1 - X)
        
        # dX/dz = rate * V / (F_A0 * L)
        return rate * reactor_volume / (feed_conc_naoh * feed_flow_rate * tube_length)
    
    # Solve ODE to get conversion profile along the reactor length
    z_span = (0, 1)  # dimensionless length (0 to 1)
    z_eval = np.linspace(0, 1, 100)  # points to evaluate
    
    # Initial condition: zero conversion at inlet
    X0 = 0
    
    # Solve ODE
    solution = solve_ivp(pfr_ode, z_span, [X0], t_eval=z_eval, method='RK45')
    
    # Extract results
    z_points = solution.t
    conversion = solution.y[0]
    
    # Calculate actual length points
    length_points = z_points * tube_length
    
    # Calculate concentrations along the reactor
    if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
        # Equal initial concentrations
        conc_naoh = feed_conc_naoh * (1 - conversion)
        conc_ea = feed_conc_ea * (1 - conversion)
    else:
        # Different initial concentrations
        if feed_conc_naoh <= feed_conc_ea:
            # NaOH is limiting
            conc_naoh = feed_conc_naoh * (1 - conversion)
            conc_ea = feed_conc_ea - feed_conc_naoh * conversion
        else:
            # Ethyl acetate is limiting
            conc_naoh = feed_conc_naoh - feed_conc_ea * conversion
            conc_ea = feed_conc_ea * (1 - conversion)
    
    # Calculate product concentration
    if feed_conc_naoh <= feed_conc_ea:
        conc_products = feed_conc_naoh * conversion
    else:
        conc_products = feed_conc_ea * conversion
    
    # Calculate final conversion and outlet concentrations
    final_conversion = conversion[-1]
    outlet_conc_naoh = conc_naoh[-1]
    outlet_conc_ea = conc_ea[-1]
    outlet_conc_products = conc_products[-1]
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Length (m)': length_points,
        'Position (dimensionless)': z_points,
        'Conversion': conversion,
        'NaOH Concentration (mol/L)': conc_naoh,
        'Ethyl Acetate Concentration (mol/L)': conc_ea,
        'Products Concentration (mol/L)': conc_products
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Reaction rate constant (k):** {k:.6f} L/(mol·min) at {temperature}°C")
        st.write(f"**Reactor volume:** {reactor_volume:.2f} L")
        st.write(f"**Residence time (τ):** {residence_time:.2f} minutes")
    
    with col2:
        st.write(f"**Final conversion:** {final_conversion*100:.2f}%")
        
        if pfr_type == "Coiled Tube":
            st.write(f"**Dean number:** {dean:.1f}")
            st.write(f"**Mixing enhancement factor:** {mixing_enhancement:.2f}")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Concentration Profiles", "Conversion Profile", "Data Table"])
    
    with tab1:
        # Concentration profile plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(length_points, conc_naoh, 'b-', label='NaOH')
        ax.plot(length_points, conc_ea, 'r-', label='Ethyl Acetate')
        ax.plot(length_points, conc_products, 'g-', label='Products')
        ax.set_xlabel('Length (m)')
        ax.set_ylabel('Concentration (mol/L)')
        ax.set_title('Concentration Profiles Along the Reactor')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    
    with tab2:
        # Conversion profile plot
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(length_points, conversion * 100, 'b-')
        ax2.set_xlabel('Length (m)')
        ax2.set_ylabel('Conversion (%)')
        ax2.set_title('Conversion Profile Along the Reactor')
        ax2.grid(True)
        st.pyplot(fig2)
        
        # Reaction rate profile
        reaction_rates = []
        for i, X in enumerate(conversion):
            if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
                # Equal initial concentrations
                rate = k * feed_conc_naoh**2 * (1 - X)**2
            else:
                # Different initial concentrations
                if feed_conc_naoh <= feed_conc_ea:
                    # NaOH is limiting
                    rate = k * feed_conc_naoh * (1 - X) * (feed_conc_ea - feed_conc_naoh * X)
                else:
                    # Ethyl acetate is limiting
                    rate = k * (feed_conc_naoh - feed_conc_ea * X) * feed_conc_ea * (1 - X)
            reaction_rates.append(rate)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(length_points, reaction_rates, 'r-')
        ax3.set_xlabel('Length (m)')
        ax3.set_ylabel('Reaction Rate (mol/L·min)')
        ax3.set_title('Reaction Rate Profile Along the Reactor')
        ax3.grid(True)
        st.pyplot(fig3)
    
    with tab3:
        # Display data table with selected points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(length_points)-1, 10).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "pfr_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Comparison with CSTR
    with st.expander("PFR vs CSTR Comparison"):
        st.write("### Comparison of PFR with CSTR of the Same Volume")
        
        # Calculate CSTR conversion for the same volume
        if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
            # Equal initial concentrations in CSTR
            X_cstr = residence_time * k * feed_conc_naoh / (1 + residence_time * k * feed_conc_naoh)
        else:
            # Different initial concentrations in CSTR - simplified approach
            M = feed_conc_ea / feed_conc_naoh
            
            # Approximate solution
            if M > 1:
                X_cstr = 1 - np.exp(-k * feed_conc_naoh * residence_time)
            else:
                X_cstr = 1 - np.exp(-k * feed_conc_ea * residence_time)
        
        st.write(f"PFR Final Conversion: {final_conversion*100:.2f}%")
        st.write(f"CSTR Conversion (same volume): {X_cstr*100:.2f}%")
        st.write(f"Efficiency Improvement: {(final_conversion - X_cstr) / X_cstr * 100:.2f}%")
        
        # Plot conversion comparison for different residence times
        residence_times = np.linspace(0.1, residence_time*2, 50)
        pfr_conversions = []
        cstr_conversions = []
        
        for rt in residence_times:
            # Simple approximation for educational purposes
            if abs(feed_conc_naoh - feed_conc_ea) < 1e-6:
                # Equal initial concentrations
                X_cstr_rt = rt * k * feed_conc_naoh / (1 + rt * k * feed_conc_naoh)
                X_pfr_rt = 1 - np.exp(-k * feed_conc_naoh * rt)
            else:
                # Different initial concentrations - simplified
                if feed_conc_naoh <= feed_conc_ea:
                    X_cstr_rt = rt * k * feed_conc_naoh / (1 + rt * k * feed_conc_naoh)
                    X_pfr_rt = 1 - np.exp(-k * feed_conc_naoh * rt)
                else:
                    X_cstr_rt = rt * k * feed_conc_ea / (1 + rt * k * feed_conc_ea)
                    X_pfr_rt = 1 - np.exp(-k * feed_conc_ea * rt)
            
            pfr_conversions.append(X_pfr_rt * 100)
            cstr_conversions.append(X_cstr_rt * 100)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(residence_times, pfr_conversions, 'b-', label='PFR')
        ax4.plot(residence_times, cstr_conversions, 'r-', label='CSTR')
        ax4.axvline(x=residence_time, color='k', linestyle='--', 
                   label=f'Current τ = {residence_time:.2f} min')
        ax4.set_xlabel('Residence Time (minutes)')
        ax4.set_ylabel('Conversion (%)')
        ax4.set_title('PFR vs CSTR Conversion Comparison')
        ax4.grid(True)
        ax4.legend()
        st.pyplot(fig4)
        
        st.write("""
        ### Key Differences Between PFR and CSTR:
        
        1. **Conversion Efficiency**: 
           - PFR generally gives higher conversion than CSTR of the same volume
           - This advantage increases with reaction order
           
        2. **Flow Pattern**: 
           - PFR has no axial mixing (plug flow)
           - CSTR has complete mixing throughout
           
        3. **Concentration Profile**:
           - In PFR, concentration changes continuously along the length
           - In CSTR, concentration is uniform and equal to the exit concentration
           
        4. **Temperature Control**:
           - PFR may have hot spots due to exothermic reactions
           - CSTR dilutes heat generation and is easier to control thermally
           
        5. **Applications**:
           - PFR is preferred for high conversion reactions with positive orders
           - CSTR is better for liquid phase reactions, highly exothermic reactions
        """)
    
    # PFR Schematic
    with st.expander("PFR Schematic"):
        if pfr_type == "Straight Tube":
            st.markdown("""
            ### Straight Tube PFR
            
            ```
            Feed → ═════════════════════════════════════════════ → Product
            ```
            
            In a straight tube PFR, reactants flow through a straight tubular reactor with no mixing in the axial direction.
            """)
        else:
            st.markdown("""
            ### Coiled Tube PFR
            
            ```
            Feed → ╭───────────╮
                   │           │
                   │           │
                   │           │
                   ╰───────────╯ → Product
            ```
            
            In a coiled tube PFR, the tube is wound into a coil. This creates secondary flow patterns (Dean vortices) 
            that enhance radial mixing while maintaining the plug flow characteristics.
            """)
        
        st.write("""
        #### PFR Characteristics:
        - No axial mixing (no back-mixing)
        - Complete radial mixing
        - Uniform velocity profile (ideally)
        - Higher conversion per unit volume compared to CSTR
        - More difficult to control thermally (potential hot spots)
        - Often used for gas-phase reactions
        """)
