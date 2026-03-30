import os

class API:
    def __init__(self):
        self.cancel_heavy_stuff = False

    def get_system_info(self):
        return {
            "os": os.name,
            "status": "Online",
            "message": "Hello from the Python backend!"
        }

    def process_data(self, data):
        print(f"Python received: {data}")
        return f"Processed {len(data)} characters."