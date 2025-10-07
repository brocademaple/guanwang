import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleui_demo.settings')
django.setup()

from django.db import connection

# 删除表的函数
def drop_tables(table_names):
    with connection.cursor() as cursor:
        for table_name in table_names:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"已删除表: {table_name}")
            except Exception as e:
                print(f"删除表 {table_name} 时出错: {e}")

# 要删除的表 - func_defect_repair应用的表
# 按照外键关系顺序删除：修复建议表 -> 缺陷表 -> 管段表
tables_to_drop = [
    'func_defect_repair_funcrepairsuggestion',  # 修复建议表
    'func_defect_repair_funcdefectinfo',        # 缺陷表
    'func_defect_repair_funcpipesection'        # 管段表
]

# 删除表
drop_tables(tables_to_drop)

# 清除迁移记录
def reset_migrations(app_names):
    with connection.cursor() as cursor:
        for app_name in app_names:
            try:
                cursor.execute("DELETE FROM django_migrations WHERE app = %s", [app_name])
                print(f"已清除 {app_name} 的迁移记录")
            except Exception as e:
                print(f"清除 {app_name} 迁移记录时出错: {e}")

reset_migrations(['func_defect_repair'])

print("\nfunc_defect_repair应用的表删除和迁移记录重置完成！现在可以运行 makemigrations 和 migrate 命令了。")