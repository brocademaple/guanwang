from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class defectinfo(models.Model):
    work_point_name = models.CharField(max_length=100, blank=True, null=True,
                                       verbose_name='工点名称')
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
    defect_name = models.CharField(max_length=20, choices=DEFECT_NAME_CHOICES,
                                   verbose_name='缺陷名称')
    DEFECT_LEVEL_CHOICES = [
        ('1级', '1级'),
        ('2级', '2级'),
        ('3级', '3级'),
        ('4级', '4级'),
    ]
    defect_level = models.CharField(max_length=5, choices=DEFECT_LEVEL_CHOICES,
                                    verbose_name='缺陷等级')
    pipe_length = models.DecimalField(max_digits=5, decimal_places=2,
                                      verbose_name='管段长度（米）',
                                      validators=[MinValueValidator(0), MaxValueValidator(200)])
    start_well_number = models.CharField(max_length=50, verbose_name='起始井号')
    end_well_number = models.CharField(max_length=50, verbose_name='终止井号')
    defect_start_position_m = models.DecimalField(max_digits=5, decimal_places=2,
                                                  verbose_name='缺陷起始位置（米）',
                                                  validators=[MinValueValidator(0), MaxValueValidator(200)])
    defect_end_position_m = models.DecimalField(max_digits=5, decimal_places=2,
                                                verbose_name='缺陷终止位置（米）',
                                                validators=[MinValueValidator(0), MaxValueValidator(200)])
    defect_start_position_clock = models.IntegerField(
        verbose_name='缺陷起始位置（钟表法）',
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True, blank=True
    )
    defect_end_position_clock = models.IntegerField(
        verbose_name='缺陷终止位置（钟表法）',
        validators=[MinValueValidator(0), MaxValueValidator(12)],
        null=True, blank=True
    )
    PIPE_TYPE_CHOICES = [
        ('雨水管', '雨水管'),
        ('污水管', '污水管'),
    ]
    pipe_type = models.CharField(max_length=10, choices=PIPE_TYPE_CHOICES,
                                 verbose_name='管道类型')
    PIPE_MATERIAL_CHOICES = [
        ('塑料管', '塑料管'),
        ('混凝土管', '混凝土管'),
    ]
    pipe_material = models.CharField(max_length=10, choices=PIPE_MATERIAL_CHOICES,
                                     verbose_name='管段材质')
    start_depth = models.DecimalField(max_digits=3, decimal_places=2,
                                      verbose_name='起点埋深（米）',
                                      validators=[MinValueValidator(0), MaxValueValidator(5)])
    end_depth = models.DecimalField(max_digits=3, decimal_places=2,
                                    verbose_name='终点埋深（米）',
                                    validators=[MinValueValidator(0), MaxValueValidator(5)])
    pipe_diameter = models.DecimalField(max_digits=6, decimal_places=2,
                                        verbose_name='管段直径（毫米）',
                                        validators=[MinValueValidator(0), MaxValueValidator(2000)])
    AREA_TYPE_CHOICES = [
        ('中心商业、附近具有甲类民用建筑工程的区域', '中心商业、附近具有甲类民用建筑工程的区域'),
        ('交通干道、附近具有乙类民用建筑工程的区域', '交通干道、附近具有乙类民用建筑工程的区域'),
        ('其他行车道路、附近具有丙类民用建筑工程的区域', '其他行车道路、附近具有丙类民用建筑工程的区域'),
        ('所有其他区域', '所有其他区域'),
    ]
    area_type = models.CharField(max_length=50, choices=AREA_TYPE_CHOICES,
                                 verbose_name='地区类别')
    structural_defect_parameter = models.DecimalField(max_digits=3, decimal_places=2,
                                                      verbose_name='管段结构性缺陷参数',
                                                      validators=[MinValueValidator(0), MaxValueValidator(10)])
    defect_density = models.DecimalField(max_digits=5, decimal_places=4,
                                         verbose_name='管段缺陷密度',
                                         validators=[MinValueValidator(0), MaxValueValidator(1)])
    SOIL_TYPE_CHOICES = [
        ('一般土层', '一般土层'),
        ('粉砂层', '粉砂层'),
        ('湿陷性黄土', '湿陷性黄土'),
        ('膨胀土', '膨胀土'),
        ('淤泥类土', '淤泥类土'),
        ('红粘土', '红粘土'),
    ]
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPE_CHOICES,
                                 verbose_name='土质影响参数')
    WET_LOESS_LEVEL_CHOICES = [
        ('Ⅰ', 'Ⅰ'),
        ('Ⅱ', 'Ⅱ'),
        ('Ⅲ', 'Ⅲ'),
        ('Ⅳ', 'Ⅳ'),
    ]
    wet_loess_level = models.CharField(max_length=5, choices=WET_LOESS_LEVEL_CHOICES,
                                       null=True, blank=True,
                                       verbose_name='湿陷性黄土等级')
    EXPANSIVE_SOIL_LEVEL_CHOICES = [
        ('强', '强'),
        ('中', '中'),
        ('弱', '弱'),
    ]
    expansive_soil_level = models.CharField(max_length=5, choices=EXPANSIVE_SOIL_LEVEL_CHOICES,
                                            null=True, blank=True,
                                            verbose_name='膨胀土等级')
    SILT_TYPE_CHOICES = [
        ('淤泥', '淤泥'),
        ('淤泥质土', '淤泥质土'),
    ]
    silt_type = models.CharField(max_length=10, choices=SILT_TYPE_CHOICES,
                                 null=True, blank=True,
                                 verbose_name='淤泥类土类型')

    # AI 新加的
    def get_soil_parameter(self):
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

    def __str__(self):
        return f"{self.work_point_name}-{self.defect_name}-{self.defect_level}"



class repairsuggestion(models.Model):
    defect_info = models.OneToOneField(defectinfo, on_delete=models.CASCADE)
    repair_suggestion = models.TextField()

    def __str__(self):
        return f"{self.defect_info}-{self.repair_suggestion}"