import streamlit as st
import os

def display_demo_video(experiment_name):
    """Display a demonstration video for the specified experiment
    
    Args:
        experiment_name (str): The name of the experiment to show a demo for
    """
    st.title(f"Demonstration Video: {experiment_name.replace('_', ' ').title()}")
    
    # Map experiment names to their titles for display
    experiment_titles = {
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
    
    # Get the title for the current experiment
    title = experiment_titles.get(experiment_name, experiment_name.replace('_', ' ').title())
    
    # Video file path (assuming videos are stored in the videos directory with the same name as the experiment)
    video_file = f"videos/{experiment_name}.mp4"
    
    # For now, we'll use placeholder images or generated images
    # Check if the video file exists
    if os.path.exists(video_file):
        # Display the video
        st.video(video_file)
    elif experiment_name == "batch_reactor":
        # Show series of batch reactor images in tabs
        st.info("This is a demonstration using sequential images. Video format coming soon!")
        tabs = st.tabs(["t = 0 min", "t = 2 min", "t = 5 min", "t = 10 min"])
        with tabs[0]:
            st.image("videos/batch_reactor_t0.png", caption="Batch Reactor at t = 0 minutes")
        with tabs[1]:
            st.image("videos/batch_reactor_t2.png", caption="Batch Reactor at t = 2 minutes")
        with tabs[2]:
            st.image("videos/batch_reactor_t5.png", caption="Batch Reactor at t = 5 minutes")
        with tabs[3]:
            st.image("videos/batch_reactor_t10.png", caption="Batch Reactor at t = 10 minutes")
    elif experiment_name == "pfr":
        # Show series of PFR images in tabs
        st.info("This is a demonstration using sequential images. Video format coming soon!")
        tabs = st.tabs(["Flow Rate: 0.5", "Flow Rate: 1.0", "Flow Rate: 2.0", "Flow Rate: 3.0"])
        with tabs[0]:
            st.image("videos/pfr_flow0.5.png", caption="PFR with Flow Rate = 0.5 units")
        with tabs[1]:
            st.image("videos/pfr_flow1.0.png", caption="PFR with Flow Rate = 1.0 units")
        with tabs[2]:
            st.image("videos/pfr_flow2.0.png", caption="PFR with Flow Rate = 2.0 units")
        with tabs[3]:
            st.image("videos/pfr_flow3.0.png", caption="PFR with Flow Rate = 3.0 units")
    elif experiment_name == "cstr":
        # Show series of CSTR images in tabs
        st.info("This is a demonstration using sequential images. Video format coming soon!")
        tabs = st.tabs(["τ = 0.5 min", "τ = 1.0 min", "τ = 2.0 min", "τ = 5.0 min"])
        with tabs[0]:
            st.image("videos/cstr_tau0.5.png", caption="CSTR with Residence Time = 0.5 minutes")
        with tabs[1]:
            st.image("videos/cstr_tau1.0.png", caption="CSTR with Residence Time = 1.0 minutes")
        with tabs[2]:
            st.image("videos/cstr_tau2.0.png", caption="CSTR with Residence Time = 2.0 minutes")
        with tabs[3]:
            st.image("videos/cstr_tau5.0.png", caption="CSTR with Residence Time = 5.0 minutes")
    else:
        # Display a placeholder image from our generated placeholders
        placeholder_file = f"videos/placeholders/{experiment_name}_placeholder.png"
        if os.path.exists(placeholder_file):
            st.image(placeholder_file, caption=f"{title} Demonstration Video (Coming Soon)")
        else:
            st.image("videos/placeholders/generic_placeholder.png", caption=f"{title} Demonstration Video (Coming Soon)")
        st.info("The actual video for this experiment is under development.")
    
    # Add description and context
    st.markdown(f"### About the {title} Experiment")
    
    # Custom descriptions for each experiment
    if experiment_name == "batch_reactor":
        st.markdown("""
        This video demonstrates the operation of an isothermal batch reactor, showing:
        
        - How the system is loaded with reactants
        - The reaction progress in real time
        - Sampling procedures for concentration measurement
        - Data collection and analysis
        
        Key concepts illustrated include stoichiometry, reaction kinetics, and conversion calculations.
        """)
        
    elif experiment_name == "semi_batch_reactor":
        st.markdown("""
        This demonstration shows a semi-batch reactor in operation, highlighting:
        
        - Controlled addition of reactants over time
        - Temperature control mechanisms
        - Mixing patterns and efficiency
        - Comparison with batch operation
        
        The video illustrates how semi-batch operation can improve selectivity and safety for exothermic reactions.
        """)
        
    elif experiment_name == "cstr":
        st.markdown("""
        This video shows the continuous stirred tank reactor (CSTR) in action:
        
        - Steady-state operation with continuous feed and product removal
        - Mixing patterns inside the reactor
        - Temperature and flow rate control
        - Steady-state vs. transient behavior
        
        The demonstration highlights how CSTR operation differs from batch processing and the implications for conversion.
        """)
        
    elif experiment_name == "pfr":
        st.markdown("""
        This demonstration of a plug flow reactor (PFR) shows:
        
        - Fluid flow patterns through the tubular reactor
        - Concentration gradient along the reactor length
        - Residence time distribution effects
        - Comparison with CSTR performance
        
        The video highlights the advantages of PFRs for certain reaction types and higher conversions.
        """)
        
    elif experiment_name == "crushers":
        st.markdown("""
        This video demonstrates crusher and ball mill operation:
        
        - Feed material handling and classification
        - Crushing mechanisms and principles
        - Product size distribution analysis
        - Energy consumption measurements
        
        The demonstration illustrates size reduction theories and equipment selection criteria.
        """)
        
    elif experiment_name == "filter_press":
        st.markdown("""
        This demonstration shows a plate and frame filter press in operation:
        
        - Assembly of the filter plates and frames
        - Slurry feed and filtration process
        - Cake formation and washing
        - Disassembly and cake removal
        
        The video illustrates filtration theory, resistance calculation, and operation cycles.
        """)
        
    elif experiment_name == "rotary_vacuum_filter":
        st.markdown("""
        This demonstration of a rotary vacuum filter shows:
        
        - Continuous drum rotation through slurry
        - Vacuum application and cake formation
        - Washing and drying zones
        - Cake discharge mechanisms
        
        The video highlights the advantages of continuous filtration over batch processes.
        """)
        
    elif experiment_name == "centrifuge_flotation":
        st.markdown("""
        This video demonstrates both centrifuge and flotation operations:
        
        - Centrifugal separation principles
        - Feed introduction and product removal
        - Flotation cell operation and froth formation
        - Recovery and grade measurements
        
        The demonstration illustrates separation techniques based on density and surface properties.
        """)
        
    elif experiment_name == "classifiers":
        st.markdown("""
        This demonstration shows hydraulic classifiers in operation:
        
        - Particle settling in fluid environments
        - Upward flow and classification zones
        - Product stream collection and analysis
        - Thickener operation principles
        
        The video illustrates how particle size and density affect separation efficiency.
        """)
        
    elif experiment_name == "trommel":
        st.markdown("""
        This video demonstrates a trommel screen in operation:
        
        - Feed introduction and drum rotation
        - Screening action and particle movement
        - Oversize and undersize material collection
        - Screen efficiency calculation
        
        The demonstration illustrates mechanical screening principles and equipment design.
        """)
        
    else:
        st.markdown("""
        This demonstration video shows the key operational aspects of the experiment, including:
        
        - Equipment setup and configuration
        - Process variables and their effects
        - Data collection methodology
        - Analysis techniques and interpretation
        
        The video provides a visual reference for the simulation you can interact with in the app.
        """)
    
    # Add call-to-action to try the simulation
    st.markdown("---")
    st.info("Switch to 'Simulation' mode to interact with this experiment and adjust parameters yourself!")