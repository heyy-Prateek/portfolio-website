"""
Android Application Bridge for Chemical Engineering Lab Simulator
This file serves as a bridge between the Streamlit app and the Android platform.
It uses the BeeWare/Toga framework to create a native Android interface,
while running the Streamlit app in an embedded web view.
"""

import os
import sys
import subprocess
import threading
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import time

class ChemicalEngSimulatorApp(toga.App):
    def startup(self):
        """
        Startup the main window and begin the application
        """
        # Main window
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        # Create a loading message
        self.loading_label = toga.Label(
            'Starting Chemical Engineering Lab Simulator...',
            style=Pack(text_align='center', padding=20)
        )
        
        # Create the main container with the loading message
        main_box = toga.Box(
            style=Pack(direction=COLUMN, flex=1)
        )
        main_box.add(self.loading_label)
        
        # Set the content of the main window
        self.main_window.content = main_box
        
        # Show the main window
        self.main_window.show()
        
        # Start the Streamlit server in a separate thread
        self.streamlit_thread = threading.Thread(target=self.start_streamlit_server)
        self.streamlit_thread.daemon = True
        self.streamlit_thread.start()
        
        # Schedule the creation of the WebView after a short delay
        self.add_background_task(self.create_webview)

    def start_streamlit_server(self):
        """
        Start the Streamlit server in the background
        """
        try:
            # Get the path to the app.py file
            app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py')
            
            # Start Streamlit server on a specific port
            subprocess.run([
                sys.executable, 
                "-m", "streamlit", 
                "run", 
                app_path,
                "--server.port", "8501",
                "--server.headless", "true",
                "--server.enableCORS", "false",
                "--browser.serverAddress", "localhost"
            ])
        except Exception as e:
            print(f"Error starting Streamlit server: {e}")

    async def create_webview(self, **kwargs):
        """
        Create the WebView to display the Streamlit app
        """
        # Wait for the server to start (adjust time as needed)
        await asyncio.sleep(5)
        
        # Create a WebView that points to the Streamlit server
        self.webview = toga.WebView(
            style=Pack(flex=1),
            on_webview_load=self.on_webview_loaded
        )
        self.webview.url = "http://localhost:8501"
        
        # Replace the loading screen with the WebView
        main_box = toga.Box(
            style=Pack(direction=COLUMN, flex=1)
        )
        main_box.add(self.webview)
        
        # Set the content of the main window
        self.main_window.content = main_box

    def on_webview_loaded(self, widget, **kwargs):
        """
        Called when the WebView has loaded
        """
        print("WebView loaded successfully")
        
        # Inject custom CSS to make the app more mobile-friendly
        css = """
        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
        }
        .stApp {
            max-width: 100% !important;
        }
        .block-container {
            padding: 1rem !important;
        }
        """
        
        # Inject the CSS into the WebView
        inject_script = f"var style = document.createElement('style'); style.innerHTML = `{css}`; document.head.appendChild(style);"
        self.webview.evaluate_javascript(inject_script)


def main():
    return ChemicalEngSimulatorApp('Chemical Engineering Lab Simulator', 'com.chemengsim')


if __name__ == '__main__':
    app = main()
    app.main_loop()