# 管网缺陷系统 MySQL 环境配置说明

本文档提供了如何为管网缺陷系统配置MySQL环境的详细指南。

## 配置概述

我们已经对项目进行了以下配置：

1. 更新了 `docker-compose.yml`，添加了MySQL服务
2. 修改了 `settings.py`，支持从环境变量读取数据库配置
3. 创建了数据库初始化脚本 `setup_database.py`
4. 确保项目支持Python 3.8版本

## 环境要求

- Python 3.8
- Docker 和 Docker Compose（推荐用于容器化部署）
- 或本地安装的MySQL 8.0
- pip 包管理工具

## 使用 Docker Compose 部署（推荐）

### 步骤1：确保MySQL驱动已安装

项目的 `requirements.txt` 已经包含了 `mysqlclient==2.0.3`，这是Django连接MySQL所必需的。

### 步骤2：启动服务

在项目根目录下执行：

```bash
docker-compose up -d
```

这将：
- 启动MySQL 8.0容器，创建名为`pipedb`的数据库
- 启动Django应用容器，并连接到MySQL

### 步骤3：执行数据库迁移

连接到Django容器并执行迁移：

```bash
docker exec -it simpleui_demo_docker python manage.py makemigrations
docker exec -it simpleui_demo_docker python manage.py migrate
```

### 步骤4：创建超级用户

```bash
docker exec -it simpleui_demo_docker python manage.py createsuperuser
```

按照提示输入用户名、邮箱和密码。

## 本地开发环境设置

如果您希望在本地开发环境中使用MySQL：

### 步骤1：确保MySQL已安装并运行

确保本地MySQL服务器已安装并运行在端口3306上。

### 步骤2：创建数据库

登录MySQL并创建数据库：

```sql
CREATE DATABASE pipedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 步骤3：运行初始化脚本

执行我们提供的初始化脚本：

```bash
python setup_database.py
```

该脚本会自动：
- 检查Python版本（需要3.8或更高）
- 安装项目依赖
- 执行数据库迁移
- 准备好数据库环境

### 步骤4：创建超级用户

```bash
python manage.py createsuperuser
```

### 步骤5：启动开发服务器

```bash
python manage.py runserver
```

## 数据库配置参数

| 参数 | 容器内值 | 本地默认值 | 说明 |
|------|----------|------------|------|
| DB_HOST | db | 127.0.0.1 | 数据库主机地址 |
| DB_PORT | 3306 | 3306 | 数据库端口 |
| DB_NAME | pipedb | pipedb | 数据库名称 |
| DB_USER | root | root | 数据库用户名 |
| DB_PASSWORD | root | root | 数据库密码 |

## 环境变量配置

如果需要自定义数据库连接，可以通过设置以下环境变量来覆盖默认配置：

```bash
# Windows 命令提示符
set DB_HOST=your_host
set DB_PORT=your_port
set DB_NAME=your_db_name
set DB_USER=your_username
set DB_PASSWORD=your_password

# PowerShell
$env:DB_HOST="your_host"
$env:DB_PORT="your_port"
$env:DB_NAME="your_db_name"
$env:DB_USER="your_username"
$env:DB_PASSWORD="your_password"
```

## 注意事项

1. 确保使用Python 3.8版本，初始化脚本会自动检查版本兼容性
2. 确保MySQL版本兼容（推荐8.0版本）
3. 首次运行时需要等待MySQL服务完全启动后再执行迁移
4. 数据库字符集已设置为`utf8mb4`，支持存储更多字符
5. 如遇到连接问题，请检查防火墙设置和端口占用情况

## 故障排除

### 常见错误及解决方案

1. **mysqlclient 安装失败**
   - Windows: 安装 Visual C++ Build Tools 或使用预编译的 wheel 文件
   - Linux: 安装 `libmysqlclient-dev` 包

2. **数据库连接失败**
   - 检查MySQL服务是否运行
   - 验证用户名和密码是否正确
   - 确认数据库名称是否存在

3. **Docker 容器启动失败**
   - 使用 `docker-compose logs` 查看详细错误信息
   - 确保端口 3306 和 8000 未被占用

4. **Python版本不兼容**
   - 确保使用Python 3.8版本
   - 可以使用虚拟环境管理不同项目的Python版本

## 联系与支持

如有任何问题，请联系系统管理员获取帮助。