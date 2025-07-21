import json
import asyncio
import uvicorn
import threading
import time
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import simulator modules
import chemengsim.experiments as experiments
from chemengsim.report_generation import generate_report

# Create FastAPI app
app = FastAPI(title="Chemical Engineering Simulator API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve React build files
static_files_path = os.path.join(os.path.dirname(__file__), "react_build")
if os.path.exists(static_files_path):
    app.mount("/", StaticFiles(directory=static_files_path, html=True), name="static")

# Active WebSocket connections
active_connections: List[WebSocket] = []

# Active simulations
active_simulations: Dict[str, Dict[str, Any]] = {}

# Models for request validation
class ExperimentParameters(BaseModel):
    experimentId: str
    parameters: Dict[str, Any] = {}

class SimulationUpdate(BaseModel):
    parameters: Dict[str, Any]

class ReportOptions(BaseModel):
    experimentId: str
    title: Optional[str] = None
    description: Optional[str] = None
    includeCharts: bool = True
    format: str = "docx"

# Add route for React UI
@app.get("/react", response_class=HTMLResponse)
async def get_react_ui():
    """Serve the React UI"""
    react_ui_path = os.path.join(os.path.dirname(__file__), "react_build", "index.html")
    if os.path.exists(react_ui_path):
        with open(react_ui_path, "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    else:
        # Print debug information
        print(f"React UI not found at {react_ui_path}")
        base_dir = os.path.dirname(__file__)
        print(f"Base directory: {base_dir}")
        react_build_dir = os.path.join(base_dir, "react_build")
        print(f"React build directory: {react_build_dir}")
        if os.path.exists(react_build_dir):
            print(f"Contents of react_build directory:")
            for item in os.listdir(react_build_dir):
                print(f"  - {item}")
        
        raise HTTPException(status_code=404, detail="React UI not found")

# API routes
@app.get("/api/status")
async def get_status():
    """Check if the API is running"""
    return {"status": "ok", "version": "1.0"}

@app.get("/api/experiments")
async def get_experiments():
    """Get all available experiments"""
    try:
        # Get experiment data from the experiments module
        experiment_data = []
        experiment_modules = experiments.get_experiments()
        
        for exp_id, exp_module in experiment_modules.items():
            experiment_data.append({
                "id": exp_id,
                "name": exp_module.name,
                "description": exp_module.description,
                "thumbnail": f"/api/experiments/{exp_id}/thumbnail" if hasattr(exp_module, "thumbnail") else None,
                "parameters": exp_module.default_parameters if hasattr(exp_module, "default_parameters") else {}
            })
            
        return experiment_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get experiments: {str(e)}")

@app.get("/api/experiments/{experiment_id}")
async def get_experiment_details(experiment_id: str):
    """Get details of a specific experiment"""
    try:
        # Get experiment data from the experiments module
        experiment_modules = experiments.get_experiments()
        
        if experiment_id not in experiment_modules:
            raise HTTPException(status_code=404, detail=f"Experiment with ID {experiment_id} not found")
            
        exp_module = experiment_modules[experiment_id]
        
        return {
            "id": experiment_id,
            "name": exp_module.name,
            "description": exp_module.description,
            "thumbnail": f"/api/experiments/{experiment_id}/thumbnail" if hasattr(exp_module, "thumbnail") else None,
            "parameters": exp_module.default_parameters if hasattr(exp_module, "default_parameters") else {},
            "equations": exp_module.equations if hasattr(exp_module, "equations") else [],
            "variables": exp_module.variables if hasattr(exp_module, "variables") else {}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get experiment details: {str(e)}")

@app.get("/api/experiments/{experiment_id}/thumbnail")
async def get_experiment_thumbnail(experiment_id: str):
    """Get thumbnail for a specific experiment"""
    try:
        # Get experiment data from the experiments module
        experiment_modules = experiments.get_experiments()
        
        if experiment_id not in experiment_modules:
            raise HTTPException(status_code=404, detail=f"Experiment with ID {experiment_id} not found")
            
        exp_module = experiment_modules[experiment_id]
        
        if not hasattr(exp_module, "thumbnail") or not os.path.exists(exp_module.thumbnail):
            # Return default thumbnail
            default_thumbnail = os.path.join(os.path.dirname(__file__), "static/default_thumbnail.png")
            return FileResponse(default_thumbnail)
            
        return FileResponse(exp_module.thumbnail)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get experiment thumbnail: {str(e)}")

@app.post("/api/report")
async def create_report(report_options: ReportOptions):
    """Generate a report for an experiment"""
    try:
        # Check if experiment exists
        experiment_modules = experiments.get_experiments()
        
        if report_options.experimentId not in experiment_modules:
            raise HTTPException(status_code=404, detail=f"Experiment with ID {report_options.experimentId} not found")
            
        # Generate report using the report_generation module
        report_path = generate_report(
            experiment_id=report_options.experimentId,
            title=report_options.title,
            description=report_options.description,
            include_charts=report_options.includeCharts,
            format=report_options.format
        )
        
        if not report_path or not os.path.exists(report_path):
            raise HTTPException(status_code=500, detail="Failed to generate report")
            
        # Return download link
        report_filename = os.path.basename(report_path)
        return {
            "success": True,
            "reportPath": f"/api/reports/{report_filename}",
            "reportName": report_filename
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.get("/api/reports/{filename}")
async def get_report(filename: str):
    """Download a generated report"""
    try:
        reports_dir = os.path.join(os.path.dirname(__file__), "reports")
        report_path = os.path.join(reports_dir, filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail=f"Report {filename} not found")
            
        return FileResponse(
            report_path,
            filename=filename,
            media_type="application/octet-stream"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get report: {str(e)}")

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                await handle_websocket_message(websocket, message)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "payload": {"message": "Invalid JSON format"}
                })
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        if websocket in active_connections:
            active_connections.remove(websocket)

async def handle_websocket_message(websocket: WebSocket, message: Dict[str, Any]):
    """Handle incoming WebSocket messages"""
    message_type = message.get("type", "")
    payload = message.get("payload", {})
    
    if message_type == "start_experiment":
        await start_experiment(websocket, payload)
    elif message_type == "stop_experiment":
        await stop_experiment(websocket)
    elif message_type == "pause_experiment":
        await pause_experiment(websocket)
    elif message_type == "resume_experiment":
        await resume_experiment(websocket)
    elif message_type == "update_parameters":
        await update_experiment_parameters(websocket, payload)
    else:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": f"Unknown message type: {message_type}"}
        })

async def start_experiment(websocket: WebSocket, data: Dict[str, Any]):
    """Start a new experiment simulation"""
    experiment_id = data.get("experimentId")
    parameters = data.get("parameters", {})
    
    if not experiment_id:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "Missing experimentId"}
        })
        return
        
    try:
        # Get experiment from experiments module
        experiment_modules = experiments.get_experiments()
        
        if experiment_id not in experiment_modules:
            await websocket.send_json({
                "type": "error",
                "payload": {"message": f"Experiment with ID {experiment_id} not found"}
            })
            return
            
        exp_module = experiment_modules[experiment_id]
        
        # Create a copy of default parameters and update with provided parameters
        merged_parameters = {}
        if hasattr(exp_module, "default_parameters"):
            merged_parameters.update(exp_module.default_parameters)
        merged_parameters.update(parameters)
        
        # Create simulation instance
        simulation_instance = {
            "id": f"sim_{time.time()}",
            "experiment_id": experiment_id,
            "module": exp_module,
            "parameters": merged_parameters,
            "websocket": websocket,
            "running": True,
            "paused": False,
            "data": {},
            "start_time": time.time(),
            "thread": None
        }
        
        # Start simulation in a separate thread
        thread = threading.Thread(
            target=run_simulation,
            args=(simulation_instance,)
        )
        thread.daemon = True
        simulation_instance["thread"] = thread
        
        # Store simulation instance
        client_id = id(websocket)
        active_simulations[client_id] = simulation_instance
        
        # Start simulation thread
        thread.start()
        
        # Send confirmation
        await websocket.send_json({
            "type": "simulation_state",
            "payload": {
                "status": "running",
                "simulationId": simulation_instance["id"],
                "experimentId": experiment_id
            }
        })
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": f"Failed to start experiment: {str(e)}"}
        })

