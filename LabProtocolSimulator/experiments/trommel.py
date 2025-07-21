import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.title("Experiment 10: Trommel")
    
    st.markdown("""
    ## Objective
    Study of particle screening using a trommel (rotary screen).
    
    ## Aim
    To determine the screening efficiency and capacity of a trommel for different operating conditions.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Trommel Theory
        
        A trommel is a cylindrical rotating screen used to separate materials by size. The feed material enters one end of the trommel, and as the trommel rotates, undersized particles fall through the screen openings while oversized particles are carried to the discharge end.
        
        The key principles governing trommel operation include:
        
        1. **Probability of Screening**: The probability of a particle passing through the screen depends on:
           - Particle size relative to screen aperture
           - Presentation of the particle to the screen surface
           - Number of presentations (residence time)
        
        2. **Stratification**: The lifting and tumbling action of the trommel causes particles to stratify, with smaller particles migrating toward the screen surface.
        
        3. **Capacity and Efficiency**: The screening capacity and efficiency depend on:
           - Feed rate
           - Trommel diameter and length
           - Rotation speed
           - Screen aperture size
           - Material characteristics
           - Inclination angle
        
        The screening efficiency is typically calculated as:
        
        $$E = \\frac{m_u}{m_f \\times p} \\times 100\\%$$
        
        Where:
        - $E$ = screening efficiency (%)
        - $m_u$ = mass of undersize in underflow
        - $m_f$ = mass of feed
        - $p$ = proportion of undersize in feed
        
        The actual capacity of a trommel depends on several factors and is often described by empirical relationships, such as:
        
        $$C = f_a \\times f_s \\times f_o \\times f_h \\times C_0$$
        
        Where:
        - $C$ = actual capacity
        - $C_0$ = base capacity
        - $f_a$ = aperture size factor
        - $f_s$ = material specific gravity factor
        - $f_o$ = oversize factor
        - $f_h$ = moisture factor
        """)
    
    # Input parameters
    st.sidebar.header("Trommel Parameters")
    
    # Trommel dimensions
    trommel_diameter = st.sidebar.slider("Trommel diameter (m)", 0.5, 3.0, 1.5, 0.1)
    
    trommel_length = st.sidebar.slider("Trommel length (m)", 1.0, 10.0, 4.0, 0.5)
    
    inclination_angle = st.sidebar.slider("Inclination angle (degrees)", 1, 10, 5, 1)
    
    # Screen parameters
    aperture_size = st.sidebar.slider("Screen aperture size (mm)", 1, 100, 10, 1)
    
    open_area = st.sidebar.slider("Screen open area (%)", 20, 60, 40, 5)
    
    # Operational parameters
    rotation_speed = st.sidebar.slider("Rotation speed (rpm)", 5, 30, 15, 1)
    
    feed_rate = st.sidebar.slider("Feed rate (tons/h)", 5, 200, 50, 5)
    
    # Material properties
    bulk_density = st.sidebar.slider("Material bulk density (kg/m³)", 500, 2500, 1500, 100)
    
    moisture_content = st.sidebar.slider("Material moisture content (%)", 0, 30, 5, 1)
    
    # Feed size distribution parameters
    d_min = st.sidebar.slider("Minimum particle size (mm)", 0.1, 10.0, 1.0, 0.1)
    
    d_max = st.sidebar.slider("Maximum particle size (mm)", 10, 200, 50, 5)
    
    # Calculate parameters
    # Calculate critical speed
    # Critical speed is when centrifugal force equals gravitational force at drum periphery
    g = 9.81  # m/s²
    critical_speed = np.sqrt(g / (trommel_diameter/2)) * 60 / (2 * np.pi)  # rpm
    
    # Calculate relative speed (as percentage of critical)
    relative_speed = rotation_speed / critical_speed * 100  # %
    
    # Calculate residence time
    # Use empirical formula for residence time
    # t = K * L / (N * D * sin(alpha))
    # where K is a constant (typically 0.15-0.25), L is length, N is rpm,
    # D is diameter, and alpha is inclination angle
    K = 0.2  # empirical constant
    residence_time = K * trommel_length / (rotation_speed * trommel_diameter * np.sin(np.radians(inclination_angle)))  # min
    
    # Calculate trommel volume
    trommel_volume = np.pi * (trommel_diameter/2)**2 * trommel_length  # m³
    
    # Calculate material volume in trommel
    # Typically 10-15% of trommel volume
    fill_percentage = 10 + 5 * (feed_rate / 100)  # % of trommel volume, increases with feed rate
    fill_percentage = min(30, max(5, fill_percentage))  # limit between 5% and 30%
    
    material_volume = trommel_volume * fill_percentage / 100  # m³
    
    # Calculate material mass in trommel
    material_mass = material_volume * bulk_density / 1000  # tons
    
    # Calculate screen area
    screen_area = np.pi * trommel_diameter * trommel_length  # m²
    
    # Calculate effective screen area
    effective_area = screen_area * open_area / 100  # m²
    
    # Calculate unit capacity
    unit_capacity = feed_rate / effective_area  # tons/h/m²
    
    # Generate particle size distribution
    # Use log-normal distribution
    num_points = 50
    size_points = np.logspace(np.log10(d_min), np.log10(d_max), num_points)
    
    # Parameters for log-normal distribution
    geo_mean = np.sqrt(d_min * d_max)
    geo_std = (d_max / d_min)**(1/4)
    
    # Calculate density function
    def log_normal_pdf(x, mu, sigma):
        return (1 / (x * sigma * np.sqrt(2*np.pi))) * np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2))
    
    log_mu = np.log(geo_mean)
    log_sigma = np.log(geo_std)
    
    pdf_values = log_normal_pdf(size_points, log_mu, log_sigma)
    
    # Normalize to get mass fractions
    mass_fractions = pdf_values / np.sum(pdf_values)
    
    # Calculate cumulative distribution
    cumulative_distribution = np.cumsum(mass_fractions)
    
    # Calculate efficiency for each size fraction
    # Use a probability model based on particle size to aperture ratio
    efficiencies = np.zeros_like(size_points)
    
    for i, size in enumerate(size_points):
        # Size ratio (particle size / aperture size)
        size_ratio = size / aperture_size
        
        if size_ratio < 0.5:
            # Fine particles - high passage probability
            base_efficiency = 0.99
        elif size_ratio < 0.8:
            # Intermediate sizes - some hindrance
            base_efficiency = 0.95 - 0.3 * (size_ratio - 0.5) / 0.3
        elif size_ratio < 1.0:
            # Near-aperture sizes - transition zone
            base_efficiency = 0.65 - 0.65 * (size_ratio - 0.8) / 0.2
        else:
            # Oversize - ideally zero, but some passage may occur due to elongated particles
            base_efficiency = max(0, 0.05 * (1.3 - size_ratio) / 0.3) if size_ratio < 1.3 else 0
        
        # Modify efficiency based on residence time
        # More time increases chances of presentation to the aperture
        time_factor = min(1, residence_time / 2)  # Normalizes residence time effect
        
        # Modify efficiency based on moisture (high moisture reduces efficiency)
        moisture_factor = 1 - 0.5 * (moisture_content / 30)
        
        # Modify efficiency based on relative speed
        # Too slow: insufficient presentations
        # Too fast: centrifugal force pins material to screen
        speed_factor = 1 - 0.5 * abs(relative_speed - 40) / 40
        
        # Combined efficiency
        efficiencies[i] = base_efficiency * time_factor * moisture_factor * speed_factor
    
    # Calculate mass of each size fraction in feed, oversize, and undersize
    feed_mass = feed_rate  # tons/h
    feed_size_masses = mass_fractions * feed_mass
    
    undersize_size_masses = feed_size_masses * efficiencies
    oversize_size_masses = feed_size_masses - undersize_size_masses
    
    # Calculate total masses
    total_undersize_mass = np.sum(undersize_size_masses)
    total_oversize_mass = np.sum(oversize_size_masses)
    
    # Calculate actual cut size (d50)
    # This is the size at which 50% of the particles report to oversize
    # Find the size at which efficiency is closest to 0.5
    efficiency_diff = np.abs(efficiencies - 0.5)
    d50_index = np.argmin(efficiency_diff)
    actual_cut_size = size_points[d50_index]
    
    # Calculate theoretical cut size (aperture size)
    theoretical_cut_size = aperture_size
    
    # Calculate overall efficiency
    # Define theoretical undersize as everything below aperture size
    theoretical_undersize_index = np.where(size_points <= aperture_size)[0]
    theoretical_undersize_mass = np.sum(feed_size_masses[theoretical_undersize_index])
    theoretical_undersize_fraction = theoretical_undersize_mass / feed_mass
    
    # Actual undersize recovered in underflow
    actual_undersize_recovered = np.sum(undersize_size_masses[theoretical_undersize_index])
    
    # Screening efficiency
    if theoretical_undersize_mass > 0:
        screening_efficiency = actual_undersize_recovered / theoretical_undersize_mass * 100
    else:
        screening_efficiency = 0
    
    # Calculate partition numbers for partition curve
    partition_numbers = 100 * (1 - efficiencies)  # percent to oversize
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Particle Size (mm)': size_points,
        'Mass Fraction': mass_fractions,
        'Cumulative Distribution (%)': cumulative_distribution * 100,
        'Screening Efficiency (%)': efficiencies * 100,
        'Partition Number (%)': partition_numbers,
        'Feed (tons/h)': feed_size_masses,
        'Undersize (tons/h)': undersize_size_masses,
        'Oversize (tons/h)': oversize_size_masses
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Screen area:** {screen_area:.2f} m²")
        st.write(f"**Effective screen area:** {effective_area:.2f} m²")
        st.write(f"**Critical speed:** {critical_speed:.2f} rpm")
        st.write(f"**Relative speed:** {relative_speed:.2f}% of critical")
        st.write(f"**Residence time:** {residence_time:.2f} min")
    
    with col2:
        st.write(f"**Theoretical cut size:** {theoretical_cut_size:.2f} mm")
        st.write(f"**Actual cut size (d50):** {actual_cut_size:.2f} mm")
        st.write(f"**Undersize production:** {total_undersize_mass:.2f} tons/h")
        st.write(f"**Oversize production:** {total_oversize_mass:.2f} tons/h")
        st.write(f"**Screening efficiency:** {screening_efficiency:.2f}%")
    
    # Create tabs for different displays
    tab1, tab2, tab3, tab4 = st.tabs(["Size Distribution", "Partition Curve", "Parameter Effects", "Data Table"])
    
    with tab1:
        # Size distribution visualization
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.semilogx(size_points, cumulative_distribution * 100, 'k-', label='Feed')
        
        # Calculate undersize and oversize cumulative distributions
        if total_undersize_mass > 0:
            cum_undersize = np.cumsum(undersize_size_masses) / total_undersize_mass * 100
            ax.semilogx(size_points, cum_undersize, 'b-', label='Undersize')
        
        if total_oversize_mass > 0:
            cum_oversize = np.cumsum(oversize_size_masses) / total_oversize_mass * 100
            ax.semilogx(size_points, cum_oversize, 'r-', label='Oversize')
        
        # Add vertical line for aperture size
        ax.axvline(x=aperture_size, color='g', linestyle='--', 
                  label=f'Aperture Size: {aperture_size} mm')
        
        # Add vertical line for actual cut size
        ax.axvline(x=actual_cut_size, color='m', linestyle='--', 
                  label=f'Actual Cut Size: {actual_cut_size:.2f} mm')
        
        ax.set_xlabel('Particle Size (mm)')
        ax.set_ylabel('Cumulative Passing (%)')
        ax.set_title('Size Distribution Curves')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
        
        # Size distribution histogram
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        # Use fewer points for better visualization
        plot_indices = np.linspace(0, len(size_points)-1, 20, dtype=int)
        
        bar_width = np.diff(np.log10(size_points[plot_indices]))
        bar_width = np.append(bar_width, bar_width[-1])
        
        ax2.bar(np.log10(size_points[plot_indices]), mass_fractions[plot_indices]*100, 
               width=bar_width*0.8, alpha=0.7, label='Feed')
        
        # Add vertical line for aperture size
        ax2.axvline(x=np.log10(aperture_size), color='g', linestyle='--', 
                   label=f'Aperture Size: {aperture_size} mm')
        
        ax2.set_xlabel('Particle Size (mm)')
        ax2.set_ylabel('Mass Fraction (%)')
        ax2.set_title('Feed Size Distribution')
        
        # Set x-ticks to actual sizes (not log values)
        tick_locs = np.log10(size_points[plot_indices])
        ax2.set_xticks(tick_locs)
        ax2.set_xticklabels([f'{s:.1f}' for s in size_points[plot_indices]])
        plt.xticks(rotation=45)
        
        ax2.grid(True)
        ax2.legend()
        st.pyplot(fig2)
    
    with tab2:
        # Partition curve visualization
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.semilogx(size_points, partition_numbers, 'b-')
        
        # Add horizontal line at 50%
        ax3.axhline(y=50, color='r', linestyle='--')
        
        # Add vertical lines for cut size and aperture
        ax3.axvline(x=actual_cut_size, color='m', linestyle='--', 
                   label=f'Actual Cut Size: {actual_cut_size:.2f} mm')
        ax3.axvline(x=aperture_size, color='g', linestyle='--', 
                   label=f'Aperture Size: {aperture_size} mm')
        
        ax3.set_xlabel('Particle Size (mm)')
        ax3.set_ylabel('Percent to Oversize (%)')
        ax3.set_title('Partition Curve')
        ax3.grid(True)
        ax3.legend()
        st.pyplot(fig3)
        
        # Screening efficiency curve
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        
        ax4.semilogx(size_points, efficiencies * 100, 'g-')
        
        # Add vertical lines for cut size and aperture
        ax4.axvline(x=actual_cut_size, color='m', linestyle='--', 
                   label=f'Actual Cut Size: {actual_cut_size:.2f} mm')
        ax4.axvline(x=aperture_size, color='g', linestyle='--', 
                   label=f'Aperture Size: {aperture_size} mm')
        
        ax4.set_xlabel('Particle Size (mm)')
        ax4.set_ylabel('Screening Efficiency (%)')
        ax4.set_title('Screening Efficiency vs Particle Size')
        ax4.grid(True)
        ax4.legend()
        st.pyplot(fig4)
    
    with tab3:
        # Parameter effects visualization
        st.write("### Effect of Operating Parameters on Screening Efficiency")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Effect of rotation speed
            speeds = np.linspace(5, 30, 10)
            efficiencies_speed = []
            
            for speed in speeds:
                # Calculate relative speed
                rel_speed = speed / critical_speed * 100
                
                # Calculate residence time
                res_time = K * trommel_length / (speed * trommel_diameter * np.sin(np.radians(inclination_angle)))
                
                # Calculate modified efficiency based on speed and time
                time_factor = min(1, res_time / 2)
                speed_factor = 1 - 0.5 * abs(rel_speed - 40) / 40
                
                # Use same base efficiency but modify with new factors
                modified_efficiency = np.mean(efficiencies / (residence_time / 2) / (1 - 0.5 * abs(relative_speed - 40) / 40))
                efficiency_speed = modified_efficiency * time_factor * speed_factor * 100
                
                efficiencies_speed.append(efficiency_speed)
            
            fig5, ax5 = plt.subplots(figsize=(8, 5))
            ax5.plot(speeds, efficiencies_speed, 'b-o')
            ax5.axvline(x=rotation_speed, color='r', linestyle='--', 
                       label=f'Current: {rotation_speed} rpm')
            
            ax5.set_xlabel('Rotation Speed (rpm)')
            ax5.set_ylabel('Overall Efficiency (%)')
            ax5.set_title('Effect of Rotation Speed on Efficiency')
            ax5.grid(True)
            ax5.legend()
            st.pyplot(fig5)
        
        with col2:
            # Effect of inclination angle
            angles = np.linspace(1, 10, 10)
            efficiencies_angle = []
            
            for angle in angles:
                # Calculate new residence time
                res_time = K * trommel_length / (rotation_speed * trommel_diameter * np.sin(np.radians(angle)))
                
                # Calculate modified efficiency based on time
                time_factor = min(1, res_time / 2)
                
                # Use same base efficiency but modify with new time factor
                modified_efficiency = np.mean(efficiencies / (residence_time / 2))
                efficiency_angle = modified_efficiency * time_factor * 100
                
                efficiencies_angle.append(efficiency_angle)
            
            fig6, ax6 = plt.subplots(figsize=(8, 5))
            ax6.plot(angles, efficiencies_angle, 'g-o')
            ax6.axvline(x=inclination_angle, color='r', linestyle='--', 
                       label=f'Current: {inclination_angle} degrees')
            
            ax6.set_xlabel('Inclination Angle (degrees)')
            ax6.set_ylabel('Overall Efficiency (%)')
            ax6.set_title('Effect of Inclination Angle on Efficiency')
            ax6.grid(True)
            ax6.legend()
            st.pyplot(fig6)
        
        # Effect of moisture content
        moistures = np.linspace(0, 30, 10)
        efficiencies_moisture = []
        
        for moisture in moistures:
            # Calculate moisture factor
            moisture_factor = 1 - 0.5 * (moisture / 30)
            
            # Use same base efficiency but modify with new moisture factor
            modified_efficiency = np.mean(efficiencies / (1 - 0.5 * (moisture_content / 30)))
            efficiency_moisture = modified_efficiency * moisture_factor * 100
            
            efficiencies_moisture.append(efficiency_moisture)
        
        fig7, ax7 = plt.subplots(figsize=(10, 6))
        ax7.plot(moistures, efficiencies_moisture, 'r-o')
        ax7.axvline(x=moisture_content, color='r', linestyle='--', 
                   label=f'Current: {moisture_content}%')
        
        ax7.set_xlabel('Moisture Content (%)')
        ax7.set_ylabel('Overall Efficiency (%)')
        ax7.set_title('Effect of Moisture Content on Efficiency')
        ax7.grid(True)
        ax7.legend()
        st.pyplot(fig7)
    
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
            "trommel_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Trommel schematic
    with st.expander("Trommel Schematic"):
        st.markdown("""
        ### Trommel Schematic
        
        ```
                            Feed
                             ↓
                         ┌───────┐
         ┌───────────────┤       │
         │               │       │
         │  ┌──────────────────────┐
         │  │   o  o  o  o  o  o   │
         │  │  o  o  o  o  o  o  o │ ← Rotation
         │  │   o  o  o  o  o  o   │
         │  └──────────────────────┘
         │               │       │
         └───────────────┘       │
                         └───────┘
                             ↓
           ↓                Oversize
        Undersize
        ```
        
        ### Key Components:
        
        - **Feed Chute**: Delivers material to the trommel
        - **Rotating Drum**: Cylindrical screen with apertures
        - **Screen Surface**: Contains openings of specific size
        - **Drive System**: Rotates the drum at controlled speed
        - **Support Structure**: Holds the drum at specified inclination
        
        ### Operating Principle:
        
        As the drum rotates, material tumbles inside. Particles smaller than the screen apertures fall through as undersize, while larger particles travel to the end of the drum and exit as oversize.
        
        ### Factors Affecting Performance:
        
        - **Rotation Speed**: Affects residence time and material movement
        - **Inclination Angle**: Controls material flow rate through drum
        - **Feed Rate**: Determines bed depth and screening opportunity
        - **Aperture Size**: Defines the separation size
        - **Moisture Content**: Affects screening efficiency (dry material screens better)
        - **Material Characteristics**: Size distribution, shape, density
        
        ### Advantages:
        
        - Effective for coarse materials
        - Good for difficult materials (sticky, fibrous)
        - Self-cleaning due to tumbling action
        - Simple operation and maintenance
        """)
