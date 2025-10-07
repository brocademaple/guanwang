# 模拟计算管道缺陷参数
# 基于PipeSection类的计算逻辑
# 图片数据分析：缺陷点A、B、C、D、E、F、G及其间距

class SimulatedDefect:
    def __init__(self, start_pos, end_pos, score):
        self.defect_start_position_m = start_pos
        self.defect_end_position_m = end_pos
        self._score = score
    
    def get_defect_score(self):
        return self._score

class SimulatedPipeSection:
    def __init__(self):
        # 模拟图片中的缺陷数据
        self.defects = [
            SimulatedDefect(0, 0.1, 10),  # A点
            SimulatedDefect(1.9, 2.0, 20),  # B点
            SimulatedDefect(3.3, 3.4, 30),  # C点
            SimulatedDefect(4.0, 4.1, 40),  # D点
            SimulatedDefect(5.3, 5.4, 25),  # E点
            SimulatedDefect(5.5, 5.6, 35),  # F点
            SimulatedDefect(5.8, 5.9, 45),  # G点
        ]
        
        # 模拟管段属性
        self.pipe_length = 10.0  # 假设管段长度为10米
        self.pipe_diameter = 800  # 假设直径为800毫米
        self.area_type = '所有其他区域'  # 假设地区类别
        self.soil_type = '一般土层'  # 假设土质类型
        self.pipe_type = '污水管'  # 假设管道类型
        self.pipe_material = '混凝土管'  # 假设管道材质
    
    def merge_and_classify_defects(self):
        # 复制原始合并分类逻辑
        all_defects = self.defects
        
        if not all_defects:
            return [], [], []
        
        # 按照缺陷起始位置排序
        sorted_defects = sorted(all_defects, key=lambda d: d.defect_start_position_m)
        
        # 计算每个缺陷的中心点位置
        defects_with_center = []
        for defect in sorted_defects:
            center = (defect.defect_start_position_m + defect.defect_end_position_m) / 2
            length = defect.defect_end_position_m - defect.defect_start_position_m
            defects_with_center.append({
                'defect': defect,
                'start': defect.defect_start_position_m,
                'end': defect.defect_end_position_m,
                'center': center,
                'length': length,
                'score': defect.get_defect_score()
            })
        
        # 合并相邻中心点距离小于1m的缺陷
        merged_defects = []
        i = 0
        while i < len(defects_with_center):
            current_group = [defects_with_center[i]]
            current_start = defects_with_center[i]['start']
            current_end = defects_with_center[i]['end']
            current_score = defects_with_center[i]['score']
            
            j = i + 1
            while j < len(defects_with_center):
                distance = defects_with_center[j]['center'] - defects_with_center[j-1]['center']
                if distance < 1.0:
                    current_group.append(defects_with_center[j])
                    current_end = defects_with_center[j]['end']
                    current_score += (defects_with_center[j]['score'] + defects_with_center[j-1]['score'])
                    j += 1
                else:
                    break
            
            merged_center = (current_start + current_end) / 2
            merged_length = current_end - current_start
            
            merged_defects.append({
                'start': current_start,
                'end': current_end,
                'center': merged_center,
                'length': merged_length,
                'score': current_score
            })
            
            i = j
        
        # 分类缺陷
        defects_1_5m_plus = []
        defects_1_0m_to_1_5m = []
        
        for i in range(1, len(merged_defects)):
            prev_defect = merged_defects[i-1]
            curr_defect = merged_defects[i]
            distance = curr_defect['center'] - prev_defect['center']
            
            if distance > 1.5:
                if prev_defect not in defects_1_5m_plus:
                    defects_1_5m_plus.append(prev_defect)
                if curr_defect not in defects_1_5m_plus:
                    defects_1_5m_plus.append(curr_defect)
        
        for defect in merged_defects:
            if defect not in defects_1_5m_plus:
                defects_1_0m_to_1_5m.append(defect)
        
        return merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m
    
    def calculate_S(self):
        merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m = self.merge_and_classify_defects()
        
        n = len(merged_defects)
        n1 = len(defects_1_5m_plus)
        n2 = n - n1
        
        sum_Pi1 = sum(defect['score'] for defect in defects_1_5m_plus)
        sum_Pi2 = sum(defect['score'] for defect in defects_1_0m_to_1_5m)
        
        alpha = 1.1
        
        if n > 0:
            S = (sum_Pi1 + alpha * sum_Pi2) / n
            return S
        else:
            return 0
    
    def calculate_F(self):
        all_defects = self.defects
        
        if not all_defects:
            return 0
        
        S = self.calculate_S()
        scores = [defect.get_defect_score() for defect in all_defects]
        Smax = max(scores) if scores else 0
        
        return Smax if Smax >= S else S
    
    def calculate_Sm(self):
        merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m = self.merge_and_classify_defects()
        
        if not merged_defects:
            return 0
        
        L = float(self.pipe_length)
        if L <= 0:
            return 0
        
        S = self.calculate_S()
        if S <= 0:
            return 0
        
        sum_Pi1_Li1 = sum(defect['score'] * defect['length'] for defect in defects_1_5m_plus)
        sum_Pi2_Li2 = sum(defect['score'] * defect['length'] for defect in defects_1_0m_to_1_5m)
        
        alpha = 1.1
        
        Sm = (sum_Pi1_Li1 + alpha * sum_Pi2_Li2) / (S * L)
        return Sm
    
    def get_area_value_K(self):
        area_type_mapping = {
            '中心商业、附近具有甲类民用建筑工程的区域': 10,
            '交通干道、附近具有乙类民用建筑工程的区域': 6,
            '其他行车道路、附近具有丙类民用建筑工程的区域': 3,
            '所有其他区域': 0
        }
        return area_type_mapping.get(self.area_type, 0)
    
    def calculate_E(self):
        diameter = float(self.pipe_diameter)
        if diameter > 1500:
            return 10
        elif 1000 < diameter <= 1500:
            return 6
        elif 600 <= diameter <= 1000:
            return 3
        elif diameter < 600:
            return 0
        return 0
    
    def get_soil_parameter_T(self):
        if self.soil_type == '一般土层':
            return 0
        # 其他土质类型的逻辑省略，这里只使用一般土层
        return 0
    
    def calculate_RI(self):
        F = self.calculate_F()
        K = self.get_area_value_K()
        E = self.calculate_E()
        T = self.get_soil_parameter_T()
        
        RI = 0.7 * F + 0.1 * K + 0.05 * E + 0.15 * T
        return RI
    
    def get_repair_suggestion(self):
        # 根据models.py中的逻辑实现修复建议计算
        RI = self.calculate_RI()
        F = self.calculate_F()
        Sm = self.calculate_Sm()
        
        # 根据文档中的修复建议表格进行判断
        if RI <= 1:
            return "不修复"
        elif 1 < RI <= 4:
            if F <= 3:
                return "不修复"
            elif F > 3:
                if Sm < 0.1:
                    return "局部修复"
                else:  # Sm >= 0.1
                    return "整体修复"
        else:  # RI > 4
            if Sm < 0.1:
                return "局部修复"
            else:  # Sm >= 0.1
                return "整体修复"

