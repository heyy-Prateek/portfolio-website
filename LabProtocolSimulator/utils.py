import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt

def set_plot_style():
    """
    Sets a consistent style for all matplotlib plots in the application.
    Should be called at the beginning of each experiment module.
    """
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.facecolor'] = '#FFFFFF'
    plt.rcParams['axes.facecolor'] = '#F0F2F6'
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['lines.linewidth'] = 2.5
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3

def create_download_link(df, filename, text="Download data as CSV"):
    """
    Creates a download link for a DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame to be downloaded
    filename : str
        Name of the file to be downloaded
    text : str
        Text to display for the download link
        
    Returns:
    --------
    str
        HTML string containing the download link
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href

def display_chemical_equation(reactants, products, arrow_type="→"):
    """
    Formats and displays a chemical equation.
    
    Parameters:
    -----------
    reactants : str or list
        String or list of strings representing reactants
    products : str or list
        String or list of strings representing products
    arrow_type : str
        Type of arrow to use in the equation
        
    Returns:
    --------
    str
        Formatted chemical equation
    """
    if isinstance(reactants, list):
        reactants_str = " + ".join(reactants)
    else:
        reactants_str = reactants
        
    if isinstance(products, list):
        products_str = " + ".join(products)
    else:
        products_str = products
    
    equation = f"{reactants_str} {arrow_type} {products_str}"
    return equation
