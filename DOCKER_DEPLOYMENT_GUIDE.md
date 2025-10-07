# 管网缺陷管理系统 - Docker环境使用与交付指南

## 一、环境准备

### 1. 前提条件
- 安装Docker Desktop (Windows/macOS) 或 Docker Engine (Linux)
- 确保Docker版本 ≥ 19.03
- 确保Docker Compose版本 ≥ 1.28
- 克隆或下载项目代码到本地

### 2. 项目文件准备
确保以下关键文件存在于项目根目录：
- `docker-compose.yml` - Docker容器编排配置
- `Dockerfile` - Django应用容器构建配置
- `pipedb.sql` - 数据库初始化SQL文件
- `requirements.txt` - Python依赖列表
- `setup_database.py` - 环境设置辅助脚本

## 二、使用Docker管理项目环境

### 1. 首次构建与启动

```bash
# 进入项目目录
cd Pipe-network-defect-system25.2.4

# 构建镜像并启动容器（第一次运行会自动导入pipedb.sql）
docker-compose up -d

# 查看容器运行状态
docker-compose ps
```

### 2. 访问系统
- 应用系统: http://localhost:8000
- 数据库管理工具: http://localhost:8080 (phpMyAdmin)
  - 用户名: root
  - 密码: root

### 3. 常用Docker命令

```bash
# 停止所有容器
docker-compose down

# 重新构建并启动（当修改了Dockerfile或代码时）
docker-compose up -d --build

# 查看容器日志
docker-compose logs -f

# 查看Django应用容器日志
docker-compose logs -f web

# 查看MySQL容器日志
docker-compose logs -f db

# 进入Django应用容器（调试用）
docker-compose exec web bash
```

## 三、SQL文件自动导入机制

系统已配置自动导入数据库功能，工作原理如下：

1. 在`docker-compose.yml`中，已将`pipedb.sql`文件挂载到MySQL容器的初始化目录：
   ```yaml
   volumes:
     - ./pipedb.sql:/docker-entrypoint-initdb.d/01_pipedb.sql
   ```

2. MySQL容器启动时，会自动执行`/docker-entrypoint-initdb.d/`目录下的所有SQL文件

3. 导入过程在容器首次启动时自动完成，无需手动操作

> **注意**：如果需要导入新的SQL文件，只需将新文件放在项目根目录，并修改docker-compose.yml中的挂载配置

## 四、开发环境管理

### 1. 实时代码更新
由于我们在`docker-compose.yml`中配置了代码目录挂载：
```yaml
volumes:
  - .:/work
```

您对本地代码的修改会实时同步到容器中，无需重新构建镜像即可看到效果。

### 2. 数据库迁移
当Django模型发生变化时，需要执行数据库迁移：

```bash
# 在容器内执行数据库迁移
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

## 五、交付指南（一步到位方案）

### 1. 交付包内容准备
将以下文件打包交付给客户：
- 整个项目目录（包含所有代码和配置文件）
- 本指南文档
- pipedb.sql数据库文件

### 2. 客户端部署步骤（一键启动）

客户只需按照以下步骤操作即可完成部署：

1. 安装Docker Desktop（Windows/macOS）或Docker Engine（Linux）
2. 解压项目文件到本地
3. 打开命令行工具，进入项目目录
4. 执行一键启动命令：
   ```bash
   docker-compose up -d
   ```
5. 等待容器启动完成（首次启动约需3-5分钟）
6. 访问 http://localhost:8000 即可使用系统

### 3. 交付注意事项

- **数据库安全**：默认配置使用root用户和简单密码，生产环境请修改docker-compose.yml中的数据库凭证
- **端口冲突**：如本地已占用3306、8000或8080端口，请在docker-compose.yml中修改映射端口
- **数据持久化**：数据库数据存储在Docker卷中，不会因为容器重启而丢失
- **备份方案**：建议客户定期备份数据卷和pipedb.sql文件

## 六、故障排除

### 1. 容器无法启动

```bash
# 查看详细错误日志
docker-compose logs -f
```

### 2. 数据库连接失败

- 检查MySQL容器是否正常运行：`docker-compose ps db`
- 查看MySQL日志：`docker-compose logs -f db`
- 确认环境变量配置正确

### 3. 应用访问缓慢

- 检查Docker资源分配是否充足
- 优化MySQL性能配置

### 4. 常见错误及解决方法

- **错误**: `Error starting userland proxy: listen tcp 0.0.0.0:3306: bind: address already in use`
  **解决**: 停止本地MySQL服务或修改docker-compose.yml中的端口映射

- **错误**: `django.db.utils.OperationalError: (1045, "Access denied for user 'root'@'xxx'")`
  **解决**: 确认docker-compose.yml中的数据库密码配置正确

## 七、升级与维护

### 1. 升级应用

```bash
# 停止当前容器
docker-compose down

# 更新代码
# git pull 或 替换代码文件

# 重新构建并启动
docker-compose up -d --build
```

### 2. 备份数据

```bash
# 备份数据库到SQL文件
docker-compose exec db mysqldump -u root -proot pipedb > pipedb_backup.sql
```

## 八、总结

本项目通过Docker实现了完整的容器化部署，主要优势：

1. **环境一致性**：开发、测试、生产环境完全一致
2. **一键部署**：客户只需一条命令即可完成部署
3. **隔离性**：不影响客户现有系统和环境
4. **可移植性**：支持Windows、macOS和Linux系统
5. **自动数据导入**：SQL文件会在容器启动时自动导入

如有任何问题，请参考Docker官方文档或联系技术支持。