import os

class API:
    def __init__(self):
        self.env = os.getenv("APP_ENV", "production")
        base_dir = "build" if self.env == "production" else "static"
        self.assets_dir = os.path.join(os.path.dirname(__file__), base_dir, "assets")
        self.hair_dir = os.path.join(self.assets_dir, "Mii_Hairs")

    def get_models_list(self):
        """Returns a list of .obj filenames found in the assets directory."""
        try:
            if not os.path.exists(self.hair_dir):
                return []
            
            return [f for f in os.listdir(self.hair_dir) if f.endswith(".obj")]
        except Exception as e:
            print(f"Error reading models: {e}")
            return []

    def process_data(self, data):
        print(f"Python received: {data}")
        return f"Processed {len(data)} characters."