# 运行模拟计算
pipe = SimulatedPipeSection()

# 获取合并和分类结果
merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m = pipe.merge_and_classify_defects()

# 打印中间结果
print("合并后的缺陷:")
for i, defect in enumerate(merged_defects):
    print(f"  缺陷{i+1}: 起始={defect['start']}, 结束={defect['end']}, 中心={defect['center']}, "
          f"长度={defect['length']}, 分值={defect['score']}")

print("\n距离>1.5m的缺陷数量:", len(defects_1_5m_plus))
print("距离1.0-1.5m的缺陷数量:", len(defects_1_0m_to_1_5m))

# 计算并打印各参数
S = pipe.calculate_S()
F = pipe.calculate_F()
Sm = pipe.calculate_Sm()
K = pipe.get_area_value_K()
E = pipe.calculate_E()
T = pipe.get_soil_parameter_T()
RI = pipe.calculate_RI()
repair_suggestion = pipe.get_repair_suggestion()

print("\n计算结果:")
print(f"S (管段损坏状况参数): {S:.2f}")
print(f"F (结构性缺陷参数): {F:.2f}")
print(f"Sm (结构性缺陷密度): {Sm:.4f}")
print(f"K (地区类别值): {K}")
print(f"E (管道重要性参数): {E}")
print(f"T (土质影响参数): {T}")
print(f"RI (修复指数): {RI:.2f}")
print(f"修复建议: {repair_suggestion}")

