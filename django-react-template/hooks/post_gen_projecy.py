from pathlib import Path
import subprocess


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


if __name__ == "__main__":
    print(main.ROOT_DIR)
    main()
