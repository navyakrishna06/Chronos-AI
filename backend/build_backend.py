import os
import sys
import shutil
import subprocess

def main():
    base_dir = r"C:\Users\navya\OneDrive\Documents\Chronos"
    backend_app = os.path.join(base_dir, "backend", "app.py")
    model_file = os.path.join(base_dir, "models", "chronos_random_forest.pkl")
    dist_dir = os.path.join(base_dir, "dist-backend")
    work_dir = os.path.join(base_dir, "build-backend-temp")

    print("====================================================")
    print("CHRONOS AI: COMPILING FASTAPI BACKEND VIA PYINSTALLER")
    print("====================================================")
    print("Backend script:", backend_app)
    print("Model file:    ", model_file)
    print("Output dist:   ", dist_dir)

    # Clean old dist
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir, ignore_errors=True)
    if os.path.exists(work_dir):
        shutil.rmtree(work_dir, ignore_errors=True)

    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--noconfirm",
        "--onedir",
        "--name", "chronos-backend",
        "--add-data", f"{model_file};models",
        "--distpath", dist_dir,
        "--workpath", work_dir,
        "--specpath", work_dir,
        "--hidden-import", "uvicorn",
        "--hidden-import", "uvicorn.logging",
        "--hidden-import", "uvicorn.loops",
        "--hidden-import", "uvicorn.loops.auto",
        "--hidden-import", "uvicorn.protocols",
        "--hidden-import", "uvicorn.protocols.http",
        "--hidden-import", "uvicorn.protocols.http.auto",
        "--hidden-import", "uvicorn.protocols.websockets",
        "--hidden-import", "uvicorn.protocols.websockets.auto",
        "--hidden-import", "uvicorn.lifespan",
        "--hidden-import", "uvicorn.lifespan.on",
        "--hidden-import", "fastapi",
        "--hidden-import", "pydantic",
        "--hidden-import", "pandas",
        "--hidden-import", "joblib",
        "--hidden-import", "sklearn",
        "--hidden-import", "sklearn.ensemble",
        "--hidden-import", "sklearn.ensemble._forest",
        "--hidden-import", "pymongo",
        "--hidden-import", "sqlite3",
        backend_app
    ]

    print("Running command:", " ".join(cmd))
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("ERROR: PyInstaller build failed!")
        sys.exit(result.returncode)

    # Also make sure the model is explicitly copied into models/ in the output bundle
    target_models_dir = os.path.join(dist_dir, "chronos-backend", "models")
    os.makedirs(target_models_dir, exist_ok=True)
    shutil.copy2(model_file, os.path.join(target_models_dir, "chronos_random_forest.pkl"))

    print("====================================================")
    print("BACKEND COMPILED SUCCESSFULLY!")
    print("Binary location:", os.path.join(dist_dir, "chronos-backend", "chronos-backend.exe"))
    print("====================================================")

if __name__ == "__main__":
    main()
