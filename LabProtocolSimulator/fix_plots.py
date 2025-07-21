"""
Plot Styling Fix Script

This script updates all experiment files to use consistent matplotlib styling.
"""

import os
import re

def fix_matplotlib_imports(file_path):
    """
    Adds the styling import to experiment files
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Check if already fixed
    if "set_plot_style()" in content:
        print(f"Skipping {file_path} - already fixed")
        return
    
    # Update imports
    if "import matplotlib.pyplot as plt" in content:
        if "from utils import" in content:
            # Add to existing import
            content = re.sub(
                r'from utils import (.*)',
                r'from utils import \1, set_plot_style',
                content
            )
        else:
            # Add new import
            content = re.sub(
                r'import matplotlib.pyplot as plt(.*)',
                r'import matplotlib.pyplot as plt\1\nfrom utils import set_plot_style',
                content
            )
        
        # Add the style initialization after imports
        if "def app():" in content:
            content = re.sub(
                r'(import.*\n+)(def app\(\):)',
                r'\1# Set consistent style for plots\nset_plot_style()\n\n\2',
                content
            )
        
        # Enhance plot parameters
        content = re.sub(
            r'fig, ax = plt\.subplots\(figsize=\((\d+), (\d+)\)\)',
            r'fig, ax = plt.subplots(figsize=(\1, \2), dpi=100)',
            content
        )
        
        # Add tight_layout to all plots
        content = re.sub(
            r'(st\.pyplot\(fig[^)]*\))',
            r'fig.tight_layout()\n        \1',
            content
        )
        
        # Update legend formatting
        content = re.sub(
            r'ax\.legend\(\)',
            r'ax.legend(frameon=True, fancybox=True, shadow=True)',
            content
        )
        
        # Fix grid styles
        content = re.sub(
            r'ax\.grid\(True\)',
            r'ax.grid(True, alpha=0.3)',
            content
        )
        
        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Fixed {file_path}")

def main():
    """Fix all experiment files"""
    experiments_dir = "chemengsim/experiments"
    
    for filename in os.listdir(experiments_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            file_path = os.path.join(experiments_dir, filename)
            fix_matplotlib_imports(file_path)

if __name__ == "__main__":
    main()
    print("Plot styling fixed in all experiment files.") 