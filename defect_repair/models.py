# defect_repair/models.py
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal


class PipeSection(models.Model):
    """管段信息模型"""
    # 工点名称：用户可自行输入任何文字
    work_point_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='工点名称')
    
    # 管段长度：用户可输入0-200之间可保留两位小数的数字（单位米）
    pipe_length = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='管段长度（米）',
                                     validators=[MinValueValidator(0), MaxValueValidator(200)])
    
    # 起始井号（均为用户输入字符格式）
    start_well_number = models.CharField(max_length=50, verbose_name='起始井号')
    
    # 终止井号（均为用户输入字符格式）
    end_well_number = models.CharField(max_length=50, verbose_name='终止井号')
    
    # 管道类型：可选择雨水管和污水管两种类型
    PIPE_TYPE_CHOICES = [
        ('雨水管', '雨水管'),
        ('污水管', '污水管'),
    ]
    pipe_type = models.CharField(max_length=10, choices=PIPE_TYPE_CHOICES, verbose_name='管道类型')
    
    # 管段材质：可选择塑料管、混凝土管2种
    PIPE_MATERIAL_CHOICES = [
        ('塑料管', '塑料管'),
        ('混凝土管', '混凝土管'),
    ]
    pipe_material = models.CharField(max_length=10, choices=PIPE_MATERIAL_CHOICES, verbose_name='管段材质')
    
    # 起点埋深、终点埋深：用户输入0-5之间可保留两位小数的数字（单位米）
    start_depth = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='起点埋深（米）',
                                     validators=[MinValueValidator(0), MaxValueValidator(5)])
    end_depth = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='终点埋深（米）',
                                   validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    # 管段直径：用户可输入0-2000之间可保留两位小数的数字（单位毫米）
    pipe_diameter = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='管段直径（毫米）',
                                       validators=[MinValueValidator(0), MaxValueValidator(2000)])
    
    # 地区类别K值
    AREA_TYPE_CHOICES = [
        ('中心商业、附近具有甲类民用建筑工程的区域', '中心商业、附近具有甲类民用建筑工程的区域'),
        ('交通干道、附近具有乙类民用建筑工程的区域', '交通干道、附近具有乙类民用建筑工程的区域'),
        ('其他行车道路、附近具有丙类民用建筑工程的区域', '其他行车道路、附近具有丙类民用建筑工程的区域'),
        ('所有其他区域', '所有其他区域'),
    ]
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES, verbose_name='地区类别')
    
    # 土质影响参数T及相关子选项
    SOIL_TYPE_CHOICES = [
        ('一般土层', '一般土层'),
        ('粉砂层', '粉砂层'),
        ('湿陷性黄土', '湿陷性黄土'),
        ('膨胀土', '膨胀土'),
        ('淤泥类土', '淤泥类土'),
        ('红粘土', '红粘土'),
    ]
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES, verbose_name='土质影响参数')
    
    # 湿陷性黄土等级
    WET_LOESS_LEVEL_CHOICES = [
        ('Ⅰ', 'Ⅰ'),
        ('Ⅱ', 'Ⅱ'),
        ('Ⅲ', 'Ⅲ'),
        ('Ⅳ', 'Ⅳ'),
    ]
    wet_loess_level = models.CharField(max_length=5, choices=WET_LOESS_LEVEL_CHOICES,
                                      null=True, blank=True,
                                      verbose_name='湿陷性黄土等级')
    
    # 膨胀土等级
    EXPANSIVE_SOIL_LEVEL_CHOICES = [
        ('强', '强'),
        ('中', '中'),
        ('弱', '弱'),
    ]
    expansive_soil_level = models.CharField(max_length=5, choices=EXPANSIVE_SOIL_LEVEL_CHOICES,
                                           null=True, blank=True,
                                           verbose_name='膨胀土等级')
    
    # 淤泥类土类型
    SILT_TYPE_CHOICES = [
        ('淤泥', '淤泥'),
        ('淤泥质土', '淤泥质土'),
    ]
    silt_type = models.CharField(max_length=10, choices=SILT_TYPE_CHOICES,
                                null=True, blank=True,
                                verbose_name='淤泥类土类型')
    
    # 其他计算字段（保留现有功能）
    # 管段缺陷密度
    defect_density = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='管段缺陷密度',
                                        validators=[MinValueValidator(0), MaxValueValidator(1)],
                                        default=0)
    
    # 新增字段：结构性缺陷参数F值
    F_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='结构性缺陷参数F值',
                                 validators=[MinValueValidator(0)],
                                 default=0)
    
    # 新增字段：结构性缺陷密度Sm值
    Sm_value = models.DecimalField(max_digits=5, decimal_places=4, verbose_name='结构性缺陷密度Sm值',
                                  validators=[MinValueValidator(0)],
                                  default=0)
    
    # 新增字段：修复指数RI值
    RI_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='修复指数RI值',
                                 validators=[MinValueValidator(0)],
                                 default=0)
    
    def __str__(self):
        return f"{self.work_point_name or '未命名'}-{self.start_well_number}-{self.end_well_number}"
    
    # # 新增方法获取地区类别对应的K值
    # def get_area_value_K(self):
    #     area_type_mapping = {
    #         '中心商业、附近具有甲类民用建筑工程的区域': 10,
    #         '交通干道、附近具有乙类民用建筑工程的区域': 6,
    #         '其他行车道路、附近具有丙类民用建筑工程的区域': 3,
    #         '所有其他区域': 0
    #     }
    #     return area_type_mapping.get(self.area_type, 0)
    
    # 计算管道重要性参数E
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

    # 新增方法获取地区类别对应的K值
    def get_area_value_K(self):
        area_type_mapping = {
            '中心商业、附近具有甲类民用建筑工程的区域': 10,
            '交通干道、附近具有乙类民用建筑工程的区域': 6,
            '其他行车道路、附近具有丙类民用建筑工程的区域': 3,
            '所有其他区域': 0
        }
        return area_type_mapping.get(self.area_type, 0)
    
    # 获取土质影响参数T值
    def get_soil_parameter_T(self):
        if self.soil_type == '一般土层':
            return 0
        elif self.soil_type == '粉砂层':
            return 10
        elif self.soil_type == '湿陷性黄土':
            if self.wet_loess_level in ['Ⅰ', 'Ⅱ']:
                return 6
            elif self.wet_loess_level == 'Ⅲ':
                return 8
            elif self.wet_loess_level == 'Ⅳ':
                return 10
        elif self.soil_type == '膨胀土':
            if self.expansive_soil_level == '强':
                return 10
            elif self.expansive_soil_level == '中':
                return 8
            elif self.expansive_soil_level == '弱':
                return 6
        elif self.soil_type == '淤泥类土':
            if self.silt_type == '淤泥':
                return 10
            elif self.silt_type == '淤泥质土':
                return 8
        elif self.soil_type == '红粘土':
            return 8
        return 0
    
    # 合并并分类缺陷的辅助函数
    def merge_and_classify_defects(self):
        """
        合并中心点距离小于1m的缺陷，并将缺陷分类为不同纵向净距的组
        
        返回值:
        - merged_defects: 已合并1m内缺陷，重新输出的经过整合的缺陷列表
        - defects_1_5m_plus: 纵向净距大于1.5m的缺陷列表
        - defects_1_0m_to_1_5m: 纵向净距在1.0-1.5m之间的缺陷列表
        """
        # 获取管段中所有缺陷
        all_defects = self.defects.all()
        
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
        
        # 第一步：合并相邻中心点距离小于1m的缺陷
        # 使用迭代方法，直到没有可以合并的缺陷为止
        merged_defects = defects_with_center.copy()
        merged = True
        
        while merged:
            merged = False
            new_merged = []
            i = 0
            
            while i < len(merged_defects):
                # 开始一个新的合并组
                current_group = [merged_defects[i]]
                current_start = merged_defects[i]['start']
                current_end = merged_defects[i]['end']
                current_score = merged_defects[i]['score']
                
                # 尝试合并后续所有可以合并的缺陷
                j = i + 1
                while j < len(merged_defects):
                    # 计算当前组最后一个缺陷与下一个缺陷的中心点距离
                    # 注意：这里不是j和j-1的距离，而是当前组最后一个和下一个的距离
                    last_defect_in_group = current_group[-1]
                    next_defect = merged_defects[j]
                    distance = next_defect['center'] - last_defect_in_group['center']
                    
                    if distance < 1.0:
                        # 需要合并
                        current_group.append(next_defect)
                        current_end = next_defect['end']
                        current_score += next_defect['score']
                        merged = True
                        j += 1
                    else:
                        break
                
                # 如果只合并了一个缺陷，直接添加
                if len(current_group) == 1:
                    new_merged.append(current_group[0])
                else:
                    # 计算合并后缺陷的中心点和长度
                    merged_center = (current_start + current_end) / 2
                    merged_length = current_end - current_start
                    
                    # 添加合并后的缺陷
                    new_merged.append({
                        'start': current_start,
                        'end': current_end,
                        'center': merged_center,
                        'length': merged_length,
                        'score': current_score
                    })
                
                # 更新i，跳过已合并的缺陷
                i = j
            
            # 更新merged_defects为新的合并结果
            merged_defects = new_merged
        
        # 第二步：根据合并后缺陷之间的距离分类
        defects_1_5m_plus = []  # 纵向净距大于1.5m的缺陷
        defects_1_0m_to_1_5m = []  # 纵向净距在1.0-1.5m之间的缺陷
        
        # 检查合并后的缺陷之间的距离
        for i in range(len(merged_defects)):
            current_defect = merged_defects[i]
            
            # 检查当前缺陷是否应该被分类为defects_1_5m_plus
            is_1_5m_plus = False
            
            # 检查与前一个缺陷的距离（如果有）
            if i > 0:
                prev_defect = merged_defects[i-1]
                distance = current_defect['center'] - prev_defect['center']
                if distance > 1.5:
                    is_1_5m_plus = True
                    # 前一个缺陷也应该被分类为defects_1_5m_plus
                    if prev_defect not in defects_1_5m_plus:
                        defects_1_5m_plus.append(prev_defect)
            
            # 检查与后一个缺陷的距离（如果有）
            if i < len(merged_defects) - 1:
                next_defect = merged_defects[i+1]
                distance = next_defect['center'] - current_defect['center']
                if distance > 1.5:
                    is_1_5m_plus = True
            
            # 根据检查结果分类
            if is_1_5m_plus:
                if current_defect not in defects_1_5m_plus:
                    defects_1_5m_plus.append(current_defect)
            else:
                if current_defect not in defects_1_0m_to_1_5m:
                    defects_1_0m_to_1_5m.append(current_defect)
        
        # 确保所有缺陷都被分类
        # 检查是否有缺陷既不在defects_1_5m_plus也不在defects_1_0m_to_1_5m中
        for defect in merged_defects:
            if defect not in defects_1_5m_plus and defect not in defects_1_0m_to_1_5m:
                # 默认归类到defects_1_0m_to_1_5m
                defects_1_0m_to_1_5m.append(defect)
        
        return merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m
    
    # 计算管段损坏状况参数S
    def calculate_S(self):
        # 根据公式：S = 1/n × (Σ P_i1 + α Σ P_i2)
        print(f"=== 计算管段 {self.id} 的S值 ===")
        # 获取合并并分类后的缺陷列表
        merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m = self.merge_and_classify_defects()
        
        print(f"合并后的缺陷数量: {len(merged_defects)}")
        print(f"纵向净距>1.5m的缺陷数量: {len(defects_1_5m_plus)}")
        print(f"纵向净距1.0-1.5m的缺陷数量: {len(defects_1_0m_to_1_5m)}")
        
        # 计算总缺陷数量
        n = len(merged_defects)
        n1 = len(defects_1_5m_plus)
        n2 = n - n1
        
        # 计算各类缺陷的分值之和
        sum_Pi1 = sum(defect['score'] for defect in defects_1_5m_plus)
        sum_Pi2 = sum(defect['score'] for defect in defects_1_0m_to_1_5m)
        
        print(f"sum_Pi1 (纵向净距>1.5m缺陷分值总和): {sum_Pi1}")
        print(f"sum_Pi2 (纵向净距1.0-1.5m缺陷分值总和): {sum_Pi2}")
        
        # 结构性缺陷影响系数
        alpha = 1.1  # 纵向净距大于1.0m且不大于1.5m时
        print(f"影响系数alpha: {alpha}")
        
        # 计算S值
        if n > 0:
            S = (sum_Pi1 + alpha * sum_Pi2) / n
            print(f"计算得到的S值: {S}")
            return S
        else:
            print("无缺陷，S值为0")
            return 0
    
    # 计算结构性缺陷参数F
    def calculate_F(self):
        # 根据文档要求：当Smax ≥ S时，F = Smax；当Smax < S时，F = S
        # 获取当前管段的所有缺陷
        all_defects = self.defects.all()
        
        if not all_defects:
            return 0
        
        # 计算S值
        S = self.calculate_S()
        
        # 计算Smax值（所有缺陷的最大分值）
        scores = [defect.get_defect_score() for defect in all_defects]
        Smax = max(scores) if scores else 0
        
        print(f"=== 计算管段 {self.id} 的F值 ===")
        print(f"S值: {S}, Smax值: {Smax}")
        
        # 根据条件返回F值
        if Smax >= S:
            print(f"Smax >= S，F值取Smax: {Smax}")
            return Smax
        else:
            print(f"Smax < S，F值取S: {S}")
            return S
    
    # 计算结构性缺陷密度Sm
    def calculate_Sm(self):
        # 根据公式：S_M = 1/(SL) × (Σ P_i1 L_i1 + α Σ P_i2 L_i2)
        print(f"=== 计算管段 {self.id} 的Sm值 ===")
        # 获取合并并分类后的缺陷列表
        merged_defects, defects_1_5m_plus, defects_1_0m_to_1_5m = self.merge_and_classify_defects()
        
        if not merged_defects:
            print("无缺陷，Sm值为0")
            return 0
        
        # 获取管段长度L
        L = float(self.pipe_length)
        print(f"管段长度L: {L}")
        
        if L <= 0:
            print("管段长度无效，Sm值为0")
            return 0
        
        # 计算S值，S是calculate_S函数的结果
        S = self.calculate_S()
        print(f"使用的S值: {S}")
        
        if S <= 0:
            print("S值无效，Sm值为0")
            return 0
        
        # 计算各类缺陷的分值×长度之和
        sum_Pi1_Li1 = sum(float(defect['score']) * float(defect['length']) for defect in defects_1_5m_plus)
        sum_Pi2_Li2 = sum(float(defect['score']) * float(defect['length']) for defect in defects_1_0m_to_1_5m)
        
        print(f"sum_Pi1_Li1 (纵向净距>1.5m缺陷分值×长度总和): {sum_Pi1_Li1}")
        print(f"sum_Pi2_Li2 (纵向净距1.0-1.5m缺陷分值×长度总和): {sum_Pi2_Li2}")
        
        # 结构性缺陷影响系数
        alpha = 1.1  # 纵向净距大于1.0m且不大于1.5m时
        print(f"影响系数alpha: {alpha}")
        
        # 计算Sm值，使用S*L作为分母，确保所有值都是float类型
        denominator = float(S) * L
        numerator = sum_Pi1_Li1 + alpha * sum_Pi2_Li2
        Sm = numerator / denominator
        
        print(f"分子: {numerator}, 分母: {denominator}")
        print(f"计算得到的Sm值: {Sm}")
        
        # 保留三位小数返回
        result = round(Sm, 3)
        print(f"保留三位小数后的Sm值: {result}")
        return result
    
    # 计算修复指数RI
    def calculate_RI(self):
        # 根据公式：RI=0.7×F+0.1×K+0.05×E+0.15×T
        F = self.calculate_F()
        K = self.get_area_value_K()
        E = self.calculate_E()
        T = self.get_soil_parameter_T()
        
        RI = 0.7 * F + 0.1 * K + 0.05 * E + 0.15 * T
        return RI
    
    # 新增方法：当管段信息更新时，更新该管段所有缺陷的修复建议
    def update_all_defect_suggestions(self):
        """更新当前管段所有结构性缺陷的修复建议
        
        当管段信息更新或添加新缺陷时，需要重新计算该管段所有缺陷的修复建议，
        因为修复建议依赖于管段的RI、Sm、F参数，这些参数会随着缺陷数量变化而变化。
        """
        # 计算并更新管段的F值、Sm值和RI值
        self.F_value = self.calculate_F()
        self.Sm_value = self.calculate_Sm()
        self.RI_value = self.calculate_RI()
        self.save(update_suggestions=False)  # 保存更新后的参数值，但不触发update_suggestions
        
        # 获取管段所有缺陷
        all_defects = defectinfo.objects.filter(pipe_section=self)
        
        # 遍历所有缺陷，更新它们的修复建议
        for defect in all_defects:
            # 获取或创建repairsuggestion实例，并调用其update方法
            repairsuggestion_obj, created = repairsuggestion.objects.get_or_create(defect_info=defect)
            repairsuggestion_obj.update()
            repairsuggestion_obj.save()  # 手动保存修复建议
    
    # 管段保存后更新关联的修复建议
    def save(self, *args, update_suggestions=True, **kwargs):
        super().save(*args, **kwargs)
        # 当管段信息更新时，更新该管段所有缺陷的修复建议
        if update_suggestions:
            self.update_all_defect_suggestions()


