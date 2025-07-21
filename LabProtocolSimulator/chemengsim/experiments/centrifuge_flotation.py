import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import set_plot_style
from scipy.optimize import curve_fit

# Set consistent style for plots
set_plot_style()

def app():
    st.title("Experiment 8: Centrifuge and Flotation")
    
    # Selection menu for centrifuge or flotation
    experiment_type = st.radio("Select Experiment Type:", ["Basket Centrifuge", "Froth Flotation Cell"])
    
    if experiment_type == "Basket Centrifuge":
        centrifuge_app()
    else:
        flotation_app()

def centrifuge_app():
    st.header("Basket Centrifuge")
    
    st.markdown("""
    ## Objective
    Study of solid-liquid separation using a basket centrifuge.
    
    ## Aim
    To determine the separation efficiency, cake moisture content, and performance characteristics of a basket centrifuge.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Centrifugation Theory
        
        Centrifugation is a mechanical separation process that uses centrifugal force to separate components of a mixture based on their density differences. The centrifugal force generated is much greater than gravity, accelerating the separation process.
        
        The basic equation relating centrifugal force to gravitational force is:
        
        $$\\frac{F_{centrifugal}}{F_{gravitational}} = \\frac{\\omega^2 r}{g}$$
        
        Where:
        - $\\omega$ = angular velocity (rad/s)
        - $r$ = radius of rotation (m)
        - $g$ = gravitational acceleration (9.81 m/s²)
        
        This ratio is known as the relative centrifugal force (RCF) or "g-force".
        
        For sedimentation or filtration in a centrifuge, Stokes' Law can be modified for centrifugal fields:
        
        $$v = \\frac{d^2(\\rho_p - \\rho_f)\\omega^2 r}{18\\mu}$$
        
        Where:
        - $v$ = particle velocity (m/s)
        - $d$ = particle diameter (m)
        - $\\rho_p$ = particle density (kg/m³)
        - $\\rho_f$ = fluid density (kg/m³)
        - $\\mu$ = fluid viscosity (Pa·s)
        
        ### Basket Centrifuge
        
        A basket centrifuge consists of a perforated cylindrical basket lined with a filter medium. The basket rotates at high speed, creating a centrifugal force that drives the liquid through the filter medium while the solids form a cake on the inside of the basket.
        
        The operation cycle typically includes:
        1. **Loading**: The slurry is fed into the rotating basket
        2. **Spinning**: Centrifugal force drives liquid through the filter medium
        3. **Washing** (optional): Wash liquid is added to displace impurities
        4. **Drying**: Continued spinning removes residual liquid
        5. **Unloading**: The cake is discharged, often by stopping the centrifuge
        
        Key performance parameters include:
        - Cake moisture content
        - Filtration rate
        - Cake thickness
        - Cake density
        - Separation efficiency
        """)
    
    # Input parameters
    st.sidebar.header("Centrifuge Parameters")
    
    # Operational parameters
    basket_diameter = st.sidebar.slider("Basket diameter (m)", 0.3, 2.0, 0.8, 0.1)
    
    basket_height = st.sidebar.slider("Basket height (m)", 0.2, 1.0, 0.5, 0.05)
    
    rotation_speed = st.sidebar.slider("Rotation speed (rpm)", 500, 3000, 1200, 100)
    
    # Slurry properties
    solid_density = st.sidebar.slider("Solid density (kg/m³)", 1200, 5000, 2500, 100)
    
    liquid_density = st.sidebar.slider("Liquid density (kg/m³)", 800, 1200, 1000, 50)
    
    slurry_concentration = st.sidebar.slider("Slurry concentration (wt%)", 5, 40, 20, 1)
    
    particle_size = st.sidebar.slider("Average particle size (μm)", 1, 1000, 100, 10)
    
    liquid_viscosity = st.sidebar.number_input("Liquid viscosity (Pa·s)", 
                                            min_value=0.0005, max_value=0.05, value=0.001, step=0.0001, format="%.4f")
    
    # Operational cycle parameters
    feeding_time = st.sidebar.slider("Feeding time (s)", 30, 300, 120, 10)
    
    spinning_time = st.sidebar.slider("Spinning time (s)", 60, 600, 300, 30)
    
    # Calculate parameters
    # Convert rpm to rad/s
    omega = rotation_speed * 2 * np.pi / 60  # rad/s
    
    # Calculate basket volume and area
    basket_radius = basket_diameter / 2
    basket_volume = np.pi * basket_radius**2 * basket_height  # m³
    basket_area = 2 * np.pi * basket_radius * basket_height  # m² (side area only)
    
    # Calculate relative centrifugal force (RCF) or "g-force"
    rcf = omega**2 * basket_radius / 9.81
    
    # Calculate particle settling velocity using modified Stokes' Law
    particle_diameter = particle_size * 1e-6  # convert μm to m
    settling_velocity = (particle_diameter**2 * (solid_density - liquid_density) * omega**2 * basket_radius) / (18 * liquid_viscosity)  # m/s
    
    # Estimate cake properties
    # Convert slurry concentration from wt% to volume fraction
    volume_fraction = (slurry_concentration / 100) / ((slurry_concentration / 100) + ((100 - slurry_concentration) / 100) * (solid_density / liquid_density))
    
    # Maximum cake thickness (assuming all solids in slurry form the cake)
    total_slurry_volume = basket_volume * 0.8  # 80% fill
    solids_volume = total_slurry_volume * volume_fraction
    
    # Cake porosity decreases with spinning time and RCF
    initial_porosity = 0.6
    final_porosity = 0.3 - 0.1 * (rcf / 1000)  # Higher RCF leads to lower final porosity
    final_porosity = max(0.1, min(0.5, final_porosity))  # Keep within reasonable bounds
    
    # Cake volume with porosity
    cake_volume = solids_volume / (1 - final_porosity)
    cake_thickness = cake_volume / basket_area  # m
    
    # Calculate moisture content
    # Moisture content decreases with spinning time
    initial_moisture = 0.8
    final_moisture = 0.2 + 0.2 * np.exp(-spinning_time / 200)  # Exponential decrease with spinning time
    final_moisture = max(0.05, min(0.5, final_moisture))  # Keep within reasonable bounds
    
    # Simulate the centrifugation process
    # Time points
    time_points = np.linspace(0, feeding_time + spinning_time, 100)
    
    # Initialize arrays
    cake_thickness_arr = np.zeros_like(time_points)
    moisture_content = np.ones_like(time_points) * initial_moisture
    filtrate_volume = np.zeros_like(time_points)
    
    for i, t in enumerate(time_points):
        if t <= feeding_time:
            # During feeding, cake thickness increases linearly
            cake_thickness_arr[i] = (t / feeding_time) * cake_thickness
            
            # During feeding, moisture content stays high
            moisture_content[i] = initial_moisture - (initial_moisture - final_moisture) * 0.1 * (t / feeding_time)
            
            # Filtrate volume increases with cake formation
            filtrate_volume[i] = total_slurry_volume * (t / feeding_time) * (1 - volume_fraction)
            
        else:
            # After feeding, cake thickness is constant
            cake_thickness_arr[i] = cake_thickness
            
            # Moisture content decreases during spinning
            spin_t = t - feeding_time
            moisture_content[i] = initial_moisture - (initial_moisture - final_moisture) * (1 - np.exp(-spin_t / (spinning_time / 3)))
            
            # Additional filtrate from cake dewatering
            cake_volume_water_initial = cake_volume * initial_porosity
            cake_volume_water_current = cake_volume * moisture_content[i] / (1 - moisture_content[i])
            additional_filtrate = cake_volume_water_initial - cake_volume_water_current
            
            filtrate_volume[i] = total_slurry_volume * (1 - volume_fraction) + additional_filtrate
    
    # Convert units for display
    cake_thickness_mm = cake_thickness_arr * 1000  # mm
    
    # Calculate filtration rate
    filtration_rate = np.zeros_like(time_points)
    for i in range(1, len(time_points)):
        dt = time_points[i] - time_points[i-1]
        dv = filtrate_volume[i] - filtrate_volume[i-1]
        if dt > 0:
            filtration_rate[i] = dv / dt
    
    # Calculate yields and efficiencies
    total_solids_in = total_slurry_volume * volume_fraction * solid_density
    solids_in_cake = total_solids_in  # Assume all solids are captured
    solids_recovery = 100.0  # Percentage
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (s)': time_points,
        'Cake Thickness (mm)': cake_thickness_mm,
        'Moisture Content (fraction)': moisture_content,
        'Filtrate Volume (m³)': filtrate_volume,
        'Filtration Rate (m³/s)': filtration_rate
    })
    
    # Add process stage
    df['Stage'] = 'Spinning'
    df.loc[df['Time (s)'] <= feeding_time, 'Stage'] = 'Feeding'
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Relative centrifugal force (RCF):** {rcf:.1f} g")
        st.write(f"**Basket surface area:** {basket_area:.3f} m²")
        st.write(f"**Particle settling velocity:** {settling_velocity:.5f} m/s")
        st.write(f"**Final cake thickness:** {cake_thickness*1000:.2f} mm")
    
    with col2:
        st.write(f"**Final moisture content:** {final_moisture*100:.1f}%")
        st.write(f"**Final cake porosity:** {final_porosity*100:.1f}%")
        st.write(f"**Total filtrate volume:** {filtrate_volume[-1]*1000:.1f} L")
        st.write(f"**Solids recovery:** {solids_recovery:.1f}%")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Process Performance", "Moisture & Filtration", "Data Table"])
    
    with tab1:
        # Process performance visualization
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        # Plot cake thickness
        ax.plot(time_points, cake_thickness_mm, 'b-', label='Cake Thickness (mm)')
        
        # Add vertical line at feeding time
        ax.axvline(x=feeding_time, color='r', linestyle='--', label=f'End of Feeding ({feeding_time} s)')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Cake Thickness (mm)')
        ax.set_title('Cake Formation in Basket Centrifuge')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
        
        # RCF effect visualization
        speeds = np.linspace(500, 3000, 6)
        final_moistures = []
        
        for speed in speeds:
            omega_test = speed * 2 * np.pi / 60
            rcf_test = omega_test**2 * basket_radius / 9.81
            moisture = 0.2 + 0.2 * np.exp(-spinning_time / 200) - 0.05 * (rcf_test / 1000)
            moisture = max(0.05, min(0.5, moisture))
            final_moistures.append(moisture * 100)  # Percentage
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(speeds, final_moistures, 'g-o')
        ax2.axvline(x=rotation_speed, color='r', linestyle='--', 
                   label=f'Current Speed: {rotation_speed} rpm')
        
        ax2.set_xlabel('Rotation Speed (rpm)')
        ax2.set_ylabel('Final Moisture Content (%)')
        ax2.set_title('Effect of Rotation Speed on Moisture Content')
        ax2.grid(True)
        ax2.legend()
        fig.tight_layout()
        st.pyplot(fig2)
    
    with tab2:
        # Moisture content and filtration rate
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        # Plot moisture content
        ax3.plot(time_points, moisture_content * 100, 'b-', label='Moisture Content (%)')
        
        # Add vertical line at feeding time
        ax3.axvline(x=feeding_time, color='r', linestyle='--', label=f'End of Feeding ({feeding_time} s)')
        
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Moisture Content (%)')
        ax3.set_title('Moisture Content vs Time')
        ax3.grid(True)
        ax3.legend()
        fig.tight_layout()
        st.pyplot(fig3)
        
        # Filtration rate
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(time_points, filtration_rate * 1000, 'g-', label='Filtration Rate (L/s)')
        
        # Add vertical line at feeding time
        ax4.axvline(x=feeding_time, color='r', linestyle='--', label=f'End of Feeding ({feeding_time} s)')
        
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Filtration Rate (L/s)')
        ax4.set_title('Filtration Rate vs Time')
        ax4.grid(True)
        ax4.legend()
        fig.tight_layout()
        st.pyplot(fig4)
    
    with tab3:
        # Display data table with selected points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(df)-1, 20).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "basket_centrifuge_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Basket centrifuge schematic
    with st.expander("Basket Centrifuge Schematic"):
        st.markdown("""
        ### Basket Centrifuge Schematic
        
        ```
                    Feed Pipe
                        ↓
                    ┌─────┐
                    │  ↓  │
               ┌────┴─────┴────┐
               │    Motor      │
               │      ↓        │
               │  ┌───────┐    │
               │  │       │    │
               │  │       │    │
               │  │       │    │
               │  └───────┘    │
               │  Rotating     │
               │   Basket      │
               └───────────────┘
                      ↓
                   Filtrate
        ```
        
        ### Key Components:
        
        - **Feed Pipe**: Delivers slurry to the rotating basket
        - **Rotating Basket**: Perforated cylinder lined with filter medium
        - **Drive Motor**: Rotates the basket at high speed
        - **Housing**: Contains the rotating parts and collects the filtrate
        
        ### Operation Cycle:
        
        1. **Feeding**: Slurry is introduced into the spinning basket
        2. **Spinning**: Centrifugal force drives liquid through the filter medium
        3. **Washing** (optional): Wash liquid is added to displace impurities
        4. **Dewatering**: Continued spinning to reduce cake moisture
        5. **Discharge**: Cake is removed, often by stopping the centrifuge
        
        ### Advantages:
        
        - High centrifugal forces enable efficient separation
        - Capable of producing drier cakes than conventional filters
        - Can process fine particles
        - Suitable for washing operations
        """)

