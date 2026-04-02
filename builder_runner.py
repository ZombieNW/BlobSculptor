import subprocess
import os
import platform
import shutil

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

def run_blender_task(template_path, obj_path, output_path, scale=(1.0, 1.0, 1.0), position=(0.0, 0.0, 0.0)):
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
        *[str(p) for p in position]
    ]

    # flags with script params
    command = [blender_exe, "-b", "-P", worker_script, "--"] + script_params

    print(f"Starting Blender to process hair: {os.path.basename(obj_path)}...")
    
    try:
        # Run the process and capture output
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True, 
            encoding='utf-8', 
            errors='backslashreplace'
        )
        print("Done.")
    except subprocess.CalledProcessError as e:
        print("Blender Error:")
        print(e.stdout)
        print(e.stderr)

if __name__ == "__main__":
    # debugging
    run_blender_task(
        template_path = "static/assets/Rig_V2/rig.blend",
        obj_path      = "static/assets/Mii_Hairs/Hair.001.obj",
        output_path   = "output.blend",
        scale         = (1.6, 1.6, 1.6),
        position      = (0.0, 0.0, 0.9)
    )