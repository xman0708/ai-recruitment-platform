import requests
import time
import subprocess
import threading
import sys
import os

# Disable proxy for localhost
os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["ALL_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
os.environ["all_proxy"] = ""
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

# Start server
def start_server():
    subprocess.run(["./venv/bin/uvicorn", "main:app", "--port", "8000"])

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# Wait for server to start
time.sleep(2)

try:
    # 1. Test root
    res = requests.get("http://localhost:8000/")
    print("Root:", res.json())
    
    # 2. Test upload
    with open("dummy_resume.txt", "w") as f:
        f.write("张三的简历内容: Python, Vue3...")
    
    with open("dummy_resume.txt", "rb") as f:
        files = {"file": ("dummy_resume.txt", f, "text/plain")}
        res = requests.post("http://localhost:8000/api/v1/candidates/upload", files=files)
    
    data = res.json()
    print("Upload Response:", data)
    task_id = data["task_id"]
    
    # 3. Test status polling
    for i in range(5):
        status_res = requests.get(f"http://localhost:8000/api/v1/candidates/upload-status/{task_id}")
        status_data = status_res.json()
        print(f"Polling {i}, status:", status_data["status"])
        if status_data["status"] == "completed":
            print("Completed result:", status_data["result"])
            break
        time.sleep(1)
        
    print("Test passed.")
except Exception as e:
    print("Test failed:", e)
    sys.exit(1)
