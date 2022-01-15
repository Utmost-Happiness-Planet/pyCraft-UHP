# 微软登录方法

1. clone仓库至本地

2. 安装所需环境

3. 命令行输入指令
    ```basg
    python .\start.py -h
    ```
    获取帮助信息。
  
4. 使用帮助中`-m`条目提供的网址登录微软账号

5. 复制重定向后url的code参数。（注意不要包含lc参数）

6. 命令行输入指令
    ```bash
    python .\setup.py -m <code>
    ```
  
7. 即可启动
