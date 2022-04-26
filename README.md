# 1、安装python版本3.10
# 2、安装requirements.txt中的库
# 3、安装 pip install uvicorn
# 4、运行 src.sql_app.tasks:app --host '0.0.0.0' --port 8000 --reload，会在工程根目录下创建名为"check_bank_name.db" ，包含bot表和tasks表
# 5、准备就绪后，执行项目工程目录的run.py文件
# 6、del_done_task JOB 删除数据的定时任务，每天00:30:30 删除状态为"Done"的数据
# 7、run JOB 拉取任务订单的定时任务，每隔2秒，可以指定任意间隔时间
# 8、login JOB  登录定时任务，项目启动后，立即执行一次（需要手动输入验证码，暂时没有使用解析图形验证码自动登录）