class defectinfo(models.Model):
    """缺陷信息模型"""
    # 关联到管段，一个管段可以有多个缺陷，一个缺陷只能属于一个管段
    pipe_section = models.ForeignKey(PipeSection, on_delete=models.CASCADE, related_name='defects', verbose_name='所属管段')
    
    # 缺陷信息部分
    # 缺陷名称：可选择破裂、渗漏、脱节、变形、错口、腐蚀、接口材料脱落、异物刺入、支管暗接、起伏共10种
    DEFECT_NAME_CHOICES = [
        ('破裂', '破裂'),
        ('渗漏', '渗漏'),
        ('脱节', '脱节'),
        ('变形', '变形'),
        ('错口', '错口'),
        ('腐蚀', '腐蚀'),
        ('接口材料脱落', '接口材料脱落'),
        ('异物刺入', '异物刺入'),
        ('支管暗接', '支管暗接'),
        ('起伏', '起伏'),
    ]
    defect_name = models.CharField(max_length=20, choices=DEFECT_NAME_CHOICES, verbose_name='缺陷名称')
    
    # 缺陷等级：可选择1级、2级、3级、4级共四种
    DEFECT_LEVEL_CHOICES = [
        ('1级', '1级'),
        ('2级', '2级'),
        ('3级', '3级'),
        ('4级', '4级'),
    ]
    defect_level = models.CharField(max_length=5, choices=DEFECT_LEVEL_CHOICES, verbose_name='缺陷等级')
    
    # 缺陷起始位置（米）
    defect_start_position_m = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='缺陷起始位置（米）',
                                                 validators=[MinValueValidator(0), MaxValueValidator(200)])
    
    # 缺陷终止位置（米）
    defect_end_position_m = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='缺陷终止位置（米）',
                                               validators=[MinValueValidator(0), MaxValueValidator(200)])
    
    # 缺陷起始位置（钟表法）
    defect_start_position_clock = models.IntegerField(
        verbose_name='缺陷起始位置（钟表法）',
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True, blank=True
    )
    
    # 缺陷终止位置（钟表法）
    defect_end_position_clock = models.IntegerField(
        verbose_name='缺陷终止位置（钟表法）',
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True, blank=True
    )
    
    # 其他计算字段
    # 管段结构性缺陷参数F
    structural_defect_parameter = models.DecimalField(max_digits=5, decimal_places=2,
                                                      verbose_name='管段结构性缺陷参数F',
                                                      validators=[MinValueValidator(0), MaxValueValidator(100)],
                                                      default=0)
    
    # 纵向净距大于1.5m的缺陷长度
    defect_length_over_1_5m = models.DecimalField(max_digits=5, decimal_places=2,
                                                 verbose_name='纵向净距大于1.5m的缺陷长度（米）',
                                                 validators=[MinValueValidator(0), MaxValueValidator(200)],
                                                 default=0)
    
    # 纵向净距在1 - 1.5m的缺陷长度
    defect_length_1_to_1_5m = models.DecimalField(max_digits=5, decimal_places=2,
                                                 verbose_name='纵向净距在1 - 1.5m的缺陷长度（米）',
                                                 validators=[MinValueValidator(0), MaxValueValidator(200)],
                                                 default=0)
    
    # 缺陷分值
    defect_score = models.DecimalField(max_digits=5, decimal_places=2,
                                      verbose_name='缺陷分值',
                                      validators=[MinValueValidator(0)],
                                      default=0)
    
    # 基本信息
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '缺陷信息'
        verbose_name_plural = '缺陷信息'

    # 获取缺陷分值
    def get_defect_score(self):
        # 根据表8.2.3中的分值进行计算
        defect_scores = {
            '破裂': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5,
                '4级': 10
            },
            '变形': {
                '1级': 1,
                '2级': 2,
                '3级': 5,
                '4级': 10
            },
            '腐蚀': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5
            },
            '错口': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5,
                '4级': 10
            },
            '起伏': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5,
                '4级': 10
            },
            '脱节': {
                '1级': 1,
                '2级': 3,
                '3级': 5,
                '4级': 10
            },
            '接口材料脱落': {
                '1级': 1,
                '2级': 3
            },
            '支管暗接': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5
            },
            '异物刺入': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5
            },
            '渗漏': {
                '1级': 0.5,
                '2级': 2,
                '3级': 5,
                '4级': 10
            }
        }

        try:
            return defect_scores[self.defect_name][self.defect_level]
        except KeyError:
            return 0

    # 根据计算结果给出修复建议
    def get_repair_suggestion(self):
        RI = self.pipe_section.calculate_RI()
        # 从管段级别获取F和Sm值
        F = self.pipe_section.calculate_F()
        Sm = self.pipe_section.calculate_Sm()
        
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
    


    def get_repair_measures(self):
        # 先获取总体修复建议
        repair_suggestion = self.get_repair_suggestion()
        
        # 如果建议不修复，则直接返回
        if repair_suggestion == "不修复":
            return "不修复"
        
        # 获取缺陷相关信息
        defect_name = self.defect_name
        defect_level = self.defect_level
        diameter = float(self.pipe_section.pipe_diameter)
        
        # 根据修复建议类型和表格实现具体修复措施
        # 局部修复措施
        if repair_suggestion == "局部修复":
            # 变形
            if defect_name == "变形":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "不作处理"
                    elif defect_level == "3级":
                        return "不作处理"
                    elif defect_level == "4级":
                        return "无"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢双胀环/不锈钢快速锁"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                    elif defect_level == "4级":
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
            
            # 错口
            elif defect_name == "错口":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化"
                    elif defect_level == "3级":
                        return "点状原位固化"
                    elif defect_level == "4级":
                        return "开挖修复"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢双胀环"
                    elif defect_level == "3级":
                        return "开挖修复"
                    elif defect_level == "4级":
                        return "开挖修复"
            
            # 腐蚀
            elif defect_name == "腐蚀":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "4级":
                        return "无"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "不锈钢快速锁/点状原位固化/不锈钢双胀环"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                    elif defect_level == "4级":
                        return "无"
            
            # 破裂
            elif defect_name == "破裂":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "4级":
                        return "点状原位固化/不锈钢快速锁"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "不锈钢快速锁/点状原位固化/不锈钢双胀环"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                    elif defect_level == "4级":
                        return "不锈钢快速锁/点状原位固化"
            
            # 渗漏
            elif defect_name == "渗漏":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化"
                    elif defect_level == "3级":
                        return "点状原位固化"
                    elif defect_level == "4级":
                        return "高聚物土体固化+不锈钢快速锁"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "点状原位固化"
                    elif defect_level == "3级":
                        return "点状原位固化"
                    elif defect_level == "4级":
                        return "高聚物土体固化+不锈钢快速锁"
            
            # 脱节
            elif defect_name == "脱节":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "3级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "4级":
                        return "点状原位固化/不锈钢快速锁"
                elif diameter >= 800:
                    if defect_level in ["2级", "3级", "4级"]:
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
            
            # 接口材料脱落
            elif defect_name == "接口材料脱落":
                if 300 <= diameter < 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢快速锁"
                    elif defect_level == "3级":
                        return "无"
                    elif defect_level == "4级":
                        return "无"
                elif diameter >= 800:
                    if defect_level == "2级":
                        return "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                    elif defect_level == "3级":
                        return "无"
                    elif defect_level == "4级":
                        return "无"
        
        # 整体修复措施
        elif repair_suggestion == "整体修复":
            # 变形
            if defect_name == "变形":
                if 300 <= diameter < 800:
                    return "翻转式原位固化/紫外光原位固化/短管内衬/热塑成型法"
                elif diameter >= 800:
                    return "翻转式原位固化/紫外光原位固化"
            
            # 错口
            elif defect_name == "错口":
                if 300 <= diameter < 800:
                    return "翻转式原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                elif diameter >= 800:
                    return "无"
            
            # 腐蚀
            elif defect_name == "腐蚀":
                if 300 <= diameter < 800:
                    return "翻转式原位固化/紫外光原位固化/垫衬法/热塑成型法"
                elif diameter >= 800:
                    return "水泥基材料喷筑/翻转式原位固化/紫外光原位固化/垫衬法"
            
            # 破裂
            elif defect_name == "破裂":
                if 300 <= diameter < 800:
                    return "翻转式原位固化/紫外光原位固化/垫衬法/热塑成型法"
                elif diameter >= 800:
                    return "水泥基材料喷筑/高分子材料喷涂/翻转式原位固化/紫外光原位固化/垫衬法"
            
            # 渗漏
            elif defect_name == "渗漏":
                if 300 <= diameter < 800:
                    return "热水原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                elif diameter >= 800:
                    return "热水原位固化/紫外光原位固化/垫衬法"
            
            # 脱节
            elif defect_name == "脱节":
                if 300 <= diameter < 800:
                    return "热水原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                elif diameter >= 800:
                    return "热水原位固化/紫外光原位固化/垫衬法/水泥基材料喷筑/高分子材料喷涂"
            
            # 接口材料脱落
            elif defect_name == "接口材料脱落":
                if 300 <= diameter < 800:
                    return "热水原位固化/紫外光原位固化/垫衬法/热塑成型法"
                elif diameter >= 800:
                    return "热水原位固化/紫外光原位固化/垫衬法/水泥基材料喷筑/高分子材料喷涂"
        
        # 默认情况
        return "请人工确认修复措施"

    # 数据验证方法
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # 确保缺陷起始位置和终止位置在管段长度范围内
        if self.defect_start_position_m > self.pipe_section.pipe_length:
            raise ValidationError('缺陷起始位置不能超过管段长度')
        if self.defect_end_position_m > self.pipe_section.pipe_length:
            raise ValidationError('缺陷终止位置不能超过管段长度')
        # 确保起始位置不大于终止位置
        if self.defect_start_position_m > self.defect_end_position_m:
            raise ValidationError('缺陷起始位置不能大于终止位置')

    # 新增方法：更新修复建议
    def update_repair_suggestion(self):
        """更新当前缺陷的修复建议
        
        调用repairsuggestion模型的update方法，该方法会同时考虑：
        1. 管段的RI、Sm、F参数
        2. 当前缺陷的具体等级、所在管径
        """
        # 重新计算F值
        self.structural_defect_parameter = self.pipe_section.calculate_F()
        self.save()  # 保存更新后的F值
        
        # 获取或创建repairsuggestion实例，并调用其update方法
        repairsuggestion_obj, created = repairsuggestion.objects.get_or_create(defect_info=self)
        repairsuggestion_obj.update()
    
    def save(self, *args, **kwargs):
        # 保存前先验证数据
        self.clean()
        # 保存前计算F值
        self.structural_defect_parameter = self.pipe_section.calculate_F()
        self.defect_score = self.get_defect_score()
        super().save(*args, **kwargs)

        # 更新管段的缺陷密度
        from django.db.models import Sum
        all_defects = defectinfo.objects.filter(pipe_section=self.pipe_section)
        total_defect_score = all_defects.aggregate(Sum('defect_score'))['defect_score__sum'] or 0
        self.pipe_section.defect_density = total_defect_score / self.pipe_section.pipe_length if self.pipe_section.pipe_length > 0 else 0
        self.pipe_section.save()

        # 重要修改：更新该管段所有缺陷的修复建议，确保整体对齐
        self.pipe_section.update_all_defect_suggestions()

    def __str__(self):
        return f"{self.pipe_section.work_point_name or '未命名'}-{self.defect_name}-{self.defect_level}"


