from nbt import nbt


class Schematic:
    def __init__(self, schematic_path: str):
        self.schematic = nbt.NBTFile(schematic_path)
        self.size = self.schematic[3][0][4]
        self.sizeX = self.size[0].value
        self.sizeY = self.size[1].value
        self.sizeZ = self.size[2].value
        self.totalVolume = self.sizeX * self.sizeY * self.sizeZ
        self.sizeLayer = self.sizeX * self.sizeZ

        self.bitArray = ""

    def getIndex(self, x: int, y: int, z: int):
        return (y * self.sizeLayer) + z * self.sizeX + x
