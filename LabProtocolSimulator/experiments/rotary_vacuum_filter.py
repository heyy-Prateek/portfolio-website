import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def app():
    st.title("Experiment 7: Rotary Vacuum Filter")
    
    st.markdown("""
    ## Objective
    Study of continuous solid-liquid separation using a rotary vacuum filter.
    
    ## Aim
    To determine the filtration rate, cake thickness, and performance characteristics of a rotary vacuum filter.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Rotary Vacuum Filter Theory
        
        A rotary vacuum filter is a continuous filtration device consisting of a rotating drum partially immersed in a slurry. The drum surface is divided into sections, each connected to a vacuum system. As the drum rotates, it picks up slurry, forms a cake, which is then washed, dried, and discharged.
        
        The filtration process in a rotary vacuum filter can be described by the same basic equation as used for batch filtration:
        
        $$\\frac{dt}{dV} = \\frac{\\mu \\alpha c}{A^2 \\Delta P}V + \\frac{\\mu R_m}{A \\Delta P}$$
        
        Where:
        - $t$ = filtration time (s)
        - $V$ = filtrate volume (m³)
        - $\\mu$ = filtrate viscosity (Pa·s)
        - $\\alpha$ = specific cake resistance (m/kg)
        - $c$ = mass of dry cake per unit volume of filtrate (kg/m³)
        - $A$ = filter area (m²)
        - $\\Delta P$ = pressure drop across filter (Pa)
        - $R_m$ = filter medium resistance (1/m)
        
        The key operational parameters for a rotary vacuum filter are:
        
        1. **Drum Speed**: Determines the cycle time and production rate
        2. **Submergence**: Percentage of drum immersed in the slurry
        3. **Vacuum Level**: Affects filtration rate and cake moisture
        4. **Cake Thickness**: Determined by the filtration time and slurry properties
        
        The filter cycle consists of several zones:
        
        1. **Pickup Zone**: Where the slurry is picked up and initial cake formation occurs
        2. **Cake Formation Zone**: Where filtration continues and the cake thickens
        3. **Washing Zone** (optional): Where the cake is washed
        4. **Drying Zone**: Where air is drawn through the cake to reduce moisture
        5. **Discharge Zone**: Where the cake is removed from the drum
        """)
    
    # Input parameters
    st.sidebar.header("Rotary Filter Parameters")
    
    # Operational parameters
    drum_diameter = st.sidebar.slider("Drum diameter (m)", 0.5, 5.0, 2.0, 0.1)
    
    drum_length = st.sidebar.slider("Drum length (m)", 0.5, 5.0, 2.5, 0.1)
    
    drum_speed = st.sidebar.slider("Drum speed (rpm)", 0.1, 5.0, 1.0, 0.1)
    
    submergence = st.sidebar.slider("Submergence (%)", 10, 50, 30, 1)
    
    vacuum_pressure = st.sidebar.slider("Vacuum pressure (kPa)", 10, 100, 50, 5)
    
    # Slurry properties
    slurry_concentration = st.sidebar.slider("Slurry concentration (kg/m³)", 50, 500, 200, 10)
    
    filtrate_viscosity = st.sidebar.number_input("Filtrate viscosity (Pa·s)", 
                                              min_value=0.0005, max_value=0.05, value=0.001, step=0.0001, format="%.4f")
    
    # Calculated parameters
    # Calculate drum surface area
    drum_surface_area = np.pi * drum_diameter * drum_length  # m²
    
    # Calculate specific cake resistance (pressure dependent)
    specific_cake_resistance = 5e10 * (vacuum_pressure / 50)**0.5  # m/kg
    medium_resistance = 1e10  # 1/m
    
    # Calculate rotational period
    rotation_period = 60 / drum_speed  # seconds
    
    # Calculate submergence angle and time
    submergence_angle = submergence * 360 / 100  # degrees
    submergence_time = rotation_period * submergence_angle / 360  # seconds
    
    # Simulation
    # Define time points for one full rotation
    time_points = np.linspace(0, rotation_period, 100)
    
    # Define angular position at each time point
    angles = time_points * 360 / rotation_period
    
    # Determine if point is submerged
    is_submerged = angles <= submergence_angle
    
    # Calculate filtration time for each position
    filtration_times = np.zeros_like(time_points)
    active_filtration_time = 0
    
    for i, submerged in enumerate(is_submerged):
        if submerged:
            # Point is in submergence zone - cake is forming
            if i > 0:
                active_filtration_time += time_points[i] - time_points[i-1]
            filtration_times[i] = active_filtration_time
        else:
            # Point is out of submergence - cake dewatering/discharge
            filtration_times[i] = submergence_time
    
    # Calculate cake thickness at each position
    # Constants for the filtration equation
    k1 = (filtrate_viscosity * specific_cake_resistance * slurry_concentration) / (2 * drum_surface_area**2 * (vacuum_pressure * 1000))
    k2 = (filtrate_viscosity * medium_resistance) / (drum_surface_area * (vacuum_pressure * 1000))
    
    # Calculate filtrate volume at each position
    filtrate_volumes = np.zeros_like(time_points)
    
    for i, t in enumerate(filtration_times):
        if t > 0:
            filtrate_volumes[i] = (-k2 + np.sqrt(k2**2 + 4*k1*t)) / (2*k1)
    
    # Assume cake density is 2.5 times the slurry concentration (dry basis)
    cake_density = 2.5 * slurry_concentration  # kg/m³
    
    # Calculate cake thickness
    cake_thicknesses = np.zeros_like(time_points)
    for i, submerged in enumerate(is_submerged):
        if i > 0:  # Skip first point
            if submerged:
                # During submergence, cake continues to form
                cake_thicknesses[i] = slurry_concentration * filtrate_volumes[i] / (cake_density * drum_surface_area)  # m
            else:
                # After submergence, cake thickness remains constant until discharge
                if angles[i] < 330:  # Before discharge
                    cake_thicknesses[i] = cake_thicknesses[np.argmax(angles >= submergence_angle) - 1]
                else:  # Discharge zone
                    cake_thicknesses[i] = 0
    
    # Convert to mm for display
    cake_thicknesses_mm = cake_thicknesses * 1000  # mm
    
    # Calculate cake moisture content
    # Assume initial moisture is 80% and decreases during drying
    initial_moisture = 0.8
    final_moisture = 0.3
    moisture_content = np.ones_like(time_points) * initial_moisture
    
    for i, angle in enumerate(angles):
        if angle > submergence_angle:
            # Dewatering occurs after submergence
            fraction_dried = min(1.0, (angle - submergence_angle) / (330 - submergence_angle))
            moisture_content[i] = initial_moisture - fraction_dried * (initial_moisture - final_moisture)
    
    # Calculate production rate
    max_cake_thickness = np.max(cake_thicknesses)
    cake_volume_per_rotation = max_cake_thickness * drum_surface_area  # m³/rotation
    cake_mass_per_rotation = cake_volume_per_rotation * cake_density  # kg/rotation
    production_rate = cake_mass_per_rotation * drum_speed * 60  # kg/h
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Time (s)': time_points,
        'Angle (degrees)': angles,
        'Filtration Time (s)': filtration_times,
        'Filtrate Volume (m³)': filtrate_volumes,
        'Cake Thickness (mm)': cake_thicknesses_mm,
        'Moisture Content (fraction)': moisture_content
    })
    
    # Mark different zones
    df['Zone'] = 'Discharge'
    df.loc[angles <= submergence_angle, 'Zone'] = 'Pickup/Cake Formation'
    df.loc[(angles > submergence_angle) & (angles <= 180), 'Zone'] = 'Washing'
    df.loc[(angles > 180) & (angles <= 330), 'Zone'] = 'Drying'
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Drum surface area:** {drum_surface_area:.2f} m²")
        st.write(f"**Rotation period:** {rotation_period:.2f} s")
        st.write(f"**Submergence time:** {submergence_time:.2f} s")
        st.write(f"**Maximum cake thickness:** {np.max(cake_thicknesses_mm):.2f} mm")
    
    with col2:
        st.write(f"**Specific cake resistance:** {specific_cake_resistance:.2e} m/kg")
        st.write(f"**Medium resistance:** {medium_resistance:.2e} 1/m")
        st.write(f"**Final moisture content:** {final_moisture*100:.1f}%")
        st.write(f"**Production rate:** {production_rate:.2f} kg/h")
    
    # Create tabs for different displays
    tab1, tab2, tab3, tab4 = st.tabs(["Drum Operation", "Cake Formation", "Moisture Profile", "Data Table"])
    
    with tab1:
        # Rotary drum operation visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot different zones with different colors
        zone_colors = {
            'Pickup/Cake Formation': 'blue',
            'Washing': 'green',
            'Drying': 'orange',
            'Discharge': 'red'
        }
        
        for zone in zone_colors:
            zone_data = df[df['Zone'] == zone]
            ax.plot(zone_data['Angle (degrees)'], zone_data['Cake Thickness (mm)'], 
                    color=zone_colors[zone], label=zone)
        
        ax.set_xlabel('Angular Position (degrees)')
        ax.set_ylabel('Cake Thickness (mm)')
        ax.set_title('Cake Thickness Around Drum Circumference')
        ax.grid(True)
        ax.legend()
        
        # Add drum schematic
        theta = np.linspace(0, 2*np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        ax.plot(x*360/(2*np.pi), y*np.max(cake_thicknesses_mm)*1.5, 'k--', alpha=0.5)
        
        # Indicate submergence level
        submergence_angle_rad = submergence_angle * np.pi / 180
        ax.fill_between([0, submergence_angle], [-np.max(cake_thicknesses_mm)*2, -np.max(cake_thicknesses_mm)*2], 
                         [np.max(cake_thicknesses_mm)*2, np.max(cake_thicknesses_mm)*2], 
                         color='skyblue', alpha=0.3)
        
        st.pyplot(fig)
    
    with tab2:
        # Cake formation visualization
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        # Filter for cake formation zone
        formation_data = df[df['Zone'] == 'Pickup/Cake Formation']
        
        ax2.plot(formation_data['Filtration Time (s)'], formation_data['Cake Thickness (mm)'], 'b-')
        
        ax2.set_xlabel('Filtration Time (s)')
        ax2.set_ylabel('Cake Thickness (mm)')
        ax2.set_title('Cake Formation During Submergence')
        ax2.grid(True)
        st.pyplot(fig2)
        
        # Filtration rate
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        # Calculate filtration rate
        filtration_rate = np.zeros_like(time_points)
        for i in range(1, len(formation_data)):
            dt = formation_data.iloc[i]['Filtration Time (s)'] - formation_data.iloc[i-1]['Filtration Time (s)']
            dv = formation_data.iloc[i]['Filtrate Volume (m³)'] - formation_data.iloc[i-1]['Filtrate Volume (m³)']
            if dt > 0:
                idx = formation_data.index[i]
                filtration_rate[idx] = dv / dt
        
        # Plot filtration rate
        ax3.plot(formation_data['Filtration Time (s)'], filtration_rate[formation_data.index], 'g-')
        
        ax3.set_xlabel('Filtration Time (s)')
        ax3.set_ylabel('Filtration Rate (m³/s)')
        ax3.set_title('Filtration Rate During Submergence')
        ax3.grid(True)
        st.pyplot(fig3)
    
    with tab3:
        # Moisture profile visualization
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        
        ax4.plot(df['Angle (degrees)'], df['Moisture Content (fraction)'] * 100, 'b-')
        
        # Mark different zones
        zone_boundaries = [0, submergence_angle, 180, 330, 360]
        zone_names = ['Pickup/Cake Formation', 'Washing', 'Drying', 'Discharge']
        
        for i in range(len(zone_names)):
            ax4.axvspan(zone_boundaries[i], zone_boundaries[i+1], 
                        alpha=0.2, color=list(zone_colors.values())[i])
            ax4.text((zone_boundaries[i] + zone_boundaries[i+1])/2, 85, 
                     zone_names[i], ha='center', alpha=0.7)
        
        ax4.set_xlabel('Angular Position (degrees)')
        ax4.set_ylabel('Moisture Content (%)')
        ax4.set_title('Moisture Content Profile Around Drum')
        ax4.grid(True)
        st.pyplot(fig4)
    
    with tab4:
        # Display data table with selected points
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(df)-1, 20).astype(int)
        st.dataframe(df.iloc[sample_indices].reset_index(drop=True))
        
        # Download link for full data
        csv = df.to_csv(index=False)
        st.download_button(
            "Download Data as CSV",
            csv,
            "rotary_vacuum_filter_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Parameter effect analysis
    with st.expander("Parameter Effect Analysis"):
        st.write("### Effect of Process Parameters on Filter Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Effect of drum speed
            st.write("**Effect of Drum Speed on Production Rate**")
            
            speeds = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
            production_rates = []
            
            for speed in speeds:
                # Calculate new rotation period
                rotation_period_new = 60 / speed
                
                # Calculate new submergence time
                submergence_time_new = rotation_period_new * submergence_angle / 360
                
                # Calculate new cake thickness (simplified)
                # Using the cake formation model
                t_sub = submergence_time_new
                v_sub = (-k2 + np.sqrt(k2**2 + 4*k1*t_sub)) / (2*k1)
                thickness_new = slurry_concentration * v_sub / (cake_density * drum_surface_area)
                
                # Calculate new production rate
                cake_volume_new = thickness_new * drum_surface_area
                cake_mass_new = cake_volume_new * cake_density
                prod_rate_new = cake_mass_new * speed * 60
                
                production_rates.append(prod_rate_new)
            
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            ax5.plot(speeds, production_rates, 'bo-')
            ax5.axvline(x=drum_speed, color='r', linestyle='--', 
                       label=f'Current: {drum_speed} rpm')
            
            ax5.set_xlabel('Drum Speed (rpm)')
            ax5.set_ylabel('Production Rate (kg/h)')
            ax5.set_title('Effect of Drum Speed on Production Rate')
            ax5.grid(True)
            ax5.legend()
            st.pyplot(fig5)
        
        with col2:
            # Effect of vacuum pressure
            st.write("**Effect of Vacuum Pressure on Cake Thickness**")
            
            pressures = [20, 30, 40, 50, 60, 70, 80]
            cake_thicknesses_max = []
            
            for pressure in pressures:
                # Calculate new specific cake resistance
                resistance_new = 5e10 * (pressure / 50)**0.5
                
                # Recalculate constants
                k1_new = (filtrate_viscosity * resistance_new * slurry_concentration) / (2 * drum_surface_area**2 * (pressure * 1000))
                k2_new = (filtrate_viscosity * medium_resistance) / (drum_surface_area * (pressure * 1000))
                
                # Calculate new filtrate volume
                v_new = (-k2_new + np.sqrt(k2_new**2 + 4*k1_new*submergence_time)) / (2*k1_new)
                
                # Calculate new cake thickness
                thickness_new = slurry_concentration * v_new / (cake_density * drum_surface_area) * 1000  # mm
                
                cake_thicknesses_max.append(thickness_new)
            
            fig6, ax6 = plt.subplots(figsize=(8, 5))
            ax6.plot(pressures, cake_thicknesses_max, 'go-')
            ax6.axvline(x=vacuum_pressure, color='r', linestyle='--', 
                       label=f'Current: {vacuum_pressure} kPa')
            
            ax6.set_xlabel('Vacuum Pressure (kPa)')
            ax6.set_ylabel('Maximum Cake Thickness (mm)')
            ax6.set_title('Effect of Vacuum Pressure on Cake Thickness')
            ax6.grid(True)
            ax6.legend()
            st.pyplot(fig6)
    
    # Rotary vacuum filter schematic
    with st.expander("Rotary Vacuum Filter Schematic"):
        st.markdown("""
        ### Rotary Vacuum Filter Schematic
        
        ```
                    ┌─────────────────────────┐
                    │    Rotary Vacuum Filter │
        ┌───────────┴─────────────────────────┴───────────┐
        │                                                 │
        │   Discharge  ───┐                   ┌─── Pickup │
        │     Zone        │                   │     Zone  │
        │                 ↓                   ↓           │
        │           ┌───────────────────────────┐         │
        │           │                           │         │
        │  Drying   │                           │  Cake   │
        │   Zone ←──┤                           ├──→ Form │
        │           │                           │  Zone   │
        │           └───────────────────────────┘         │
        │                       │                         │
        │                       ↓                         │
        │                 Washing Zone                    │
        │                                                 │
        └─────────────────────────────────────────────────┘
               │                               │
               │                               │
               ↓                               ↓
           Filtrate                         Slurry
        ```
        
        ### Operational Zones:
        
        1. **Pickup Zone**: Drum surface enters the slurry, initial cake formation begins
        2. **Cake Formation Zone**: Further filtration and cake build-up
        3. **Washing Zone**: Optional washing of the cake with wash liquid
        4. **Drying Zone**: Air is drawn through the cake to reduce moisture content
        5. **Discharge Zone**: Cake is removed from the drum surface by a scraper
        
        ### Key Components:
        
        - **Rotating Drum**: Provides filtration surface
        - **Filter Medium**: Covers the drum surface
        - **Slurry Trough**: Contains the feed slurry
        - **Vacuum System**: Provides suction through the drum surface
        - **Discharge Knife/Scraper**: Removes the cake from the drum
        
        ### Advantages:
        
        - Continuous operation
        - Good for difficult-to-filter slurries
        - Allows for cake washing
        - Provides partial dewatering
        """)
