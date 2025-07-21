import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os
from matplotlib.gridspec import GridSpec

def create_batch_reactor_video(filename="videos/batch_reactor.mp4", duration=10, fps=30):
    """Create a simple animation of a batch reactor process
    
    Args:
        filename (str): The filename to save the video to
        duration (int): The duration of the video in seconds
        fps (int): Frames per second
    """
    # Create figure and subplots
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(2, 2, figure=fig)
    
    # Add title
    fig.suptitle("Isothermal Batch Reactor Simulation", fontsize=16, fontweight='bold')
    
    # Create subplots
    ax1 = fig.add_subplot(gs[0, 0])  # Reactor diagram
    ax2 = fig.add_subplot(gs[0, 1])  # Concentration vs time
    ax3 = fig.add_subplot(gs[1, :])  # Conversion vs time
    
    # Set up the reactor diagram
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.set_aspect('equal')
    ax1.axis('off')
    
    # Draw the reactor vessel
    vessel = plt.Rectangle((3, 2), 4, 6, ec='black', fc='#d1e0e0', lw=2)
    ax1.add_patch(vessel)
    
    # Draw inlet and outlet lines
    ax1.plot([3, 1], [7, 7], 'k-', lw=2)
    ax1.plot([7, 9], [3, 3], 'k-', lw=2)
    
    # Draw inlet and outlet valves
    inlet_valve = plt.Rectangle((1.5, 6.5), 0.5, 1, ec='black', fc='red', lw=1)
    outlet_valve = plt.Rectangle((8, 2.5), 0.5, 1, ec='black', fc='red', lw=1)
    ax1.add_patch(inlet_valve)
    ax1.add_patch(outlet_valve)
    
    # Add text labels
    ax1.text(1, 7.5, 'Feed Inlet', fontsize=8)
    ax1.text(8, 2, 'Product Outlet', fontsize=8)
    ax1.text(5, 1, 'Batch Reactor', fontsize=10, ha='center')
    
    # Draw a stirrer symbol
    ax1.plot([5, 5], [8, 4], 'k-', lw=2)
    ax1.plot([4, 6], [4, 4], 'k-', lw=2)
    
    # Set up concentration plot
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Time (min)')
    ax2.set_ylabel('Concentration (mol/L)')
    ax2.set_title('Reactant Concentration vs. Time')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Set up conversion plot
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 1)
    ax3.set_xlabel('Time (min)')
    ax3.set_ylabel('Conversion')
    ax3.set_title('Conversion vs. Time')
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Create empty lines for data to be updated
    line_conc, = ax2.plot([], [], 'b-', lw=2)
    line_conv, = ax3.plot([], [], 'r-', lw=2)
    
    # Create fluid in the reactor (will be updated for color change)
    fluid = plt.Rectangle((3, 2), 4, 6, fc='#80b3ff', alpha=0.6)
    ax1.add_patch(fluid)
    
    # Initialize lists to store data for plotting
    t_data = []
    conc_data = []
    conv_data = []
    
    def init():
        """Initialize the animation"""
        line_conc.set_data([], [])
        line_conv.set_data([], [])
        fluid.set_facecolor('#80b3ff')
        fluid.set_alpha(0.6)
        return line_conc, line_conv, fluid
    
    def animate(i):
        """Update the animation for frame i"""
        t = i / fps
        
        # Only record data every few frames to prevent overcrowding
        if i % 3 == 0:
            t_data.append(t)
            
            # Calculate concentration based on first-order reaction kinetics
            # C = C0 * exp(-k*t)
            k = 0.3  # Rate constant
            C0 = 1.0  # Initial concentration
            concentration = C0 * np.exp(-k * t)
            conc_data.append(concentration)
            
            # Calculate conversion: X = 1 - C/C0
            conversion = 1 - concentration / C0
            conv_data.append(conversion)
            
            # Update plots
            line_conc.set_data(t_data, conc_data)
            line_conv.set_data(t_data, conv_data)
            
            # Update fluid color to represent reaction progression
            # Blend from blue to green as reaction proceeds
            r = 0.5 * conversion
            g = 0.7
            b = 0.8 * (1 - conversion)
            fluid.set_facecolor((r, g, b))
            
            # Add bubbles to represent reaction
            if len(t_data) % 5 == 0 and conversion < 0.9:
                bubble_x = 3 + np.random.rand() * 4
                bubble_y = 2 + np.random.rand() * 6
                bubble_size = 0.2 + np.random.rand() * 0.3
                bubble = plt.Circle((bubble_x, bubble_y), bubble_size, fc='white', alpha=0.4)
                ax1.add_patch(bubble)
                
                # Remove old bubbles to prevent clutter
                if len(ax1.patches) > 15:  # Keep vessel, valves, fluid, and a few bubbles
                    ax1.patches.pop(4)  # Remove oldest bubble (careful with the order!)
        
        return line_conc, line_conv, fluid
    
    # Create animation
    ani = animation.FuncAnimation(
        fig, animate, frames=duration*fps, 
        init_func=init, blit=True, interval=1000/fps
    )
    
    # Save animation as mp4
    ani.save(filename, writer='ffmpeg', fps=fps, dpi=100)
    plt.close()
    
    print(f"Created batch reactor video: {filename}")

