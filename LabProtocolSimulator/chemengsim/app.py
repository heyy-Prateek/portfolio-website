"""
Main application module for Chemical Engineering Lab Simulator.
"""

import streamlit as st
import platform
import os

# Detect if running on Android or mobile
is_mobile = False
user_agent = os.environ.get('HTTP_USER_AGENT', '').lower()
if 'android' in user_agent or 'mobile' in user_agent or platform.system() == "Android":
    is_mobile = True
    
# Set page configuration, background, and title
st.set_page_config(
    page_title="Chemical Engineering Lab Simulator",
    page_icon="🧪",
    layout="wide" if not is_mobile else "centered"
)

st.markdown(
    """
<style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 200px;
        background-color: #ffffff;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 200px;
        margin-left: -200px;
    }
    /* Override Streamlit's default background */
    .stApp {
        background-color: #FFFFFF;
    }
    
    .main .block-container {
        background-color: #FFFFFF;
    }
    
    /* Responsive styles */
    @media (max-width: 768px) {
        .main-heading {
            font-size: 1.8rem;
            padding: 5px;
        }
        
        .experiment-card {
            width: 220px;
            height: 200px;
        }
        
        .experiment-title {
            font-size: 16px;
        }
        
        .experiment-description {
            font-size: 12px;
            height: 80px;
        }
        
        .banner {
            height: 150px;
        }
        
        .banner h3 {
            font-size: 20px;
        }
        
        .features-grid {
            grid-template-columns: repeat(1, 1fr);
        }
    }
    
    /* Force HTML content to render properly */
    .element-container div.markdown-text-container {
        white-space: normal !important;
    }
    
    /* Streamlit sidebar styling for better display */
    [data-testid="stSidebar"] {
        z-index: 1000;
    }
    
    /* Tooltips for action buttons */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: rgba(0, 0, 0, 0.8);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        pointer-events: none;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Category styles */
    .category-card {
        display: inline-block;
        width: 150px;
        text-align: center;
        margin-right: 20px;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .category-card:hover {
        transform: scale(1.05);
    }
    
    .category-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #E3F2FD;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-size: 30px;
        color: #1E88E5;
    }
    
    .category-card:nth-child(even) .category-icon {
        background-color: #BBDEFB;
    }
    
    .category-name {
        font-weight: 500;
        color: #0D47A1;
    }
    
    /* Banner styles */
    .banner {
        width: 100%;
        height: 180px;
        border-radius: 12px;
        background: linear-gradient(90deg, #1E88E5, #0D47A1);
        position: relative;
        overflow: hidden;
        margin-bottom: 30px;
        color: white;
        display: flex;
        align-items: center;
        padding: 20px;
    }
    
    .banner-content {
        width: 60%;
    }
    
    .banner h3 {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .banner p {
        font-size: 14px;
        margin-bottom: 15px;
    }
    
    .banner-button {
        display: inline-block;
        padding: 8px 20px;
        background-color: white;
        color: #1E88E5;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
    }
    
    /* Bootstrap-like button */
    .btn-primary {
        display: inline-block;
        padding: 8px 15px;
        background-color: #1E88E5;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
        text-align: center;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Feature items with alternating colors */
    .feature-item {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid rgba(30, 136, 229, 0.1);
    }
    
    .feature-item:nth-child(even) {
        background-color: #BBDEFB;
    }
    
    .feature-icon {
        font-size: 30px;
        color: #1E88E5;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: #0D47A1;
    }
</style>
""",
    unsafe_allow_html=True,
)