async def stop_experiment(websocket: WebSocket):
    """Stop the current experiment simulation"""
    client_id = id(websocket)
    
    if client_id not in active_simulations:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "No active simulation to stop"}
        })
        return
        
    # Set running flag to False to stop simulation thread
    active_simulations[client_id]["running"] = False
    
    # Wait for thread to finish
    if active_simulations[client_id]["thread"] and active_simulations[client_id]["thread"].is_alive():
        active_simulations[client_id]["thread"].join(timeout=2)
    
    # Remove simulation from active simulations
    simulation_id = active_simulations[client_id]["id"]
    experiment_id = active_simulations[client_id]["experiment_id"]
    del active_simulations[client_id]
    
    # Send confirmation
    await websocket.send_json({
        "type": "simulation_state",
        "payload": {
            "status": "stopped",
            "simulationId": simulation_id,
            "experimentId": experiment_id
        }
    })

async def pause_experiment(websocket: WebSocket):
    """Pause the current experiment simulation"""
    client_id = id(websocket)
    
    if client_id not in active_simulations:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "No active simulation to pause"}
        })
        return
        
    # Set paused flag to True to pause simulation
    active_simulations[client_id]["paused"] = True
    
    # Send confirmation
    await websocket.send_json({
        "type": "simulation_state",
        "payload": {
            "status": "paused",
            "simulationId": active_simulations[client_id]["id"],
            "experimentId": active_simulations[client_id]["experiment_id"]
        }
    })

