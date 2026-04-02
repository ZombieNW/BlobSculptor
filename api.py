import os
import builder_runner

class API:
    def __init__(self):
        self.env = os.getenv("APP_ENV", "production")
        base_dir = "build" if self.env == "production" else "static"
        self.assets_dir = os.path.join(os.path.dirname(__file__), base_dir, "assets")
        self.hair_dir = os.path.join(self.assets_dir, "Mii_Hairs")
    
    def set_window(self, window):
        self._window = window
        print("Window set")

    def get_models_list(self):
        """Returns a list of .obj filenames found in the assets directory."""
        try:
            if not os.path.exists(self.hair_dir):
                return []
            
            return [f for f in os.listdir(self.hair_dir) if f.endswith(".obj")]
        except Exception as e:
            print(f"Error reading models: {e}")
            return []
    
    def run_blender_task(self, template_path, obj_path, output_path, scale=(1.0, 1.0, 1.0), position=(0.0, 0.0, 0.0), base_color=(1.0, 1.0, 1.0)):
        if not self._window:
            return "Error: Window not initialized"
        
        return builder_runner.run_blender_task(self._window, template_path, obj_path, output_path, scale, position, base_color)

    def process_data(self, data):
        print(f"Python received: {data}")
        return f"Processed {len(data)} characters."