def create_pfr_video(filename="videos/pfr.mp4", duration=10, fps=30):
    """Create a simple animation of a plug flow reactor process
    
    Args:
        filename (str): The filename to save the video to
        duration (int): The duration of the video in seconds
        fps (int): Frames per second
    """
    # Create figure and subplots
    fig = plt.figure(figsize=(12, 6))
    gs = GridSpec(2, 2, figure=fig)
    
    # Add title
    fig.suptitle("Isothermal Plug Flow Reactor Simulation", fontsize=16, fontweight='bold')
    
    # Create subplots
    ax1 = fig.add_subplot(gs[0, :])  # Reactor diagram
    ax2 = fig.add_subplot(gs[1, 0])  # Concentration vs position
    ax3 = fig.add_subplot(gs[1, 1])  # Conversion vs position
    
    # Set up the reactor diagram
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 3)
    ax1.set_aspect('auto')
    ax1.axis('off')
    
    # Draw the PFR tube
    pfr_tube = plt.Rectangle((1, 1), 8, 1, ec='black', fc='#d1d1e0', lw=2)
    ax1.add_patch(pfr_tube)
    
    # Draw inlet and outlet arrows
    ax1.arrow(0.5, 1.5, 0.5, 0, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax1.arrow(9, 1.5, 0.5, 0, head_width=0.2, head_length=0.1, fc='green', ec='green')
    
    # Add text labels
    ax1.text(0.5, 1.8, 'Feed\nC₀', fontsize=8)
    ax1.text(9, 1.8, 'Product\nC', fontsize=8)
    ax1.text(5, 0.5, 'Plug Flow Reactor', fontsize=10, ha='center')
    
    # Set up concentration plot
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.set_xlabel('Position (z/L)')
    ax2.set_ylabel('Concentration (C/C₀)')
    ax2.set_title('Concentration Profile')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Set up conversion plot
    ax3.set_xlim(0, 1)
    ax3.set_ylim(0, 1)
    ax3.set_xlabel('Position (z/L)')
    ax3.set_ylabel('Conversion (X)')
    ax3.set_title('Conversion Profile')
    ax3.grid(True, linestyle='--', alpha=0.7)
    
    # Create empty lines for profile plots
    line_conc, = ax2.plot([], [], 'b-', lw=2)
    line_conv, = ax3.plot([], [], 'r-', lw=2)
    
    # Create particles to visualize flow (initial positions)
    n_particles = 15
    particles = []
    particle_colors = []
    
    # Initialize lists to store profile data
    positions = np.linspace(0, 1, 50)  # Dimensionless positions along the reactor
    
    def init():
        """Initialize the animation"""
        line_conc.set_data([], [])
        line_conv.set_data([], [])
        
        # Initialize particles at random positions along the reactor
        for i in range(n_particles):
            x = 1 + np.random.rand() * 8  # Position along the reactor
            y = 1.2 + np.random.rand() * 0.6  # Random position in the tube height
            size = 0.05 + np.random.rand() * 0.1  # Random particle size
            particle = plt.Circle((x, y), size, fc='blue', alpha=0.7)
            ax1.add_patch(particle)
            particles.append(particle)
            particle_colors.append('blue')  # Initial color is blue
            
        return [line_conc, line_conv] + particles
    
    def animate(i):
        """Update the animation for frame i"""
        t = i / fps
        
        # Calculate profiles based on first-order reaction kinetics in a PFR
        # For a first-order reaction: -dC/dz = k*C
        # Solution: C/C0 = exp(-k*tau*z/L) where tau is the residence time
        k = 3.0  # Rate constant
        tau = 1.0  # Residence time
        
        # Calculate concentration profile: C/C0 = exp(-k*tau*z/L)
        conc_profile = np.exp(-k * tau * positions)
        
        # Calculate conversion profile: X = 1 - C/C0
        conv_profile = 1 - conc_profile
        
        # Update profile plots
        line_conc.set_data(positions, conc_profile)
        line_conv.set_data(positions, conv_profile)
        
        # Move particles along the reactor
        for j, particle in enumerate(particles):
            center = particle.center
            
            # Move particle to the right
            new_x = center[0] + 0.03
            
            # If particle exits the reactor, reset to the entrance
            if new_x > 9:
                new_x = 1.2
                center = (new_x, 1.2 + np.random.rand() * 0.6)
                particle.center = center
                particle_colors[j] = 'blue'  # Reset color
                particle.set_facecolor('blue')
            else:
                # Update position
                center = (new_x, center[1])
                particle.center = center
                
                # Update color based on position to represent reaction
                # Map position 1-9 to reactor dimensionless position 0-1
                z_L = (new_x - 1) / 8
                
                # Calculate local conversion
                local_conv = 1 - np.exp(-k * tau * z_L)
                
                # Update particle color based on conversion
                r = min(1, 0.2 + local_conv * 0.8)  # Increase red component with conversion
                g = min(1, 0.5 + local_conv * 0.5)  # Increase green component with conversion
                b = max(0, 1 - local_conv)  # Decrease blue component with conversion
                
                particle.set_facecolor((r, g, b))
                particle_colors[j] = (r, g, b)
        
        return [line_conc, line_conv] + particles
    
    # Create animation
    ani = animation.FuncAnimation(
        fig, animate, frames=duration*fps, 
        init_func=init, blit=True, interval=1000/fps
    )
    
    # Save animation as mp4
    ani.save(filename, writer='ffmpeg', fps=fps, dpi=100)
    plt.close()
    
    print(f"Created PFR video: {filename}")

def main():
    """Create videos for experiments"""
    # Ensure ffmpeg is available
    try:
        import matplotlib
        matplotlib.rcParams['animation.ffmpeg_path'] = 'ffmpeg'
        
        # Create videos for some experiments
        create_batch_reactor_video()
        create_pfr_video()
        
        print("Videos created successfully!")
    except Exception as e:
        print(f"Error creating videos: {str(e)}")
        print("Please ensure ffmpeg is installed and available in your PATH.")

if __name__ == "__main__":
    main()