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

# 版本更新

- v0.3 版本更新

```
1、添加获取服务器IP脚本
2、优化框架结构, 统一使用config.yaml配置, 
  2.1 记得先把config-debug.yaml修改为config.yaml
  2.2 配置方法直接看yaml文件就行
3、删除52破解脚本,绕不过人机检测都是白费
```

- v0.2 版本更新

```
1、整合优化框架结构,将代码使用模块的方式组合到一起
2、添加提醒脚本lib\notify.py
3、添加52pojie签到脚本，但这个仍不完善，需要获取cookie才能自动签到。
4、添加到期提醒脚本
5、修改hostloc脚本，添加查询积分功能
```


- v0.1 首次完成项目基础功能

```
初步完成基本功能，可以实现:
1、无验证码discuz论坛签到，适配网站https://www.guokems.com(已关闭)、https://hostloc.com
2、无验证码discuz论坛签到，适配网站https://www.ruike1.com/，再获取discuz_uid时有所不同
3、t00ls论坛签到、自动查询域名
4、提醒功能，TG提醒、server酱提醒
```

