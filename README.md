# Sign_in_script
签到脚本

# 定时任务

```
cronta -e
表示在每天的1点执行任务，实际国内时间为9点(国外要注意VPS时差)
0 1 * * * /bin/bash /root/Sign_in_script/start.sh > /dev/null 2>&1
表示在每天的10点执行任务(国内)
0 10 * * * /bin/bash /root/Sign_in_script/start.sh > /dev/null 2>&1
```

# 简单使用

目前支持的系统：t00ls、hostloc、ruike等

## 1、修改配置文件

将lib目录下的`config-debug.yaml`修改为`config.yaml`, 然后根据配置内容的注释进行填写就行

## 2、修改提醒脚本

同样是lib目录下的`notify - debug.py`修改为`notify.py`文件，根据脚本注释修改push_config的内容

## 3、修改主函数

在`main.py`中定义了四个模块，可以将不需要的模块注释掉

