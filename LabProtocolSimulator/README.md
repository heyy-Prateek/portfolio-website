# Chemical Engineering Laboratory Simulator

A comprehensive virtual laboratory application for Chemical Engineering students to simulate, learn, and practice various chemical engineering experiments.

## 📝 Overview

This application provides a platform for students to:
- Run interactive simulations of chemical engineering experiments
- Watch demonstration videos of laboratory procedures
- Take quizzes to test their knowledge
- Generate professional lab reports based on their data
- Get instant answers to chemical engineering questions through a chat assistant

## 🧪 Features

### 1. Simulation Mode

Run virtual experiments with adjustable parameters and real-time visualization:

- **Reactor Experiments**
  - Isothermal Batch Reactor
  - Isothermal Semi-batch Reactor
  - Isothermal CSTR
  - Isothermal PFR

- **Solid-Liquid Separation**
  - Plate and Frame Filter Press
  - Rotary Vacuum Filter
  - Centrifuge and Flotation
  - Classifiers

- **Particle Size Reduction**
  - Crushers and Ball Mill
  - Trommel

### 2. Demo Video Mode

Watch professionally recorded videos demonstrating actual laboratory procedures and equipment operation.

### 3. Quiz Mode

Test your understanding of chemical engineering concepts through interactive quizzes for each experiment.

### 4. Report Generation

Create professional laboratory reports by entering your observation data, with automatic calculations and visualization.

### 5. Chat Assistant

Get instant answers to your questions about chemical engineering concepts, experimental procedures, and calculations through an interactive chat interface.

### 6. Modern React UI (New!)

A modern, responsive React-based user interface with:
- Dark/Light theme support
- Real-time data visualization
- Interactive experiment controls
- Mobile-friendly design

## 💻 Implementation Details

### Core Application (`app.py`)

The main application controller that handles experiment selection and mode switching:

```python
def main():
    # Configure app title and UI elements
    st.title("Chemical Engineering Laboratory Simulator")
    
    # Set up sidebar navigation
    st.sidebar.title("Experiment Selection")
    view_mode = st.sidebar.radio("Mode", 
        ["Simulation", "Demo Video", "Quiz", "Report Generation", "Chat Assistant"])
    
    # Select experiment from dropdown
    experiment = st.sidebar.selectbox("Choose an experiment", 
        ["Home", "1. Isothermal Batch Reactor", ...])
    
    # Route to appropriate module based on selection
    if experiment == "Home":
        display_home_page()
    elif view_mode == "Chat Assistant":
        chat.chat_interface()
    elif view_mode == "Quiz":
        quiz_module.run_quiz(exp_names[exp_num])
    elif view_mode == "Demo Video":
        demo_videos.display_demo_video(exp_names[exp_num])
    elif view_mode == "Report Generation":
        report_main.main()
    else:  # Simulation mode
        # Dynamic import of experiment module
        module_name = f"chemengsim.experiments.{exp_names[exp_num]}"
        module = __import__(module_name, fromlist=['app'])
        module.app()
```

### React UI and Simulator Bridge

The application includes a modern React-based UI that communicates with the Python backend through a comprehensive API bridge:

#### FastAPI Backend (`api.py`)

The backend API handles requests from the React frontend and manages experiment simulations:

```python
@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            await handle_websocket_message(websocket, message)
    except WebSocketDisconnect:
        # Handle disconnect
        pass
```

Key API features:
- Real-time data streaming via WebSockets
- REST endpoints for experiment data
- Report generation services
- Dynamic experiment discovery

#### Simulator Bridge (`SimulatorBridge.js`)

The frontend bridge manages communication with the Python backend:

```javascript
// Singleton instance
const simulatorBridge = new SimulatorBridge();

/**
 * Hook to use the simulator bridge in React components
 */
export const useSimulatorBridge = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [experimentData, setExperimentData] = useState({});
  const [simulationState, setSimulationState] = useState({ status: 'idle' });
  
  useEffect(() => {
    // Initialize simulator bridge on component mount
    simulatorBridge.initialize();
    
    // Set up event listeners for real-time updates
    const connectionListener = simulatorBridge.addListener('connection', (data) => {
      setIsConnected(data.status === 'connected');
    });
    
    // Clean up listeners on component unmount
    return () => {
      connectionListener();
    };
  }, []);
  
  return {
    isConnected,
    experimentData,
    simulationState,
    startExperiment: simulatorBridge.startExperiment.bind(simulatorBridge),
    // Additional methods...
  };
};
```

#### Data Visualization

Real-time data visualization using SVG-based charts:

```javascript
const ExperimentChart = ({ data, type = 'concentration' }) => {
  // Prepare chart data
  const chartData = useMemo(() => {
    if (!data) return null;
    
    // Extract relevant data based on chart type
    switch (type) {
      case 'concentration':
        return {
          labels: data.times,
          datasets: [
            {
              label: 'Concentration A',
              data: data.conc_a,
              // Styling properties...
            },
            // Additional datasets...
          ]
        };
        
      // Other chart types...
    }
  }, [data, type]);
  
  // Render chart
  return (
    <ChartContainer>
      <ChartHeader>
        <ChartTitle>{/* Chart title */}</ChartTitle>
      </ChartHeader>
      {/* Chart rendering */}
    </ChartContainer>
  );
};
```

### Simulation Feature

Each experiment is implemented as a separate module in `chemengsim/experiments/` with a consistent structure:

