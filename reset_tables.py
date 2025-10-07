import os
# 注意：此文件已被拆分为两个独立的重置脚本
# 请根据需要使用以下专门的重置脚本：

# 1. 重置defect_repair应用的表和迁移记录
# python reset_defect_repair_tables.py

# 2. 重置func_defect_repair应用的表和迁移记录
# python reset_func_defect_repair_tables.py

# 这两个新脚本分别处理不同应用的表重置，避免了表之间的依赖冲突
# 它们都按照外键关系顺序删除表：修复建议表 -> 缺陷表 -> 管段表