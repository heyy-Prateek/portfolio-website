#!/usr/bin/env python
"""
Chemical Engineering Laboratory Simulator
Entry point script for running the application or building components.
"""

import os
import sys
import argparse
import subprocess

def run_application(api_only=False, streamlit_only=False):
    """Run the full application"""
    from chemengsim.__main__ import main
    
    # Set command-line arguments
    args = []
    if api_only:
        args.append("--api-only")
    elif streamlit_only:
        args.append("--streamlit-only")
    
    # Save original argv
    original_argv = sys.argv.copy()
    
    try:
        # Set new argv
        sys.argv = [sys.argv[0]] + args
        
        # Run the main function
        main()
    finally:
        # Restore original argv
        sys.argv = original_argv

def build_react():
    """Build the React frontend"""
    from chemengsim.build_react import main as build_main
    build_main()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Chemical Engineering Laboratory Simulator")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the application")
    run_parser.add_argument("--api-only", action="store_true",
                            help="Run only the API server without the Streamlit interface")
    run_parser.add_argument("--streamlit-only", action="store_true",
                            help="Run only the Streamlit interface without the API server")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build application components")
    build_parser.add_argument("--react", action="store_true",
                             help="Build the React frontend")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "run":
        run_application(args.api_only, args.streamlit_only)
    elif args.command == "build":
        if args.react:
            build_react()
        else:
            # If no specific build option is specified, build everything
            build_react()
    else:
        # Default action if no command is provided
        parser.print_help()

if __name__ == "__main__":
    main() 