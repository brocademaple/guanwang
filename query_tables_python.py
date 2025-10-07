#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
查询数据库中指定表的数据并输出为表格格式
"""

import os
import sys
import django
from tabulate import tabulate

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleui_demo.settings')
django.setup()

from django.db import connection

def query_table_data(table_name):
    """查询指定表的数据"""
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM {table_name}")
        # 获取列名
        columns = [col[0] for col in cursor.description]
        # 获取数据
        data = cursor.fetchall()
        return table_name, columns, data

def main():
    # 要查询的表名列表
    tables = [
        'defect_repair_defectinfo',
        'defect_repair_pipesection',
        'defect_repair_repairsuggestion',
        'func_defect_repair_funcdefectinfo',
        'func_defect_repair_funcpipesection',
        'func_defect_repair_funcrepairsuggestion'
    ]
    
    # 存储所有查询结果
    results = []
    
    for table in tables:
        print(f"\n正在查询表: {table}")
        try:
            table_name, columns, data = query_table_data(table)
            results.append((table_name, columns, data))
            
            # 打印表格
            if data:
                print(tabulate(data, headers=columns, tablefmt='grid', showindex=True))
                print(f"共 {len(data)} 条记录")
            else:
                print(f"表 {table} 中没有数据")
        except Exception as e:
            print(f"查询表 {table} 时出错: {str(e)}")
    
    # 将结果保存到文件
    with open('table_data_report.txt', 'w', encoding='utf-8') as f:
        for table_name, columns, data in results:
            f.write(f"\n{'='*80}\n")
            f.write(f"表名: {table_name}\n")
            f.write(f"{'='*80}\n")
            
            if data:
                f.write(tabulate(data, headers=columns, tablefmt='grid', showindex=True))
                f.write(f"\n\n共 {len(data)} 条记录\n")
            else:
                f.write(f"表 {table_name} 中没有数据\n")
    
    print("\n查询结果已保存到 table_data_report.txt 文件中")

if __name__ == "__main__":
    main()