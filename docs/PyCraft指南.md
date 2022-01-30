## PyCraft指南

> 🎀 A gift for UHP by Kl1nge5

官方文档说了等于没说，所以我不得不详细地写一遍，以便于团队开发。

*\*持续更新中…（取决于我的开发进度）\**



## 从 Packets Listening 开始

对于客户端来说，从服务器获取信息的方式当然是监听服务器发送来的数据包。

众所周知，`connection.connect()`后会启动一个连接线程，我们与服务器的通话都在该线程里进行。所以我们要注册一个数据包监听器，自然需要通过`connection`对象进行。

为了使代码更具有Python范，我们使用装饰器进行监听器注册操作。

以监听玩家坐标和视角的数据包为例：

```python
# 省略以上若干代码
connection.connect()

# 先凭借你的灵感从clientbound.play包中找到你要监听的数据包类，导入进来
# 注意数据包类是大驼峰命名法而不是下划线命名法
from minecraft.networking.packets.clientbound.play import PlayerPositionAndLookPacket

# 使用listener装饰器注册一个监听器，装饰器实参为所监听包的类，函数形参为接收到的包
@connection.listener(PlayerPositionAndLookPacket)
def printPacket(_packet):
    print(_packet)
    # Your code...
```

运行结果为每收到`PlayerPositionAndLookPacket`后会将数据包对象打印出来：

```python
0x38 PlayerPositionAndLookPacket(x=7.762499988079071, y=41.0, z=13.987740755279466, yaw=-58.84423828125, pitch=55.653663635253906, flags=0, teleport_id=1, dismount_vehicle=False)
```

提取其中数据后即可做相关运算。

> 无关紧要的小知识——关于listener装饰器的实现：
>
> ```python
> def listener(self, *packet_types, **kwds):
>         """
>         Shorthand decorator to register a function as a packet listener.
> 
>         Wraps :meth:`minecraft.networking.connection.register_packet_listener`
>         :param packet_types: Packet types to listen for.
>         :param kwds: Keyword arguments for `register_packet_listener`
>         """
>         def listener_decorator(handler_func):
>             self.register_packet_listener(handler_func, *packet_types, **kwds)
>             return handler_func
> 
>         return listener_decorator
> ```
>
> 其实相当简略，只不过在内部调用了register_packet_listener方法而已。
>
> 那不看一下这个方法的实现有点对不起它：
>
> ```python
> def register_packet_listener(self, method, *packet_types, **kwds):
>         """
>         注册一个包监听器，它会在指定的包被接收到时被提醒
> 
>         If :class:`minecraft.networking.connection.IgnorePacket` is raised from
>         within this method, no subsequent handlers will be called. 
>         如果'early=True', 它会抑制接受到该包后的默认行为，这可能会破坏连接的网络状态，所以请小心选择。
>         如果与此同时'outgoing=True',它会抑制该包的发送.
> 
>         :param method: 收到包后的回调函数
>         :param packet_types: 需要监听的包
>         :param outgoing: 如果为 'True', 监听器将监听发送至服务器的包，而不是从服务器接收的包
>         :param early: 如果为 'True', 监听器将被调用于任何内建方法之前, 及其在所有其他
>         			  'early=False'的监听器之前. 如果同时'outgoing=True', 监听器将在包被
>         			  发送前被调用，而不是发送后。
>         """
>         outgoing = kwds.pop('outgoing', False)
>         early = kwds.pop('early', False)
>         target = self.packet_listeners if not early and not outgoing \
>             else self.early_packet_listeners if early and not outgoing \
>             else self.outgoing_packet_listeners if not early \
>             else self.early_outgoing_packet_listeners
>         target.append(packets.PacketListener(method, *packet_types, **kwds))
>         # 根据不同的参数组合，在不同的监听器列表中添加PacketListener对象
> ```

你不仅能监听服务器服务器发来的包，也能监听你发给服务器的包。

当我们向服务器发包改变自身状态时，这个操作尤其有用，不然我们失去对当前玩家状态的感知了。

```python
from minecraft.networking.packets.serverbound.play import PlayerPositionAndLookPacket

# 使用listener装饰器注册一个监听器，装饰器实参为所监听包的类，函数形参为接收到的包
@connection.listener(PlayerPositionAndLookPacket, outgoing=True)
def printPacket(_packet):
    print(_packet)
    # Your code...
```



