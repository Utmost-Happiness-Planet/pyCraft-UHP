from nbt import nbt


class Block:
    """
    储存方块 id 及状态。
    """
    def __init__(self, blockTag):
        self.tag = blockTag

    def getName(self):
        """获取方块 id """
        return self.tag[0]

    def getState(self):
        """获取方块状态"""
        pass


class Schematic:
    """
    储存原理图信息，提供通过坐标获取方块的方法。
    """

    def __init__(self, schematic_path: str):
        self.schematic = nbt.NBTFile(schematic_path)
        size = self.schematic[3][0][4]
        self.sizeX = size[0].value
        self.sizeY = size[1].value
        self.sizeZ = size[2].value
        self.totalVolume = self.sizeX * self.sizeY * self.sizeZ
        self.sizeLayer = self.sizeX * self.sizeZ

        self.blockState = self.schematic[3][0][3]

        self.bitArray = self.schematic[3][0][0].value
        self.entryLength = len(bin(len(self.blockState))) - 2

        self.position = [0, 0, 0]

    def _getIndex(self, x: int, y: int, z: int) -> int:
        return (y * self.sizeLayer) + z * self.sizeX + x

    def _getIndexByAbsolutePosition(self, x, y, z):
        x -= self.position[0]
        y -= self.position[1]
        z -= self.position[2]
        return (y * self.sizeLayer) + z * self.sizeX + x

    def _getAt(self, index: int) -> int:
        i1 = (index * self.entryLength) // 64
        i2 = (index * self.entryLength) % 64
        bitArray = bin(self.bitArray[i1])[2:]
        # 前缀补0判断
        if len(bitArray) % self.entryLength:
            bitArray = bitArray.rjust(len(bitArray) + (self.entryLength - len(bitArray) % self.entryLength), '0')
        return int(bitArray[i2:i2 + self.entryLength], 2)

    def _getBlock(self, index: int):
        return self.blockState[index]

    def getBlock(self, x: int, y: int, z: int) -> Block:
        """以相对坐标（原理图原点）获取方块状态"""
        return Block(self._getBlock(self._getAt(self._getIndex(x, y, z))))

    def getBlockAbsolutely(self, x: int, y: int, z: int) -> Block:
        """以绝对坐标（地图原点）获取方块状态"""
        return Block(self._getBlock(self._getAt(self._getIndexByAbsolutePosition(x, y, z))))

    def setSchematicPosition(self, x: int, y: int, z: int) -> None:
        """设置原理图原点"""
        self.position = [x, y, z]