def main():
    st.sidebar.title("Experiment Selection")
    
    # Add mode options in sidebar
    view_mode = st.sidebar.radio("Mode", ["Simulation", "Demo Video", "Quiz", "Report Generation", "Chat Assistant"])
    
    experiment = st.sidebar.selectbox(
        "Choose an experiment",
        [
            "Home",
            "1. Isothermal Batch Reactor",
            "2. Isothermal Semi-batch Reactor",
            "3. Isothermal CSTR",
            "4. Isothermal PFR",
            "5. Crushers and Ball Mill",
            "6. Plate and Frame Filter Press",
            "7. Rotary Vacuum Filter",
            "8. Centrifuge and Flotation",
            "9. Classifiers",
            "10. Trommel"
        ]
    )
    
    # Store current experiment in session state for reference by other modules
    st.session_state['selected_experiment'] = experiment
    
    # Common experiment name mapping
    exp_names = [
        "",  # Home page has no number
        "batch_reactor",
        "semi_batch_reactor",
        "cstr",
        "pfr",
        "crushers",
        "filter_press",
        "rotary_vacuum_filter",
        "centrifuge_flotation",
        "classifiers",
        "trommel"
    ]
    
    # Display the appropriate experiment page based on selection
    if experiment == "Home":
        display_home_page()
    elif view_mode == "Chat Assistant":
        try:
            # Import chat module and display chat interface
            from chemengsim import chat
            chat.chat_interface()
        except Exception as e:
            st.error(f"Error loading chat assistant: {str(e)}")
            st.info("The chat assistant feature may still be under development.")
    elif view_mode == "Quiz":
        try:
            # Extract experiment name from selection
            exp_num = int(experiment.split(".")[0])
            
            # Import quiz module and run quiz
            from chemengsim.quizzes import quiz_module
            quiz_module.run_quiz(exp_names[exp_num])
        except Exception as e:
            st.error(f"Error loading quiz: {str(e)}")
            st.info("Some quizzes may still be under development.")
    elif view_mode == "Demo Video":
        try:
            # Skip if Home is selected
            if experiment != "Home":
                # Extract experiment name from selection
                exp_num = int(experiment.split(".")[0])
                
                # Import demo video module and display video
                from chemengsim.videos import demo_videos
                demo_videos.display_demo_video(exp_names[exp_num])
            else:
                st.title("Demonstration Videos")
                st.markdown("""
                Select an experiment from the sidebar to view its demonstration video.
                
                These videos show the actual laboratory procedures and equipment operation
                for each experiment in the Chemical Engineering Laboratory.
                """)
                st.info("Please select an experiment from the sidebar to view its demonstration video.")
        except Exception as e:
            st.error(f"Error loading demonstration video: {str(e)}")
            st.info("Some demonstration videos may still be under development.")
    elif view_mode == "Report Generation":
        # Import and run the report generation module
        try:
            from chemengsim.report_generation import main as report_main
            report_main.main()
        except Exception as e:
            st.error(f"Error loading report generation module: {str(e)}")
            st.info("The report generation feature may still be under development for some experiments.")
    else:  # Simulation mode
        if experiment != "Home":
            # Extract experiment name from selection for import
            exp_num = int(experiment.split(".")[0])
            
            try:
                # Dynamic import of the experiment module
                module_name = f"chemengsim.experiments.{exp_names[exp_num]}"
                module = __import__(module_name, fromlist=['app'])
                module.app()
            except Exception as e:
                st.error(f"Error loading experiment simulation: {str(e)}")
                st.write(f"## {experiment}")
                st.write("### What you'll learn in this experiment:")
            
            if experiment == "1. Isothermal Batch Reactor":
                st.write("""
                - How concentration changes with time in a batch reactor
                - Effect of reaction rate constant on conversion
                - Calculation of residence time and space-time
                - Analysis of reaction kinetics
                """)
                
            elif experiment == "2. Isothermal Semi-batch Reactor":
                st.write("""
                - How feed rate affects reaction progress
                - Material balances in semi-batch operation
                - Comparison with batch reactor performance
                - Effect of feeding policies on conversion
                """)
                
            elif experiment == "3. Isothermal CSTR":
                st.write("""
                - Steady-state operation of continuous reactors
                - Effect of residence time on conversion
                - Multiple steady states and stability
                - Comparison with other reactor types
                """)
                
            elif experiment == "4. Isothermal PFR":
                st.write("""
                - Plug flow behavior and its assumptions
                - Concentration profiles along reactor length
                - Conversion as a function of residence time
                - Comparison with CSTR performance
                """)
                
            elif experiment == "5. Crushers and Ball Mill":
                st.write("""
                - Size reduction principles
                - Energy requirements for crushing
                - Product size distribution analysis
                - Performance metrics for crushers
                """)
                
            elif experiment == "6. Plate and Frame Filter Press":
                st.write("""
                - Solid-liquid separation theory
                - Cake filtration fundamentals
                - Constant pressure vs. constant rate filtration
                - Determination of filter medium resistance
                """)
                
            elif experiment == "7. Rotary Vacuum Filter":
                st.write("""
                - Continuous filtration principles
                - Drum operation zones and timing
                - Effect of vacuum level on filtration rate
                - Cake washing and dewatering
                """)
                
            elif experiment == "8. Centrifuge and Flotation":
                st.write("""
                - Centrifugal separation principles
                - Effect of G-force on separation efficiency
                - Flotation chemistry and surface properties
                - Froth stability and collection mechanisms
                """)
                
            elif experiment == "9. Classifiers":
                st.write("""
                - Hydraulic classification principles
                - Settling of particles in fluids
                - Cut size and separation efficiency
                - Thickener design and operation
                """)
                
            elif experiment == "10. Trommel":
                st.write("""
                - Screening principles and equipment
                - Effect of operating parameters on screening efficiency
                - Size distribution analysis
                - Screen capacity and limitations
                """)
            
            st.markdown("---")
            if view_mode == "Simulation":
                st.info("Please check the Quiz mode to test your knowledge or the Report Generation mode to create a lab report for this experiment!")

    # Add footer to all pages
    st.markdown("---")
    
    # Footer text only
    st.markdown("""
    <div style='text-align: center;'>
        <p>© 2025 Chemical Engineering Laboratory Simulator | Created by Prateek Saxena</p>
        <p>BITS Pilani, India | Contact: +91 9458827686</p>
        <p>MADE WITH LOVE FOR CHEMICAL ENGINEERING COMMUNITY ❤️</p>
    </div>
    """, unsafe_allow_html=True)

