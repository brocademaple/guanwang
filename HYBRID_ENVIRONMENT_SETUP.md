# 混合开发环境搭建指南 - Docker数据库 + 本地Python

由于Docker Python镜像拉取遇到网络问题，我们采用混合环境方案：使用Docker管理MySQL数据库和phpMyAdmin，同时在本地运行Python应用。

## 一、Docker数据库环境（已配置完成）

目前，我们已经成功启动了以下Docker服务：

1. **MySQL数据库服务**
   - 容器名称：mysql_pipe_system
   - 端口映射：3306:3306
   - 数据库名：pipedb
   - 用户名：root
   - 密码：root
   - 已自动导入pipedb.sql数据

2. **phpMyAdmin数据库管理工具**
   - 容器名称：phpmyadmin_pipe_system
   - 访问地址：http://localhost:8080
   - 登录信息：用户名root，密码root

## 二、在本地设置Python开发环境

### 1. 安装Python 3.8

如果尚未安装Python 3.8，请从官网下载并安装：
- 下载地址：https://www.python.org/downloads/release/python-380/
- 安装时请勾选"Add Python 3.8 to PATH"

### 2. 设置Python虚拟环境

```powershell
# 打开PowerShell
# 进入项目目录
cd C:\Users\marine\Desktop\管网系统25.2.4\Pipe-network-defect-system25.2.4

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 升级pip
python -m pip install --upgrade pip

# 配置pip使用国内镜像源
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set global.trusted-host mirrors.aliyun.com

# 安装项目依赖
pip install -r requirements.txt

# 安装simpleui
pip install django-simpleui -U
```

### 3. 配置Django项目连接Docker数据库

编辑 `simpleui_demo/settings.py` 文件，确保数据库配置如下：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pipedb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',  # 因为Docker将MySQL端口映射到本地
        'PORT': '3306',
    }
}
```

### 4. 创建必要目录

```powershell
# 创建静态文件和媒体文件目录（如果不存在）
mkdir -p static
mkdir -p media
```

## 三、运行项目

```powershell
# 确保虚拟环境已激活
venv\Scripts\activate

# 收集静态文件
python manage.py collectstatic --noinput --clear

# 运行开发服务器
python manage.py runserver 0.0.0.0:8000
```

## 四、访问项目

- **Django应用**：http://localhost:8000
- **Django管理后台**：http://localhost:8000/admin
- **数据库管理**：http://localhost:8080
  - 用户名：root
  - 密码：root

## 五、开发工作流

1. **每次开发前**
   - 确保Docker数据库服务已启动（如果已停止）
     ```powershell
     docker-compose up -d
     ```
   - 激活Python虚拟环境
     ```powershell
     venv\Scripts\activate
     ```

2. **开发完成后**
   - 按 Ctrl+C 停止Django开发服务器
   - 可以选择停止Docker服务或保持运行
     ```powershell
     # 停止Docker服务（可选）
     docker-compose down
     ```
   - 退出虚拟环境
     ```powershell
     deactivate
     ```

3. **数据库迁移**
   修改models.py后，执行以下命令：
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

## 六、Docker数据库服务管理

```powershell
# 查看Docker服务状态
docker-compose ps

# 查看数据库日志
docker-compose logs db

# 重启数据库服务
docker-compose restart db

# 停止所有服务
docker-compose down

# 启动所有服务
docker-compose up -d
```

## 七、常见问题解决

1. **数据库连接失败**
   - 检查Docker服务是否正在运行：`docker-compose ps`
   - 确保MySQL端口3306未被占用

2. **Python依赖安装失败**
   - 确保虚拟环境已激活
   - 检查网络连接是否正常

3. **Django服务器启动失败**
   - 检查端口8000是否被占用
   - 确保数据库配置正确

这种混合环境方案结合了Docker管理数据库的便捷性和本地运行Python应用的灵活性，特别适合在网络受限环境下开发使用。