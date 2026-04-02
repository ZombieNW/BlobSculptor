import subprocess
import os
import platform
import shutil
import threading

def find_blender():
    """Locates the Blender executable."""
    # check path
    path_check = shutil.which("blender")
    if path_check:
        return path_check

    # check common install path
    system = platform.system()
    base = r"C:\Program Files\Blender Foundation"
    if os.path.exists(base):
        for folder in os.listdir(base):
            exe = os.path.join(base, folder, "blender.exe")
            if os.path.exists(exe): return exe
            
    # fallback to command name
    return "blender"

def run_blender_task(window, template_path, obj_path, output_path, scale=(1.0, 1.0, 1.0), position=(0.0, 0.0, 0.0), base_color=(1.0, 1.0, 1.0)):
    """
    Asks Blender to insert hair into rig template.
    """
    blender_exe = find_blender()
    worker_script = os.path.abspath("builder_processor.py")

    # build params with absolute paths
    script_params = [
        os.path.abspath(template_path),
        os.path.abspath(obj_path),
        os.path.abspath(output_path),
        *[str(s) for s in scale],
        *[str(p) for p in position],
        *[str(c) for c in base_color]
    ]

    # flags with script params
    command = [blender_exe, "-b", "-P", worker_script, "--"] + script_params

    def stream_process_output():
        # popen captures the output
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace' # fix unicode errors
        )

        for line in iter(process.stdout.readline, ''):
            if line:
                msg = line.strip().replace("'", "\\'")
                window.evaluate_js(f"window.onBlenderLog('{msg}')")
        
        process.stdout.close()
        process.wait()
        window.evaluate_js("window.onBlenderLog('Done!')")

    # Run in a background thread so the UI stays responsive
    threading.Thread(target=stream_process_output, daemon=True).start()
    
    return "Task Started"

if __name__ == "__main__":
    # debugging
    run_blender_task(
        template_path = "static/assets/Rig_V2/rig.blend",
        obj_path      = "static/assets/Mii_Hairs/Hair.001.obj",
        output_path   = "output.blend",
        scale         = (1.6, 1.6, 1.6),
        position      = (0.0, 0.0, 0.9),
        base_color    = (0.8, 0.2, 0.1)
    )