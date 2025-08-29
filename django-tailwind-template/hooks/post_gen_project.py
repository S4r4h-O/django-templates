#!/usr/bin/env python3

import os
import subprocess
import secrets
import platform
import requests
from pathlib import Path


def generate_secret_key():
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789!@#%^&*(-_=+)"
    return "".join(secrets.choice(alphabet) for _ in range(50))


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
            total_size = int(response.headers.get("content-length", 0))
            print(f"{total_size/(1024*1024):.2f} MB")
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                if total_size:
                    downloaded += len(chunk)
                    print(f"Progress: {int(downloaded/total_size * 100)}%", end="\r")

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
    static_js_dir = os.path.join(project_dir, "static", "js")
    secret = generate_secret_key()
    env_path = Path(f"{project_dir}/.env")

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

    print("Downloading htmx.min.js...")
    htmx_js_url = "https://unpkg.com/htmx.org@latest/dist/htmx.min.js"
    htmx_js_path = os.path.join(static_js_dir, "htmx.min.js")
    if not download_file(htmx_js_url, htmx_js_path):
        print("Failed to download htmx.min.js")

    with env_path.open("a", encoding="utf-8") as f:
        f.write(f"SECRET_KEY={secret}\n")

    print("Setting up python environment...")
    subprocess.run(["uv", "venv", ".venv", "--python=3.11"])
    subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=project_dir)

    print("Initializing git repository...")
    subprocess.run(["git", "init", project_dir], cwd=project_dir)

    print(
        "Running ./static/css/tailwindcss -i static/css/input.css -o static/css/output.css..."
    )
    subprocess.run(
        [
            "./static/css/tailwindcss",
            "-i",
            "./static/css/input.css",
            "-o",
            "./static/css/output.css",
        ],
        cwd=project_dir,
    )

    print(
        """ Post generation setup complete. Next steps:
    Run
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