async def resume_experiment(websocket: WebSocket):
    """Resume the paused experiment simulation"""
    client_id = id(websocket)
    
    if client_id not in active_simulations:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "No active simulation to resume"}
        })
        return
        
    # Set paused flag to False to resume simulation
    active_simulations[client_id]["paused"] = False
    
    # Send confirmation
    await websocket.send_json({
        "type": "simulation_state",
        "payload": {
            "status": "running",
            "simulationId": active_simulations[client_id]["id"],
            "experimentId": active_simulations[client_id]["experiment_id"]
        }
    })

async def update_experiment_parameters(websocket: WebSocket, parameters: Dict[str, Any]):
    """Update parameters of the current experiment simulation"""
    client_id = id(websocket)
    
    if client_id not in active_simulations:
        await websocket.send_json({
            "type": "error",
            "payload": {"message": "No active simulation to update parameters"}
        })
        return
        
    # Update parameters
    active_simulations[client_id]["parameters"].update(parameters)
    
    # Send confirmation
    await websocket.send_json({
        "type": "parameters_updated",
        "payload": {
            "simulationId": active_simulations[client_id]["id"],
            "experimentId": active_simulations[client_id]["experiment_id"],
            "parameters": active_simulations[client_id]["parameters"]
        }
    })

def run_simulation(simulation):
    """Run a simulation in a separate thread"""
    try:
        # Get the experiment module and simulation parameters
        exp_module = simulation["module"]
        parameters = simulation["parameters"]
        websocket = simulation["websocket"]
        
        # Create a simulation instance
        if hasattr(exp_module, "Simulation"):
            sim_instance = exp_module.Simulation(parameters)
        else:
            # Use a generic simulation runner if no custom class exists
            sim_instance = GenericSimulation(exp_module, parameters)
        
        # Run simulation loop
        while simulation["running"]:
            # If simulation is paused, wait
            if simulation["paused"]:
                time.sleep(0.1)
                continue
                
            # Run simulation step
            data = sim_instance.step()
            
            # Update simulation data
            simulation["data"].update(data)
            
            # Send data to websocket
            asyncio.run_coroutine_threadsafe(
                websocket.send_json({
                    "type": "experiment_data",
                    "payload": data
                }),
                asyncio.get_event_loop()
            )
            
            # Check if simulation is finished
            if sim_instance.is_finished():
                # Send simulation complete message
                asyncio.run_coroutine_threadsafe(
                    websocket.send_json({
                        "type": "simulation_state",
                        "payload": {
                            "status": "completed",
                            "simulationId": simulation["id"],
                            "experimentId": simulation["experiment_id"],
                            "executionTime": time.time() - simulation["start_time"]
                        }
                    }),
                    asyncio.get_event_loop()
                )
                break
                
            # Wait for next step
            time.sleep(sim_instance.get_step_interval())
    except Exception as e:
        # Send error message
        asyncio.run_coroutine_threadsafe(
            websocket.send_json({
                "type": "error",
                "payload": {"message": f"Simulation error: {str(e)}"}
            }),
            asyncio.get_event_loop()
        )
    finally:
        # Make sure we mark the simulation as not running
        simulation["running"] = False

class GenericSimulation:
    """Generic simulation runner for experiments without a custom simulation class"""
    def __init__(self, exp_module, parameters):
        self.exp_module = exp_module
        self.parameters = parameters
        self.current_time = 0
        self.max_time = parameters.get("simulation_time", 300)  # Default 5 minutes
        self.step_interval = parameters.get("step_interval", 0.1)  # Default 100ms
        
    def step(self):
        """Run a single simulation step"""
        # Update simulation time
        self.current_time += self.step_interval
        
        # Run step function if it exists, otherwise generate some dummy data
        if hasattr(self.exp_module, "step"):
            return self.exp_module.step(self.parameters, self.current_time)
        else:
            # Generate dummy data if no step function exists
            return {
                "time": self.current_time,
                "value": simple_simulation_model(self.current_time, self.parameters)
            }
    
    def is_finished(self):
        """Check if simulation is finished"""
        return self.current_time >= self.max_time
        
    def get_step_interval(self):
        """Get time interval between steps"""
        return self.step_interval

def simple_simulation_model(time, parameters):
    """A simple simulation model for demonstration purposes"""
    # Example: First-order reaction A -> B
    k = parameters.get("rate_constant", 0.1)
    initial_conc = parameters.get("initial_concentration", 1.0)
    
    # Calculate concentration of A
    conc_a = initial_conc * (1 - (1 - math.exp(-k * time)))
    return conc_a

# Run the server if the script is executed directly
if __name__ == "__main__":
    import math  # Import here to avoid circular imports
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 