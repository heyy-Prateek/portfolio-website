import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def app():
    st.title("Experiment 5: Crushers and Ball Mill")
    
    st.markdown("""
    ## Objective
    Study of size reduction equipment and analysis of crusher performance.
    
    ## Aim
    To determine the crushing efficiency, reduction ratio, and power consumption of different crushers.
    
    ## Types of Crushers
    1. Jaw Crusher
    2. Roll Crusher
    3. Ball Mill
    """)
    
    # Theory section with expandable detail
    with st.expander("Show Theory"):
        st.markdown("""
        ### Size Reduction Theory
        
        Size reduction operations are aimed at reducing the size of solid materials. The energy required for size reduction depends on the feed material properties, initial particle size, and final particle size.
        
        Three main laws govern the energy requirements for size reduction:
        
        1. **Kick's Law**: The energy required is proportional to the reduction in volume.
            $$E = K_1 \\log\\left(\\frac{L_1}{L_2}\\right)$$
        
        2. **Rittinger's Law**: The energy required is proportional to the new surface area created.
            $$E = K_2 \\left(\\frac{1}{L_2} - \\frac{1}{L_1}\\right)$$
        
        3. **Bond's Law**: The energy required is proportional to the new crack tip length created.
            $$E = K_3 \\left(\\frac{1}{\\sqrt{L_2}} - \\frac{1}{\\sqrt{L_1}}\\right)$$
        
        Where:
        - $E$ = energy required per unit mass
        - $L_1$ = initial particle size
        - $L_2$ = final particle size
        - $K_1, K_2, K_3$ = material-specific constants
        
        ### Size Reduction Equipment
        
        **Jaw Crusher**:
        - Consists of a fixed jaw and a movable jaw
        - Material is crushed as the movable jaw approaches the fixed jaw
        - Suitable for hard materials
        - High reduction ratio (5:1 to 8:1)
        
        **Roll Crusher**:
        - Consists of two parallel rolls rotating in opposite directions
        - Material is drawn between the rolls and crushed
        - Suitable for medium-hard materials
        - Lower reduction ratio (2:1 to 4:1)
        - Produces more uniform product
        
        **Ball Mill**:
        - Rotating cylindrical shell partially filled with grinding balls
        - Material is ground by impact and attrition
        - Used for fine grinding
        - High reduction ratio
        - Wet or dry operation
        
        ### Performance Parameters
        
        **Reduction Ratio**:
        $$R = \\frac{D_{80\\text{ feed}}}{D_{80\\text{ product}}}$$
        
        Where:
        - $D_{80\\text{ feed}}$ = 80% passing size of feed
        - $D_{80\\text{ product}}$ = 80% passing size of product
        
        **Crushing Efficiency**:
        $$\\eta = \\frac{\\text{Theoretical energy}}{{\\text{Actual energy}}} \\times 100\\%$$
        
        **Work Index (Bond)**:
        $$W_i = \\frac{10 W}{\\left(\\frac{1}{\\sqrt{P_{80}}} - \\frac{1}{\\sqrt{F_{80}}}\\right)}$$
        
        Where:
        - $W_i$ = work index (kWh/ton)
        - $W$ = specific energy consumption (kWh/ton)
        - $P_{80}$ = 80% passing size of product (μm)
        - $F_{80}$ = 80% passing size of feed (μm)
        """)
    
    # Choose crusher type
    crusher_type = st.selectbox("Select Crusher Type:", ["Jaw Crusher", "Roll Crusher", "Ball Mill"])
    
    # Input parameters - common for all crushers
    st.sidebar.header("Crusher Parameters")
    
    # Feed parameters
    feed_rate = st.sidebar.number_input("Feed rate (kg/h)", 
                                     min_value=10.0, max_value=5000.0, value=1000.0, step=10.0)
    
    # Material specific parameters
    material_density = st.sidebar.number_input("Material density (kg/m³)", 
                                            min_value=1000.0, max_value=5000.0, value=2600.0, step=100.0)
    
    material_hardness = st.sidebar.slider("Material hardness (Mohs scale)", 1, 10, 5, 1)
    
    # Bond Work Index - higher for harder materials
    bond_work_index = material_hardness * 5  # Approximate value based on hardness
    
    # Specific parameters for each crusher type
    if crusher_type == "Jaw Crusher":
        feed_size = st.sidebar.slider("Maximum feed size (mm)", 50, 500, 200, 10)
        jaw_opening = st.sidebar.slider("Jaw opening (mm)", 20, 150, 40, 5)
        jaw_length = st.sidebar.number_input("Jaw length (mm)", 
                                           min_value=200.0, max_value=2000.0, value=600.0, step=50.0)
        jaw_width = st.sidebar.number_input("Jaw width (mm)", 
                                          min_value=200.0, max_value=1500.0, value=400.0, step=50.0)
        motor_power = st.sidebar.slider("Motor power (kW)", 5, 100, 30, 5)
        eccentric_speed = st.sidebar.slider("Eccentric shaft speed (rpm)", 100, 400, 250, 10)
        
        # Approximation for product size
        product_size = jaw_opening * 0.8  # A common approximation for jaw crushers
        
        # Reduction ratio
        reduction_ratio = feed_size / product_size
        
        # Energy calculation using Bond's law
        specific_energy = bond_work_index * (1/np.sqrt(product_size/1000) - 1/np.sqrt(feed_size/1000))  # kWh/ton
        
        # Theoretical power requirement
        theoretical_power = specific_energy * feed_rate / 1000  # kW
        
        # Efficiency
        efficiency = (theoretical_power / motor_power) * 100
        
        # Capacity calculation
        capacity = feed_rate / 1000  # tons/h
        
        # Calculate crusher throughput
        throughput = jaw_length * jaw_width * eccentric_speed * jaw_opening / 1e6  # Approximate throughput formula
        
    elif crusher_type == "Roll Crusher":
        feed_size = st.sidebar.slider("Maximum feed size (mm)", 10, 100, 40, 5)
        roll_diameter = st.sidebar.slider("Roll diameter (mm)", 200, 1000, 500, 50)
        roll_length = st.sidebar.number_input("Roll length (mm)", 
                                           min_value=200.0, max_value=1500.0, value=500.0, step=50.0)
        roll_gap = st.sidebar.slider("Roll gap (mm)", 1, 30, 10, 1)
        roll_speed = st.sidebar.slider("Roll speed (rpm)", 50, 300, 150, 10)
        motor_power = st.sidebar.slider("Motor power (kW)", 5, 80, 20, 5)
        
        # Approximation for product size
        product_size = roll_gap * 1.2  # A common approximation for roll crushers
        
        # Reduction ratio
        reduction_ratio = feed_size / product_size
        
        # Energy calculation using Bond's law
        specific_energy = bond_work_index * (1/np.sqrt(product_size/1000) - 1/np.sqrt(feed_size/1000))  # kWh/ton
        
        # Theoretical power requirement
        theoretical_power = specific_energy * feed_rate / 1000  # kW
        
        # Efficiency
        efficiency = (theoretical_power / motor_power) * 100
        
        # Capacity calculation
        capacity = feed_rate / 1000  # tons/h
        
        # Calculate crusher throughput
        nip_angle = np.arccos(1 - feed_size / roll_diameter) * (180 / np.pi)
        throughput = roll_length * roll_speed * roll_gap * material_density / 60 / 1e6  # tons/h
        
    else:  # Ball Mill
        feed_size = st.sidebar.slider("Maximum feed size (mm)", 1, 20, 5, 1)
        mill_diameter = st.sidebar.slider("Mill diameter (m)", 0.5, 5.0, 2.0, 0.1)
        mill_length = st.sidebar.slider("Mill length (m)", 0.5, 8.0, 3.0, 0.1)
        ball_size = st.sidebar.slider("Ball size (mm)", 20, 100, 40, 5)
        mill_speed_percent = st.sidebar.slider("Mill speed (% of critical)", 60, 90, 75, 1)
        mill_fill_percent = st.sidebar.slider("Mill filling (%)", 30, 45, 35, 1)
        motor_power = st.sidebar.slider("Motor power (kW)", 10, 500, 150, 10)
        
        # Critical speed calculation
        critical_speed = 42.3 / np.sqrt(mill_diameter - ball_size/1000)  # rpm
        mill_speed = mill_speed_percent * critical_speed / 100  # rpm
        
        # Approximation for product size
        # Ball mill can achieve very fine grinding
        product_size = feed_size * 0.05  # An approximation for ball mills
        
        # Reduction ratio
        reduction_ratio = feed_size / product_size
        
        # Energy calculation using Bond's law
        specific_energy = bond_work_index * (1/np.sqrt(product_size/1000) - 1/np.sqrt(feed_size/1000))  # kWh/ton
        
        # Theoretical power requirement
        theoretical_power = specific_energy * feed_rate / 1000  # kW
        
        # Efficiency
        efficiency = (theoretical_power / motor_power) * 100
        
        # Capacity calculation
        capacity = feed_rate / 1000  # tons/h
        
        # Calculate mill power using empirical formula
        mill_volume = np.pi * (mill_diameter/2)**2 * mill_length  # m³
        mill_filling = mill_fill_percent / 100
        mill_power = 10.6 * mill_volume * mill_filling * material_density * 0.5 * (mill_speed_percent/100)  # kW
        
    # Main experiment area
    st.header("Simulation Results")
    
    # Display key parameters
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Feed size:** {feed_size:.1f} mm")
        st.write(f"**Product size:** {product_size:.2f} mm")
        st.write(f"**Reduction ratio:** {reduction_ratio:.2f}")
        st.write(f"**Bond work index:** {bond_work_index:.1f} kWh/ton")
    
    with col2:
        st.write(f"**Specific energy consumption:** {specific_energy:.2f} kWh/ton")
        st.write(f"**Theoretical power requirement:** {theoretical_power:.2f} kW")
        st.write(f"**Motor power:** {motor_power:.1f} kW")
        st.write(f"**Crushing efficiency:** {efficiency:.2f}%")
    
    # Create tabs for different displays
    tab1, tab2, tab3 = st.tabs(["Size Distribution", "Power Analysis", "Performance Curves"])
    
    with tab1:
        # Generate sample size distribution data
        # Feed size distribution (log-normal)
        size_range = np.logspace(np.log10(product_size/10), np.log10(feed_size*1.5), 50)
        
        # Feed cumulative distribution (assumed log-normal)
        def log_normal_cdf(x, mu, sigma):
            return 0.5 + 0.5 * np.tanh((np.log(x) - mu) / (sigma * np.sqrt(2)))
        
        # Fit parameters for feed
        feed_mu = np.log(feed_size/2)
        feed_sigma = 0.5
        
        # Fit parameters for product
        product_mu = np.log(product_size/2)
        product_sigma = 0.6  # Product usually has wider distribution
        
        # Generate distributions
        feed_cumulative = log_normal_cdf(size_range, feed_mu, feed_sigma) * 100
        product_cumulative = log_normal_cdf(size_range, product_mu, product_sigma) * 100
        
        # Find D80 values
        feed_d80 = np.interp(80, feed_cumulative, size_range)
        product_d80 = np.interp(80, product_cumulative, size_range)
        
        # Calculate actual reduction ratio using D80
        actual_reduction_ratio = feed_d80 / product_d80
        
        # Size distribution plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.semilogx(size_range, feed_cumulative, 'b-', label='Feed')
        ax.semilogx(size_range, product_cumulative, 'r-', label='Product')
        ax.axhline(y=80, color='g', linestyle='--')
        ax.axvline(x=feed_d80, color='b', linestyle='--')
        ax.axvline(x=product_d80, color='r', linestyle='--')
        
        ax.set_xlabel('Particle Size (mm)')
        ax.set_ylabel('Cumulative Passing (%)')
        ax.set_title('Size Distribution Analysis')
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
        
        st.write(f"**Feed D80:** {feed_d80:.2f} mm")
        st.write(f"**Product D80:** {product_d80:.2f} mm")
        st.write(f"**Actual reduction ratio (using D80):** {actual_reduction_ratio:.2f}")
    
    with tab2:
        # Power analysis and energy consumption
        # Create data for different feed rates
        feed_rates = np.linspace(feed_rate * 0.5, feed_rate * 1.5, 10)
        power_requirements = []
        
        for rate in feed_rates:
            power_req = specific_energy * rate / 1000  # kW
            power_requirements.append(power_req)
        
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        ax2.plot(feed_rates, power_requirements, 'b-')
        ax2.axhline(y=motor_power, color='r', linestyle='--', label=f'Available Power: {motor_power} kW')
        ax2.axvline(x=feed_rate, color='g', linestyle='--', label=f'Design Feed Rate: {feed_rate} kg/h')
        
        ax2.set_xlabel('Feed Rate (kg/h)')
        ax2.set_ylabel('Power Requirement (kW)')
        ax2.set_title('Power Requirement vs Feed Rate')
        ax2.grid(True)
        ax2.legend()
        st.pyplot(fig2)
        
        # Energy consumption vs reduction ratio
        reduction_ratios = np.linspace(1.5, feed_size/product_size * 1.5, 20)
        energy_consumptions = []
        
        for ratio in reduction_ratios:
            product_size_temp = feed_size / ratio
            energy = bond_work_index * (1/np.sqrt(product_size_temp/1000) - 1/np.sqrt(feed_size/1000))
            energy_consumptions.append(energy)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        ax3.plot(reduction_ratios, energy_consumptions, 'r-')
        ax3.axvline(x=reduction_ratio, color='g', linestyle='--', 
                   label=f'Current Reduction Ratio: {reduction_ratio:.2f}')
        
        ax3.set_xlabel('Reduction Ratio')
        ax3.set_ylabel('Specific Energy Consumption (kWh/ton)')
        ax3.set_title('Energy Consumption vs Reduction Ratio')
        ax3.grid(True)
        ax3.legend()
        st.pyplot(fig3)
    
    with tab3:
        # Performance curves specific to each crusher type
        if crusher_type == "Jaw Crusher":
            # Capacity vs feed size
            feed_sizes = np.linspace(feed_size * 0.5, feed_size * 1.5, 10)
            capacities = []
            
            for size in feed_sizes:
                # Simplified model
                relative_capacity = 0.6 + 0.4 * size / feed_size  # Relative capacity factor
                cap = throughput * relative_capacity
                capacities.append(cap)
            
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            ax4.plot(feed_sizes, capacities, 'b-')
            ax4.axvline(x=feed_size, color='g', linestyle='--', 
                       label=f'Design Feed Size: {feed_size} mm')
            
            ax4.set_xlabel('Feed Size (mm)')
            ax4.set_ylabel('Capacity (tons/h)')
            ax4.set_title('Jaw Crusher: Capacity vs Feed Size')
            ax4.grid(True)
            ax4.legend()
            st.pyplot(fig4)
            
            # Effect of eccentric speed
            speeds = np.linspace(100, 400, 10)
            capacities_speed = []
            
            for speed in speeds:
                cap = jaw_length * jaw_width * speed * jaw_opening / 1e6
                capacities_speed.append(cap)
            
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            ax5.plot(speeds, capacities_speed, 'r-')
            ax5.axvline(x=eccentric_speed, color='g', linestyle='--', 
                       label=f'Current Speed: {eccentric_speed} rpm')
            
            ax5.set_xlabel('Eccentric Shaft Speed (rpm)')
            ax5.set_ylabel('Capacity (theoretical units)')
            ax5.set_title('Jaw Crusher: Effect of Eccentric Speed')
            ax5.grid(True)
            ax5.legend()
            st.pyplot(fig5)
            
        elif crusher_type == "Roll Crusher":
            # Effect of roll gap
            gaps = np.linspace(1, 30, 10)
            product_sizes = gaps * 1.2
            reduction_ratios_gap = feed_size / product_sizes
            
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            ax4.plot(gaps, reduction_ratios_gap, 'b-')
            ax4.axvline(x=roll_gap, color='g', linestyle='--', 
                       label=f'Current Gap: {roll_gap} mm')
            
            ax4.set_xlabel('Roll Gap (mm)')
            ax4.set_ylabel('Reduction Ratio')
            ax4.set_title('Roll Crusher: Effect of Roll Gap on Reduction Ratio')
            ax4.grid(True)
            ax4.legend()
            st.pyplot(fig4)
            
            # Effect of roll speed
            speeds = np.linspace(50, 300, 10)
            throughputs = []
            
            for speed in speeds:
                throughput_temp = roll_length * speed * roll_gap * material_density / 60 / 1e6
                throughputs.append(throughput_temp)
            
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            ax5.plot(speeds, throughputs, 'r-')
            ax5.axvline(x=roll_speed, color='g', linestyle='--', 
                       label=f'Current Speed: {roll_speed} rpm')
            
            ax5.set_xlabel('Roll Speed (rpm)')
            ax5.set_ylabel('Throughput (tons/h)')
            ax5.set_title('Roll Crusher: Effect of Roll Speed on Throughput')
            ax5.grid(True)
            ax5.legend()
            st.pyplot(fig5)
            
        else:  # Ball Mill
            # Effect of mill speed
            speed_percents = np.linspace(60, 90, 10)
            mill_powers = []
            
            for speed_pct in speed_percents:
                relative_factor = -4 * (speed_pct/100 - 0.5)**2 + 1  # Empirical relation
                power = 10.6 * mill_volume * mill_filling * material_density * 0.5 * (speed_pct/100) * relative_factor
                mill_powers.append(power)
            
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            ax4.plot(speed_percents, mill_powers, 'b-')
            ax4.axvline(x=mill_speed_percent, color='g', linestyle='--', 
                       label=f'Current Speed: {mill_speed_percent}% of critical')
            
            ax4.set_xlabel('Mill Speed (% of critical)')
            ax4.set_ylabel('Mill Power (kW)')
            ax4.set_title('Ball Mill: Effect of Mill Speed on Power Consumption')
            ax4.grid(True)
            ax4.legend()
            st.pyplot(fig4)
            
            # Effect of mill filling
            fill_percents = np.linspace(20, 50, 10)
            mill_powers_fill = []
            
            for fill_pct in fill_percents:
                fill = fill_pct / 100
                power = 10.6 * mill_volume * fill * material_density * 0.5 * (mill_speed_percent/100)
                mill_powers_fill.append(power)
            
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            ax5.plot(fill_percents, mill_powers_fill, 'r-')
            ax5.axvline(x=mill_fill_percent, color='g', linestyle='--', 
                       label=f'Current Filling: {mill_fill_percent}%')
            
            ax5.set_xlabel('Mill Filling (%)')
            ax5.set_ylabel('Mill Power (kW)')
            ax5.set_title('Ball Mill: Effect of Mill Filling on Power Consumption')
            ax5.grid(True)
            ax5.legend()
            st.pyplot(fig5)
    
    # Schematic diagram section
    with st.expander("Crusher Schematic"):
        if crusher_type == "Jaw Crusher":
            st.markdown("""
            ### Jaw Crusher Schematic
            
            ```
                   ┌─────────┐
                   │         │ ← Feed
                   │ ┌─────┐ │
                   │ │     │ │
                   │ │     │ │
                   │ │     │ │
                   │ │     │ │
                 ┌─┘ └─────┘ └─┐
                 │             │
                 └──────┬──────┘
                        ↓
                     Product
            ```
            
            **Working Principle:**
            - Material is fed from the top
            - One jaw is fixed, the other moves back and forth
            - Material is crushed as it moves down between the jaws
            - Product exits from the bottom
            """)
        elif crusher_type == "Roll Crusher":
            st.markdown("""
            ### Roll Crusher Schematic
            
            ```
                        Feed
                         ↓
                     ┌───────┐
                     │       │
                 ┌───┼───┐   │
                 │   │   │   │
                 │ ◄─┼─► │   │
                 │   │   │   │
                 └───┼───┘   │
                     │       │
                     └───────┘
                         ↓
                      Product
            ```
            
            **Working Principle:**
            - Material is fed from the top
            - Two rollers rotate in opposite directions
            - The gap between rollers determines product size
            - Material is crushed as it passes between the rollers
            - Product exits from the bottom
            """)
        else:  # Ball Mill
            st.markdown("""
            ### Ball Mill Schematic
            
            ```
                Feed    
                 ↓      
             ┌────────────────────────┐
             │  o  o   o   o   o      │
             │ o    o   o  o   o   o  │ ← Rotating Drum
             │o  o  oo o oo  o o  o o │
             │ o o  o o o  o   o  o   │
             └────────────────────────┘
                         ↓
                      Product
            ```
            
            **Working Principle:**
            - Material is fed into a rotating drum containing grinding media (balls)
            - As the drum rotates, the balls are lifted and then fall, crushing the material
            - Size reduction occurs through impact and attrition
            - The product is discharged through a grate or overflow
            """)
        
        st.write(f"""
        ### Key Performance Parameters for {crusher_type}:
        
        1. **Feed Size**: Maximum size of material that can be processed
        2. **Product Size**: Size of the crushed material after processing
        3. **Reduction Ratio**: Ratio of feed size to product size
        4. **Capacity**: Amount of material that can be processed per unit time
        5. **Power Consumption**: Energy required to operate the crusher
        6. **Efficiency**: Ratio of theoretical to actual power consumption
        """)
