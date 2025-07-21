import matplotlib.pyplot as plt
import numpy as np
import os

def create_batch_reactor_images(output_dir="videos"):
    """Create a series of images for batch reactor
    
    Args:
        output_dir (str): Directory to save images
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Times to snapshot
    times = [0, 2, 5, 10]
    
    for t in times:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle(f"Batch Reactor at t = {t} minutes", fontsize=14)
        
        # First-order reaction kinetics
        k = 0.3  # Rate constant
        C0 = 1.0  # Initial concentration
        
        # Calculate concentration
        concentration = C0 * np.exp(-k * t)
        
        # Calculate conversion
        conversion = 1 - concentration / C0
        
        # Plot 1: Reactor diagram
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.set_aspect('equal')
        ax1.axis('off')
        
        # Draw reactor vessel
        vessel = plt.Rectangle((3, 2), 4, 6, ec='black', fc='#d1e0e0', lw=2)
        ax1.add_patch(vessel)
        
        # Draw inlet and outlet
        ax1.plot([3, 1], [7, 7], 'k-', lw=2)
        ax1.plot([7, 9], [3, 3], 'k-', lw=2)
        
        # Add valves
        inlet_valve = plt.Rectangle((1.5, 6.5), 0.5, 1, ec='black', fc='red', lw=1)
        outlet_valve = plt.Rectangle((8, 2.5), 0.5, 1, ec='black', fc='red', lw=1)
        ax1.add_patch(inlet_valve)
        ax1.add_patch(outlet_valve)
        
        # Add labels
        ax1.text(1, 7.5, 'Feed Inlet', fontsize=8)
        ax1.text(8, 2, 'Product Outlet', fontsize=8)
        ax1.text(5, 1, 'Batch Reactor', fontsize=10, ha='center')
        
        # Draw stirrer
        ax1.plot([5, 5], [8, 4], 'k-', lw=2)
        ax1.plot([4, 6], [4, 4], 'k-', lw=2)
        
        # Draw fluid with color based on conversion
        r = 0.5 * conversion
        g = 0.7
        b = 0.8 * (1 - conversion)
        fluid = plt.Rectangle((3, 2), 4, 6, fc=(r, g, b), alpha=0.7)
        ax1.add_patch(fluid)
        
        # Add reaction progress text
        ax1.text(5, 9, f"Conversion: {conversion:.2f}", fontsize=12, ha='center')
        ax1.text(5, 8.5, f"Concentration: {concentration:.2f} mol/L", fontsize=10, ha='center')
        
        # Plot 2: Concentration vs time
        time_range = np.linspace(0, 10, 100)
        conc_range = C0 * np.exp(-k * time_range)
        
        ax2.plot(time_range, conc_range, 'b-')
        ax2.plot(time_range, C0 - conc_range, 'g-')  # Product concentration
        
        # Mark current time
        if t > 0:
            current_conc = C0 * np.exp(-k * t)
            current_prod = C0 - current_conc
            ax2.plot(t, current_conc, 'bo', markersize=8)
            ax2.plot(t, current_prod, 'go', markersize=8)
        
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 1.1)
        ax2.set_xlabel('Time (min)')
        ax2.set_ylabel('Concentration (mol/L)')
        ax2.set_title('Concentration vs. Time')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend(['Reactant', 'Product'])
        
        plt.tight_layout()
        
        # Save figure
        filename = f"{output_dir}/batch_reactor_t{t}.png"
        plt.savefig(filename, dpi=100)
        plt.close()
        
        print(f"Created batch reactor image: {filename}")

def create_pfr_images(output_dir="videos"):
    """Create a series of images for PFR
    
    Args:
        output_dir (str): Directory to save images
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Different flow rates to demonstrate
    flow_rates = [0.5, 1.0, 2.0, 3.0]  # in arbitrary units
    
    for flow_rate in flow_rates:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Plug Flow Reactor with Flow Rate = {flow_rate} units", fontsize=14)
        
        # First-order reaction kinetics parameters
        k = 2.0  # Rate constant
        C0 = 1.0  # Initial concentration
        
        # Calculate residence time (inversely proportional to flow rate)
        tau = 2.0 / flow_rate  # residence time
        
        # Plot 1: Reactor diagram
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 3)
        ax1.axis('off')
        
        # Draw PFR tube
        rect = plt.Rectangle((1, 1), 8, 1, ec='black', fc='#d1d1e0', lw=2)
        ax1.add_patch(rect)
        
        # Draw inlet and outlet arrows
        ax1.arrow(0.5, 1.5, 0.4, 0, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
        ax1.arrow(9.1, 1.5, 0.4, 0, head_width=0.2, head_length=0.1, fc='green', ec='green')
        
        # Add labels
        ax1.text(0.5, 1.8, f'Feed\nC₀={C0}', fontsize=8)
        
        # Calculate outlet concentration
        C_out = C0 * np.exp(-k * tau)
        conversion = 1 - C_out / C0
        ax1.text(9.2, 1.8, f'Product\nC={C_out:.2f}\nX={conversion:.2f}', fontsize=8)
        
        ax1.text(5, 0.5, 'Plug Flow Reactor', fontsize=10, ha='center')
        
        # Add flow rate indicator
        ax1.text(5, 2.5, f"Flow Rate: {flow_rate} units", fontsize=10, ha='center')
        
        # Color gradient to represent concentration along the reactor
        for i in range(40):
            x = 1 + i * 0.2
            z_L = i / 40  # dimensionless position
            
            # Calculate local concentration
            local_C = C0 * np.exp(-k * tau * z_L)
            local_conv = 1 - local_C / C0
            
            # Color based on conversion
            r = min(1, 0.2 + local_conv * 0.8)
            g = min(1, 0.5 + local_conv * 0.5)
            b = max(0, 1 - local_conv)
            
            rect = plt.Rectangle((x, 1), 0.2, 1, ec=None, fc=(r, g, b), alpha=0.7)
            ax1.add_patch(rect)
        
        # Plot 2: Concentration profile
        positions = np.linspace(0, 1, 100)  # dimensionless length
        conc_profile = C0 * np.exp(-k * tau * positions)
        conv_profile = 1 - conc_profile / C0
        
        ax2.plot(positions, conc_profile, 'b-')
        ax2.plot(positions, conv_profile, 'r-')
        
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1.1)
        ax2.set_xlabel('Position (z/L)')
        ax2.set_ylabel('Concentration (C/C₀) or Conversion (X)')
        ax2.set_title('Concentration and Conversion Profiles')
        ax2.grid(True, linestyle='--', alpha=0.7)
        ax2.legend(['Concentration', 'Conversion'])
        
        plt.tight_layout()
        
        # Save figure
        filename = f"{output_dir}/pfr_flow{flow_rate:.1f}.png"
        plt.savefig(filename, dpi=100)
        plt.close()
        
        print(f"Created PFR image: {filename}")

