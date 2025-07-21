import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def app():
    st.title("Experiment 6: Plate and Frame Filter Press")
    
    st.markdown("""
    ## Objective
    Study of solid-liquid separation using a plate and frame filter press.
    
    ## Aim
    To determine the filtration characteristics, including specific cake resistance and filter medium resistance.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Filtration Theory
        
        Filtration is a process of separating solids from liquids by passing the suspension through a porous medium that retains the solids and allows the liquid (filtrate) to pass through.
        
        The basic equation governing constant pressure filtration is:
        
        $$\\frac{t}{V} = \\frac{\\mu \\alpha c}{2A^2 \\Delta P}V + \\frac{\\mu R_m}{A \\Delta P}$$
        
        Where:
        - $t$ = filtration time (s)
        - $V$ = filtrate volume (m³)
        - $\\mu$ = filtrate viscosity (Pa·s)
        - $\\alpha$ = specific cake resistance (m/kg)
        - $c$ = mass of dry cake per unit volume of filtrate (kg/m³)
        - $A$ = filter area (m²)
        - $\\Delta P$ = pressure drop across filter (Pa)
        - $R_m$ = filter medium resistance (1/m)
        
        For constant pressure filtration, a plot of $t/V$ versus $V$ should be a straight line with:
        - Slope = $\\frac{\\mu \\alpha c}{2A^2 \\Delta P}$
        - Intercept = $\\frac{\\mu R_m}{A \\Delta P}$
        
        From these, we can calculate:
        - Specific cake resistance $\\alpha$
        - Filter medium resistance $R_m$
        
        ### Plate and Frame Filter Press
        
        A plate and frame filter press consists of alternating plates and frames assembled together. The suspension is pumped into the frames, and the filtrate passes through the filter cloth on the plates and out through drain ports. The cake builds up in the frames.
        
        Key components:
        - Filter plates (with drainage surfaces)
        - Frames (provide space for cake formation)
        - Filter cloth (the actual filter medium)
        - End plates and closing mechanism (to hold assembly together)
        """)
    
    # Input parameters
    st.sidebar.header("Filtration Parameters")
    
    # Operational parameters
    filtration_pressure = st.sidebar.slider("Filtration pressure (kPa)", 100, 700, 300, 50)
    
    slurry_concentration = st.sidebar.slider("Slurry concentration (kg/m³)", 50, 500, 200, 10)
    
    filter_area = st.sidebar.number_input("Total filter area (m²)", 
                                       min_value=0.05, max_value=10.0, value=1.0, step=0.1)
    
    # Slurry properties
    filtrate_viscosity = st.sidebar.number_input("Filtrate viscosity (Pa·s)", 
                                              min_value=0.0005, max_value=0.05, value=0.001, step=0.0001, format="%.4f")
    
    # Filter press parameters
    num_plates = st.sidebar.slider("Number of plates", 5, 50, 20, 1)
    
    frame_thickness = st.sidebar.slider("Frame thickness (mm)", 10, 50, 25, 5)
    
    # Calculated total frame volume
    frame_area = filter_area / num_plates  # m²
    frame_volume = frame_area * (frame_thickness / 1000)  # m³
    total_frame_volume = frame_volume * num_plates  # m³
    
    # Assumed or calculated parameters
    specific_cake_resistance = 1e11 * (filtration_pressure / 300)**0.5  # m/kg, pressure dependent
    medium_resistance = 1e10  # 1/m
    
    # Generate filtration data
    max_time = 3600  # seconds, 1 hour maximum filtration time
    time_points = np.linspace(0, max_time, 100)
    
    # Constants for the filtration equation
    k1 = (filtrate_viscosity * specific_cake_resistance * slurry_concentration) / (2 * filter_area**2 * (filtration_pressure * 1000))
    k2 = (filtrate_viscosity * medium_resistance) / (filter_area * (filtration_pressure * 1000))
    
    # Calculate filtrate volume using quadratic formula
    # t = k1*V² + k2*V
    # V = (-k2 + sqrt(k2² + 4*k1*t)) / (2*k1)
    filtrate_volumes = np.zeros_like(time_points)
    
    for i, t in enumerate(time_points):
        if t > 0:
            filtrate_volumes[i] = (-k2 + np.sqrt(k2**2 + 4*k1*t)) / (2*k1)
    
    # Calculate t/V for plotting
    t_over_v = np.zeros_like(time_points)
    for i, (t, v) in enumerate(zip(time_points, filtrate_volumes)):
        if v > 0:
            t_over_v[i] = t / v
    
    # Calculate filtration rate
    filtration_rates = np.zeros_like(time_points)
    for i in range(1, len(time_points)):
        dt = time_points[i] - time_points[i-1]
        dv = filtrate_volumes[i] - filtrate_volumes[i-1]
        if dt > 0:
            filtration_rates[i] = dv / dt
    
    # Calculate cake thickness
    # Cake thickness = Volume of cake / Filter area
    # Volume of cake = Mass of cake / (Density of cake)
    # Mass of cake = Concentration * Filtrate volume
    
    # Assume cake density is 2.5 times the slurry concentration (dry basis)
    cake_density = 2.5 * slurry_concentration  # kg/m³
    
    cake_thicknesses = slurry_concentration * filtrate_volumes / (cake_density * filter_area)  # m
    cake_thicknesses_mm = cake_thicknesses * 1000  # mm
    
    # Check if cake thickness exceeds frame thickness
    max_cake_thickness = frame_thickness  # mm
    
    # Find the time when cake fills the frame
    fill_time_index = np.argmax(cake_thicknesses_mm >= max_cake_thickness)
    
    if fill_time_index > 0:
        fill_time = time_points[fill_time_index]
        fill_volume = filtrate_volumes[fill_time_index]
    else:
        fill_time = max_time
        fill_volume = filtrate_volumes[-1]
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (s)': time_points,
        'Filtrate Volume (m³)': filtrate_volumes,
        't/V (s/m³)': t_over_v,
        'Filtration Rate (m³/s)': filtration_rates,
        'Cake Thickness (mm)': cake_thicknesses_mm
    })
    
    # Truncate data at fill time if frame fills up
    if fill_time_index > 0:
        df = df.iloc[:fill_time_index+1].copy()
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Filtration pressure:** {filtration_pressure} kPa")
        st.write(f"**Slurry concentration:** {slurry_concentration} kg/m³")
        st.write(f"**Filter area:** {filter_area:.2f} m²")
        st.write(f"**Total frame volume:** {total_frame_volume:.4f} m³")
    
    with col2:
        st.write(f"**Specific cake resistance:** {specific_cake_resistance:.2e} m/kg")
        st.write(f"**Medium resistance:** {medium_resistance:.2e} 1/m")
        
        if fill_time_index > 0:
            st.write(f"**Time to fill frames:** {fill_time:.1f} s")
            st.write(f"**Final filtrate volume:** {fill_volume:.4f} m³")
        else:
            st.write("**Frames do not fill completely in the given time**")
            st.write(f"**Final filtrate volume:** {filtrate_volumes[-1]:.4f} m³")
    
    # Create tabs for different displays
    tab1, tab2, tab3, tab4 = st.tabs(["Filtration Curve", "Cake Formation", "Ruth Plot", "Data Table"])
    
    with tab1:
        # Filtration curve
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(time_points[:len(df)], df['Filtrate Volume (m³)'], 'b-')
        
        if fill_time_index > 0:
            ax.axvline(x=fill_time, color='r', linestyle='--', 
                      label=f'Frame Fill Time: {fill_time:.1f} s')
        
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Filtrate Volume (m³)')
        ax.set_title('Filtration Curve')
        ax.grid(True)
        if fill_time_index > 0:
            ax.legend()
        st.pyplot(fig)
        
        # Filtration rate
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(time_points[:len(df)], df['Filtration Rate (m³/s)'], 'g-')
        
        if fill_time_index > 0:
            ax2.axvline(x=fill_time, color='r', linestyle='--', 
                      label=f'Frame Fill Time: {fill_time:.1f} s')
        
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Filtration Rate (m³/s)')
        ax2.set_title('Filtration Rate vs Time')
        ax2.grid(True)
        if fill_time_index > 0:
            ax2.legend()
        st.pyplot(fig2)
    
    with tab2:
        # Cake formation
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(time_points[:len(df)], df['Cake Thickness (mm)'], 'b-')
        
        if fill_time_index > 0:
            ax3.axvline(x=fill_time, color='r', linestyle='--', 
                      label=f'Frame Fill Time: {fill_time:.1f} s')
        
        ax3.axhline(y=frame_thickness, color='g', linestyle='--', 
                   label=f'Frame Thickness: {frame_thickness} mm')
        
        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Cake Thickness (mm)')
        ax3.set_title('Cake Thickness vs Time')
        ax3.grid(True)
        ax3.legend()
        st.pyplot(fig3)
        
        # Cake porosity visualization
        st.write("### Cake Compression Visualization")
        
        # Assume porosity decreases as pressure increases
        initial_porosity = 0.7
        porosity_factor = 0.5 + 0.5 * (300 / filtration_pressure)
        final_porosity = initial_porosity * porosity_factor
        
        porosities = np.linspace(initial_porosity, final_porosity, len(df))
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(time_points[:len(df)], porosities, 'r-')
        
        ax4.set_xlabel('Time (s)')
        ax4.set_ylabel('Estimated Cake Porosity')
        ax4.set_title('Cake Porosity vs Time (Compression Effect)')
        ax4.grid(True)
        st.pyplot(fig4)
    
    with tab3:
        # Ruth plot (t/V vs V)
        # Filter out zeros to avoid division issues
        mask = df['Filtrate Volume (m³)'] > 0
        ruth_volumes = df.loc[mask, 'Filtrate Volume (m³)']
        ruth_t_over_v = df.loc[mask, 't/V (s/m³)']
        
        fig5, ax5 = plt.subplots(figsize=(10, 6))
        ax5.plot(ruth_volumes, ruth_t_over_v, 'b.')
        
        # Fit a linear model
        if len(ruth_volumes) > 2:
            # Fit a straight line to the data
            def linear_func(x, a, b):
                return a * x + b
            
            popt, pcov = curve_fit(linear_func, ruth_volumes, ruth_t_over_v)
            slope, intercept = popt
            
            # Calculate fitted line
            fit_line = linear_func(ruth_volumes, slope, intercept)
            
            # Plot the fitted line
            ax5.plot(ruth_volumes, fit_line, 'r-', label=f'Fit: y = {slope:.2e}x + {intercept:.2e}')
            
            # Calculate specific cake resistance and medium resistance from the fit
            calculated_alpha = 2 * slope * filter_area**2 * (filtration_pressure * 1000) / (filtrate_viscosity * slurry_concentration)
            calculated_rm = intercept * filter_area * (filtration_pressure * 1000) / filtrate_viscosity
            
            ax5.text(0.05, 0.9, f"Specific cake resistance: {calculated_alpha:.2e} m/kg", 
                    transform=ax5.transAxes, fontsize=10)
            ax5.text(0.05, 0.85, f"Medium resistance: {calculated_rm:.2e} 1/m", 
                    transform=ax5.transAxes, fontsize=10)
            
            ax5.legend()
        
        ax5.set_xlabel('Filtrate Volume (m³)')
        ax5.set_ylabel('t/V (s/m³)')
        ax5.set_title('Ruth Plot for Constant Pressure Filtration')
        ax5.grid(True)
        st.pyplot(fig5)
    
    with tab4:
        # Display data table with selected points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(df)-1, min(20, len(df))).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "filter_press_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Parameter effect analysis
    with st.expander("Parameter Effect Analysis"):
        st.write("### Effect of Process Parameters on Filtration Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Effect of pressure
            st.write("**Effect of Pressure on Filtration Rate**")
            
            pressures = [100, 200, 300, 400, 500, 600]
            final_volumes = []
            
            for p in pressures:
                # Recalculate constants
                specific_cake_resistance_p = 1e11 * (p / 300)**0.5  # Pressure dependent
                k1_p = (filtrate_viscosity * specific_cake_resistance_p * slurry_concentration) / (2 * filter_area**2 * (p * 1000))
                k2_p = (filtrate_viscosity * medium_resistance) / (filter_area * (p * 1000))
                
                # Calculate final volume after a specific time (say 1800 seconds)
                test_time = 1800
                final_volume_p = (-k2_p + np.sqrt(k2_p**2 + 4*k1_p*test_time)) / (2*k1_p)
                final_volumes.append(final_volume_p)
            
            fig6, ax6 = plt.subplots(figsize=(8, 5))
            ax6.plot(pressures, final_volumes, 'bo-')
            ax6.axvline(x=filtration_pressure, color='r', linestyle='--', 
                       label=f'Current: {filtration_pressure} kPa')
            
            ax6.set_xlabel('Pressure (kPa)')
            ax6.set_ylabel(f'Filtrate Volume after {test_time} s (m³)')
            ax6.set_title('Effect of Pressure on Filtration')
            ax6.grid(True)
            ax6.legend()
            st.pyplot(fig6)
        
        with col2:
            # Effect of slurry concentration
            st.write("**Effect of Slurry Concentration on Filtration Rate**")
            
            concentrations = [50, 100, 150, 200, 250, 300]
            final_volumes_conc = []
            
            for c in concentrations:
                # Recalculate constants
                k1_c = (filtrate_viscosity * specific_cake_resistance * c) / (2 * filter_area**2 * (filtration_pressure * 1000))
                k2_c = (filtrate_viscosity * medium_resistance) / (filter_area * (filtration_pressure * 1000))
                
                # Calculate final volume after a specific time (say 1800 seconds)
                test_time = 1800
                final_volume_c = (-k2_c + np.sqrt(k2_c**2 + 4*k1_c*test_time)) / (2*k1_c)
                final_volumes_conc.append(final_volume_c)
            
            fig7, ax7 = plt.subplots(figsize=(8, 5))
            ax7.plot(concentrations, final_volumes_conc, 'go-')
            ax7.axvline(x=slurry_concentration, color='r', linestyle='--', 
                       label=f'Current: {slurry_concentration} kg/m³')
            
            ax7.set_xlabel('Slurry Concentration (kg/m³)')
            ax7.set_ylabel(f'Filtrate Volume after {test_time} s (m³)')
            ax7.set_title('Effect of Concentration on Filtration')
            ax7.grid(True)
            ax7.legend()
            st.pyplot(fig7)
    
    # Filter press schematic
    with st.expander("Filter Press Schematic"):
        st.markdown("""
        ### Plate and Frame Filter Press Schematic
        
        ```
        Feed Pump
            │
            ↓
        ┌───┬───┬───┬───┬───┐
        │ P │ F │ P │ F │ P │ ← Closing Device
        └───┴───┴───┴───┴───┘
            │   │   │
            ↓   ↓   ↓
         Filtrate Outlets
        