# defect_repair/models.py
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
    #
    # # 添加结构性缺陷相关字段
    # structural_defect_parameter = models.DecimalField(max_digits=3, decimal_places=2,
    #                                                 verbose_name='管段结构性缺陷参数F',
    #                                                 validators=[MinValueValidator(0), MaxValueValidator(10)])
    #
    # defect_length_over_1_5m = models.DecimalField(max_digits=5, decimal_places=2,
    #                                              verbose_name='纵向净距大于1.5m的缺陷长度（米）',
    #                                              validators=[MinValueValidator(0), MaxValueValidator(200)],
    #                                              default=0)
    #
    # defect_length_1_to_1_5m = models.DecimalField(max_digits=5, decimal_places=2,
    #                                              verbose_name='纵向净距在1-1.5m的缺陷长度（米）',
    #                                              validators=[MinValueValidator(0), MaxValueValidator(200)],
    #                                              default=0)
    #
    # defect_score = models.DecimalField(max_digits=5, decimal_places=2,
    #                                  verbose_name='缺陷分值',
    #                                  validators=[MinValueValidator(0)],
    #                                  default=0)

    # 计算结构性缺陷参数F
    def calculate_F(self):
        # 根据图片中的公式，当Smax >= S时，F = Smax；当Smax < S时，F = S
        # 写的不对，需要改
        defect_score = self.get_defect_score()
        if defect_score > 5:
            return defect_score
        return S

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

    # 计算结构性缺陷密度Sm
    def calculate_Sm(self):
        # 根据图片中的公式：Sm = (1/L) * (∑P1*L1 + α∑P2*L2)
        # 其中：
        # L - 管段长度
        # L1 - 纵向净距大于1.5m的结构性缺陷长度
        # L2 - 纵向净距在1.0m至1.5m之间的结构性缺陷长度
        # P1, P2 - 对应的缺陷分值
        # α - 结构性缺陷影响系数，当缺陷间距有关时取1.1
        
        if not self.pipe_length:
            return 0
            
        alpha = 1.1  # 结构性缺陷影响系数
        defect_score = self.get_defect_score()
        
        term1 = defect_score * self.defect_length_over_1_5m
        term2 = alpha * defect_score * self.defect_length_1_to_1_5m
        
        return (term1 + term2) / float(self.pipe_length)

    # 新增方法获取地区类别对应的K值
    def get_area_value_K(self):
        area_type_mapping = {
            '中心商业、附近具有甲类民用建筑工程的区域': 10,
            '交通干道、附近具有乙类民用建筑工程的区域': 6,
            '其他行车道路、附近具有丙类民用建筑工程的区域': 3,
            '所有其他区域': 0
        }
        return area_type_mapping[self.area_type]


    # 计算管道重要性参数E
    def calculate_E(self):
        diameter = float(self.pipe_diameter)
        F = self.calculate_F()
        if diameter > 1500:
            E = 10
        elif 1000 < diameter <= 1500:
            E = 6
        elif 600 <= diameter <= 1000:
            E = 3
        elif diameter < 600 or F < 4:
            E = 0
        return E
    

    # 获取土质影响参数T值
    def get_soil_parameter_T(self):
        if self.soil_type == '一般土层' or self.calculate_F() == 0:
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


    # 计算修复指数 RI
    def calculate_RI(self):
        soil_parameter = self.get_soil_parameter_T()
        RI = 0.7 * self.calculate_F() + 0.1 * self.get_area_value_K() + 0.05 * self.pipe_importance_parameter + 0.15 * soil_parameter
        return RI

    # 计算结构性缺陷参数 r
    def calculate_r(self):
        total_score = self.defect_score_1_1_5 + self.defect_score_over_1_5
        total_count = self.structural_defect_count
        return total_score / total_count if total_count > 0 else 0

    # 根据计算结果给出修复建议
    def get_repair_suggestion(self):
        RI = self.calculate_RI()
        r = self.calculate_r()
        Sm = self.calculate_Sm()
        diameter = float(self.pipe_diameter)
        level = self.defect_level

        if RI < 10 and r < 2 and Sm < 0.1:
            suggestion = "不修复"
            measures = ""
        elif 300 <= diameter < 800:
            if level == '2级':
                suggestion = "局部修复"
                measures = "不锈钢快速锁、点状原位固化"
            elif level == '3级':
                suggestion = "局部修复"
                measures = "不锈钢双胀环、点状原位固化"
            elif level == '4级':
                suggestion = "整体修复"
                measures = "管线迁改 + 局部树脂固化"
            else:
                suggestion = "不明确"
                measures = ""
        elif diameter >= 800:
            if level == '2级':
                suggestion = "局部修复"
                measures = "点状原位固化、局部树脂固化"
            elif level == '3级':
                suggestion = "整体修复"
                measures = "管线迁改 + 整体树脂固化"
            elif level == '4级':
                suggestion = "整体修复"
                measures = "管线迁改 + 全部更换管道"
            else:
                suggestion = "不明确"
                measures = ""
        else:
            suggestion = "不明确"
            measures = ""

        return f"修复建议: {suggestion}\n具体修复措施: {measures}"

    # 在保存 defectinfo 实例时自动生成修复建议并保存到 repairsuggestion 模型中
    def save(self, *args, **kwargs):
        # 保存前计算F值和Sm值
        self.structural_defect_parameter = self.calculate_F()
        self.defect_density = self.calculate_Sm()
        super().save(*args, **kwargs)
        
        # 生成修复建议
        suggestion_text = self.get_repair_suggestion()
        repairsuggestion_obj, created = repairsuggestion.objects.get_or_create(defect_info=self)
        repairsuggestion_obj.repair_suggestion = suggestion_text
        repairsuggestion_obj.save()


    def __str__(self):
        return f"{self.work_point_name}-{self.defect_name}-{self.defect_level}"


class repairsuggestion(models.Model):
    defect_info = models.OneToOneField(defectinfo, on_delete=models.CASCADE)
    repair_suggestion = models.TextField()

    def __str__(self):
        return f"{self.defect_info}-{self.repair_suggestion}"