# repybridge.py
from flask import Flask, request, jsonify, send_from_directory
import threading
import webbrowser
import os
import sys
import json
from importlib import import_module

# Create Flask app
app = Flask(__name__, static_folder='react_build')

# Store experiment data
experiment_data = {}

@app.route('/api/experiments', methods=['GET'])
def get_experiments():
    """Return list of all experiments"""
    experiments = [
        {"id": 1, "name": "Isothermal Batch Reactor"},
        {"id": 2, "name": "Isothermal Semi-batch Reactor"},
        {"id": 3, "name": "Isothermal CSTR"},
        {"id": 4, "name": "Isothermal PFR"},
        {"id": 5, "name": "Crushers and Ball Mill"},
        {"id": 6, "name": "Plate and Frame Filter Press"},
        {"id": 7, "name": "Rotary Vacuum Filter"},
        {"id": 8, "name": "Centrifuge and Flotation"},
        {"id": 9, "name": "Classifiers"},
        {"id": 10, "name": "Trommel"}
    ]
    return jsonify(experiments)

@app.route('/api/run_simulation', methods=['POST'])
def run_simulation():
    """Run a simulation based on provided parameters"""
    data = request.json
    exp_id = data.get('experimentId')
    params = data.get('parameters', {})
    
    try:
        # Map experiment ID to module name
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
        
        # Import the appropriate module
        if 1 <= exp_id <= 10:
            module_name = f"chemengsim.experiments.{exp_names[exp_id]}"
            try:
                module = import_module(module_name)
                # Call the simulation function with parameters
                result = module.run_simulation_api(params)
                return jsonify({"success": True, "data": result})
            except Exception as e:
                return jsonify({"success": False, "error": str(e)})
        else:
            return jsonify({"success": False, "error": "Invalid experiment ID"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/chat', methods=['POST'])
def chat_query():
    """Process chat queries"""
    data = request.json
    query = data.get('query', '')
    use_api = data.get('use_api', False)
    
    try:
        # Import chat module
        from chemengsim import chat
        if use_api:
            response, source = chat.generate_response_with_api(query)
        else:
            response, source = chat.generate_response_builtin(query)
        return jsonify({"response": response, "source": source})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}", "source": "Error"})

@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate a report based on provided data"""
    data = request.json
    experiment = data.get('experiment')
    report_format = data.get('format', 'docx')
    student_name = data.get('studentName', '')
    exp_data = data.get('data', [])
    
    try:
        # Import report generation module
        from chemengsim.report_generation import main as report_main
        # Call the report generation function with parameters
        result = report_main.generate_report_api(experiment, report_format, student_name, exp_data)
        return jsonify({"success": True, "report_path": result})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Serve React frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def start_react_ui(port=5000):
    """Start the Flask server to serve the React UI"""
    # Start Flask in a new thread
    threading.Thread(target=lambda: app.run(port=port, debug=False, use_reloader=False)).start()
    
    # Open browser
    webbrowser.open(f'http://localhost:{port}')
    
    return f"React UI started at http://localhost:{port}" 