## 从 Packet Writing 开始

光接收数据包肯定不行啊，要和服务器交流我们还需要主动发送数据包。

同理，我们需要利用`connection`对象。

包的发送分为两步：

1. 构造要发送的数据包
2. 调用`connection.write_packet(Packet)`发送数据包

举个栗子：

```python
# 先凭借你的灵感从serverbound.play包中找到你要监听的数据包类，导入进来
from minecraft.networking.packets.serverbound.play import ChatPacket
# 实例化出一个数据包对象
p = ChatPacket()
# 设置对象的字段
p.message = "Fa♂Q"
# 发送数据包
c.write_packet(p)
```

你也许会好奇“我怎么知道要设置什么字段？”，这个我们可以点进数据包源码查看。

如`ChatPacket`源码中有：

```python
definition = [
    {'message': String}]
```

说明我们需要设置一个`message`字段。

再举个例子，`PositionAndLookPacket`中有：

```python
definition = [
    {'x': Double},
    {'feet_y': Double},
    {'z': Double},
    {'yaw': Float},
    {'pitch': Float},
    {'on_ground': Boolean}]
```

则我们需要设置`x`, `feet_y`, `z`, `yaw`, `pitch`, `on_ground`六个字段。

---

最后我们要知道，serverbound全是发送用包，clientbound全是监听用包，不要搞混了。



### 实现玩家移动

> 参考文档：https://wiki.vg/Protocol#Player_Position

首先我们需要知道 Minecraft 玩家移动的原理。

1. 客户端给服务端发送移动后的坐标
2. 服务端检测该坐标是否合理
3. 若坐标合理服务端将更新服务端上的玩家位置
4. 若不合理服务端不进行位置更新，并将当前服务端上玩家位置发回给客户端

> 所谓判断合理即判断是否移动过快，判断的实现如下：
>
> 1. 每一服务器刻，玩家当前的坐标被储存
> 2. 当玩家移动时，计算移动后坐标与移动前坐标之差，记为向量 (Δx, Δy, Δz)
> 3. 求该向量l2范数的平方，说人话就是求移动距离的平方，得 Δx² + Δy² + Δz²，记为①式
> 4. 利用之前的玩家位置变化信息计算玩家的速度
> 5. 利用玩家的速度估计其应该行走的距离，求该距离的平方即 velocityX² + velocityY² + velocityZ²，记为②式
> 6. 若①式减②式大于100（若玩家装备鞘翅则大于300），判断为移动过快

不想这么麻烦地考虑的话，只要遵守每个坐标更新包之间欧式距离不超过 100 格就行。

---

我们可以使用`PositionAndLookPacket`发送玩家的坐标信息，举个例子：

（以后所有代码中的`connection`默认指已经建立连接的`connection`对象）

```python
from minecraft.networking.packets.serverbound.play import PositionAndLookPacket
p = PositionAndLookPacket()
p.x = 7.0
p.feet_y = 41.0
p.z = 13.0
p.yaw = -58.0
p.pitch = 55.0
p.on_ground = True
connection.write_packet(p)
```

其中每个字段的含义如下：

| Field Name | Field Type |                    Notes                     |
| :--------: | :--------: | :------------------------------------------: |
|     x      |   Double   |                 绝对 X 坐标                  |
|   feet_y   |   Double   | 绝对 Y 坐标，以脚的位置为准，即头坐标 - 1.62 |
|     z      |   Double   |                 绝对 Z 坐标                  |
|    yaw     |   Float    |        X轴上的绝对旋转，以度为单位。         |
|   pitch    |   Float    |        Y轴上的绝对旋转，以度为单位。         |
| on_ground  |  Boolean   |      客户端在地面上时为True，反之False       |

如果你不知道 yaw 和 pitch 是什么，你可以这样理解：

- yaw 是你左右转头（z 轴正方向为0，负方向为180，x 轴正方向270，负方向90）
- pitch是你上下抬头低头（ 平视为0，抬头到顶为-90，低头到底为90）



## 自定义数据包

PyCraft并没有给太多的数据包类，这迫使我们想用一些功能时必须自己去写。

好在 [wiki](https://wiki.vg/Protocol) 上对协议做了充分的解析，我们可以参考其中的内容构建数据包。



