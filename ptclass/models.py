from django.db import models


class PtClass(models.Model):
    name = models.CharField(max_length=128, verbose_name='工点名称', help_text='请输入工点名称', null=False,
                            blank=False, db_index=True)
    defect_type_choices = (
        (0, '未知'),
        (1, '沉积'),
        (2, '错口'),
        (3, '破裂'),
    )
    # 缺陷描述
    defect_density = models.TextField(
        verbose_name='缺陷描述',
        help_text='请输入缺陷描述',
        default=''  # 添加默认值
    )
    defect_type = models.IntegerField(choices=defect_type_choices, verbose_name='缺陷类型', help_text='请选择缺陷类型', default=0)
    image = models.ImageField(upload_to='static/ptclass_file/', verbose_name='缺陷图像',
                              help_text='上传管段录相关缺陷图像', default='', null=True, blank=True)
    state_type = (
        (0, '无需修复'),
        (1, '立即修复'),
        (2, '尽快修复'),
        (3, '未知'),
    )
    state = models.IntegerField(verbose_name='修复类型', help_text='初步建议结果', choices=state_type, default=0)
    diagnosis = models.TextField(verbose_name='修复建议', help_text='此处为初步建议结果，若需补充可在此备注',
                                 default='暂无')
    class Meta:
        db_table = 'patient_class'
        verbose_name = "智慧方案"
        verbose_name_plural = "修复建议"

    def __str__(self):
        return self.name