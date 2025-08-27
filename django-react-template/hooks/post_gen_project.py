from pathlib import Path
import subprocess
import secrets
import string
import os


def generate_secret_key():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret_key = "".join(secrets.choice(alphabet) for _ in range(50))
    return secret_key


def main():
    ROOT_DIR = Path.cwd()
    BACKEND_DIR = ROOT_DIR / "backend"
    FRONTEND_DIR = ROOT_DIR / "frontend"

    print("Setting up python environment...\n")
    if not subprocess.run(["uv", "venv", ".venv", "--python=3.11"], cwd=BACKEND_DIR):
        print("Install uv first.")
    subprocess.run(["uv", "pip", "install", "-r", "requirements.txt"], cwd=BACKEND_DIR)

    print("Setting up Django Project...\n")
    make_migrations = subprocess.Popen(
        [str(BACKEND_DIR / ".venv/bin/python3"), "manage.py", "makemigrations"],
        cwd=BACKEND_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for line in make_migrations.stdout:
        print(line, end="")

    for line in make_migrations.stderr:
        print(line, end="")

    make_migrations.wait()

    migrate = subprocess.Popen(
        [str(BACKEND_DIR / ".venv/bin/python3"), "manage.py", "migrate"],
        cwd=BACKEND_DIR,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    for line in migrate.stdout:
        print(line, end="")

    for line in migrate.stderr:
        print(line, end="")

    migrate.wait()

    print("\nSetting up React environment...\n")
    if not subprocess.run(["npm", "install"], cwd=FRONTEND_DIR):
        print("Install npm first.")

    print("\nInitializing git repository...\n")
    if not subprocess.run(["git", "init", str(ROOT_DIR)], check=True):
        print("Install git first.")

    with open(str(BACKEND_DIR / ".env"), "a") as f:
        f.write(f"SECRET_KEY={generate_secret_key()}")

    with open(str(FRONTEND_DIR / ".env"), "a") as f:
        f.write("VITE_API_URL=http://localhost:8000/api")

    git_ignore = Path(ROOT_DIR / "gitignore")
    if git_ignore.exists():
        print(git_ignore)
        git_ignore.rename(ROOT_DIR / ".gitignore")
    else:
        print("gitignore does not exists.")


if __name__ == "__main__":
    main()