def display_home_page():
    """Display the enhanced home page with experiment cards"""
    
    # Detect if running on mobile
    global is_mobile
    
    # Add enhanced styling for Zomato-like interface
    st.markdown("""
    <style>
    /* Base styles */
    body {
        background-color: #FFFFFF;
        font-family: 'Helvetica Neue', Arial, sans-serif;
    }
    
    /* Main heading */
    .main-heading {
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        color: #1E88E5;
        margin-bottom: 20px;
        padding: 10px;
    }
    
    /* Section styles */
    .section-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0D47A1;
        padding: 10px 0;
        margin: 30px 0 15px 0;
    }
    
    /* Scrollable carousel */
    .carousel-container {
        position: relative;
        width: 100%;
        overflow-x: auto;
        white-space: nowrap;
        scrollbar-width: thin;
        scrollbar-color: #1E88E5 #f8f8f8;
        padding: 10px 0;
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }
    
    .carousel-container::-webkit-scrollbar {
        height: 6px;
    }
    
    .carousel-container::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    .carousel-container::-webkit-scrollbar-thumb {
        background: #1E88E5;
        border-radius: 10px;
    }
    
    .carousel-container::-webkit-scrollbar-thumb:hover {
        background: #0D47A1;
    }
    
    /* Experiment cards - alternating shades */
    .experiment-card {
        display: inline-block;
        width: 280px;
        height: 220px;
        margin-right: 15px;
        padding: 15px;
        border-radius: 12px;
        background-color: #FFFFFF;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        vertical-align: top;
        white-space: normal;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
        border: 1px solid rgba(30, 136, 229, 0.1);
    }
    
    .experiment-card:nth-child(even) {
        background-color: #1E88E5;
    }
    
    .experiment-card:nth-child(even) .experiment-title {
        color: #FFFFFF;
    }
    
    .experiment-card:nth-child(even) .experiment-description {
        color: #E3F2FD;
    }
    
    .experiment-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(30, 136, 229, 0.2);
        border-color: rgba(30, 136, 229, 0.3);
    }
    
    .experiment-icon {
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .experiment-title {
        color: #0D47A1;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 10px;
        white-space: normal;
    }
    
    .experiment-description {
        color: #1565C0;
        font-size: 14px;
        line-height: 1.4;
        height: 60px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        white-space: normal;
        transition: height 0.3s ease;
    }
    
    /* Action buttons on hover */
    .experiment-actions {
        display: none;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 8px;
        margin-top: 10px;
        transition: all 0.3s ease;
        justify-content: center;
    }
    
    .experiment-card:hover .experiment-description {
        height: 40px;
        -webkit-line-clamp: 2;
    }
    
    .experiment-card:hover .experiment-actions {
        display: flex;
    }
    
    .action-button {
        text-decoration: none;
        text-align: center;
        width: 40px;
        height: 40px;
        line-height: 40px;
        background-color: #1E88E5;
        color: white;
        border-radius: 50%;
        font-size: 20px;
        transition: all 0.2s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .action-button:hover {
        transform: scale(1.1);
    }
    
    /* Alternating colors for buttons */
    .experiment-card:nth-child(even) .action-button {
        background-color: #FFFFFF;
        color: #1E88E5;
    }
    
    .experiment-card:nth-child(even) .action-button:hover {
        background-color: #F5F5F5;
    }
    
    /* Fix for code display issues */
    pre, code {
        display: none !important;
        visibility: hidden !important;
    }
    
    .stCodeBlock {
        display: none !important;
    }
    
    /* Dark theme compatibility */
    [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF;
    }
    
    [data-testid="stHeader"] {
        background-color: #FFFFFF;
    }
    
    /* Force HTML content to render properly */
    .element-container div.markdown-text-container {
        white-space: normal !important;
    }
    
    /* Streamlit sidebar styling for better display */
    [data-testid="stSidebar"] {
        z-index: 1000;
    }
    
    /* Tooltips for action buttons */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: rgba(0, 0, 0, 0.8);
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 12px;
        pointer-events: none;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Category styles */
    .category-card {
        display: inline-block;
        width: 150px;
        text-align: center;
        margin-right: 20px;
        cursor: pointer;
        transition: transform 0.3s ease;
    }
    
    .category-card:hover {
        transform: scale(1.05);
    }
    
    .category-icon {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background-color: #E3F2FD;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-size: 30px;
        color: #1E88E5;
    }
    
    .category-card:nth-child(even) .category-icon {
        background-color: #BBDEFB;
    }
    
    .category-name {
        font-weight: 500;
        color: #0D47A1;
    }
    
    /* Banner styles */
    .banner {
        width: 100%;
        height: 180px;
        border-radius: 12px;
        background: linear-gradient(90deg, #1E88E5, #0D47A1);
        position: relative;
        overflow: hidden;
        margin-bottom: 30px;
        color: white;
        display: flex;
        align-items: center;
        padding: 20px;
    }
    
    .banner-content {
        width: 60%;
    }
    
    .banner h3 {
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .banner p {
        font-size: 14px;
            margin-bottom: 15px;
        }
    
    .banner-button {
        display: inline-block;
        padding: 8px 20px;
        background-color: white;
        color: #1E88E5;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
    }
    
    /* Bootstrap-like button */
    .btn-primary {
        display: inline-block;
        padding: 8px 15px;
        background-color: #1E88E5;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 10px;
        text-align: center;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }
    
    /* Feature items with alternating colors */
    .feature-item {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        border: 1px solid rgba(30, 136, 229, 0.1);
    }
    
    .feature-item:nth-child(even) {
        background-color: #BBDEFB;
    }
    
    .feature-icon {
        font-size: 30px;
        color: #1E88E5;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: #0D47A1;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main heading
    st.markdown("<h1 class='main-heading'>Chemical Engineering Laboratory Simulator</h1>", unsafe_allow_html=True)
    
    # Banner
    st.markdown("""
    <div class="banner">
        <div class="banner-content">
            <h3>Ultimate Virtual Lab Experience</h3>
            <p>Explore 10 realistic chemical engineering experiments without physical lab access</p>
            <a href="#" class="banner-button">Get Started</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("<h2 class='section-title'>Key Features</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="features-grid">
        <div class="feature-item">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Interactive Simulations</div>
            <p>Adjust parameters and observe real-time results</p>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🎓</div>
            <div class="feature-title">Educational Quizzes</div>
            <p>Test your knowledge after each experiment</p>
        </div>
        <div class="feature-item">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Report Generation</div>
            <p>Create professional lab reports automatically</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Category section - similar to Zomato's category carousel
    st.markdown("<h2 class='section-title'>Experiment Categories</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="carousel-container">
        <div class="category-card">
            <div class="category-icon">🧪</div>
            <div class="category-name">Reactors</div>
        </div>
        <div class="category-card">
            <div class="category-icon">⚙️</div>
            <div class="category-name">Size Reduction</div>
        </div>
        <div class="category-card">
            <div class="category-icon">🔄</div>
            <div class="category-name">Separation</div>
        </div>
        <div class="category-card">
            <div class="category-icon">📊</div>
            <div class="category-name">Classification</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Reactor experiments - horizontal scrollable carousel
    st.markdown("<h2 class='section-title'>Reactor Experiments</h2>", unsafe_allow_html=True)
    
    # Create a simpler HTML structure for the cards
    reactor_cards_html = """
    <script>
    function navigateTo(experiment, mode) {
        // Get the experiment index from the sidebar options
        const experiments = [
            "Home",
            "1. Isothermal Batch Reactor",
            "2. Isothermal Semi-batch Reactor", 
            "3. Isothermal CSTR",
            "4. Isothermal PFR",
            "5. Crushers and Ball Mill",
            "6. Plate and Frame Filter Press",
            "7. Rotary Vacuum Filter",
            "8. Centrifuge and Flotation",
            "9. Classifiers",
            "10. Trommel"
        ];
        
        // Find experiment in the sidebar
        const experimentOption = document.querySelector('div[data-testid="stSelectbox"] div[role="listbox"]');
        if (experimentOption) {
            experimentOption.click();
            setTimeout(() => {
                const options = document.querySelectorAll('div[role="option"]');
                for (let option of options) {
                    if (option.textContent === experiment) {
                        option.click();
                        break;
                    }
                }
                
                // After selecting experiment, select the mode
                setTimeout(() => {
                    const modeOptions = document.querySelectorAll('div[data-testid="stRadio"] label');
                    for (let modeOption of modeOptions) {
                        if (modeOption.textContent.includes(mode)) {
                            modeOption.click();
                            break;
                        }
                    }
                }, 300);
            }, 300);
        }
    }
    </script>
    
    <div class="carousel-container">
            <div class="experiment-card">
            <div class="experiment-icon">🧪</div>
            <div class="experiment-title">1. Isothermal Batch Reactor</div>
            <div class="experiment-description">Study of a non-catalytic homogeneous reaction in a batch reactor, including concentration profiles and conversion analysis.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('1. Isothermal Batch Reactor', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('1. Isothermal Batch Reactor', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('1. Isothermal Batch Reactor', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('1. Isothermal Batch Reactor', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('1. Isothermal Batch Reactor', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">⏱️</div>
            <div class="experiment-title">2. Isothermal Semi-batch Reactor</div>
            <div class="experiment-description">Simulation of reactions in semi-batch mode with continuous addition of one reactant.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('2. Isothermal Semi-batch Reactor', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('2. Isothermal Semi-batch Reactor', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('2. Isothermal Semi-batch Reactor', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('2. Isothermal Semi-batch Reactor', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('2. Isothermal Semi-batch Reactor', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">🔄</div>
            <div class="experiment-title">3. Isothermal CSTR</div>
            <div class="experiment-description">Continuous stirred tank reactor simulation with heat transfer analysis.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('3. Isothermal CSTR', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('3. Isothermal CSTR', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('3. Isothermal CSTR', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('3. Isothermal CSTR', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('3. Isothermal CSTR', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">➡️</div>
            <div class="experiment-title">4. Isothermal PFR</div>
            <div class="experiment-description">Plug flow reactor with variable parameters and comparison to other reactor types.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('4. Isothermal PFR', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('4. Isothermal PFR', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('4. Isothermal PFR', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('4. Isothermal PFR', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('4. Isothermal PFR', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
    </div>
    """
    
    st.markdown(reactor_cards_html, unsafe_allow_html=True)
    
    # Separation experiments - horizontal scrollable carousel
    st.markdown("<h2 class='section-title'>Separation & Classification</h2>", unsafe_allow_html=True)
    
    # Create a simpler HTML structure for the separation cards
    separation_cards_html = """
    <div class="carousel-container">
            <div class="experiment-card">
            <div class="experiment-icon">🔨</div>
            <div class="experiment-title">5. Crushers and Ball Mill</div>
            <div class="experiment-description">Size reduction equipment simulation and analysis of product size distribution.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('5. Crushers and Ball Mill', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('5. Crushers and Ball Mill', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('5. Crushers and Ball Mill', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('5. Crushers and Ball Mill', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('5. Crushers and Ball Mill', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">🔍</div>
            <div class="experiment-title">6. Plate and Frame Filter Press</div>
            <div class="experiment-description">Solid-liquid separation with analysis of filtration rates and cake formation.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('6. Plate and Frame Filter Press', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('6. Plate and Frame Filter Press', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('6. Plate and Frame Filter Press', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('6. Plate and Frame Filter Press', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('6. Plate and Frame Filter Press', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">🔄</div>
            <div class="experiment-title">7. Rotary Vacuum Filter</div>
            <div class="experiment-description">Continuous filtration process with drum operation visualization.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('7. Rotary Vacuum Filter', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('7. Rotary Vacuum Filter', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('7. Rotary Vacuum Filter', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('7. Rotary Vacuum Filter', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('7. Rotary Vacuum Filter', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">🌀</div>
            <div class="experiment-title">8. Centrifuge and Flotation</div>
            <div class="experiment-description">Solid-liquid separation in basket centrifuge and mineral separation in flotation cells.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('8. Centrifuge and Flotation', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('8. Centrifuge and Flotation', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('8. Centrifuge and Flotation', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('8. Centrifuge and Flotation', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('8. Centrifuge and Flotation', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">📊</div>
            <div class="experiment-title">9. Classifiers</div>
            <div class="experiment-description">Particle classification using cone classifiers and thickeners for solid-liquid separation.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('9. Classifiers', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('9. Classifiers', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('9. Classifiers', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('9. Classifiers', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('9. Classifiers', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">🥁</div>
            <div class="experiment-title">10. Trommel</div>
            <div class="experiment-description">Rotary screen simulation with particle size distribution and efficiency analysis.</div>
            <div class="experiment-actions">
                <a href="javascript:void(0)" onclick="navigateTo('10. Trommel', 'Simulation')" class="action-button tooltip">🔬<span class="tooltiptext">Simulation</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('10. Trommel', 'Demo Video')" class="action-button tooltip">📽️<span class="tooltiptext">Demo Video</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('10. Trommel', 'Chat Assistant')" class="action-button tooltip">💬<span class="tooltiptext">Chat Assistant</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('10. Trommel', 'Quiz')" class="action-button tooltip">📝<span class="tooltiptext">Quiz</span></a>
                <a href="javascript:void(0)" onclick="navigateTo('10. Trommel', 'Report Generation')" class="action-button tooltip">📋<span class="tooltiptext">Report</span></a>
            </div>
        </div>
    </div>
    """
    
    st.markdown(separation_cards_html, unsafe_allow_html=True)
    
    # Learning modes section
    st.markdown("<h2 class='section-title'>Learning Modes</h2>", unsafe_allow_html=True)
    
    # Create a simpler HTML structure for the learning mode cards
    learning_cards_html = """
    <div class="carousel-container">
        <div class="experiment-card">
            <div class="experiment-icon">🧪</div>
            <div class="experiment-title">Simulation Mode</div>
            <div class="experiment-description">Interact with virtual equipment, adjust parameters, and observe real-time results with data visualization.</div>
        </div>
        <div class="experiment-card">
            <div class="experiment-icon">🎥</div>
            <div class="experiment-title">Demo Video Mode</div>
            <div class="experiment-description">Watch demonstration videos showing real lab procedures and equipment operation.</div>
        </div>
        <div class="experiment-card">
            <div class="experiment-icon">📝</div>
            <div class="experiment-title">Quiz Mode</div>
            <div class="experiment-description">Test your knowledge and understanding of experiment principles with interactive quizzes.</div>
        </div>
        <div class="experiment-card">
            <div class="experiment-icon">📊</div>
            <div class="experiment-title">Report Generation</div>
            <div class="experiment-description">Create professional lab reports with your simulation data, analyses, and observations.</div>
        </div>
            <div class="experiment-card">
            <div class="experiment-icon">💬</div>
            <div class="experiment-title">Chat Assistant</div>
            <div class="experiment-description">Get help and answers to your questions about experiments and chemical engineering concepts.</div>
        </div>
            </div>
    """
    
    st.markdown(learning_cards_html, unsafe_allow_html=True)
    
    # Getting started info - normal streamlit component for better accessibility
    st.markdown("---")
    st.markdown("### 🚀 Getting Started")
    st.markdown("""
    1. Select an experiment from the sidebar
    2. Choose a mode (Simulation, Demo Video, Quiz, or Report Generation)
    3. Interact with the interface based on your selected mode
    4. Use the chat assistant if you need help
    """)
    
    st.success("All features are available! Select an experiment from the sidebar to begin exploring.")