import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import set_plot_style
from scipy.optimize import curve_fit

# Set consistent style for plots
set_plot_style()

def app():
    st.title("Experiment 9: Classifiers")
    
    # Selection menu for classifier type
    classifier_type = st.radio("Select Classifier Type:", ["Cone Classifier", "Thickener"])
    
    if classifier_type == "Cone Classifier":
        cone_classifier_app()
    else:
        thickener_app()

def cone_classifier_app():
    st.header("Cone Classifier")
    
    st.markdown("""
    ## Objective
    Study of particle classification using a cone classifier.
    
    ## Aim
    To determine the classification efficiency and cut size of a cone classifier.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Cone Classifier Theory
        
        A cone classifier is a gravity-based separation device used to classify particles based on their settling velocities. It consists of a conical tank where particles are separated based on their size, density, and shape.
        
        The basic principle of operation is based on the balance between the upward velocity of the fluid and the settling velocity of the particles. If a particle's settling velocity is greater than the upward velocity of the fluid, it will settle and report to the underflow; otherwise, it will be carried by the fluid to the overflow.
        
        The settling velocity of a particle can be described by Stokes' Law (for laminar flow conditions):
        
        $$v_s = \\frac{g(\\rho_p - \\rho_f)d^2}{18\\mu}$$
        
        Where:
        - $v_s$ = particle settling velocity (m/s)
        - $g$ = gravitational acceleration (9.81 m/s²)
        - $\\rho_p$ = particle density (kg/m³)
        - $\\rho_f$ = fluid density (kg/m³)
        - $d$ = particle diameter (m)
        - $\\mu$ = fluid viscosity (Pa·s)
        
        The cut size or separation size ($d_{50}$) is the particle size that has a 50% probability of reporting to either the overflow or underflow. It can be estimated by:
        
        $$d_{50} = \\sqrt{\\frac{18\\mu v_u}{g(\\rho_p - \\rho_f)}}$$
        
        Where $v_u$ is the upward velocity of the fluid.
        
        The classification efficiency is typically characterized by the sharpness of separation, which is often quantified using the imperfection value:
        
        $$I = \\frac{d_{75} - d_{25}}{2d_{50}}$$
        
        Where $d_{75}$ and $d_{25}$ are the particle sizes that have 75% and 25% probability of reporting to the underflow, respectively.
        """)
    
    # Input parameters
    st.sidebar.header("Cone Classifier Parameters")
    
    # Operational parameters
    cone_diameter = st.sidebar.slider("Cone diameter (m)", 0.5, 5.0, 2.0, 0.1)
    
    cone_height = st.sidebar.slider("Cone height (m)", 1.0, 10.0, 4.0, 0.5)
    
    feed_rate = st.sidebar.slider("Feed rate (m³/h)", 5, 100, 30, 5)
    
    underflow_rate = st.sidebar.slider("Underflow rate (m³/h)", 1, 50, 10, 1)
    
    # Material properties
    solid_density = st.sidebar.slider("Solid density (kg/m³)", 1500, 5000, 2700, 100)
    
    fluid_density = st.sidebar.slider("Fluid density (kg/m³)", 800, 1500, 1000, 50)
    
    fluid_viscosity = st.sidebar.number_input("Fluid viscosity (Pa·s)", 
                                           min_value=0.0005, max_value=0.05, value=0.001, step=0.0001, format="%.4f")
    
    # Feed characteristics
    pulp_density = st.sidebar.slider("Feed pulp density (% solids by weight)", 5, 40, 20, 1)
    
    # Particle size distribution parameters
    d_min = st.sidebar.slider("Minimum particle size (μm)", 1, 100, 10, 5)
    
    d_max = st.sidebar.slider("Maximum particle size (μm)", 100, 2000, 500, 50)
    
    # Calculate parameters
    # Calculate overflow rate
    overflow_rate = feed_rate - underflow_rate  # m³/h
    
    # Calculate cone volume and area
    cone_radius = cone_diameter / 2
    cone_volume = (1/3) * np.pi * cone_radius**2 * cone_height  # m³
    
    # Calculate residence time
    residence_time = cone_volume / feed_rate  # h
    
    # Calculate upward velocity
    # Simplified - actual velocity varies with height
    # Average cross-sectional area of cone = pi * (cone_radius/2)^2
    average_area = np.pi * (cone_radius/2)**2  # m²
    upward_velocity = overflow_rate / average_area  # m/h
    upward_velocity_mps = upward_velocity / 3600  # m/s
    
    # Calculate theoretical cut size using simplified Stokes' Law
    cut_size_stokes = np.sqrt((18 * fluid_viscosity * upward_velocity_mps) / 
                             (9.81 * (solid_density - fluid_density)))  # m
    cut_size_microns = cut_size_stokes * 1e6  # μm
    
    # Adjust for non-ideal conditions - empirical correction factor
    non_ideal_factor = 1.2  # Typical for cone classifiers
    actual_cut_size = cut_size_microns * non_ideal_factor
    
    # Calculate imperfection
    imperfection = 0.2 + 0.3 * (feed_rate / 50)  # Simplified model - higher flow rates tend to have higher imperfection
    
    # Calculate d25 and d75
    d25 = actual_cut_size * (1 - imperfection)
    d75 = actual_cut_size * (1 + imperfection)
    
    # Generate particle size distribution data
    # Use log-normal distribution for feed
    size_points = np.logspace(np.log10(d_min), np.log10(d_max), 100)
    
    # Parameters for log-normal distribution
    geo_mean = np.sqrt(d_min * d_max)
    geo_std = np.sqrt(d_max / d_min)
    
    # Calculate cumulative distribution function (CDF)
    cdf_feed = 0.5 + 0.5 * np.tanh(np.log(size_points / geo_mean) / np.log(geo_std))
    
    # Calculate partition curve
    # Simplified model: S-shaped curve ranging from 0 to 1
    # Particle size / Cut size determines placement on curve
    partition_curve = 1 / (1 + (actual_cut_size / size_points)**2)
    
    # Calculate mass flow to underflow and overflow for each size fraction
    feed_mass_flow = feed_rate * pulp_density / 100 * fluid_density  # kg/h
    
    # Calculate differential distribution of feed
    diff_feed = np.zeros_like(size_points)
    for i in range(1, len(size_points)):
        diff_feed[i] = cdf_feed[i] - cdf_feed[i-1]
    
    # Calculate flow rates to underflow and overflow for each size fraction
    underflow_dist = diff_feed * partition_curve
    overflow_dist = diff_feed * (1 - partition_curve)
    
    # Normalize to ensure mass balance
    underflow_dist = underflow_dist / np.sum(underflow_dist) * np.sum(diff_feed)
    overflow_dist = overflow_dist / np.sum(overflow_dist) * np.sum(diff_feed)
    
    # Calculate cumulative distributions for underflow and overflow
    cum_underflow = np.cumsum(underflow_dist)
    cum_overflow = np.cumsum(overflow_dist)
    
    # Normalize to 0-100% scale
    cum_underflow = cum_underflow / cum_underflow[-1] * 100
    cum_overflow = cum_overflow / cum_overflow[-1] * 100
    
    # Create dataframe for results
    df = pd.DataFrame({
        'Particle Size (μm)': size_points,
        'Feed CDF (%)': cdf_feed * 100,
        'Partition Coefficient': partition_curve,
        'Underflow CDF (%)': cum_underflow,
        'Overflow CDF (%)': cum_overflow
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Cone volume:** {cone_volume:.2f} m³")
        st.write(f"**Residence time:** {residence_time*60:.2f} min")
        st.write(f"**Upward velocity:** {upward_velocity_mps*1000:.2f} mm/s")
        st.write(f"**Theoretical cut size (Stokes):** {cut_size_microns:.2f} μm")
    
    with col2:
        st.write(f"**Actual cut size (d50):** {actual_cut_size:.2f} μm")
        st.write(f"**d25 value:** {d25:.2f} μm")
        st.write(f"**d75 value:** {d75:.2f} μm")
        st.write(f"**Imperfection:** {imperfection:.3f}")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Partition Curve", "Size Distributions", "Data Table"])
    
    with tab1:
        # Partition curve visualization
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        ax.semilogx(size_points, partition_curve * 100, 'b-')
        
        # Add markers for d25, d50, d75
        ax.axhline(y=50, color='r', linestyle='--')
        ax.axhline(y=25, color='g', linestyle='--')
        ax.axhline(y=75, color='g', linestyle='--')
        
        ax.axvline(x=actual_cut_size, color='r', linestyle='--', 
                  label=f'd50 = {actual_cut_size:.2f} μm')
        ax.axvline(x=d25, color='g', linestyle='--', 
                  label=f'd25 = {d25:.2f} μm')
        ax.axvline(x=d75, color='g', linestyle='--', 
                  label=f'd75 = {d75:.2f} μm')
        
        ax.set_xlabel('Particle Size (μm)')
        ax.set_ylabel('Percent to Underflow (%)')
        ax.set_title('Partition Curve')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
        
        # Fish-hook effect visualization
        st.write("### Fish-hook Effect in Partition Curve")
        
        # Create a modified partition curve with fish-hook effect at fine sizes
        size_points_fh = np.logspace(np.log10(d_min/2), np.log10(d_max), 100)
        
        # Standard partition curve
        partition_std = 1 / (1 + (actual_cut_size / size_points_fh)**2)
        
        # Fish-hook modification for fine particles
        fh_factor = np.exp(-(np.log(size_points_fh) - np.log(actual_cut_size/5))**2 / 2)
        fh_factor = fh_factor * 0.2  # Scale the effect
        
        # Add fish-hook to standard curve
        partition_fh = partition_std + fh_factor
        partition_fh = np.minimum(partition_fh, 1.0)  # Cap at 1.0
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.semilogx(size_points_fh, partition_std * 100, 'b-', label='Ideal')
        ax2.semilogx(size_points_fh, partition_fh * 100, 'r-', label='With Fish-hook Effect')
        
        ax2.set_xlabel('Particle Size (μm)')
        ax2.set_ylabel('Percent to Underflow (%)')
        ax2.set_title('Partition Curve with Fish-hook Effect')
        ax2.grid(True)
        ax2.legend()
        fig.tight_layout()
        st.pyplot(fig2)
        
        st.write("""
        The "fish-hook" effect is a phenomenon observed in some classifiers where the partition curve shows 
        an upturn (hook) at fine particle sizes instead of continuing to decrease smoothly. This can be 
        caused by various factors including:
        
        - Particle aggregation
        - Short-circuiting of fine particles to underflow
        - Entrainment of fine particles in the boundary layer of coarse particles
        
        The fish-hook effect reduces classification efficiency for fine particles.
        """)
    
    with tab2:
        # Size distribution visualization
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.semilogx(size_points, cdf_feed * 100, 'k-', label='Feed')
        ax3.semilogx(size_points, cum_underflow, 'b-', label='Underflow')
        ax3.semilogx(size_points, cum_overflow, 'r-', label='Overflow')
        
        # Add marker for d50
        ax3.axvline(x=actual_cut_size, color='g', linestyle='--', 
                   label=f'd50 = {actual_cut_size:.2f} μm')
        
        ax3.set_xlabel('Particle Size (μm)')
        ax3.set_ylabel('Cumulative Passing (%)')
        ax3.set_title('Size Distributions')
        ax3.grid(True)
        ax3.legend()
        fig.tight_layout()
        st.pyplot(fig3)
        
        # Effect of upward velocity
        st.write("### Effect of Upward Velocity on Cut Size")
        
        velocities = np.linspace(0.5, 2.0, 10) * upward_velocity_mps
        cut_sizes = []
        
        for vel in velocities:
            cs = np.sqrt((18 * fluid_viscosity * vel) / (9.81 * (solid_density - fluid_density))) * 1e6 * non_ideal_factor
            cut_sizes.append(cs)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(velocities * 1000, cut_sizes, 'g-o')
        ax4.axvline(x=upward_velocity_mps * 1000, color='r', linestyle='--', 
                   label=f'Current Velocity: {upward_velocity_mps*1000:.2f} mm/s')
        
        ax4.set_xlabel('Upward Velocity (mm/s)')
        ax4.set_ylabel('Cut Size (μm)')
        ax4.set_title('Effect of Upward Velocity on Cut Size')
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
            "cone_classifier_data.csv",
            "text/csv",
            key='download-csv'
        )
    
    # Cone classifier schematic
    with st.expander("Cone Classifier Schematic"):
        st.markdown("""
        ### Cone Classifier Schematic
        
        ```
                Feed
                 ↓
              ┌─────┐
              │     │
              │     │ ← Overflow
              │     │
              │     │
              │     │
              │     │
              │     │
              └──┬──┘
                 │
                 ↓
              Underflow
        ```
        
        ### Key Components:
        
        - **Feed Entry**: Where slurry is introduced
        - **Cone Section**: Where separation occurs
        - **Overflow Launder**: Collects the fine particles in the overflow
        - **Underflow Discharge**: Where coarse particles exit
        
        ### Operating Principle:
        
        The cone classifier operates based on the balance between the settling velocity of particles and the upward velocity of the fluid:
        
        - Particles with settling velocity > upward fluid velocity report to the underflow
        - Particles with settling velocity < upward fluid velocity report to the overflow
        
        ### Advantages:
        
        - Simple design with no moving parts
        - Low maintenance requirements
        - Relatively low operating costs
        - Effective for certain size ranges
        
        ### Limitations:
        
        - Relatively low capacity
        - Limited control over separation
        - Low efficiency compared to modern classifiers
        - Sensitive to feed variations
        """)

def thickener_app():
    st.header("Thickener")
    
    st.markdown("""
    ## Objective
    Study of solid-liquid separation using a gravity thickener.
    
    ## Aim
    To determine the settling rate, underflow density, and overflow clarity in a thickener.
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Thickener Theory
        
        A thickener is a continuous sedimentation device used to separate solids from liquids using gravity. Its primary function is to increase the solids concentration of a slurry by allowing the solids to settle and removing the clarified liquid.
        
        The operation of a thickener is based on four key zones:
        
        1. **Clarification Zone**: Where clear liquid overflows
        2. **Free Settling Zone**: Where particles settle freely
        3. **Hindered Settling Zone**: Where particle concentration increases and settling is impeded
        4. **Compression Zone**: Where particles form a compacted bed
        
        The design and operation of a thickener is often based on batch settling tests and the concept of unit area, which is defined as:
        
        $$A = \\frac{Q}{u_0}$$
        
        Where:
        - $A$ = thickener area (m²)
        - $Q$ = feed volumetric flow rate (m³/h)
        - $u_0$ = critical settling velocity (m/h)
        
        The critical settling velocity is typically determined from batch settling tests using the Kynch theory or Coe-Clevenger method.
        
        For continuous operation, the underflow solids concentration is governed by:
        
        $$C_u = \\frac{Q_f C_f - Q_o C_o}{Q_u}$$
        
        Where:
        - $C_u$ = underflow solids concentration
        - $C_f$ = feed solids concentration
        - $C_o$ = overflow solids concentration
        - $Q_f$ = feed flow rate
        - $Q_o$ = overflow flow rate
        - $Q_u$ = underflow flow rate
        
        The settling behavior of particles in a thickener is affected by:
        - Particle size, shape, and density
        - Liquid density and viscosity
        - Solids concentration
        - Flocculation and coagulation
        - Temperature
        """)
    
    # Input parameters
    st.sidebar.header("Thickener Parameters")
    
    # Thickener dimensions
    thickener_diameter = st.sidebar.slider("Thickener diameter (m)", 2.0, 30.0, 10.0, 1.0)
    
    thickener_height = st.sidebar.slider("Thickener height (m)", 1.0, 10.0, 4.0, 0.5)
    
    rake_speed = st.sidebar.slider("Rake speed (rpm)", 0.01, 0.5, 0.1, 0.01)
    
    # Feed properties
    feed_rate = st.sidebar.slider("Feed rate (m³/h)", 5, 200, 50, 5)
    
    feed_solids = st.sidebar.slider("Feed solids concentration (% by weight)", 1, 30, 10, 1)
    
    overflow_solids = st.sidebar.slider("Overflow solids (ppm)", 10, 1000, 100, 10)
    
    underflow_solids_target = st.sidebar.slider("Target underflow solids (% by weight)", 20, 70, 50, 5)
    
    # Material properties
    solid_density = st.sidebar.slider("Solid density (kg/m³)", 1500, 5000, 2700, 100)
    
    liquid_density = st.sidebar.slider("Liquid density (kg/m³)", 800, 1500, 1000, 50)
    
    # Particle settling properties
    particle_size = st.sidebar.slider("Average particle size (μm)", 1, 500, 75, 5)
    
    flocculant_dosage = st.sidebar.slider("Flocculant dosage (g/ton)", 0, 300, 50, 10)
    
    # Calculate parameters
    # Calculate thickener area
    thickener_radius = thickener_diameter / 2
    thickener_area = np.pi * thickener_radius**2  # m²
    
    # Calculate unit area loading
    unit_area_loading = feed_rate / thickener_area  # m³/h/m²
    
    # Calculate residence time
    thickener_volume = thickener_area * thickener_height  # m³
    residence_time = thickener_volume / feed_rate  # h
    
    # Convert concentrations
    feed_solids_fraction = feed_solids / 100  # as a fraction
    overflow_solids_fraction = overflow_solids / 1e6  # ppm to fraction
    underflow_solids_target_fraction = underflow_solids_target / 100  # as a fraction
    
    # Calculate settling velocity (based on simplified Stokes' Law and empirical factors)
    particle_diameter = particle_size * 1e-6  # μm to m
    
    # Base settling velocity from Stokes' Law
    fluid_viscosity = 0.001  # Pa·s (water at 20°C)
    stokes_velocity = 9.81 * (solid_density - liquid_density) * particle_diameter**2 / (18 * fluid_viscosity)  # m/s
    
    # Adjust for hindered settling (Richardson-Zaki equation)
    # v = v_0 * (1 - C)^n, where n is typically 4.65 for small particles
    hindered_factor = (1 - feed_solids_fraction)**4.65
    
    # Adjust for flocculation
    floc_factor = 1 + 2 * (flocculant_dosage / 100)**0.5  # Empirical adjustment
    
    # Final settling velocity
    settling_velocity = stokes_velocity * hindered_factor * floc_factor  # m/s
    settling_velocity_mh = settling_velocity * 3600  # m/h
    
    # Calculate underflow rate based on solids balance
    # Qf*Cf = Qu*Cu + Qo*Co
    # Qf = Qu + Qo
    
    feed_solids_flow = feed_rate * feed_solids_fraction  # m³/h * fraction = mass flow
    overflow_solids_flow = feed_rate * overflow_solids_fraction  # Assuming Qo ≈ Qf as typically Qu << Qf
    
    # Calculate required underflow rate
    underflow_rate = (feed_solids_flow - overflow_solids_flow) / underflow_solids_target_fraction  # m³/h
    
    # Calculate overflow rate
    overflow_rate = feed_rate - underflow_rate  # m³/h
    
    # Calculate thickener capacity
    solids_loading = feed_rate * feed_solids_fraction * solid_density  # kg/h
    unit_area_solids_loading = solids_loading / thickener_area  # kg/h/m²
    
    # Check if thickener is overloaded
    # Typical maximum capacity for gravity thickeners
    max_capacity = 100 + flocculant_dosage  # kg/m²/h, increases with flocculant
    
    is_overloaded = unit_area_solids_loading > max_capacity
    
    # Simulate settling test
    # Time points for batch settling test
    settling_times = np.linspace(0, 60, 100)  # minutes
    
    # Height of interface in a settling test (simplified model)
    initial_height = 1.0  # m
    
    # Parameters for settling curve
    settling_rate_initial = settling_velocity * 60  # m/min
    compression_time = 20  # minutes, when compression zone begins to dominate
    final_height = initial_height * (1 - 0.9*feed_solids_fraction / underflow_solids_target_fraction)
    
    # Calculate interface height
    interface_heights = np.zeros_like(settling_times)
    
    for i, t in enumerate(settling_times):
        if t <= compression_time:
            # Free settling zone
            height = initial_height - settling_rate_initial * t
            height = max(height, final_height)  # Don't go below final height
        else:
            # Compression zone - asymptotic approach to final height
            height = final_height + (interface_heights[np.where(settling_times == compression_time)[0][0]] - final_height) * np.exp(-(t - compression_time) / 10)
        
        interface_heights[i] = height
    
    # Calculate settling rates
    settling_rates = np.zeros_like(settling_times)
    for i in range(1, len(settling_times)):
        dt = settling_times[i] - settling_times[i-1]
        dh = interface_heights[i-1] - interface_heights[i]
        if dt > 0:
            settling_rates[i] = dh / dt  # m/min
    
    # Create dataframe for batch settling test results
    df_batch = pd.DataFrame({
        'Time (min)': settling_times,
        'Interface Height (m)': interface_heights,
        'Settling Rate (m/min)': settling_rates
    })
    
    # Create dataframe for continuous thickener results
    # Simulate multiple heights in thickener
    heights = np.linspace(0, thickener_height, 20)
    
    # Calculate solids concentration at different heights
    # Simplified model - concentration increases exponentially towards the bottom
    solids_conc = np.zeros_like(heights)
    
    for i, h in enumerate(heights):
        if h < 0.1 * thickener_height:  # Clarification zone
            solids_conc[i] = overflow_solids_fraction * 100  # convert to %
        elif h < 0.3 * thickener_height:  # Free settling zone
            factor = (h - 0.1*thickener_height) / (0.2*thickener_height)
            solids_conc[i] = overflow_solids_fraction * 100 + factor * (feed_solids - overflow_solids_fraction * 100)
        elif h < 0.7 * thickener_height:  # Hindered settling zone
            factor = (h - 0.3*thickener_height) / (0.4*thickener_height)
            solids_conc[i] = feed_solids + factor * (underflow_solids_target - feed_solids)
        else:  # Compression zone
            solids_conc[i] = underflow_solids_target
    
    # Create dataframe for continuous thickener results
    df_continuous = pd.DataFrame({
        'Height from Bottom (m)': thickener_height - heights,
        'Solids Concentration (%)': solids_conc
    })
    
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Thickener area:** {thickener_area:.2f} m²")
        st.write(f"**Unit area loading:** {unit_area_loading:.2f} m³/h/m²")
        st.write(f"**Solids loading:** {unit_area_solids_loading:.2f} kg/h/m²")
        
        if is_overloaded:
            st.error(f"**Thickener is overloaded!** Maximum capacity: {max_capacity:.2f} kg/h/m²")
        else:
            st.success(f"**Thickener capacity is adequate.** Maximum capacity: {max_capacity:.2f} kg/h/m²")
    
    with col2:
        st.write(f"**Settling velocity:** {settling_velocity_mh:.4f} m/h")
        st.write(f"**Underflow rate:** {underflow_rate:.2f} m³/h")
        st.write(f"**Overflow rate:** {overflow_rate:.2f} m³/h")
        st.write(f"**Residence time:** {residence_time*60:.2f} min")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Batch Settling Test", "Continuous Operation", "Data Table"])
    
    with tab1:
        # Batch settling test visualization
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        ax.plot(settling_times, interface_heights, 'b-')
        
        # Mark the compression point
        ax.axvline(x=compression_time, color='r', linestyle='--', 
                 label=f'Compression Zone Start: {compression_time} min')
        
        ax.set_xlabel('Time (min)')
        ax.set_ylabel('Interface Height (m)')
        ax.set_title('Batch Settling Test')
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=True, fancybox=True, shadow=True)
        fig.tight_layout()
        st.pyplot(fig)
        
        # Settling velocity curve
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        
        ax2.plot(settling_times, settling_rates, 'g-')
        
        # Mark the compression point
        ax2.axvline(x=compression_time, color='r', linestyle='--', 
                  label=f'Compression Zone Start: {compression_time} min')
        
        ax2.set_xlabel('Time (min)')
        ax2.set_ylabel('Settling Rate (m/min)')
        ax2.set_title('Settling Rate vs Time')
        ax2.grid(True)
        ax2.legend()
        fig.tight_layout()
        st.pyplot(fig2)
        
        st.write("""
        ### Interpretation of Batch Settling Test:
        
        The batch settling test provides essential information for thickener design:
        
        1. **Initial Settling Rate**: Indicates the maximum settling velocity of the suspension
        2. **Compression Point**: Where the suspension transitions from hindered settling to compression
        3. **Final Compacted Height**: Indicates the maximum achievable solids concentration
        
        The critical settling velocity for thickener design is typically taken at the feed concentration 
        or at the compression point, depending on the design method used.
        """)
    
    with tab2:
        # Continuous thickener visualization
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        
        ax3.plot(solids_conc, thickener_height - heights, 'b-')
        
        # Mark the zones
        zone_heights = [0.7, 0.3, 0.1, 0.0]
        zone_names = ['Compression', 'Hindered Settling', 'Free Settling', 'Clarification']
        zone_colors = ['red', 'orange', 'green', 'blue']
        
        for i in range(len(zone_heights)-1):
            ax3.axhspan(zone_heights[i+1]*thickener_height, zone_heights[i]*thickener_height, 
                       alpha=0.2, color=zone_colors[i])
            ax3.text(np.max(solids_conc)*0.5, (zone_heights[i+1] + (zone_heights[i]-zone_heights[i+1])/2)*thickener_height, 
                    zone_names[i], ha='center', va='center')
        
        ax3.set_xlabel('Solids Concentration (%)')
        ax3.set_ylabel('Height from Bottom (m)')
        ax3.set_title('Solids Concentration Profile in Thickener')
        ax3.grid(True)
        fig.tight_layout()
        st.pyplot(fig3)
        
        # Effect of flocculant dosage
        st.write("### Effect of Flocculant Dosage on Settling Velocity")
        
        flocculant_range = np.linspace(0, 300, 10)
        settling_velocities = []
        
        for dosage in flocculant_range:
            floc_factor_test = 1 + 2 * (dosage / 100)**0.5
            vel = stokes_velocity * hindered_factor * floc_factor_test * 3600  # m/h
            settling_velocities.append(vel)
        
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        ax4.plot(flocculant_range, settling_velocities, 'g-o')
        ax4.axvline(x=flocculant_dosage, color='r', linestyle='--', 
                   label=f'Current Dosage: {flocculant_dosage} g/ton')
        
        ax4.set_xlabel('Flocculant Dosage (g/ton)')
        ax4.set_ylabel('Settling Velocity (m/h)')
        ax4.set_title('Effect of Flocculant Dosage on Settling Velocity')
        ax4.grid(True)
        ax4.legend()
        fig.tight_layout()
        st.pyplot(fig4)
    
    with tab3:
        # Display data tables
        st.write("### Batch Settling Test Data")
        # Sample at regular intervals for clarity
        sample_indices = np.linspace(0, len(df_batch)-1, 15).astype(int)
        st.dataframe(df_batch.iloc[sample_indices].reset_index(drop=True))
        
        st.write("### Continuous Thickener Data")
        st.dataframe(df_continuous)
        
        # Download links for full data
        csv_batch = df_batch.to_csv(index=False)
        st.download_button(
            "Download Batch Test Data as CSV",
            csv_batch,
            "thickener_batch_test_data.csv",
            "text/csv",
            key='download-batch-csv'
        )
        
        csv_continuous = df_continuous.to_csv(index=False)
        st.download_button(
            "Download Continuous Operation Data as CSV",
            csv_continuous,
            "thickener_continuous_data.csv",
            "text/csv",
            key='download-continuous-csv'
        )
    
    # Thickener schematic
    with st.expander("Thickener Schematic"):
        st.markdown("""
        ### Thickener Schematic
        
        ```
                           Feed
                            ↓
            ┌───────────────┼───────────────┐
            │        Overflow Launder       │
            │      ┌───────────┐            │
            │      │ Feedwell  │            │
            │      └───────────┘            │
            │                               │
            │         Clarification         │
            │            Zone               │
            │                               │
            │         Free Settling         │
            │            Zone               │
            │                               │
            │       Hindered Settling       │
            │            Zone               │
            │                               │
            │         Compression           │
            │            Zone               │
            │       ┌───────────┐           │
            │       │   Rake    │           │
            └───────┴───────────┴───────────┘
                           ↓
                        Underflow
        ```
        
        ### Key Components:
        
        - **Feedwell**: Distributes feed and dissipates energy
        - **Overflow Launder**: Collects clarified liquid
        - **Rake**: Moves settled solids to discharge point
        - **Underflow Discharge**: Where thickened slurry exits
        
        ### Zones in a Thickener:
        
        1. **Clarification Zone**: Clear liquid at the top
        2. **Free Settling Zone**: Particles settle individually
        3. **Hindered Settling Zone**: Particles interfere with each other's settling
        4. **Compression Zone**: Particles form a networked bed that compresses
        
        ### Advantages:
        
        - Continuous operation
        - Large capacity
        - Low operating costs
        - Effective for many applications
        
        ### Applications:
        
        - Mineral processing
        - Wastewater treatment
        - Chemical processing
        - Pulp and paper industry
        """)
