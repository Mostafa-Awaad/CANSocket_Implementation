#!/bin/sh
#!/source/myenv/bin/cantools
import can
import sys
import subprocess
def install(cantools):
    subprocess.check_call([sys.executable, "-m", "pip", "install", cantools])
import cantools
