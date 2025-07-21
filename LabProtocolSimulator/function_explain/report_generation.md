# Report Generation Feature

The Report Generation feature allows students to create professional laboratory reports by entering their observation data. It automates calculations, generates appropriate graphs, and produces formatted documents ready for submission.

## Implementation Overview

The report generation system is designed to:
1. Provide experiment-specific data entry forms
2. Automate calculations based on entered data
3. Generate visualizations of results
4. Create downloadable document reports (DOCX format)

## Code Structure

The report generation feature is implemented in the `chemengsim/report_generation/` directory. The main entry point is typically `main.py`, which handles experiment selection and delegates to experiment-specific modules.

```python
# Main entry point in app.py for the Report Generation feature
elif view_mode == "Report Generation":
    # Import and run the report generation module
    try:
        from chemengsim.report_generation import main as report_main
        report_main.main()
    except Exception as e:
        st.error(f"Error loading report generation module: {str(e)}")
        st.info("The report generation feature may still be under development for some experiments.")
```

## Report Generation Module Structure

The main report generation module typically follows this structure:

```python
import streamlit as st
import pandas as pd
import numpy as np
import subprocess
import sys
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
```

## Experiment-Specific Report Modules

Each experiment has its own report generation module following a similar pattern:

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .report_generator import ReportGenerator
import plotly.graph_objects as go

def calculate_results(data):
    """Calculate results from entered data"""
    # Experiment-specific calculation logic
    results = data.copy()
    # ... calculation steps ...
    return results

def generate_plots(results):
    """Generate visualization plots for the report"""
    # Create interactive plots for display in app
    fig = go.Figure()
    # ... plot configuration ...
    return fig

def generate_matplotlib_plots(results):
    """Generate static plots for embedding in documents"""
    # Create static plots for the Word document
    fig, ax = plt.subplots(figsize=(8, 5))
    # ... plot configuration ...
    return fig

def create_experiment_form():
    """Create input form for experiment data entry"""
    st.title("Experiment Name")
    
    st.markdown("""
    ## Experiment Description
    Brief explanation of the experiment and what will be calculated.
    """)
    
    # Constants section
    st.subheader("Constants")
    const1 = st.number_input("Constant 1", value=default_value)
    const2 = st.number_input("Constant 2", value=default_value)
    
    # Student information
    st.subheader("Student Information")
    student_name = st.text_input("Your Name", key="experiment_student_name")
    student_id = st.text_input("Your ID", key="experiment_student_id")
    
    # Observation data
    st.subheader("Observation Data")
    
    # Initialize or get session state
    if 'experiment_data' not in st.session_state:
        # Default empty dataframe with example structure
        st.session_state.experiment_data = pd.DataFrame({
            'Column1': [1, 2, 3],
            'Column2': ['', '', ''],
            'Column3': ['', '', '']
        })
    
    # Create a copy to edit
    edited_df = st.data_editor(
        st.session_state.experiment_data,
        use_container_width=True,
        num_rows="dynamic"
    )
    
    # Update session state when changes are made
    if edited_df is not None:
        st.session_state.experiment_data = edited_df
    
    # Generate report button
    generate_report = st.button("Generate Report", key="experiment_generate_report")
    
    if generate_report:
        if not student_name or not student_id:
            st.error("Please enter your name and ID before generating the report.")
            return
        
        # Check if all required data is entered
        if edited_df['Column2'].isna().any() or (edited_df['Column2'] == '').any():
            st.error("Please fill in all observation data before generating the report.")
            return
        
        # Generate report
        with st.spinner("Generating report..."):
            # Perform calculations
            results = calculate_results(edited_df)
            
            # Create interactive plot for display
            fig = generate_plots(results)
            
            # Create matplotlib plot for document
            doc_fig = generate_matplotlib_plots(results)
            
            # Display results
            st.subheader("Results")
            st.dataframe(results)
            
            # Display plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Create Word document report
            report = ReportGenerator("experiment_template", "Experiment Name")
            report.create_new_document()
            
            # Add student info
            student_info = {'name': student_name, 'id': student_id}
            report.add_title_page(student_info)
            
            # Add aim and objectives
            aim = "Aim of the experiment"
            objectives = [
                "Objective 1",
                "Objective 2"
            ]
            report.add_aim_and_objective(aim, objectives)
            
            # Add observations
            report.add_observation_table(edited_df)
            
            # Add calculations
            calculations_text = "Explanation of calculations performed..."
            sample_calculations = "Step-by-step example calculation..."
            report.add_calculations(calculations_text, sample_calculations)
            
            # Add results
            report.add_results_table(results)
            
            # Add graph
            report.add_graph(doc_fig, "Figure Caption")
            
            # Add discussion
            discussion = [
                "Discussion point 1...",
                "Discussion point 2..."
            ]
            report.add_discussion(discussion)
            
            # Add conclusion
            conclusion = [
                "Conclusion 1...",
                "Conclusion 2..."
            ]
            report.add_conclusion(conclusion)
            
            # Create download button
            report.create_downloadable_report()

def main():
    """Entry point for the experiment module when called from main.py"""
    create_experiment_form()
