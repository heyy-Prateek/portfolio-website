"""
Main module for report generation functionality
"""

import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import sys
import importlib.util
import importlib

def check_dependencies():
    """Check and install missing dependencies for report generation"""
    # Map package names to their import names
    package_map = {
        'python-docx': 'docx',
        'docxtpl': 'docxtpl',
        'pdfkit': 'pdfkit'
    }
    
    missing_packages = []
    
    for package, import_name in package_map.items():
        # Check if package is installed
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        st.warning(f"Missing dependencies: {', '.join(missing_packages)}")
        
        # Create columns for installation options
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Install Missing Packages", key="install_dependencies_button"):
                try:
                    for package in missing_packages:
                        st.info(f"Installing {package}...")
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                    st.success("All dependencies installed successfully!")
                    st.info("Please reload this page to continue.")
                    # Add a placeholder to prevent the rest of the page from loading
                    st.stop()
                except Exception as e:
                    st.error(f"Failed to install dependencies: {str(e)}")
        
        with col2:
            st.info("Manual installation command:")
            st.code(f"pip install {' '.join(missing_packages)}")
        
        return False
    
    return True

def main():
    """Main function for report generation module"""
    
    # Check dependencies first
    if not check_dependencies():
        return
    
    st.title("Laboratory Report Generator")
    st.write("""
    This tool allows you to generate a professional report from your experiment data.
    Select the experiment and enter the required information.
    """)
    
    # Experiment selection
    experiment = st.selectbox(
        "Select Experiment",
        [
            "Batch Reactor",
            "Semi-Batch Reactor",
            "CSTR",
            "PFR",
            "Crushers & Ball Mill",
            "Filter Press",
            "Rotary Vacuum Filter",
            "Centrifuge & Flotation",
            "Classifiers",
            "Trommel"
        ]
    )
    
    # Display appropriate report generator based on selection
    if experiment == "Rotary Vacuum Filter":
        from chemengsim.report_generation import rotary_vacuum_filter
        rotary_vacuum_filter.main()
    elif experiment == "Classifiers":
        from chemengsim.report_generation import classifiers
        classifiers.main()
    elif experiment == "Centrifuge & Flotation":
        # Use tabs to prevent widget conflicts
        tab1, tab2 = st.tabs(["Basket Centrifuge", "Froth Flotation"])
        
        with tab1:
            from chemengsim.report_generation import basket_centrifuge
            basket_centrifuge.main()
        
        with tab2:
            from chemengsim.report_generation import froth_flotation
            froth_flotation.main()
    else:
        st.info(f"Report generator for {experiment} is currently under development.")

if __name__ == "__main__":
    main()