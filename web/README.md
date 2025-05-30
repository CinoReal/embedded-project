# Web Interface

This project streams video from a Raspberry Pi camera (or a local webcam for development) to a web interface. It consists of a Python backend (Flask + Picamera2/OpenCV) and is intended to be used with a Vue.js frontend (setup for frontend not detailed here but anticipated).

## Project Structure

```
web/
├── backend/                  # Python Flask backend
│   ├── .venv/                # Virtual environment created by uv (ignored by git)
│   ├── src/
│   │   └── pi_camera_app/    # Python package source
│   │       ├── __init__.py
│   │       ├── camera.py     # Camera handling (OpenCV/Picamera2)
│   │       └── server.py     # Flask application
│   ├── pyproject.toml        # Project metadata and dependencies for uv
│   └── requirements.txt      # Basic list of Python dependencies
├── frontend/                 # Placeholder for Vue.js frontend
│   └── ...
├── scripts/
│   └── start-dev.sh          # Script to start the backend and frontend servers
└── README.md                 # This file
```

## I. System-Level Requirements

**1. `uv` - The Python Packager:**

- `uv` is used to manage Python dependencies and virtual environments.
- Installation instructions: [https://github.com/astral-sh/uv#installation](https://github.com/astral-sh/uv#installation)

**2. For Raspberry Pi Camera Support (Only on the Raspberry Pi):**

- **Install `libcamera` System Libraries & Python Bindings:**
  ```bash
  sudo apt update
  sudo apt install -y python3-libcamera libcamera-apps build-essential python3-dev libcap-dev
  ```
  - `python3-libcamera`: System-level Python bindings for libcamera.
  - `libcamera-apps`: Command-line tools (e.g., `libcamera-still`) for testing.
  - `build-essential python3-dev libcap-dev`: Needed if `picamera2` or its dependencies (like `python-prctl`) need to be compiled from source during `uv sync`.
- **Test `libcamera`:**
  ```bash
  libcamera-still -o test.jpg --timeout 1000
  ```
  If this saves a `test.jpg`, your system camera setup is likely working.

**3. For Local Webcam Development (e.g., on a Laptop):**

- No specific system packages are usually needed beyond what OpenCV requires, which are typically handled by the `opencv-python-headless` Python package. Ensure your webcam is functional.

**4. Node.js and npm (for Frontend - if you add one):**

- Node.js LTS version is required
- A version manager is recommended:
  - We recommend using [fnm](https://github.com/Schniz/fnm) for Node.js version management
- We use [pnpm](https://pnpm.io/) as the package manager
- Installation:
  1. Install fnm: Follow instructions at [https://github.com/Schniz/fnm#installation](https://github.com/Schniz/fnm#installation)
  2. Install Node.js LTS: `fnm install --lts`
  3. Install pnpm: `npm install -g pnpm`

## II. Backend Setup & Running

The backend is managed using `uv`.

**1. Clone the Repository (if you haven't):**

```bash
git clone https://github.com/mitsimi/embedded-project.git
cd embedded-project
```

**2. Navigate to the Backend Directory:**

```bash
cd backend
```

**3. Create/Ensure Virtual Environment with System Site-Packages (Important for Picamera2):**
The `start-dev.sh` script attempts to manage this. However, if setting up manually for the first time, especially on the Pi:

```bash
# If .venv exists and was NOT created with system-site-packages, remove it
# rm -rf .venv

# Create venv using uv, ensuring it can see system-installed libcamera bindings
uv venv --system-site-packages .venv
```

This step is crucial for `picamera2` to find the system `libcamera` bindings.

**4. Install Python Dependencies using `uv sync`:**
The `scripts/start-dev.sh` script handles this based on whether you're on a Pi or developing locally.

- **For Local Development (using OpenCV for webcam):**
  The script will run:

  ```bash
  # (from backend/ directory)
  # export USE_OPENCV=1 # Done by the script
  uv sync
  ```

- **For Raspberry Pi (using Picamera2):**
  The script will run:
  ```bash
  # (from backend/ directory)
  # export USE_OPENCV=0 # Done by the script
  uv sync --extra pi
  ```
  This installs the `picamera2` package and its dependencies. If `python-prctl` fails to build, ensure you've run `sudo apt install build-essential python3-dev libcap-dev`.

**5. Running the Backend Server:**

Use the provided script from the **project root directory** (`robo-vue/`):

```bash
chmod +x scripts/start-dev.sh
```

- **To run with local webcam (e.g., on your laptop):**

  ```bash
  ./scripts/start-dev.sh
  ```

  This sets `USE_OPENCV=1` and syncs core dependencies.

- **To run with Raspberry Pi camera (on the Pi):**
  ```bash
  ./scripts/start-dev.sh --pi
  ```
  This sets `USE_OPENCV=0` and syncs with the `pi` extra (installing `picamera2`).

The backend server will start (by default on `http://localhost:5000`).

- The MJPEG video stream will be available at `http://localhost:5000/video`.
- A simple HTML page with the embedded stream is at `http://localhost:5000/`.
- Logs from the backend server are saved to `backend/backend_server.log`.

**6. Stopping the Server:**
Press `Ctrl+C` in the terminal where `start-dev.sh` is running. The script has a cleanup trap to attempt to stop the backend server.

## III. Frontend Setup (Vue.js with pnpm)

1. Navigate to the Frontend Directory:

```bash
cd frontend
```

2. Install Dependencies using pnpm:

```bash
pnpm install
```

3. Start the Development Server:

```bash
pnpm run dev
```

## IV. Development Notes

- **`USE_OPENCV` Environment Variable:** The `backend/src/pi_camera_app/camera.py` module uses the `USE_OPENCV` environment variable (set by `start-dev.sh`) to switch between using `cv2.VideoCapture` (if `USE_OPENCV=1`) and `picamera2` (if `USE_OPENCV=0` or not set).
- **Virtual Environment:** `uv` creates and manages a virtual environment typically in `backend/.venv/`. You generally don't need to activate it manually if you use `uv run` or the `start-dev.sh` script.
- **Debugging `libcamera` on Pi:** If `picamera2` fails with `libcamera` errors:
  - Ensure `sudo apt install python3-libcamera libcamera-apps` was successful.
  - Test with `libcamera-still -o test.jpg`.
  - Ensure the `.venv` was created with `--system-site-packages` so `uv`'s environment can see the system `libcamera` Python bindings.
