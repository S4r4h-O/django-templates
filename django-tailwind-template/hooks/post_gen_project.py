#!/usr/bin/env python3

import os
import subprocess
import sys
import platform
import requests


def run_command(command, cwd=None, background=False):
    try:
        if background:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
            )
            return process
        else:
            result = subprocess.run(
                command, shell=True, cwd=cwd, capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error executing: {command}")
                print(f"Stderr: {result.stderr}")
                return False
            return True
    except Exception as e:
        print(f"Exception executing {command}: {e}")
        return False


def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False


def get_tailwind_executable_url():
    system = platform.system().lower()
    arch = platform.machine().lower()

    base_url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download"

    if system == "linux":
        if "arm" in arch or "aarch" in arch:
            return f"{base_url}/tailwindcss-linux-arm64"
        else:
            return f"{base_url}/tailwindcss-linux-x64"
    elif system == "darwin":
        if "arm" in arch:
            return f"{base_url}/tailwindcss-macos-arm64"
        else:
            return f"{base_url}/tailwindcss-macos-x64"
    elif system == "windows":
        return f"{base_url}/tailwindcss-windows-x64.exe"
    else:
        print(f"Unsupported operating system: {system}")
        return None


def main():
    project_dir = os.getcwd()
    static_css_dir = os.path.join(project_dir, "static", "css")

    if "{{ cookiecutter.init_git }}".lower() == "true":
        print("Initializing Git repository...")
        if run_command("git init", cwd=project_dir):
            run_command("git add .", cwd=project_dir)
            run_command('git commit -m "Initial commit"', cwd=project_dir)
            print("Git repository initialized")

    print("Downloading Tailwind CSS executable...")
    tailwind_url = get_tailwind_executable_url()
    if not tailwind_url:
        print("Failed to determine Tailwind executable for this system")
        return

    executable_name = (
        "tailwindcss.exe" if platform.system().lower() == "windows" else "tailwindcss"
    )
    tailwind_path = os.path.join(static_css_dir, executable_name)

    if download_file(tailwind_url, tailwind_path):
        if platform.system().lower() != "windows":
            run_command(f"chmod +x {tailwind_path}")
        print("Tailwind CSS executable downloaded")
    else:
        print("Failed to download Tailwind CSS executable")
        return

    print("Downloading daisyui.js...")
    daisyui_js_url = (
        "https://github.com/saadeghi/daisyui/releases/latest/download/daisyui.js"
    )
    daisyui_js_path = os.path.join(static_css_dir, "daisyui.js")
    if not download_file(daisyui_js_url, daisyui_js_path):
        print("Failed to download daisyui.js")

    print("Downloading daisyui-theme.js...")
    daisyui_theme_url = (
        "https://github.com/saadeghi/daisyui/releases/latest/download/daisyui-theme.js"
    )
    daisyui_theme_path = os.path.join(static_css_dir, "daisyui-theme.js")
    if not download_file(daisyui_theme_url, daisyui_theme_path):
        print("Failed to download daisyui-theme.js")

    tailwind_process = None
    if "{{ cookiecutter.start_tailwind_watch }}".lower() == "true":
        print("Starting Tailwind watch process...")
        watch_cmd = f'"{tailwind_path}" -i static/css/input.css -o static/css/output.css --watch'
        tailwind_process = run_command(watch_cmd, cwd=project_dir, background=True)
        if tailwind_process:
            print("Tailwind watch process started in background")
        else:
            print("Failed to start Tailwind watch process")

    if tailwind_process:
        with open(".background_processes", "w") as f:
            f.write(f"Tailwind PID: {tailwind_process.pid}\n")

    print("Post-generation setup completed")
    print("Next steps:")
    print(
        """Run
    cd {{ cookiecutter.project_slug }}
    ./static/css/tailwindcss -i static/css/input.css -o static/css/output.css or
    ./static/css/tailwindcss -i static/css/input.css -o static/css/output.css --watch

    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    """
    )


if __name__ == "__main__":
    main()
