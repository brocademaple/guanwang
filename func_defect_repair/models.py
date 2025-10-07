from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class FuncPipeSection(models.Model):
    """功能性缺陷的管段信息模型"""
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
    
    # 计算E值：根据管段直径计算
    def calculate_E(self):
        diameter = float(self.pipe_diameter)
        if diameter < 600:
            return 0
        elif 600 <= diameter <= 1000:
            return 3
        elif 1000 < diameter <= 1500:
            return 6
        else:  # diameter > 1500
            return 10
    
    def __str__(self):
        return f"{self.work_point_name or '未命名'}-{self.start_well_number}-{self.end_well_number}"


class funcdefectinfo(models.Model):
    """功能性缺陷信息模型"""
    # 关联到管段，一个管段可以有多个缺陷，一个缺陷只能属于一个管段
    pipe_section = models.ForeignKey(FuncPipeSection, on_delete=models.CASCADE, related_name='func_defects', verbose_name='所属管段', null=True, blank=True)
    
    # 缺陷信息部分
    # 缺陷名称：可选择沉积、结垢、树根、障碍物、残墙坝根、浮渣6种
    DEFECT_NAME_CHOICES = [
        ('沉积', '沉积(CJ)'),
        ('结垢', '结垢(JG)'),
        ('树根', '树根(SG)'),
        ('障碍物', '障碍物(ZW)'),
        ('残墙坝根', '残墙坝根(CQ)'),
        ('浮渣', '浮渣(FZ)')
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
    
    # 验证缺陷位置是否在管段长度范围内
    def clean(self):
        super().clean()
        # 检查起始位置是否小于等于终止位置
        if self.defect_start_position_m > self.defect_end_position_m:
            raise ValidationError('缺陷起始位置不能大于缺陷终止位置')
        
        # 检查缺陷位置是否在管段长度范围内
        if self.pipe_section and (
            self.defect_start_position_m > self.pipe_section.pipe_length or
            self.defect_end_position_m > self.pipe_section.pipe_length
        ):
            raise ValidationError('缺陷位置不能超过管段长度')
    
    # 自动生成修复建议
    def get_repair_suggestion(self):
        if not self.pipe_section:
            return "请先选择管段"
        
        d = float(self.pipe_section.pipe_diameter)
        name = self.defect_name
        level = self.defect_level
        
        # 根据图片内容和补充信息实现修复建议逻辑
        if name in ['沉积', '结垢']:
            if d < 400:
                return "高压水射流管道清淤+绞车疏通辅助"
            elif 400 <= d <= 600:
                return "高压水射流管道清淤+绞车疏通辅助"
            else:
                return "高压水射流管道清淤+人工清除辅助"
        elif name == '树根':
            if level == "1级" or level == "2级":
                return "机器人切割"
            elif level == "3级" or level == "4级":
                return "加井或翻建"
            else:
                return "请人工判定"
        elif name == '障碍物':
            return "机器人清通"
        elif name == '残墙坝根':
            return "机器人清通"
        elif name == '浮渣':
            return "高压水射流管道清淤+绞车疏通辅助"
        else:
            return "请人工判定"
    
    def save(self, *args, **kwargs):
        # 调用clean方法进行验证
        self.clean()
        super().save(*args, **kwargs)
        
        # 自动生成修复建议
        suggestion, created = funcrepairsuggestion.objects.get_or_create(defect_info=self)
        suggestion.repair_suggestion = self.get_repair_suggestion()
        suggestion.save()
    
    def __str__(self):
        if self.pipe_section:
            return f"{self.pipe_section.work_point_name or '未命名'}-{self.defect_name}-{self.defect_level}"
        return f"未关联管段-{self.defect_name}-{self.defect_level}"


class funcrepairsuggestion(models.Model):
    """功能性缺陷修复建议模型"""
    defect_info = models.OneToOneField(funcdefectinfo, on_delete=models.CASCADE)
    repair_suggestion = models.TextField()
    
    def __str__(self):
        return f"{self.defect_info}-{self.repair_suggestion[:20]}..."