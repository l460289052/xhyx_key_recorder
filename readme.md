# 使用说明

小鹤音形按键记录&查询&分析工具。原理：记录按键，在查询时，根据按键在words文件夹下的码表查询对应的词，并在码表中查询更短的编码以提供建议。

注意：虽然本工具不会将你的信息上传（因为根本没钱租服务器，笑死），但毕竟会保留按键记录。因此请勿在使用本工具的时候输入用户名、密码等，以免发生隐私泄漏！！！！！！

## 安装说明

### 从zip运行

> 只支持64位计算机

+ 解压

+ 运行key_recorder.exe

  > windows 7 若启动不成功，需要安装[KB2533623补丁](https://support.microsoft.com/en-us/topic/microsoft-security-advisory-insecure-library-loading-could-allow-remote-code-execution-486ea436-2d47-27e5-6cb9-26ab7230c704)。官网似乎无法下载，需要自行百度从第三方网站下载。

+ 给予网络权限

  > 网络权限要求是由于需要运行web服务器以提供网页服务。

### 从源码运行

+ 安装npm
+ 在client目录下，运行npm run build
+ 安装python3.8
+ 在根目录下，运行pip install -r requirements.txt
+ python key_recorder.py 运行

## 功能说明

+ 程序运行后，在系统创建托盘，右键托盘可打开浏览器进行查看。
+ 在浏览器中可以
  + 查询汉字或编码
  + 查看击键记录
  + 查看输入记录及建议

## 码表说明

+ 为了保证良好的使用体验，请导出码表并放在words目录下，格式请参照已有的文件来（按照windows下的小鹤音形码表的格式），里面可以放多个文件，都会作为码表的一部分。
+ 按键记录在logs目录下，使用文本形式。

# 反馈&建议

遇到问题或有建议，可以在[github]([l460289052/xhyx_key_recorder: 小鹤音形按键优化 (github.com)](https://github.com/l460289052/xhyx_key_recorder))上面提交，或通过邮件发送460289052@qq.com。QQ群里说我看不到的。