def create_cstr_images(output_dir="videos"):
    """Create a series of images for CSTR
    
    Args:
        output_dir (str): Directory to save images
    """
    # Create directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Different residence times to demonstrate
    residence_times = [0.5, 1.0, 2.0, 5.0]  # tau in minutes
    
    for tau in residence_times:
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig.suptitle(f"Continuous Stirred Tank Reactor with τ = {tau} minutes", fontsize=14)
        
        # First-order reaction kinetics parameters
        k = 1.0  # Rate constant
        C0 = 1.0  # Initial concentration
        
        # Calculate steady-state concentration and conversion
        C_out = C0 / (1 + k * tau)
        conversion = 1 - C_out / C0
        
        # Plot 1: Reactor diagram
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.axis('off')
        
        # Draw reactor vessel
        circle = plt.Circle((5, 5), 3, ec='black', fc='#d1e0e0', lw=2)
        ax1.add_patch(circle)
        
        # Draw inlet and outlet pipes
        ax1.plot([1, 2.5], [7, 7], 'k-', lw=2)
        ax1.arrow(2.2, 7, 0.3, 0, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
        
        ax1.plot([5, 8.5], [2, 2], 'k-', lw=2)
        ax1.arrow(8.2, 2, 0.3, 0, head_width=0.2, head_length=0.1, fc='green', ec='green')
        
        # Draw stirrer
        ax1.plot([5, 5], [8, 6], 'k-', lw=2)
        ax1.plot([4, 6], [6, 6], 'k-', lw=2)
        
        # Add labels
        ax1.text(1, 7.5, f'Feed\nC₀={C0}', fontsize=9)
        ax1.text(8.5, 2.5, f'Product\nC={C_out:.2f}\nX={conversion:.2f}', fontsize=9)
        ax1.text(5, 1, 'CSTR', fontsize=10, ha='center')
        
        # Add residence time
        ax1.text(5, 9, f"Residence Time (τ): {tau} min", fontsize=10, ha='center')
        
        # Fill with fluid color based on conversion
        r = min(1, 0.2 + conversion * 0.8)
        g = min(1, 0.5 + conversion * 0.5)
        b = max(0, 1 - conversion)
        
        fluid = plt.Circle((5, 5), 2.9, fc=(r, g, b), alpha=0.7)
        ax1.add_patch(fluid)
        
        # Plot 2: CSTR performance graph
        tau_range = np.linspace(0.1, 10, 100)
        conv_range = tau_range / (1/k + tau_range)
        
        ax2.plot(tau_range, conv_range, 'r-')
        ax2.plot(tau, conversion, 'ro', markersize=8)  # Mark current point
        
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 1.1)
        ax2.set_xlabel('Residence Time (min)')
        ax2.set_ylabel('Conversion')
        ax2.set_title('CSTR Conversion vs. Residence Time')
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Compare with PFR (for same volume)
        pfr_conv_range = 1 - np.exp(-k * tau_range)
        ax2.plot(tau_range, pfr_conv_range, 'b-')
        ax2.plot(tau, 1 - np.exp(-k * tau), 'bo', markersize=8)  # Mark current point
        
        ax2.legend(['CSTR', 'CSTR (current)', 'PFR', 'PFR (current)'])
        
        plt.tight_layout()
        
        # Save figure
        filename = f"{output_dir}/cstr_tau{tau:.1f}.png"
        plt.savefig(filename, dpi=100)
        plt.close()
        
        print(f"Created CSTR image: {filename}")

def main():
    """Create simple images for video demonstrations"""
    print("Creating batch reactor images...")
    create_batch_reactor_images()
    
    print("Creating PFR images...")
    create_pfr_images()
    
    print("Creating CSTR images...")
    create_cstr_images()
    
    print("All images created successfully!")

if __name__ == "__main__":
    main()