```python
def app():
    """Main function for the experiment simulation"""
    st.title("Experiment Name")
    
    # 1. Parameter Input Section
    st.sidebar.header("Simulation Parameters")
    param1 = st.sidebar.slider("Parameter 1", min_value, max_value, default_value)
    
    # 2. Calculation Model
    results = calculate_results(param1)
    
    # 3. Visualization
    fig = create_visualization(results)
    st.plotly_chart(fig)
    
    # 4. Results and Interpretation
    st.dataframe(results)
```

Key simulation functions:
- `calculate_results()`: Implements the mathematical model for each experiment
- `create_visualization()`: Generates interactive plots using Plotly
- `handle_user_input()`: Manages parameter changes and updates

### Demo Video Feature

The demo video system in `chemengsim/videos/` manages video content and playback:

```python
def display_demo_video(experiment_name):
    """Display demonstration video with contextual information"""
    if experiment_name in VIDEO_SOURCES:
        video_data = VIDEO_SOURCES[experiment_name]
        
        # Display video title and embedded video
        st.title(video_data["title"])
        st.video(video_data["source"])
        
        # Display description
        st.markdown("## Video Description")
        st.markdown(video_data["description"])
```

Video implementation options:
- YouTube embedding via `st.video()`
- Local video files for offline use
- Custom embedding options for other platforms

### Quiz Feature

The quiz system in `chemengsim/quizzes/` provides interactive assessments:

```python
def run_quiz(experiment_name):
    """Main function to run the quiz for an experiment"""
    st.title(f"Quiz: {experiment_name.replace('_', ' ').title()}")
    
    # Load quiz questions
    questions = load_quiz_data(experiment_name)
    
    # Initialize session state
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.score = 0
    
    # Display current question
    current_question = questions[st.session_state.question_index]
    if current_question["type"] == "multiple_choice":
        display_multiple_choice(current_question)
    elif current_question["type"] == "numerical":
        display_numerical(current_question)
```

Quiz module components:
- `load_quiz_data()`: Retrieves questions from JSON files or dictionaries
- `display_multiple_choice()`: Renders multiple choice questions with options
- `display_numerical()`: Creates numerical input questions with validation
- `check_answer()`: Evaluates user responses and updates score

### Report Generation

The report generation system in `chemengsim/report_generation/` automates lab report creation:

```python
def create_experiment_form():
    """Create input form for experiment data entry"""
    st.title("Experiment Name")
    
    # Constants section
    st.subheader("Constants")
    const1 = st.number_input("Constant 1", value=default_value)
    
    # Student information
    student_name = st.text_input("Your Name", key="unique_key")
    
    # Observation data
    edited_df = st.data_editor(
        st.session_state.experiment_data,
        num_rows="dynamic"
    )
    
    # Generate report button
    if st.button("Generate Report", key="unique_button_key"):
        results = calculate_results(edited_df)
        fig = generate_plots(results)
        
        # Create Word document report
        report = ReportGenerator("experiment", "Title")
        report.create_new_document()
        report.add_title_page(student_info)
        report.add_observation_table(edited_df)
        report.add_graph(fig, "Caption")
        report.create_downloadable_report()
```

Report generation components:
- `ReportGenerator` class: Core document generation functionality
- `check_dependencies()`: Ensures required packages are installed
- `calculate_results()`: Performs experiment-specific calculations
- `generate_plots()`: Creates visualizations for reports
- `create_downloadable_report()`: Produces formatted DOCX files

### Chat Assistant

The chat assistant system in `chemengsim/chat.py` provides interactive help for chemical engineering concepts:

```python
def chat_interface():
    """Displays a chat interface for answering chemical engineering questions"""
    st.title("Chemical Engineering Chat Assistant")
    
    # Chat input
    user_input = st.chat_input("Ask a question about chemical engineering...")
    
    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Generate and display response
        with st.chat_message("assistant"):
            response = generate_response(user_input)
            st.markdown(response)
```

Chat assistant components:
- `chat_interface()`: Main function for displaying the chat UI
- `generate_response()`: Analyzes user questions and provides relevant answers
- Topic coverage includes reactors, separation techniques, size reduction, and report preparation

## 📋 Dependencies

### Core Dependencies
- **Python 3.8+**
- **Streamlit**: Web application framework
  ```bash
  pip install streamlit
  ```
- **Pandas**: Data manipulation and analysis
  ```bash
  pip install pandas
  ```
- **NumPy**: Numerical computation
  ```bash
  pip install numpy
  ```

### Feature-Specific Dependencies

#### Simulation Dependencies
- **Matplotlib**: Plotting library
  ```bash
  pip install matplotlib
  ```
- **Plotly**: Interactive visualization
  ```bash
  pip install plotly
  ```
- **SciPy**: Scientific computing
  ```bash
  pip install scipy
  ```

#### Report Generation Dependencies
- **Python-DOCX**: Word document generation
  ```bash
  pip install python-docx
  ```
- **DOCXTPL**: Word document templating
  ```bash
  pip install docxtpl
  ```

#### React UI Dependencies
- **FastAPI**: API framework for backend
  ```bash
  pip install fastapi uvicorn
  ```
- **React**: JS framework for UI
- **Styled Components**: CSS-in-JS library
- **React Router**: Navigation for React

## 🚀 Installation and Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/chemengsim.git
   cd chemengsim
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Build the React UI (requires Node.js):
   ```bash
   python run.py build --react
   ```

5. Run the application:
   ```bash
   python run.py run
   ```

## 🌐 Mobile Support

The application can be accessed on mobile devices through:
- Web browser
- Streamlit's mobile-friendly interface
- React UI with responsive design

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Creator

Developed by Saxen for Chemical Engineering students. 