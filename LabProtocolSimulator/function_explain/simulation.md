# Simulation Feature

The Simulation feature is the core functionality of the Chemical Engineering Laboratory Simulator, allowing users to interact with virtual experiments and observe the effects of parameter changes in real-time.

## Implementation Overview

Each experiment is implemented as a separate module with a consistent structure:
1. Parameter input UI for user interaction
2. Mathematical model for calculations
3. Visual components (plots, animations, diagrams)
4. Results display and interpretation

## Code Structure

Each simulation is located in the `chemengsim/experiments/` directory. The main application dynamically imports the appropriate module based on the user's selection:

```python
# Dynamic import of the experiment module
module_name = f"chemengsim.experiments.{exp_names[exp_num]}"
module = __import__(module_name, fromlist=['app'])
module.app()
```

## Typical Simulation Module Structure

Each experiment module follows a similar structure:

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def app():
    """Main function for the experiment simulation"""
    st.title("Experiment Name")
    
    # 1. Parameter Input Section
    st.sidebar.header("Simulation Parameters")
    param1 = st.sidebar.slider("Parameter 1", min_value, max_value, default_value)
    param2 = st.sidebar.slider("Parameter 2", min_value, max_value, default_value)
    
    # 2. Calculation Model
    results = calculate_results(param1, param2)
    
    # 3. Visualization
    fig = create_visualization(results)
    st.plotly_chart(fig)
    
    # 4. Results and Interpretation
    st.subheader("Results")
    st.dataframe(results)
    
    st.subheader("Interpretation")
    display_interpretation(results)

def calculate_results(param1, param2):
    """Implement the mathematical model for the experiment"""
    # Calculation logic specific to the experiment
    return results

def create_visualization(results):
    """Create interactive visualizations of the results"""
    # Visualization code
    return fig

def display_interpretation(results):
    """Explain the results and their significance"""
    # Interpretation logic
```

## Example: Batch Reactor Simulation

The Batch Reactor simulation demonstrates the implementation pattern:

```python
def app():
    """Main function for batch reactor simulation"""
    st.title("Isothermal Batch Reactor Simulation")
    
    # Parameter input
    st.sidebar.header("Reaction Parameters")
    reaction_order = st.sidebar.selectbox("Reaction Order", [0, 1, 2], 1)
    k = st.sidebar.slider("Rate Constant (k)", 0.01, 1.0, 0.1, 0.01)
    C_A0 = st.sidebar.slider("Initial Concentration (C_A0)", 1.0, 10.0, 5.0, 0.1)
    time_max = st.sidebar.slider("Simulation Time (min)", 1, 60, 30)
    
    # Create time array
    time = np.linspace(0, time_max, 100)
    
    # Calculate concentration profile based on reaction order
    if reaction_order == 0:
        # Zero-order reaction: C_A = C_A0 - k*t
        C_A = C_A0 - k * time
        C_A = np.maximum(C_A, 0)  # Ensure non-negative concentration
        equation = r'$C_A = C_{A0} - kt$'
    elif reaction_order == 1:
        # First-order reaction: C_A = C_A0 * exp(-k*t)
        C_A = C_A0 * np.exp(-k * time)
        equation = r'$C_A = C_{A0}e^{-kt}$'
    else:  # reaction_order == 2
        # Second-order reaction: 1/C_A = 1/C_A0 + k*t
        C_A = 1 / (1/C_A0 + k * time)
        equation = r'$\frac{1}{C_A} = \frac{1}{C_{A0}} + kt$'
    
    # Calculate conversion
    X_A = (C_A0 - C_A) / C_A0
    
    # Create dataframe for results
    results = pd.DataFrame({
        'Time (min)': time,
        'Concentration (mol/L)': C_A,
        'Conversion': X_A
    })
    
    # Display concentration plot
    st.subheader("Concentration Profile")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time, 
        y=C_A, 
        mode='lines', 
        name='C_A',
        line=dict(color='blue', width=2)
    ))
    fig.update_layout(
        xaxis_title="Time (min)",
        yaxis_title="Concentration (mol/L)",
        title=f"Concentration vs. Time for {reaction_order}-Order Reaction ({equation})"
    )
    st.plotly_chart(fig)
    
    # Display conversion plot
    st.subheader("Conversion Profile")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=time, 
        y=X_A, 
        mode='lines', 
        name='X_A',
        line=dict(color='green', width=2)
    ))
    fig2.update_layout(
        xaxis_title="Time (min)",
        yaxis_title="Conversion (X_A)",
        title=f"Conversion vs. Time for {reaction_order}-Order Reaction"
    )
    st.plotly_chart(fig2)
    
    # Display numerical results
    st.subheader("Numerical Results")
    st.dataframe(results.iloc[::10])  # Display every 10th row to avoid overcrowding
```

## Key Simulation Components

### 1. Parameter Input

Uses Streamlit widgets such as:
- `st.slider`: For numerical parameters with a range
- `st.selectbox`: For options from a fixed set
- `st.number_input`: For precise numerical input
- `st.checkbox`: For boolean options

### 2. Calculation Model

Implements the mathematical model for each experiment:
- Uses NumPy for numerical calculations
- Performs differential equation solving for dynamic systems
- Implements material and energy balances
- Calculates performance metrics

### 3. Visualization

Creates interactive plots and diagrams:
- Uses Plotly for interactive plots
- Provides multiple visualization options (concentration profiles, conversion plots, etc.)
- Updates in real-time as parameters change

### 4. Results Interpretation

Provides contextual interpretation of results:
- Explains what the results mean
- Highlights key performance indicators
- Offers educational insights
- Makes connections to theory

## Extending the Simulation Feature

To add a new experiment simulation:

1. Create a new module in `chemengsim/experiments/`
2. Implement the `app()` function as the entry point
3. Add necessary calculation functions
4. Create visualization components
5. Update the experiment list in `app.py`

This modular structure allows for easy addition of new experiments without modifying the core application code. 