from nbt import nbt


class Schematic:
    def __init__(self, schematic_path: str):
        self.schematic = nbt.NBTFile(schematic_path)
        print(self.schematic)
