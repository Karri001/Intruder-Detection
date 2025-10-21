from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import threading
import os
import uvicorn
import psutil  # for process handling
from train_model import capture_faces, store_multiple_encodings, delete_person

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

detection_thread = None

@app.post("/train/")
def train_person(name: str = Form(...)):
    capture_faces(name, num_images=50)  # Runs in main thread
    store_multiple_encodings()          # Runs in main thread — avoids SQLite threading bug
    return {"message": f"Trained {name}"}

@app.post("/delete/")
def remove_person(name: str = Form(...)):
    delete_person(name)
    return {"message": f"Deleted {name}"}

@app.post("/start_detection/")
def start_detection():
    global detection_thread
    if detection_thread and detection_thread.is_alive():
        return {"message": "Detection already running."}
    
    def run_detection():
        os.system("python detect_intruder.py")

    detection_thread = threading.Thread(target=run_detection)
    detection_thread.start()
    return {"message": "Started intruder detection."}

@app.post("/stop_detection/")
def stop_detection():
    current_pid = os.getpid()
    killed = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                if proc.pid != current_pid:
                    # Check if this python process is running detect_intruder.py
                    cmdline = proc.info['cmdline']
                    if cmdline and any("detect_intruder.py" in part for part in cmdline):
                        proc.terminate()  # gently terminate
                        proc.wait(timeout=5)
                        killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    if killed > 0:
        return {"message": f"Stopped detection. Killed {killed} detection process(es)."}
    else:
        return {"message": "No detection process running."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
