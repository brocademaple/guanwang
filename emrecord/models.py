from django.db import models


# Create your models here.
# class Pno(models.Model):
#     pno = models.CharField(max_length=25, verbose_name='住院号', help_text='患者的住院号应该唯一', unique=True, db_index=True)
#
#     class Meta:
#         db_table = 'emr_pno'
#
#     def __str__(self):
#         return self.pno


# 患者
from django.db import models


class Patient(models.Model):
    # 序号
    serial_number = models.CharField(
        max_length=25,
        verbose_name='序号',
        help_text='序号应该唯一',
        unique=True,
        db_index=True
    )

    # 管段类型
    segment_type = models.CharField(
        max_length=25,
        verbose_name='管段类型',
        db_index=True
    )

    # 管段材质
    material_choices = (
        (1, '塑料管'),
        (2, '混凝土管'),
    )
    material = models.IntegerField(
        choices=material_choices,
        verbose_name='管段材质',
        help_text='请选择管段材质'
    )

    # 管段直径
    diameter = models.FloatField(
        verbose_name='管段直径mm',
        help_text='请输入管段直径'
    )

    # 管段长度
    length = models.FloatField(
        verbose_name='管段长度m',
        help_text='请输入管段长度'
    )

    # 缺陷类型
    defect_type_choices = (
        (1, '结构性'),
        (2, '功能性'),
    )
    defect_type = models.IntegerField(
        choices=defect_type_choices,
        verbose_name='缺陷类型',
        help_text='请选择缺陷类型'
    )

    # 缺陷名称
    defect_name = models.CharField(
        max_length=50,
        verbose_name='缺陷名称',
        help_text='请输入缺陷名称'
    )

    # 缺陷代码
    defect_code = models.CharField(
        max_length=25,
        verbose_name='缺陷代码',
        help_text='请输入缺陷代码'
    )
    # 缺陷图片
    defect_image = models.ImageField(
        upload_to='static/icon/',
        verbose_name='缺陷图片',
        help_text='请上传缺陷的图片'
    )

    # # 缺陷等级
    # defect_level_choices = (
    #     (1, '等级 1'),
    #     (2, '等级 2'),
    #     (3, '等级 3'),
    #     (4, '等级 4'),
    # )
    # defect_level = models.IntegerField(
    #     choices=defect_level_choices,
    #     verbose_name='缺陷等级',
    #     help_text='请选择缺陷等级'
    # )

    # 缺陷描述
    defect_density = models.CharField(
        max_length=50,
        verbose_name='缺陷描述',
        help_text='请输入缺陷描述'
    )

    class Meta:
        verbose_name = '管段信息'
        verbose_name_plural = '管段信息'
    # class Meta:
    #     db_table = 'emr_pt'
    #     # ordering = ['pno']
    #     verbose_name = "缺陷清单"
    #     verbose_name_plural = verbose_name  # 模型类的复数名

    def __str__(self):
        return f"{self.serial_number} - {self.segment_type}"  # 确保使用有效的属性

# 医嘱medical order
# class Morder(models.Model):
#     # pno = models.ForeignKey(Pno, models.CASCADE, verbose_name='住院号')  # CASCADE关联删除
#     pno = models.CharField(max_length=25, verbose_name='住院号', help_text='患者的住院号应该唯一', unique=True,
#                            db_index=True)
#     # name = models.ForeignKey(Patient, models.CASCADE, verbose_name='患者姓名')
#     name = models.CharField(max_length=25, verbose_name='患者姓名', db_index=True)
#     # mo = models.CharField(max_length=15, verbose_name='医嘱')
#     imgmo1 = models.ImageField(upload_to='static/morder/', verbose_name='临时医嘱', help_text='请上传患者临时医嘱',
#                                null=True, blank=True, )
#     imgmo2 = models.ImageField(upload_to='static/morder/', verbose_name='长期医嘱', help_text='请上传患者长期医嘱',
#                                null=True, blank=True, )
#     remarks = models.TextField(max_length=400, null=True, blank=True, verbose_name='备注', default='暂无')
#     choices = (
#         (0, '暂无医嘱'),
#         (1, '存在医嘱'),
#     )
#     state = models.IntegerField(verbose_name='医嘱情况', choices=choices, editable=False, default=0)
#
#     class Meta:
#         db_table = 'emr_mo'
#         # ordering = ['pno']
#         verbose_name = "医嘱"
#         verbose_name_plural = verbose_name  # 模型类的复数名
#
#     def __str__(self):
#         return self.name
class PatientRecord(models.Model):
    name = models.CharField(max_length=128, verbose_name='工点名称', default='', help_text='请输入工点名称',
                            null=False, blank=False, db_index=True)
    image = models.ImageField(upload_to='static/ptclass_file/', verbose_name='缺陷图像',
                              help_text='上传缺陷记录记录相关缺陷图像', default='', null=True, blank=True)
    before_text = models.TextField(verbose_name='相关描述', help_text='缺陷记录，包含描述及缺陷图像', default='',
                                   null=True, blank=True)

    class Meta:
        db_table = 'patient_record'
        verbose_name = "缺陷记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name