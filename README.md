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

### TODO

目前该项目可连接至原版Minecraft服务器。

```python
39.99.130.154:25565  # 试验田
```

但连接UHP服务器时会报错。

需要修复。 **@SakuraPuare @mccube2000**
