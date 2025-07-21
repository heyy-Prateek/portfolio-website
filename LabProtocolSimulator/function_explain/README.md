# Chemical Engineering Laboratory Simulator - Features Guide

This folder contains detailed documentation for the four main features of the Chemical Engineering Laboratory Simulator application:

1. [Simulation](./simulation.md) - Interactive simulations of chemical engineering experiments
2. [Demo Video](./demo_video.md) - Educational videos demonstrating laboratory procedures
3. [Quiz](./quiz.md) - Knowledge assessment tools for each experiment
4. [Report Generation](./report_generation.md) - Tools to create professional lab reports

Each documentation file explains the feature's implementation with code examples and detailed explanations.

## Feature Overview

| Feature | Description | Key Components |
|---------|-------------|----------------|
| Simulation | Interactive simulator for each experiment with adjustable parameters | Dynamic parameter inputs, Real-time calculations, Interactive visualization |
| Demo Video | Video demonstrations of actual laboratory procedures | Embedded videos, Descriptive text, Links to additional resources |
| Quiz | Knowledge assessment for each experiment | Multiple choice questions, Assessment scoring, Progress tracking |
| Report Generation | Professional report creation tools | Data input forms, Calculation automation, DOCX/PDF generation |

## Implementation Architecture

All features are implemented within the application's modular architecture:

```
chemengsim/
  ├── experiments/       # Simulation modules
  ├── videos/            # Demo video modules  
  ├── quizzes/           # Quiz modules
  ├── report_generation/ # Report generation modules
  └── app.py             # Main application entry point
```

## Common Implementation Patterns

All features follow similar implementation patterns:

1. **Main Entry Point**: Each feature has a main entry function in app.py
2. **Module-based Architecture**: Features are organized in dedicated directories
3. **Dynamic Loading**: Experiment-specific modules are loaded based on user selection
4. **Consistent UI**: Streamlit components provide a uniform interface

## Function Implementation Details

### Main App Controller (app.py)

The main application controller in `app.py` handles mode selection and routes to the appropriate module based on user selection:

```python
# Display the appropriate experiment page based on selection
if experiment == "Home":
    display_home_page()
elif view_mode == "Chat Assistant":
    # Chat assistant implementation
    from chemengsim import chat
    chat.chat_interface()
elif view_mode == "Quiz":
    # Quiz implementation
    exp_num = int(experiment.split(".")[0])
    from chemengsim.quizzes import quiz_module
    quiz_module.run_quiz(exp_names[exp_num])
elif view_mode == "Demo Video":
    # Demo video implementation
    if experiment != "Home":
        exp_num = int(experiment.split(".")[0])
        from chemengsim.videos import demo_videos
        demo_videos.display_demo_video(exp_names[exp_num])
    else:
        # Display demo video homepage
elif view_mode == "Report Generation":
    # Report generation implementation
    from chemengsim.report_generation import main as report_main
    report_main.main()
else:  # Simulation mode
    # Dynamic import of the experiment module
    module_name = f"chemengsim.experiments.{exp_names[exp_num]}"
    module = __import__(module_name, fromlist=['app'])
    module.app()
```

### Key Functions in Each Feature

#### 1. Simulation Feature

- **app()** - Main entry point for each experiment simulation
- **calculate_results()** - Implements mathematical models and calculations
- **create_visualization()** - Generates interactive plots and diagrams
- **handle_user_input()** - Processes UI interactions and parameter changes

#### 2. Demo Video Feature

- **display_demo_video()** - Renders embedded videos with contextual information
- **load_video_sources()** - Manages the catalog of available videos
- **handle_playback_options()** - Controls video playback settings

#### 3. Quiz Feature

- **run_quiz()** - Main quiz controller function
- **load_quiz_data()** - Loads question sets from files or dictionaries
- **display_question()** - Renders different question types
- **check_answer()** - Evaluates user responses and provides feedback
- **track_progress()** - Manages quiz state and score

#### 4. Report Generation Feature

- **main()** - Handles experiment selection for report generation
- **check_dependencies()** - Verifies required packages are installed
- **create_experiment_form()** - Generates data entry forms
- **calculate_results()** - Performs experiment-specific calculations
- **generate_plots()** - Creates visualizations for reports
- **create_downloadable_report()** - Produces formatted document files

## Dependencies

The application has several dependencies, varying by feature:

### Core Dependencies (required for all features)

- **Python 3.8+**: Base programming language
- **Streamlit**: Web application framework for UI
  - Install with: `pip install streamlit`
- **Pandas**: Data manipulation library
  - Install with: `pip install pandas`
- **NumPy**: Numerical computation library
  - Install with: `pip install numpy`
- **Matplotlib**: Static visualization library
  - Install with: `pip install matplotlib`
- **Plotly**: Interactive visualization library
  - Install with: `pip install plotly`

### Feature-Specific Dependencies

#### Simulation Feature

- **SciPy**: For differential equation solving and scientific calculations
  - Install with: `pip install scipy`

#### Demo Video Feature

- No additional dependencies beyond core libraries
- Internet connection for streaming videos

#### Quiz Feature

- **JSON**: For quiz data storage (part of Python standard library)

#### Report Generation Feature

- **Python-DOCX**: For Word document creation
  - Install with: `pip install python-docx`
- **DocXTpl** (optional): For template-based document generation
  - Install with: `pip install docxtpl`
- **Pdfkit** (optional): For PDF conversion
  - Install with: `pip install pdfkit`
  - Requires wkhtmltopdf system dependency

### Environment Setup

To set up the development environment with all dependencies:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies
pip install streamlit pandas numpy matplotlib plotly

# Install feature-specific dependencies
pip install scipy python-docx docxtpl pdfkit
```

## Extending the Application

The modular architecture makes it easy to extend the application:

1. **Add New Experiments**: Create new modules in the respective feature directories
2. **Enhance Existing Features**: Modify specific modules without affecting other parts
3. **Add New Features**: Create new directories and update the main app controller

For detailed implementation guidance for each feature, see the individual documentation files. 