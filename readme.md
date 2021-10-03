# 使用说明

小鹤音形按键记录&查询&分析工具。注意：虽然本工具不会将你的信息上传（因为根本没钱租服务器，笑死），但毕竟会保留按键记录。因此请勿在使用本工具的时候输入用户名、密码等，以免发生隐私泄漏！！！！！！

## 安装说明

### 从zip运行

> 只支持64位计算机

+ 解压
+ 运行key_recorder.exe
+ 给予网络权限
+ 网络权限要求是由于需要运行web服务器以提供网页服务。

### 从源码运行

+ 安装npm
+ 在client目录下，运行npm run build
+ 安装python3.8
+ 在根目录下，运行pip install -r requirements.txt
+ python key_recorder.py 运行

> windows 7 若启动不成功，需要安装[KB2533623补丁](https://support.microsoft.com/en-us/topic/microsoft-security-advisory-insecure-library-loading-could-allow-remote-code-execution-486ea436-2d47-27e5-6cb9-26ab7230c704)。官网似乎无法下载，需要自行百度从第三方网站下载。

## 使用说明

+ 码表放在words目录下，格式已给出，按照windows下的小鹤音形码表格式给出，里面可以放多个文件，都会作为码表的一部分
+ 按键记录在logs目录下，使用文本形式。
+ 程序运行后，在系统创建托盘，右键托盘可打开浏览器进行查看。
