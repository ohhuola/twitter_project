# tweet_project
## 简介
tweet_project是一个Python环境下基于flask和adminlte,bootstrap模板的WEB后台推特用户管理系统，目标是用极少量的代码，快速构建小型WEB应用。请勿在大中型项目中进行尝试。  

1. 使用较传统的重后端+轻前端的方式，降低总体代码量
2. Web框架使用Flask，默认Jinja模版
3. ORM框架使用Peewee
4. 前端套用基于BootStrap的AdminLTE模板,echarts,jvectormap

## 系统截图
- 登录页  
![](https://i.loli.net/2018/11/18/5bf14012e5d85.png)

- 主页  
![](https://i.loli.net/2018/11/18/5bf140156fee7.png)

- 用户管理界面  
![](https://i.loli.net/2018/11/18/5bf1401646a87.png)  

- 用户增加界面
![](https://i.loli.net/2018/11/18/5bf140151e15a.png)

- 用户查询界面  
![](https://i.loli.net/2018/11/18/5bf1401e81956.png)

- 用户个人详细信息：主要信息

![](https://i.loli.net/2018/11/18/5bf14014a5ab7.png)

- 用户个人详细信息：图表信息（使用标签次数，提及用户）
![](https://i.loli.net/2018/11/18/5bf140151e12b.png)

-用户个人详细信息：相关链接
![](https://i.loli.net/2018/11/18/5bf140151e15a.png)

-用户个人详细信息:发送的推文
![](https://i.loli.net/2018/11/18/5bf1401645dd9.png)


## 第三方依赖
- peewee
- pymysql
- flask
- flask-script
- flask-wtf
- flask-login


## 环境配置
### venv虚拟环境安装配置
```
sudo pip3 install virtualenv
virtualenv venv
. venv/bin/activate
```

### 第三方依赖安装
```
pip3 install -r requirements.txt

```
### 系统参数配置
1. 编辑`config.py`， 修改SECRET_KEY及MySQL数据库相关参数
```
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret'
DB_HOST = '127.0.0.1'
DB_USER = 'xxxxx'
DB_PASSWD = 'xxxxx'
DB_DATABASE = 'xxxxx'
```

2. 编辑log-app.conf，修改日志路径
```
args=('/path/to/log/flask-rest-sample.log','a','utf8')
```

### 数据库初始化
1. 将sql文件夹中的两个sql文件导入数据库，并创建user表（也可以运行model.py创建）


2. 在user表中插入管理员用户（默认admin/admin)
```
INSERT INTO `user` (`id`, `username`, `password`, `fullname`, `email`, `phone`, `status`)
VALUES
	(1, 'admin', 'pbkdf2:sha1:1000$Km1vdx3W$9aa07d3b79ab88aae53e45d26d0d4d4e097a6cd3', '管理员', 'admin@admin.com', '18612341234', 1);
```

### 启动应用
```
nohup ./manage.py runserver 2>&1 &
或
./run_app_dev.py (仅限测试)
```


## 项目目录结构
![](https://i.loli.net/2018/11/18/5bf14425783ba.png)
  
- /app/auth  用户认证相关代码
- /app/main  主要功能点相关代码
- /app/static  JS、CSS等静态文件
- /app/template  页面模版
- /app/models.py  Peewee模型
- /app/utils.py  工具模块
- /conf  系统参数及日志配置


## 相关学习文档
- [http://flask.pocoo.org](http://flask.pocoo.org)
- [https://flask-login.readthedocs.io](https://flask-login.readthedocs.io)
- [https://flask-script.readthedocs.io](https://flask-script.readthedocs.io)
- [https://flask-wtf.readthedocs.io](https://flask-wtf.readthedocs.io)
- [http://docs.peewee-orm.com](http://docs.peewee-orm.com)
- [https://almsaeedstudio.com/preview](https://almsaeedstudio.com/preview)
- [http://echarts.baidu.com/](http://echarts.baidu.com/)
- [http://jvectormap.com/](http://jvectormap.com/)
