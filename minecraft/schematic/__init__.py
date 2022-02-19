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

        self.blockState = self.schematic[3][0][3]

        self.bitArray = self.schematic[3][0][0].value
        self.entryLength = len(bin(len(self.blockState))) - 2

    def _getIndex(self, x: int, y: int, z: int) -> int:
        return (y * self.sizeLayer) + z * self.sizeX + x

    def _getAt(self, index: int) -> int:
        i1 = (index * self.entryLength) // 64
        i2 = (index * self.entryLength) % 64
        bitArray = bin(self.bitArray[i1])[2:]
        if len(bitArray) % self.entryLength:
            bitArray = bitArray.rjust(len(bitArray) + (self.entryLength - len(bitArray) % self.entryLength), '0')
        return int(bitArray[i2:i2+self.entryLength], 2)

    def _getBlock(self, index: int):
        return self.blockState[index]

    def getBlock(self, x: int, y: int, z: int):
        return Block(self._getBlock(self._getAt(self._getIndex(x, y, z))))


class Block:
    def __init__(self, blockTag):
        self.tag = blockTag

    def getName(self):
        return self.tag[0]

    def getState(self):
        pass