class repairsuggestion(models.Model):
    defect_info = models.OneToOneField(defectinfo, on_delete=models.CASCADE)
    repair_suggestion = models.TextField()
    repair_measures = models.TextField()

    def update(self):
        """更新修复建议和修复措施
        
        同时考虑两个因素：
        1. 管段的RI、Sm、F参数（决定不修复/局部修复/整体修复）
        2. 当前缺陷的具体等级、所在管径（决定具体修复措施）
        """
        # 初始化变量，确保在所有代码路径中都有值
        suggestion_text = "请人工确认修复建议"
        measures_text = "请人工确认修复措施"
        
        # 获取管段参数
        pipe_section = self.defect_info.pipe_section
        RI = pipe_section.calculate_RI()
        F = pipe_section.calculate_F()
        Sm = pipe_section.calculate_Sm()
        
        # 根据图1的规则计算修复建议
        if RI <= 1:
            suggestion_text = "不修复"
        elif 1 < RI <= 4:
            if F <= 3:
                suggestion_text = "不修复"
            elif F > 3:
                if Sm < 0.1:
                    suggestion_text = "局部修复"
                else:  # Sm >= 0.1
                    suggestion_text = "整体修复"
        else:  # RI > 4
            if Sm < 0.1:
                suggestion_text = "局部修复"
            else:  # Sm >= 0.1
                suggestion_text = "整体修复"
        
        # 如果建议不修复，则直接使用不修复
        if suggestion_text == "不修复":
            measures_text = "不修复"
        else:
            # 获取缺陷相关信息计算具体修复措施
            defect_name = self.defect_info.defect_name
            defect_level = self.defect_info.defect_level
            diameter = float(pipe_section.pipe_diameter)
            
            # 根据修复建议类型和表格实现具体修复措施
            # 局部修复措施
            if suggestion_text == "局部修复":
                # 变形
                if defect_name == "变形":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "不作处理"
                        elif defect_level == "3级":
                            measures_text = "不作处理"
                        elif defect_level == "4级":
                            measures_text = "无"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢双胀环/不锈钢快速锁"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                        elif defect_level == "4级":
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                
                # 错口
                elif defect_name == "错口":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化"
                        elif defect_level == "4级":
                            measures_text = "开挖修复"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢双胀环"
                        elif defect_level == "3级":
                            measures_text = "开挖修复"
                        elif defect_level == "4级":
                            measures_text = "开挖修复"
                
                # 腐蚀
                elif defect_name == "腐蚀":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "4级":
                            measures_text = "无"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "不锈钢快速锁/点状原位固化/不锈钢双胀环"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                        elif defect_level == "4级":
                            measures_text = "无"
                
                # 破裂
                elif defect_name == "破裂":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "4级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "不锈钢快速锁/点状原位固化/不锈钢双胀环"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                        elif defect_level == "4级":
                            measures_text = "不锈钢快速锁/点状原位固化"
                
                # 渗漏
                elif defect_name == "渗漏":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化"
                        elif defect_level == "4级":
                            measures_text = "高聚物土体固化+不锈钢快速锁"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化"
                        elif defect_level == "4级":
                            measures_text = "高聚物土体固化+不锈钢快速锁"
                
                # 脱节
                elif defect_name == "脱节":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "3级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "4级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                    elif diameter >= 800:
                        if defect_level in ["2级", "3级", "4级"]:
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                
                # 接口材料脱落
                elif defect_name == "接口材料脱落":
                    if 300 <= diameter < 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢快速锁"
                        elif defect_level == "3级":
                            measures_text = "无"
                        elif defect_level == "4级":
                            measures_text = "无"
                    elif diameter >= 800:
                        if defect_level == "2级":
                            measures_text = "点状原位固化/不锈钢快速锁/不锈钢双胀环"
                        elif defect_level == "3级":
                            measures_text = "无"
                        elif defect_level == "4级":
                            measures_text = "无"
                
                # 其他缺陷类型
                else:
                    measures_text = "请人工确认修复措施"
            
            # 整体修复措施
            elif suggestion_text == "整体修复":
                # 变形
                if defect_name == "变形":
                    if 300 <= diameter < 800:
                        measures_text = "翻转式原位固化/紫外光原位固化/短管内衬/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "翻转式原位固化/紫外光原位固化"
                
                # 错口
                elif defect_name == "错口":
                    if 300 <= diameter < 800:
                        measures_text = "翻转式原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "无"
                
                # 腐蚀
                elif defect_name == "腐蚀":
                    if 300 <= diameter < 800:
                        measures_text = "翻转式原位固化/紫外光原位固化/垫衬法/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "水泥基材料喷筑/翻转式原位固化/紫外光原位固化/垫衬法"
                
                # 破裂
                elif defect_name == "破裂":
                    if 300 <= diameter < 800:
                        measures_text = "翻转式原位固化/紫外光原位固化/垫衬法/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "水泥基材料喷筑/高分子材料喷涂/翻转式原位固化/紫外光原位固化/垫衬法"
                
                # 渗漏
                elif defect_name == "渗漏":
                    if 300 <= diameter < 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法"
                
                # 脱节
                elif defect_name == "脱节":
                    if 300 <= diameter < 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法/短管内衬/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法/水泥基材料喷筑/高分子材料喷涂"
                
                # 接口材料脱落
                elif defect_name == "接口材料脱落":
                    if 300 <= diameter < 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法/热塑成型法"
                    elif diameter >= 800:
                        measures_text = "热水原位固化/紫外光原位固化/垫衬法/水泥基材料喷筑/高分子材料喷涂"
                
                # 其他缺陷类型
                else:
                    measures_text = "请人工确认修复措施"
            
            # 默认情况
            else:
                measures_text = "请人工确认修复措施"
        
        # 更新字段
        self.repair_suggestion = suggestion_text
        self.repair_measures = measures_text
        # 注意：不再在这里调用self.save()，由调用方负责保存

    def __str__(self):
        return f"{self.defect_info}-{self.repair_suggestion}"
