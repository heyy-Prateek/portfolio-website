import matplotlib.pyplot as plt
import numpy as np
import os

def create_placeholder_image(title, filename, size=(640, 360)):
    """Create a placeholder image with the given title
    
    Args:
        title (str): The title to display on the image
        filename (str): The filename to save the image to
        size (tuple): The size of the image in pixels
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(size[0]/100, size[1]/100), dpi=100)
    
    # Set background color
    ax.set_facecolor('#2E3B4E')
    
    # Add title text
    ax.text(0.5, 0.6, f"{title}", 
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=20, 
            color='white',
            fontweight='bold',
            transform=ax.transAxes)
    
    # Add 'Coming Soon' text
    ax.text(0.5, 0.4, "Demonstration Video\nComing Soon", 
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=14, 
            color='#FFD700',  # Gold color
            fontweight='normal',
            transform=ax.transAxes)
    
    # Remove axes
    ax.axis('off')
    
    # Tight layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(filename, bbox_inches='tight')
    plt.close()
    
    print(f"Created placeholder image: {filename}")

def main():
    """Create placeholder images for all experiments"""
    # Create directory for placeholders
    os.makedirs('videos/placeholders', exist_ok=True)
    
    # List of experiments
    experiments = {
        "batch_reactor": "Isothermal Batch Reactor",
        "semi_batch_reactor": "Isothermal Semi-batch Reactor",
        "cstr": "Isothermal CSTR",
        "pfr": "Isothermal PFR",
        "crushers": "Crushers and Ball Mill",
        "filter_press": "Plate and Frame Filter Press",
        "rotary_vacuum_filter": "Rotary Vacuum Filter",
        "centrifuge_flotation": "Centrifuge and Flotation",
        "classifiers": "Classifiers",
        "trommel": "Trommel"
    }
    
    # Create a placeholder image for each experiment
    for exp_name, title in experiments.items():
        create_placeholder_image(
            title, 
            f"videos/placeholders/{exp_name}_placeholder.png"
        )
    
    # Create a generic placeholder
    create_placeholder_image(
        "Chemical Engineering Experiment", 
        "videos/placeholders/generic_placeholder.png"
    )

if __name__ == "__main__":
    main()