```

## Report Generator Class

The core functionality is implemented in a `ReportGenerator` class that handles document creation:

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
import io
import base64
import streamlit as st
import pandas as pd
from datetime import datetime

class ReportGenerator:
    """Class to generate formatted lab reports"""
    
    def __init__(self, template_name, experiment_title):
        """Initialize with template name and experiment title"""
        self.template_name = template_name
        self.experiment_title = experiment_title
        self.document = None
    
    def create_new_document(self):
        """Create a new document"""
        self.document = Document()
        # Set default font
        style = self.document.styles['Normal']
        font = style.font
        font.name = 'Calibri'
        font.size = Pt(11)
    
    def add_title_page(self, student_info):
        """Add a title page with student information"""
        # Add title
        title = self.document.add_heading(self.experiment_title, 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add student info
        student_para = self.document.add_paragraph()
        student_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        student_para.add_run(f"Name: {student_info['name']}\n").bold = True
        student_para.add_run(f"ID: {student_info['id']}\n").bold = True
        student_para.add_run(f"Date: {datetime.now().strftime('%B %d, %Y')}").bold = True
        
        # Add page break
        self.document.add_page_break()
    
    def add_aim_and_objective(self, aim, objectives):
        """Add aim and objectives section"""
        self.document.add_heading("Aim", level=1)
        self.document.add_paragraph(aim)
        
        self.document.add_heading("Objectives", level=1)
        for objective in objectives:
            self.document.add_paragraph(objective, style='List Bullet')
    
    def add_observation_table(self, table_data, table_title="Observations"):
        """Add a table of observations"""
        self.document.add_heading(table_title, level=1)
        
        # Convert dataframe to a Word table
        table = self.document.add_table(rows=1, cols=len(table_data.columns))
        table.style = 'Table Grid'
        
        # Add header row
        header_cells = table.rows[0].cells
        for i, column_name in enumerate(table_data.columns):
            header_cells[i].text = column_name
        
        # Add data rows
        for _, row in table_data.iterrows():
            row_cells = table.add_row().cells
            for i, value in enumerate(row):
                row_cells[i].text = str(value)
    
    def add_calculations(self, calculations_text, sample_calculations):
        """Add a calculations section"""
        self.document.add_heading("Calculations", level=1)
        self.document.add_paragraph(calculations_text)
        
        self.document.add_heading("Sample Calculations", level=2)
        self.document.add_paragraph(sample_calculations)
    
    def add_results_table(self, results_data, table_title="Results"):
        """Add a table of results"""
        self.document.add_heading(table_title, level=1)
        
        # Convert dataframe to a Word table
        table = self.document.add_table(rows=1, cols=len(results_data.columns))
        table.style = 'Table Grid'
        
        # Add header row
        header_cells = table.rows[0].cells
        for i, column_name in enumerate(results_data.columns):
            header_cells[i].text = column_name
        
        # Add data rows
        for _, row in results_data.iterrows():
            row_cells = table.add_row().cells
            for i, value in enumerate(row):
                row_cells[i].text = str(value)
    
    def add_graph(self, fig, caption, width=6):
        """Add a matplotlib figure to the document"""
        # Save the figure to a bytes buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        
        # Add the figure to the document
        self.document.add_picture(buf, width=Inches(width))
        
        # Add caption
        caption_para = self.document.add_paragraph(caption)
        caption_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_para.style = 'Caption'
    
    def add_discussion(self, discussion_text):
        """Add a discussion section"""
        self.document.add_heading("Discussion", level=1)
        
        if isinstance(discussion_text, list):
            for paragraph in discussion_text:
                self.document.add_paragraph(paragraph)
        else:
            self.document.add_paragraph(discussion_text)
    
    def add_conclusion(self, conclusion_text):
        """Add a conclusion section"""
        self.document.add_heading("Conclusion", level=1)
        
        if isinstance(conclusion_text, list):
            for paragraph in conclusion_text:
                self.document.add_paragraph(paragraph)
        else:
            self.document.add_paragraph(conclusion_text)
    
    def generate_report_download_link(self, document, filename):
        """Generate download link for a document"""
        # Save document to bytes buffer
        buf = io.BytesIO()
        document.save(buf)
        buf.seek(0)
        
        # Create a download link
        b64 = base64.b64encode(buf.read()).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{filename}">Download {filename}</a>'
        return href
    
    def create_downloadable_report(self):
        """Create a downloadable report"""
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.template_name}_{timestamp}.docx"
        
        # Create download link
        download_link = self.generate_report_download_link(self.document, filename)
        st.markdown(download_link, unsafe_allow_html=True)
        
        # Also provide standard Streamlit download option
        bio = io.BytesIO()
        self.document.save(bio)
        st.download_button(
            label="Download Report",
            data=bio.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
```

## Supporting Utility Functions

Additional utility functions are often implemented to support report generation:

```python
# Utility module: report_utils.py
import streamlit as st
import io
import base64
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_download_link(content, filename, display_text):
    """Create a download link for any file content"""
    b64 = base64.b64encode(content).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{display_text}</a>'

def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    return base64.b64encode(buf.read()).decode()

def create_table_dataframe(data, headers):
    """Create a pandas DataFrame from raw data and headers"""
    df = pd.DataFrame(data, columns=headers)
    return df
```

## Dependencies

The Report Generation feature has several external dependencies:

- **Streamlit**: For UI components and user interaction
- **Python-DOCX**: For creating Word documents
  - Install with: `pip install python-docx`
- **DocXTpl**: For template-based document generation (optional)
  - Install with: `pip install docxtpl`
- **Pandas**: For data handling and table creation
- **NumPy**: For numerical calculations
- **Matplotlib**: For creating static graphs for document embedding
- **Plotly**: For interactive visualizations in the web interface
- **Pdfkit** (optional): For PDF conversion
  - Install with: `pip install pdfkit`
  - Requires `wkhtmltopdf` system dependency

## Extending the Report Generation Feature

To add a new experiment report generator:

1. Create a new module in `chemengsim/report_generation/`
2. Implement the necessary calculation functions
3. Create a form for data entry
4. Design appropriate visualizations
5. Add the report generation logic using the ReportGenerator class
6. Update the main.py module to include the new experiment

This modular approach allows for easy addition of new experiment reports without modifying the core report generation code. 