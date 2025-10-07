#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
数据库初始化脚本
用于创建数据库并执行迁移操作
"""

import os
import sys
import subprocess
import time
import platform

# 检查Python版本
required_version = (3, 8)
current_version = sys.version_info[:2]

print(f"检测到Python版本: {sys.version}")
print(f"推荐Python版本: {required_version[0]}.{required_version[1]}")

# 提示但不强制要求使用特定版本，因为用户环境中可能有不同版本
if current_version != required_version:
    print(f"警告: 推荐使用Python {required_version[0]}.{required_version[1]} 版本，当前版本为 {current_version[0]}.{current_version[1]}")
    print("继续执行，但可能会遇到兼容性问题...")

def run_command(command, cwd=None, show_output=True):
    """执行命令并打印输出"""
    if show_output:
        print(f"执行命令: {' '.join(command)}")
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=(sys.platform == 'win32')
        )
        if result.stdout and show_output:
            print(result.stdout)
        if result.stderr and show_output:
            print(f"错误: {result.stderr}")
        return result
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return None

def check_dependencies():
    """检查关键依赖是否已安装"""
    try:
        import django
        print(f"Django已安装: {django.__version__}")
        return True
    except ImportError:
        print("Django未安装")
        return False

def setup_database():
    """设置数据库"""
    # 确保在项目根目录
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    print("=== 开始初始化数据库 ===")
    
    # 检查操作系统
    print(f"操作系统: {platform.system()} {platform.version()}")
    
    # 安装依赖
    print("\n=== 安装项目依赖 ===")
    if os.path.exists('requirements.txt'):
        # 升级pip
        print("升级pip...")
        run_command([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
        
        # 安装依赖，使用国内镜像提高速度
        print("安装项目依赖...")
        # 先尝试使用阿里云镜像
        result = run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-i', 'https://mirrors.aliyun.com/pypi/simple/'])
        
        # 如果失败，尝试不使用镜像
        if result is None or result.returncode != 0:
            print("\n尝试不使用镜像安装...")
            run_command([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        
        # 验证安装是否成功
        if not check_dependencies():
            print("\n错误: 依赖安装失败，请手动安装依赖：")
            print(f"{sys.executable} -m pip install -r requirements.txt")
            
            # 对于Windows用户，提供mysqlclient的特殊安装提示
            if platform.system() == 'Windows':
                print("\nWindows用户安装mysqlclient可能需要：")
                print("1. 安装 Visual C++ Build Tools")
                print("2. 或从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient 下载对应版本的wheel文件")
                print("3. 然后执行: pip install mysqlclient‑*.whl")
            return
    else:
        print("警告: requirements.txt 不存在")
        return
    
    # 执行数据库迁移
    print("\n=== 执行数据库迁移 ===")
    # 确保数据库已经准备好
    print("等待数据库准备就绪...")
    time.sleep(3)  # 减少等待时间，因为可能没有运行MySQL服务
    
    # 生成迁移文件
    print("生成迁移文件...")
    run_command([sys.executable, 'manage.py', 'makemigrations'], cwd=project_dir)
    
    # 应用迁移
    print("应用迁移...")
    run_command([sys.executable, 'manage.py', 'migrate'], cwd=project_dir)
    
    # 创建超级用户（可选）
    print("\n=== 数据库初始化完成 ===")
    print("您可以通过以下命令创建超级用户：")
    print(f"{sys.executable} manage.py createsuperuser")
    
    print("\n=== 使用说明 ===")
    print("1. 确保MySQL服务已启动并创建了pipedb数据库")
    print("2. 在本地运行时，可以直接使用: python manage.py runserver")
    print("3. 使用Docker运行时，可以使用: docker-compose up -d")
    print("4. 数据库配置已经设置为从环境变量读取，确保环境变量正确设置")
    print(f"5. 当前Python版本: {sys.version}")
    print("\n注意: 如果遇到数据库连接问题，请确保MySQL服务正在运行且配置正确")

if __name__ == "__main__":
    setup_database()