import os
import django

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleui_demo.settings')
django.setup()

from django.db import connection

# 执行SQL修改structural_defect_parameter字段的精度
with connection.cursor() as cursor:
    cursor.execute('ALTER TABLE defect_repair_defectinfo MODIFY COLUMN structural_defect_parameter DECIMAL(5,2) NOT NULL DEFAULT 0;')
    print('数据库表结构已更新成功！')