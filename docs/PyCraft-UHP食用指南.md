## PyCraft-UHP食用指南

> PyCraft-UHP是对PyCraft的进一步封装
>
> 新增两个模块：
>
> ​	backend —— 用于维系玩家对象的数据
>
> ​	operation —— 玩家操作库
>
> 新增对象：
>
> ​	Player —— 一切操作的入口

### Quick Start

我们需要交互式运行程序。

如果你用的是 PyCharm，请在 Run/Debug Configurations 中勾选 Run with python console.

如果你用的是其他IDE，我也不知道要怎么做。总之你要在运行`start.py`后，程序不直接结束而是等待你的交互式输入。

---

`start.py`的主入口点如下：

```python
if __name__ == "__main__":
    connection = main()
    player = register_backend(connection)
```

通过已经建立的连接我们可以注册一个后端，它将返回一个`player` 对象。

我们可以通过`player`对象对玩家进行控制。

#### 玩家移动

方法原型：

```python
def player.moveTo(self, destination: list[3])
```

参数表：

| 参数        | 描述                     |
| ----------- | ------------------------ |
| destination | 包含目的地三维坐标的列表 |

样例：

```python
player.moveTo([10, 20, 30])  # 从当前位置移动向x=10,y=20,z=30
```

