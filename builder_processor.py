import bpy
import sys
import os
import math

DEFAULT_ROTATION = (math.pi / 2, 0.0, math.pi / 2)
PARENT_NAME = "Head Hook"

def setup_material(obj, color_rgb):
    """Creates and assigns hair material"""
    mat_name = f"Mat_{obj.name}"
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    
    # Principled BSDF node
    bsdf = nodes.get("Principled BSDF")
    
    if bsdf:
        # Base Color (RGBA)
        bsdf.inputs["Base Color"].default_value = (*color_rgb, 1.0)
        
        # Roughness
        bsdf.inputs["Roughness"].default_value = 0.3
        
        # Subsurface Settings
        if "Subsurface Weight" in bsdf.inputs:
            # Modern Blender
            bsdf.inputs["Subsurface Weight"].default_value = 1.0
        else:
            # Older Blender
            bsdf.inputs["Subsurface"].default_value = 1.0
            
        bsdf.inputs["Subsurface Scale"].default_value = 1.5

    # Assign to object
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def process_obj_into_template(template_path, obj_path, output_path, scale, position, color_rgb):
    # open template
    if not os.path.exists(template_path) or os.path.getsize(template_path) == 0:
        print(f"FATAL: Template file is missing or empty at {template_path}")
        sys.exit(1)

    try:
        bpy.ops.wm.open_mainfile(filepath=template_path)
    except Exception as e:
        print(f"FATAL: Blender could not read the blend file: {e}")
        sys.exit(1)
    
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

            # apply material
            if obj.type == 'MESH':
                setup_material(obj, color_rgb)

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
        cl = (float(args[9]), float(args[10]), float(args[11]))
        
        process_obj_into_template(tmpl_file, obj_file, out_file, sc, ps, cl)
        
    except (IndexError, ValueError) as e:
        print(f"Argument Error: {e}")
        print("Expected: <tmpl> <obj> <out> <sx> <sy> <sz> <px> <py> <pz> <r g b>")