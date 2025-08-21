from pathlib import Path
import subprocess

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

PATHS = [
    "static",
    "static/src",
    "static/dist",
    "static/dist/css",
    "templates",
    "components",
]

PATHS = [Path(path) for path in PATHS]

print("Creating dirs...")
for path in PATHS:
    Path.mkdir(path)

PACKAGE_JSON = """
{
  "name": "django-tailwind-template",
  "version": "1.0.0",
  "description": "Template Django com Tailwind CSS, DaisyUI e suporte a Alpine.js",
  "scripts": {
    "clean": "rm -rf ./static/dist/css/*",
    "dev": "npx tailwindcss -i ./static/src/styles.css -o ./static/dist/css/main.css --watch",
    "build": "npx tailwindcss -i ./static/src/styles.css -o ./static/dist/css/main.css --minify",
    "rebuild": "npm run clean && npm run build"
  },
  "dependencies": {
    "alpinejs": "^3.12.0"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.14",
    "postcss": "^8.4.24",
    "tailwindcss": "^3.3.0",
    "daisyui": "^4.12.22"
  }
}
"""

TAILWIND_CONFIG = """
const path = require("path");
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./*/templates/**/*.html", 
    "./apps/*/templates/**/*.html",
    "./static/src/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark", "cupcake"],
  },
};
"""

POSTCSS_CONFIG = """
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  }
}
"""

STYLES_CSS = """
@tailwind base;
@tailwind components;
@tailwind utilities;
"""

GIT_IGNORE = """
# Python-generated files
__pycache__/
*.py[oc]
build/
dist/
wheels/
*.egg-info

# Virtual environments
.venv
.env

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules/
dist
dist-ssr
*.local
static/dist/

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

HTML_TEMPLATES = """
{% load static %}
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{% block title %}{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'dist/css/main.css' %}">
    {% block css %}{% endblock %}
  </head>
  <body>
    {% block content %}
    {% endblock %}
  </body>
</html>
"""

BLANK_FILES = [
    "templates/index.html",
    "static/dist/css/main.css",
]


CONFIG_FILES = {
    "package.json": PACKAGE_JSON,
    "tailwind.config.js": TAILWIND_CONFIG,
    "postcss.config.js": POSTCSS_CONFIG,
    ".gitignore": GIT_IGNORE,
    "static/src/styles.css": STYLES_CSS,
    "templates/base.html": HTML_TEMPLATES,
}


FILES = [
    {"path": Path(path), "content": CONFIG_FILES.get(path, "")}
    for path in list(CONFIG_FILES.keys()) + BLANK_FILES
]


print("Creating files...")
for file in FILES:
    f = file["path"]
    f.touch()
    f.write_text(file["content"])

print("Installing npm packages...")
subprocess.run(["npm", "install"])
subprocess.run(["npm", "run", "build"])

print(
    """
Add to your settings.py:

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]

INSTALLED_APPS = [
...
"django_components",
]
"""
)
