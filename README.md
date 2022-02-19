<div align='center'>
    
  # pyCraft-UHP
  
  ✨ A awesome headless Minecraft Client adapted to UHP server. ✨
</div>

### 环境准备

Clone 本仓库到本地。

安装`requirements.txt`中所需的环境

### 微软登录方法

打开终端，进入项目目录。

运行

```bash
python ./start.py -m * --save
```

将输出的网址在浏览器中打开，登录 Microsoft 账号。

登录成功后，网页将重定向至空白页面。复制网址中的`code`参数。（注意不要包含后面的`lc`参数）

将获得的`code`输入终端。

输入连接的服务器，格式为`IP[:PORT]`，端口不填即为25565。

输出`Connected`即为连接成功。

### 第二次快速登录

刚才运行脚本时，已经通过`--save`参数将登录信息保存在了`LOGIN_INFO`文件中。

运行

```bash
python ./start.py -f
```

即可自动读取`LOGIN_INFO`文件实现快速登录。


## TODO

- [x] 支持玩家移动操作
- [ ] 支持玩家放置方块操作 - Attempting
- [ ] 监听世界方块信息
- [x] 解析原理图文件的模块
- [ ] 完善原理图模块 - Attempting
- [ ] 编写自动建造算法
