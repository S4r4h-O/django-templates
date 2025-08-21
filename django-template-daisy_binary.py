from pathlib import Path
import subprocess
import platform

print("You are creating a new Django Project")
project_name = str(input("Enter you project name: "))
print("Setting up environment and project...")

subprocess.run(["uv", "venv", "--seed", ".venv", "--python=3.10"], check=True)
subprocess.run(["uv", "pip", "install", "django", "django_components"], check=True)
subprocess.run("uv pip freeze > requirements.txt", shell=True, check=True)
subprocess.run(["git", "init"])
subprocess.run(
    [".venv/bin/django-admin", "startproject", project_name, "."], check=True
)

# Create directory structure
PATHS = [
    "static",
    "static/css", 
    "templates",
    "components",
]
PATHS = [Path(path) for path in PATHS]
print("Creating dirs...")
for path in PATHS:
    Path.mkdir(path)

print("Downloading Tailwind CSS and DaisyUI binaries...")

# Detect architecture for Linux
arch = platform.machine().lower()
if arch in ['x86_64', 'amd64']:
    tailwind_binary = "tailwindcss-linux-x64"
elif arch in ['aarch64', 'arm64']:
    tailwind_binary = "tailwindcss-linux-arm64"
else:
    print(f"Unsupported architecture: {arch}, defaulting to x64")
    tailwind_binary = "tailwindcss-linux-x64"

# Download binaries
subprocess.run([
    "curl", "-sLo", "static/css/tailwindcss", 
    f"https://github.com/tailwindlabs/tailwindcss/releases/latest/download/{tailwind_binary}"
], check=True)

subprocess.run([
    "curl", "-sLo", "static/css/daisyui.js",
    "https://github.com/saadeghi/daisyui/releases/latest/download/daisyui.js"
], check=True)

subprocess.run([
    "curl", "-sLo", "static/css/daisyui-theme.js", 
    "https://github.com/saadeghi/daisyui/releases/latest/download/daisyui-theme.js"
], check=True)

# Make Tailwind binary executable
subprocess.run(["chmod", "+x", "static/css/tailwindcss"], check=True)

INPUT_CSS = """@import "tailwindcss" source(none);
@plugin "./daisyui.js";
@source "../../templates";
"""

BASE_HTML = """{% load static %}
<!DOCTYPE html>
<html lang="en" data-theme="cupcake">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="X-UA-Compatible" content="ie=edge">
  <title>{% block title %}{% endblock %}</title>
  <link rel="stylesheet" href="{% static 'css/output.css' %}">
  {% block css %}{% endblock %}
</head>
<body>
  <div class="m-12">
    {% block content %}
    {% endblock %}
  </div>
</body>
</html>
"""

INDEX_HTML = """{% extends 'base.html' %}

{% block content %}
<div>
  <h1 class="text-4xl text-success mb-4">Contact Manager</h1>
  <button class="btn btn-primary">Hello daisyUI</button>
</div>
{% endblock %}
"""

GIT_IGNORE = """# Python-generated files
**pycache**/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
.env

# Static files
static/css/output.css

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Others
pyrightconfig.json
*.sqlite3
"""

CONFIG_FILES = {
    "static/css/input.css": INPUT_CSS,
    "templates/base.html": BASE_HTML,
    "templates/index.html": INDEX_HTML,
    ".gitignore": GIT_IGNORE,
}

print("Creating files...")
for file_path, content in CONFIG_FILES.items():
    file = Path(file_path)
    file.write_text(content)

# Build CSS
print("Building CSS...")
subprocess.run([
    "./static/css/tailwindcss", 
    "-i", "static/css/input.css", 
    "-o", "static/css/output.css"
], check=True)

print("""
Setup complete!

Add to your settings.py:
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
INSTALLED_APPS = [
    ...
    "django_components",
]

To rebuild CSS after changes:
./static/css/tailwindcss -i static/css/input.css -o static/css/output.css

To watch for changes:
./static/css/tailwindcss -i static/css/input.css -o static/css/output.css --watch
""")
