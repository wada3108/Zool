import os
import subprocess


GLADIA_API_KEY = os.getenv("GLADIA_API_KEY")

pre_buf = ""
buf = ""

def transcriptor(tscript_q):
    gl_proc = subprocess.Popen(["python", "./utils/live-from-microphone.py", GLADIA_API_KEY], stdout=subprocess.PIPE, text=True)

    for line in gl_proc.stdout:
        tscript_q.add_buffer(line)