'''
# 管段情况图示和详细分析

## 管段缺陷分布图示（基于图片数据）

```
0.0m  1.9m   3.3m  4.0m   5.3m  5.5m  5.8m  10.0m
 |     |      |     |      |     |     |     |
 [A]  [B]    [C---D]     [E-F-G]
```

缺陷点间距：
- A到B: 1.9m
- B到C: 1.4m
- C到D: 0.7m (合并)
- D到E: 1.3m
- E到F: 0.2m (合并)
- F到G: 0.3m (合并)

## 合并前缺陷情况

| 缺陷点 | 起始位置(m) | 结束位置(m) | 分值 | 特点 |
|--------|------------|------------|------|------|
| A      | 0.0        | 0.1        | 10   | 独立缺陷 |
| B      | 1.9        | 2.0        | 20   | 独立缺陷 |
| C      | 3.3        | 3.4        | 30   | 与D距离<1m，将合并 |
| D      | 4.0        | 4.1        | 40   | 与C距离<1m，将合并 |
| E      | 5.3        | 5.4        | 25   | 连续与F、G距离<1m，将合并 |
| F      | 5.5        | 5.6        | 35   | 连续与E、G距离<1m，将合并 |
| G      | 5.8        | 5.9        | 45   | 连续与F距离<1m，将合并 |

## 合并后缺陷情况

| 缺陷 | 起始位置(m) | 结束位置(m) | 中心位置(m) | 长度(m) | 分值 | 分类 |
|------|------------|------------|------------|--------|------|------|
| A    | 0.0        | 0.1        | 0.05       | 0.1    | 10   | >1.5m |
| B    | 1.9        | 2.0        | 1.95       | 0.1    | 20   | >1.5m |
| CD   | 3.3        | 4.1        | 3.70       | 0.8    | 100  | >1.5m |
| EFG  | 5.3        | 5.9        | 5.60       | 0.6    | 165  | >1.5m |

## 管段属性参数

- 管段长度: 10.0米
- 管道直径: 800毫米 (重要性参数E=3)
- 管道类型: 污水管
- 管道材质: 混凝土管
- 地区类别: 所有其他区域 (K=0)
- 土质类型: 一般土层 (T=0)

## 缺陷合并过程详解

### 1. CD合并过程
- C和D中心点距离为0.7m < 1m，符合合并条件
- 合并后起始位置: 3.3m（C的起始位置）
- 合并后结束位置: 4.1m（D的结束位置）
- 合并后长度: 0.8m（4.1m - 3.3m）
- 合并后分值: 100 = 30(C) + 40(D) + 30(交互得分)

### 2. EFG合并过程
- E和F中心点距离为0.2m < 1m，先合并成EF
- EF和G中心点距离为0.3m < 1m，继续合并成EFG
- 成功实现了多点连续合并
- 合并后起始位置: 5.3m（E的起始位置）
- 合并后结束位置: 5.9m（G的结束位置）
- 合并后长度: 0.6m（5.9m - 5.3m）
- 合并后分值: 165 = 25(E) + 35(F) + 45(G) + 60(交互得分)

## 参数计算详细过程

### 1. S值计算 (管段损坏状况参数)
```
S = (ΣPi1 + αΣPi2) / n
  = (10+20+100+165 + 1.1×0) / 4
  = 295 / 4
  = 73.75
```

### 2. F值计算 (结构性缺陷参数)
```
F = max(Smax, S)
  = max(45, 73.75)
  = 73.75
```

### 3. Sm值计算 (结构性缺陷密度)
```
Sm = (ΣPi1Li1 + αΣPi2Li2) / (S×L)
  = (10×0.1 + 20×0.1 + 100×0.8 + 165×0.6) / (73.75×10)
  = (1 + 2 + 80 + 99) / 737.5
  = 182 / 737.5
  = 0.2468
```

### 4. RI值计算 (修复指数)
```
RI = 0.7×F + 0.1×K + 0.05×E + 0.15×T
  = 0.7×73.75 + 0.1×0 + 0.05×3 + 0.15×0
  = 51.625 + 0 + 0.15 + 0
  = 51.77
```

### 5. 修复建议计算
根据models.py中的修复建议逻辑：
```
if RI <= 1:
    return "不修复"
elif 1 < RI <= 4:
    if F <= 3:
        return "不修复"
    elif F > 3:
        if Sm < 0.1:
            return "局部修复"
        else:
            return "整体修复"
else:  # RI > 4
    if Sm < 0.1:
        return "局部修复"
    else:
        return "整体修复"
```

由于本例中：
- RI = 51.77 > 4 (满足第三个条件)
- Sm = 0.2468 >= 0.1 (满足整体修复条件)

因此，修复建议为：**整体修复**

## 计算结果总结

### 关键参数值

| 参数 | 数值 | 含义 | 判定标准 |
|------|------|------|----------|
| S    | 73.75 | 管段损坏状况参数 | 较高 |
| F    | 73.75 | 结构性缺陷参数 | 较高 |
| Sm   | 0.2468 | 结构性缺陷密度 | 大于0.1 |
| K    | 0 | 地区类别值 | 所有其他区域 |
| E    | 3 | 管道重要性参数 | 中等重要性(600≤直径≤1000) |
| T    | 0 | 土质影响参数 | 一般土层 |
| RI   | 51.77 | 修复指数 | 远大于4 |
| 修复建议 | 整体修复 | 基于RI和Sm值的修复决策 | RI>4且Sm≥0.1 |
'''