# Docker开发环境搭建步骤指南

以下是在Docker上搭建管网缺陷管理系统开发环境的详细步骤：

## 一、准备工作

1. **确保Docker Desktop已安装并运行**
   - 打开Docker Desktop应用程序
   - 等待Docker图标显示为绿色，表示Docker服务已正常运行

2. **检查项目文件**
   确保项目根目录下包含以下关键文件：
   - `docker-compose.yml` - 容器编排配置
   - `Dockerfile` - Django应用构建配置
   - `pipedb.sql` - 数据库初始化文件

## 二、搭建开发环境

### 1. 启动Docker容器

```bash
# 打开命令行工具（Windows使用PowerShell或CMD）
# 进入项目目录
cd C:\Users\marine\Desktop\管网系统25.2.4\Pipe-network-defect-system25.2.4

# 构建镜像并启动容器
docker-compose up -d
```

### 2. 等待初始化完成

首次启动时，系统会执行以下操作（约需3-5分钟）：
- 下载必要的Docker镜像
- 构建Django应用镜像
- 启动MySQL数据库并自动导入pipedb.sql
- 启动Django应用和phpMyAdmin

### 3. 验证环境是否成功搭建

```bash
# 检查容器运行状态
docker-compose ps

# 查看日志确认启动情况
docker-compose logs -f web
```

## 三、开发工作流程

### 1. 访问开发环境

- **Django管理后台**：http://localhost:8000/admin
- **数据库管理**：http://localhost:8080
  - 用户名: root
  - 密码: root
  - 数据库名: pipedb

### 2. 代码修改与调试

项目代码目录已挂载到容器内，您对本地代码的修改会实时同步到容器中：

- 修改models.py后执行数据库迁移：
  ```bash
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```

- 查看Django应用日志：
  ```bash
  docker-compose logs -f web
  ```

### 3. 常用开发命令

```bash
# 进入Django容器内部（可执行Python命令调试）
docker-compose exec web bash

# 运行测试
docker-compose exec web python manage.py test

# 创建新的Django应用
docker-compose exec web python manage.py startapp new_app

# 收集静态文件
docker-compose exec web python manage.py collectstatic --noinput
```

## 四、开发结束后的操作

```bash
# 停止开发环境
docker-compose down

# 下次开发时重新启动
docker-compose up -d
```

## 五、注意事项

1. **端口冲突**：如果本地已使用8000或8080端口，请修改docker-compose.yml中的端口映射
2. **数据持久化**：数据库数据存储在Docker卷中，不会因为容器重启而丢失
3. **权限问题**：Windows下可能遇到文件权限问题，通常重新启动Docker Desktop可以解决

## 六、故障排除

如果遇到问题，可以尝试以下操作：

```bash
# 查看详细日志
docker-compose logs

# 重建所有镜像（当Dockerfile或依赖变更时）
docker-compose up -d --build --force-recreate

# 检查MySQL连接
docker-compose exec db mysql -u root -proot -e "SHOW DATABASES;"
```

如有其他问题，请参考项目中的DOCKER_DEPLOYMENT_GUIDE.md文档获取更详细的指导。