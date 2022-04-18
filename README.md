# python_script_tool

1. feishu
   1. 支持将昨天的日报，移动到文件夹：`99. 日报备份`
   2. 基于模板，创建今天的日报 - 仍需人工修改标题
   3. 发送飞书信息，通知相关群，进行日报填写

   > 参考crontab配置 - `30 17 * * * cd /Users/nick/project/github/python_script_tool && python3 feishu.py`