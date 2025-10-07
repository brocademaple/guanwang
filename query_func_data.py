# 查询功能性缺陷及对应修复措施的文件
# 运行方式：python query_func_data.py 
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpleui_demo.settings')
django.setup()

# 现在可以导入模型了
from func_defect_repair.models import FuncPipeSection, funcdefectinfo, funcrepairsuggestion

print('=== FuncPipeSection 数据 ===')
for section in FuncPipeSection.objects.all()[:3]:
    print(f'ID: {section.id}, 工点: {section.work_point_name}, 长度: {section.pipe_length}米, 类型: {section.pipe_type}, 材质: {section.pipe_material}')

print('\n=== funcdefectinfo 数据 ===')
for defect in funcdefectinfo.objects.all()[:5]:
    print(f'ID: {defect.id}, 缺陷: {defect.defect_name}, 等级: {defect.defect_level}, 管段: {defect.pipe_section.work_point_name if defect.pipe_section else None}')

print('\n=== funcrepairsuggestion 数据 ===')
for suggestion in funcrepairsuggestion.objects.all()[:3]:
    print(f'ID: {suggestion.id}, 缺陷: {suggestion.defect_info.defect_name}, 建议: {suggestion.repair_suggestion[:50]}...')


'''
示例：
=== FuncPipeSection 数据 ===
ID: 1, 工点: 测试功能性缺陷-管径小于400, 长度: 100.00米, 类型: 雨水管, 材质: 混凝土管
ID: 2, 工点: 测试功能性缺陷-管径400600, 长度: 100.00米, 类型: 雨水管, 材质: 塑料管
ID: 3, 工点: 测试功能性缺陷-管径大于600, 长度: 100.00米, 类型: 雨水管, 材质: 塑料管

=== funcdefectinfo 数据 ===
ID: 1, 缺陷: 沉积, 等级: 1级, 管段: 测试功能性缺陷-管径小于400
ID: 2, 缺陷: 沉积, 等级: 1级, 管段: 测试功能性缺陷-管径400600
ID: 3, 缺陷: 沉积, 等级: 1级, 管段: 测试功能性缺陷-管径大于600
ID: 4, 缺陷: 结垢, 等级: 1级, 管段: 测试功能性缺陷-管径小于400
ID: 5, 缺陷: 结垢, 等级: 1级, 管段: 测试功能性缺陷-管径400600

=== funcrepairsuggestion 数据 ===
ID: 1, 缺陷: 沉积, 建议: 高压水射流管道清淤+绞车疏通辅助...
ID: 2, 缺陷: 沉积, 建议: 高压水射流管道清淤+绞车疏通辅助...
ID: 3, 缺陷: 沉积, 建议: 高压水射流管道清淤+人工清除辅助...
'''
