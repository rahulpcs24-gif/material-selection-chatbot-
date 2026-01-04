import json
import os

class MaterialDatabase:
    def __init__(self, data_path):
        self.data_path = data_path
        self.materials = self._load_data()

    def _load_data(self):
        """Loads materials from the JSON file."""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Database file not found at {self.data_path}")
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_all_materials(self):
        """Returns the list of all materials."""
        return self.materials

    def get_material_by_name(self, name):
        """Finds a material by its name."""
        for mat in self.materials:
            if mat['name'].lower() == name.lower():
                return mat
        return None
