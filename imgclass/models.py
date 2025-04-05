from django.db import models


class ImgClass(models.Model):
    name = models.CharField(max_length=15, verbose_name='工点名称', help_text='请输入工点名称')
    image = models.ImageField(upload_to='static/imgclass_img/', verbose_name='图像', help_text='请上传需判断图像')

    state_type = (
        (0, '图像待判断......'),
        (1, '沉积'),
        (2, '破裂'),
        (3, '错口'),
    )
    state = models.IntegerField(verbose_name='初步判断结果', help_text='初步分类', choices=state_type, editable=False,
                                default=0)

    class Meta:
        db_table = 'image_class'
        verbose_name = "缺陷分类"
        verbose_name_plural = "图像辅助判断"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # 这里不进行状态设置
        super().save(*args, **kwargs)  # 调用父类的 save 方法


class TextClass(models.Model):
    name = models.CharField(max_length=15, verbose_name='工点名称', help_text='请输入工点名称')
    pipe_type = models.CharField(max_length=50, verbose_name='管段类型', help_text='请输入管段类型', default='YC')
    # pipe_material_choices = (
    #     (0, '未知'),
    #     (1, '混凝土管'),
    #     (2, '塑料管'),
    #     (3, 'PVC管'),
    # )
    # pipe_material = models.IntegerField(choices=pipe_material_choices, verbose_name='管段材质',
    #                                     help_text='请选择管段材质', default=0)
    pipe_material = models.CharField(max_length=100, verbose_name='管段材质', help_text='请输入管段材质')
    pipe_diameter = models.FloatField(verbose_name='管段直径(mm)', help_text='请输入管段直径')
    pipe_length = models.FloatField(verbose_name='管段长度(m)', help_text='请输入管段长度')
    inspection_length = models.FloatField(verbose_name='检测长度(m)', help_text='请输入检测长度')
    start_depth = models.FloatField(verbose_name='起点埋深(m)', help_text='请输入起点埋深')
    end_depth = models.FloatField(verbose_name='终点埋深(m)', help_text='请输入终点埋深')
    defect_location = models.CharField(max_length=100, verbose_name='缺陷位置', help_text='请输入缺陷位置')
    # defect_type_choices = (
    #     (0, '未知'),
    #     (1, '结构性'),
    #     (2, '功能性'),
    # )
    # defect_type = models.IntegerField(choices=defect_type_choices, verbose_name='缺陷类型', help_text='请选择缺陷类型',
    #                                   default=0)
    defect_type = models.CharField(max_length=100, verbose_name='缺陷类型', help_text='请输入缺陷类型')
    inspection_description = models.TextField(verbose_name='检测描述', help_text='请输入检测描述')

    state_type = (
        (0, '待判断......'),
        (1, '沉积'),
        (2, '破裂'),
        (3, '错口'),
        (4, '脱节'),
    )
    state = models.IntegerField(verbose_name='缺陷类别', help_text='缺陷分类', choices=state_type, editable=False,
                                default=0)

    class Meta:
        db_table = 'text_class'
        verbose_name = "缺陷分类"
        verbose_name_plural = "文本缺陷分类"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # 调用父类的 save 方法