def flotation_app():
    st.header("Froth Flotation Cell")
    
    st.markdown("""
    ## Objective
    Study of mineral separation using a froth flotation cell.
    
    ## Aim
    To determine the recovery and grade of valuable minerals using froth flotation.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Froth Flotation Theory
        
        Froth flotation is a physicochemical separation process that exploits differences in the surface properties of minerals. Hydrophobic (water-repelling) particles attach to air bubbles and rise to the surface, forming a mineral-rich froth that is collected, while hydrophilic (water-loving) particles remain in the pulp.
        
        The process involves several key steps:
        
        1. **Conditioning**: Reagents are added to modify mineral surface properties
        2. **Aeration**: Air is introduced to create bubbles
        3. **Bubble-particle attachment**: Hydrophobic particles attach to air bubbles
        4. **Froth formation and collection**: Mineral-laden bubbles form a froth that is collected
        
        The key reagents used in flotation include:
        
        - **Collectors**: Make mineral surfaces hydrophobic
        - **Frothers**: Stabilize air bubbles
        - **Modifiers**: Enhance selectivity (activators, depressants, pH regulators)
        
        The performance of a flotation process is typically characterized by:
        
        - **Recovery**: Percentage of the valuable mineral recovered in the concentrate
            $$Recovery = \\frac{c \\times m_c}{f \\times m_f} \\times 100\\%$$
        
        - **Grade**: Concentration of the valuable mineral in the concentrate
            $$Grade = c \\times 100\\%$$
        
        Where:
        - $c$ = concentration of valuable mineral in concentrate
        - $m_c$ = mass of concentrate
        - $f$ = concentration of valuable mineral in feed
        - $m_f$ = mass of feed
        
        The relationship between recovery and grade often involves a trade-off; higher recoveries typically come at the expense of lower grades, and vice versa.
        """)
    
    # Input parameters
    st.sidebar.header("Flotation Parameters")
    
    # Feed properties
    feed_rate = st.sidebar.slider("Feed rate (kg/h)", 10, 1000, 200, 10)
    
    feed_grade = st.sidebar.slider("Feed grade (% valuable mineral)", 0.5, 20.0, 5.0, 0.5)
    
    pulp_density = st.sidebar.slider("Pulp density (% solids by weight)", 20, 40, 30, 1)
    
    particle_size = st.sidebar.slider("Average particle size (μm)", 10, 200, 75, 5)
    
    # Flotation cell parameters
    cell_volume = st.sidebar.slider("Flotation cell volume (m³)", 0.1, 10.0, 2.0, 0.1)
    
    aeration_rate = st.sidebar.slider("Aeration rate (m³/min)", 0.1, 5.0, 1.0, 0.1)
    
    impeller_speed = st.sidebar.slider("Impeller speed (rpm)", 200, 1200, 600, 50)
    
    # Reagent parameters
    collector_dosage = st.sidebar.slider("Collector dosage (g/ton)", 10, 500, 100, 10)
    
    frother_dosage = st.sidebar.slider("Frother dosage (g/ton)", 10, 200, 50, 5)
    
    # Flotation time
    flotation_time = st.sidebar.slider("Flotation time (min)", 1, 30, 10, 1)
    
    # Calculate parameters
    # Calculate pulp volume
    pulp_volume = cell_volume * 0.8  # 80% of cell volume
    
    # Calculate solids mass in the cell
    solids_density = 2700  # kg/m³ (typical for many minerals)
    water_density = 1000  # kg/m³
    
    # Calculate mass of solids in the pulp
    pulp_density_frac = pulp_density / 100
    pulp_mass = pulp_volume * ((pulp_density_frac * solids_density) + ((1 - pulp_density_frac) * water_density))
    solids_mass = pulp_mass * pulp_density_frac
    
    # Calculate residence time
    residence_time = solids_mass / feed_rate  # h
    residence_time_min = residence_time * 60  # min
    
    # Calculate recovery model parameters
    # Use a first-order kinetic model: R = R_max * (1 - exp(-k*t))
    # Where R is recovery, R_max is maximum possible recovery, k is rate constant, t is time
    
    # Model parameters dependent on operational variables
    k_base = 0.2  # Base rate constant (min^-1)
    
    # Influence of particle size on rate constant
    # Finer particles typically float faster up to a point, then very fine particles may be slower
    size_factor = np.exp(-(particle_size - 75)**2 / 2500)
    
    # Influence of reagent dosages
    collector_factor = 0.5 + 0.5 * np.tanh((collector_dosage - 50) / 100)
    frother_factor = 0.5 + 0.5 * np.tanh((frother_dosage - 25) / 50)
    
    # Influence of aeration and impeller speed
    aeration_factor = 0.5 + 0.5 * np.tanh((aeration_rate - 0.5) / 1)
    impeller_factor = 0.5 + 0.5 * np.tanh((impeller_speed - 400) / 400)
    
    # Combined rate constant
    k = k_base * size_factor * collector_factor * frother_factor * aeration_factor * impeller_factor
    
    # Maximum possible recovery (dependent on mineral liberation, etc.)
    R_max = 95  # Maximum recovery percentage
    
    # Simulate the flotation process
    # Time points
    time_points = np.linspace(0, flotation_time, 100)
    
    # Calculate recovery at each time point
    recovery = R_max * (1 - np.exp(-k * time_points))
    
    # Calculate concentrate grade
    # In reality, grade would depend on many factors, but we'll use a simplified model
    # Grade typically decreases with increasing recovery
    initial_grade_factor = 5  # Initial enrichment ratio
    
    # Maximum theoretical grade (assuming perfect separation)
    max_grade = 100  # Assuming pure mineral can be achieved theoretically
    
    # Calculate grade at each time point
    # Use a model where grade decreases with increasing recovery
    # Grade = (max_grade * recovery/100) / (recovery/100 + (100-recovery)/100 * feed_grade/100 * initial_grade_factor)
    grade = max_grade * feed_grade / (feed_grade + (100 - recovery) * (max_grade - feed_grade) / 100)
    
    # Calculate mass of concentrate
    # From the recovery formula: Recovery = (c * mc) / (f * mf) * 100%
    # Where c is concentrate grade (fraction), mc is concentrate mass
    # f is feed grade (fraction), mf is feed mass
    # For mass balance: mc = (Recovery * f * mf) / (c * 100)
    feed_grade_frac = feed_grade / 100
    
    concentrate_mass = np.zeros_like(time_points)
    for i, (r, g) in enumerate(zip(recovery, grade)):
        if g > 0:
            concentrate_mass[i] = (r * feed_grade_frac * feed_rate * time_points[i] / 60) / (g / 100)
    
    # Calculate tailing grade
    # Mass balance: f * mf = c * mc + t * mt
    # Where t is tailing grade, mt is tailing mass
    # mt = mf - mc
    feed_mass = feed_rate * time_points / 60  # kg
    tailing_mass = feed_mass - concentrate_mass
    
    tailing_grade = np.zeros_like(time_points)
    for i, (fm, cm, tm) in enumerate(zip(feed_mass, concentrate_mass, tailing_mass)):
        if tm > 0:
            tailing_grade[i] = ((feed_grade_frac * fm) - (grade[i] / 100 * cm)) / tm * 100
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (min)': time_points,
        'Recovery (%)': recovery,
        'Concentrate Grade (%)': grade,
        'Tailing Grade (%)': tailing_grade,
        'Concentrate Mass (kg)': concentrate_mass,
        'Tailing Mass (kg)': tailing_mass
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Flotation rate constant (k):** {k:.4f} min⁻¹")
        st.write(f"**Cell residence time:** {residence_time_min:.2f} min")
        st.write(f"**Maximum possible recovery:** {R_max:.1f}%")
        st.write(f"**Final recovery (at {flotation_time} min):** {recovery[-1]:.2f}%")
    
    with col2:
        st.write(f"**Feed grade:** {feed_grade:.2f}%")
        st.write(f"**Final concentrate grade:** {grade[-1]:.2f}%")
        st.write(f"**Final tailing grade:** {tailing_grade[-1]:.2f}%")
        st.write(f"**Enrichment ratio:** {grade[-1]/feed_grade:.2f}")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Recovery & Grade", "Kinetics", "Data Table"])
    
    with tab1:
        # Recovery and grade visualization
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        # Plot recovery and grade
        ax.plot(time_points, recovery, 'b-', label='Recovery (%)')
        ax.plot(time_points, grade, 'r-', label='Concentrate Grade (%)')
        
        ax.set_xlabel('Flotation Time (min)')
        ax.set_ylabel('Percentage (%)')
        ax.set_title('Recovery and Grade vs Flotation Time')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
        
        # Recovery-grade relationship
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(recovery, grade, 'g-')
        
        # Mark the final point
        ax2.plot(recovery[-1], grade[-1], 'ro', label=f'Final Point ({recovery[-1]:.1f}%, {grade[-1]:.1f}%)')
        
        ax2.set_xlabel('Recovery (%)')
        ax2.set_ylabel('Concentrate Grade (%)')
        ax2.set_title('Grade-Recovery Curve')
        ax2.grid(True)
        ax2.legend()
        fig.tight_layout()
        st.pyplot(fig2)
    
    with tab2:
        # Flotation kinetics visualization
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        # Plot experimental data
        ax3.plot(time_points, recovery, 'bo', label='Simulated Data')
        
        # Plot model fit
        model_time = np.linspace(0, flotation_time * 1.5, 100)
        model_recovery = R_max * (1 - np.exp(-k * model_time))
        ax3.plot(model_time, model_recovery, 'r-', label=f'Model: R = {R_max:.1f}*(1-exp(-{k:.3f}*t))')
        
        ax3.set_xlabel('Flotation Time (min)')
        ax3.set_ylabel('Recovery (%)')
        ax3.set_title('Flotation Kinetics')
        ax3.grid(True)
        ax3.legend()
        fig.tight_layout()
        st.pyplot(fig3)
        
        # Parameter sensitivity analysis
        st.write("### Parameter Sensitivity Analysis")
        
        # Calculate recovery at fixed time for different parameters
        fixed_time = flotation_time
        
        # Collector dosage effect
        collector_range = np.linspace(10, 300, 10)
        recovery_collector = []
        
        for dosage in collector_range:
            coll_factor = 0.5 + 0.5 * np.tanh((dosage - 50) / 100)
            k_test = k_base * size_factor * coll_factor * frother_factor * aeration_factor * impeller_factor
            rec = R_max * (1 - np.exp(-k_test * fixed_time))
            recovery_collector.append(rec)
        
        # Frother dosage effect
        frother_range = np.linspace(10, 150, 10)
        recovery_frother = []
        
        for dosage in frother_range:
            fro_factor = 0.5 + 0.5 * np.tanh((dosage - 25) / 50)
            k_test = k_base * size_factor * collector_factor * fro_factor * aeration_factor * impeller_factor
            rec = R_max * (1 - np.exp(-k_test * fixed_time))
            recovery_frother.append(rec)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig4, ax4 = plt.subplots(figsize=(8, 5))
            ax4.plot(collector_range, recovery_collector, 'g-o')
            ax4.axvline(x=collector_dosage, color='r', linestyle='--', 
                        label=f'Current: {collector_dosage} g/ton')
            
            ax4.set_xlabel('Collector Dosage (g/ton)')
            ax4.set_ylabel(f'Recovery at {fixed_time} min (%)')
            ax4.set_title('Effect of Collector Dosage on Recovery')
            ax4.grid(True)
            ax4.legend()
            fig.tight_layout()
        st.pyplot(fig4)
        
        with col2:
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            ax5.plot(frother_range, recovery_frother, 'b-o')
            ax5.axvline(x=frother_dosage, color='r', linestyle='--', 
                        label=f'Current: {frother_dosage} g/ton')
            
            ax5.set_xlabel('Frother Dosage (g/ton)')
            ax5.set_ylabel(f'Recovery at {fixed_time} min (%)')
            ax5.set_title('Effect of Frother Dosage on Recovery')
            ax5.grid(True)
            ax5.legend()
            fig.tight_layout()
        st.pyplot(fig5)
    
    with tab3:
        # Display data table with selected points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(df)-1, 20).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "froth_flotation_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Froth flotation schematic
    with st.expander("Froth Flotation Schematic"):
        st.markdown("""
        ### Froth Flotation Cell Schematic
        
        ```
                Froth Collection
                      ↑
             ┌────────┴────────┐
             │     Froth       │
             │ ┌────────────┐  │
             │ │            │  │
             │ │    Pulp    │  │ ← Feed
             │ │            │  │
             │ └────────────┘  │
             │       ↑↑↑       │
             │      ┌┴─┴┐      │
             └──────┤   ├──────┘
                    └───┘
                  Impeller     → Tailings
                     ↑
                     Air
        ```
        
        ### Key Components:
        
        - **Feed Entry**: Where the conditioned pulp enters the cell
        - **Impeller**: Creates turbulence and disperses air bubbles
        - **Air Injection**: Provides air bubbles for mineral attachment
        - **Froth Zone**: Where mineral-laden bubbles collect
        - **Froth Overflow**: Where concentrate is collected
        - **Pulp Zone**: Where bubble-particle attachment occurs
        - **Tailings Discharge**: Where gangue minerals exit
        
        ### Flotation Process:
        
        1. **Conditioning**: Reagents modify mineral surface properties
        2. **Aeration**: Air bubbles are created and dispersed
        3. **Collection**: Hydrophobic minerals attach to air bubbles
        4. **Separation**: Mineral-laden bubbles rise to form froth
        5. **Recovery**: Froth overflows as concentrate
        
        ### Advantages:
        
        - Effective for separating fine particles
        - Can achieve high selectivity with proper reagents
        - Applicable to many mineral systems
        - Economical for processing low-grade ores
        """)
