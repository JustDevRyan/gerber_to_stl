import json
import os

class SettingsManager:
    """Handles persistent storage of UI settings in core/user_settings.json."""
    def __init__(self, filename="user_settings.json", default_port=8000):
        # Get the directory where THIS script is located
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Logic to prevent core/core/
        if os.path.basename(current_dir) == "core":
            self.target_dir = current_dir
        else:
            self.target_dir = os.path.join(current_dir, "core")

        # Final path to the file
        self.filepath = os.path.join(self.target_dir, filename)
        
        # Ensure the folder exists before saving
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        self.defaults = {
            "port": str(default_port),
            "customize_port": False,
            "auto_open": False
        }

    def load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    return {**self.defaults, **json.load(f)}
            except:
                return self.defaults
        return self.defaults

    def save(self, data):
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving settings to {self.filepath}: {e}")