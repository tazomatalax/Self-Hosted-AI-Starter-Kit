#!/usr/bin/env python3
"""
start_services.py

This script starts the Supabase stack first, waits for it to initialize, and then starts
the local AI stack. Both stacks use the same Docker Compose project name ("ai-stack")
so they appear together in Docker Desktop.
"""

import os
import subprocess
import shutil
import time
import argparse
import requests
from requests.exceptions import ConnectionError

def run_command(cmd, cwd=None):
    """Run a shell command and print it."""
    print("Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def clone_supabase_repo():
    """Clone the Supabase repository using sparse checkout if not already present."""
    if not os.path.exists("supabase"):
        print("Cloning the Supabase repository...")
        run_command([
            "git", "clone", "--filter=blob:none", "--no-checkout",
            "https://github.com/supabase/supabase.git"
        ])
        os.chdir("supabase")
        run_command(["git", "sparse-checkout", "init", "--cone"])
        run_command(["git", "sparse-checkout", "set", "docker"])
        run_command(["git", "checkout", "master"])
        os.chdir("..")
    else:
        print("Supabase repository already exists, updating...")
        os.chdir("supabase")
        run_command(["git", "pull"])
        os.chdir("..")

def prepare_supabase_env():
    """Copy .env to .env in supabase/docker."""
    env_path = os.path.join("supabase", "docker", ".env")
    env_example_path = os.path.join(".env")
    
    if not os.path.exists(env_example_path):
        print("Warning: .env file not found in project root. Supabase may not work correctly.")
        return False
        
    print("Copying .env in root to .env in supabase/docker...")
    shutil.copyfile(env_example_path, env_path)
    return True

def stop_existing_containers():
    """Stop and remove existing containers for our unified project ('ai-stack')."""
    print("Stopping and removing existing containers for the project 'ai-stack'...")
    run_command([
        "docker", "compose",
        "-p", "ai-stack",
        "-f", "docker-compose.yml",
        "-f", "supabase/docker/docker-compose.yml",
        "down"
    ])

def start_supabase():
    """Start the Supabase services (using its compose file)."""
    print("Starting Supabase services...")
    return run_command([
        "docker", "compose", "-p", "ai-stack", "-f", "supabase/docker/docker-compose.yml", "up", "-d"
    ])

def start_local_ai(profile=None):
    """Start the local AI services (using its compose file)."""
    print("Starting AI stack services...")
    cmd = ["docker", "compose", "-p", "ai-stack"]
    if profile and profile != "none":
        cmd.extend(["--profile", profile])
    cmd.extend(["-f", "docker-compose.yml", "up", "-d"])
    return run_command(cmd)

def wait_for_supabase_ready(max_retries=30, delay=10):
    """Wait for Supabase to be ready by checking the health endpoint."""
    print(f"Waiting for Supabase to initialize (max {max_retries*delay} seconds)...")
    
    # Check if Postgres is ready by trying to connect to it
    for i in range(max_retries):
        try:
            # Use docker inspect to check if the database container is healthy
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", "ai-stack-db-1"],
                capture_output=True,
                text=True
            )
            
            status = result.stdout.strip()
            if status == "healthy":
                print("Supabase database is ready!")
                return True
            
            print(f"Waiting for Supabase database to be ready... (attempt {i+1}/{max_retries})")
            time.sleep(delay)
            
        except Exception as e:
            print(f"Error checking Supabase status: {e}")
            time.sleep(delay)
    
    print("Timed out waiting for Supabase to be ready.")
    return False

def main():
    parser = argparse.ArgumentParser(description='Start the AI Stack and Supabase services.')
    parser.add_argument('--profile', choices=['cpu', 'gpu-nvidia', 'gpu-amd', 'none'], default='cpu',
                      help='Profile to use for Docker Compose (default: cpu)')
    parser.add_argument('--skip-supabase', action='store_true',
                      help='Skip starting Supabase services')
    parser.add_argument('--wait-time', type=int, default=30,
                      help='Maximum wait time for Supabase initialization in seconds (default: 30)')
    args = parser.parse_args()

    if not args.skip_supabase:
        clone_supabase_repo()
        if not prepare_supabase_env():
            print("Warning: Environment setup issue detected.")
        stop_existing_containers()
        
        # Start Supabase first
        if not start_supabase():
            print("Failed to start Supabase services. Exiting.")
            return
        
        # Wait for Supabase to be ready
        if not wait_for_supabase_ready(max_retries=args.wait_time//10, delay=10):
            print("Warning: Supabase may not be fully initialized. Continuing anyway...")
    else:
        print("Skipping Supabase startup as requested.")
    
    # Then start the local AI services
    if not start_local_ai(args.profile):
        print("Failed to start AI stack services.")
        return
    
    print("\nAI stack startup complete!")
    print("You can access the following services:")
    print("- Open WebUI: http://localhost:3000")
    print("- N8N: http://localhost:5678")
    print("- Flowise: http://localhost:3001")
    print("- Qdrant: http://localhost:6333")
    print("- Homepage: http://localhost:3333")
    print("- Portainer: http://localhost:9000")

if __name__ == "__main__":
    main()