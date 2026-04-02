import bpy
import sys
import os
import math

DEFAULT_ROTATION = (math.pi / 2, 0.0, math.pi / 2)
PARENT_NAME = "Head Hook"

def process_obj_into_template(template_path, obj_path, output_path, scale=(1.0, 1.0, 1.0), position=(0.0, 0.0, 0.0)):
    # open template
    if os.path.exists(template_path):
        bpy.ops.wm.open_mainfile(filepath=template_path)
    else:
        print(f"Error: Template file not found at {template_path}")
        return
    
    parent_hook = bpy.data.objects.get(PARENT_NAME)
    if not parent_hook:
        print(f"Error: '{PARENT_NAME}' not found in template.")

    # import obj
    try:
        # modern blender
        bpy.ops.wm.obj_import(filepath=obj_path)
    except AttributeError:
        # old blender
        bpy.ops.import_scene.obj(filepath=obj_path)

    # grab imported obj
    imported_objs = bpy.context.selected_objects
    
    if not imported_objs:
        print(f"Error: No objects were imported from {obj_path}")
    else:
        # position and scale
        for obj in imported_objs:
            # parent
            if parent_hook:
                obj.parent = parent_hook
                obj.matrix_parent_inverse = parent_hook.matrix_world.inverted()
            
            # transform
            obj.location = position
            obj.scale = scale
            obj.rotation_euler = DEFAULT_ROTATION

    # save a copy
    bpy.ops.wm.save_as_mainfile(filepath=output_path)
    print(f"Project saved successfully to: {output_path}")

# cli crap
if __name__ == "__main__":
    try:
        # Get everything after '--'
        args = sys.argv[sys.argv.index("--") + 1:]
        
        # Parse standard paths
        tmpl_file = args[0]
        obj_file  = args[1]
        out_file  = args[2]
        
        # parse scale and pos as floats
        sc = (float(args[3]), float(args[4]), float(args[5]))
        ps = (float(args[6]), float(args[7]), float(args[8]))
        
        process_obj_into_template(tmpl_file, obj_file, out_file, sc, ps)
        
    except (IndexError, ValueError) as e:
        print(f"Argument Error: {e}")
        print("Expected: <tmpl> <obj> <out> <sx> <sy> <sz> <px> <py> <pz>")