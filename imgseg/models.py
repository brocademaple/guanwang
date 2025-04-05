from django.db import models

from django.utils.html import format_html
from django.utils.safestring import mark_safe


class Image(models.Model):
    name = models.CharField(max_length=15, verbose_name='工点名称', help_text='工点名称')
    icon = models.ImageField(upload_to='static/icon/', verbose_name='图像', help_text='请上传需处理图像')
    # crack_width = models.FloatField(verbose_name='裂隙宽度', default='0')  # 裂隙宽度
    # crack_area = models.FloatField(verbose_name='裂隙面积',  default='0')  # 裂隙面积
    choices = (
        (0, '待处理'),
        (1, '已处理'),
        (2, '处理有误'),
    )
    state = models.IntegerField(verbose_name='状态', choices=choices, editable=False, default=0)
    tips = models.TextField(verbose_name='备注', help_text='若处理有误可在此处添加备注', default='暂无')

    class Meta:
        db_table = 'imgseg_image'
        verbose_name = "缺陷识别"
        verbose_name_plural = "图像处理"

    def __str__(self):
        return self.name

    # def image_data(self):
    #     if not self.icon:
    #         return format_html('<span>无照片</span>',)
    #     else:
    #         html_img = """
    #         <div οnclick='$(".my_set_image_img").hide();$(this).next().show();'>
    #         <img src='/{}' style='width:400px;height:400px;' title='点击可放大图片'>
    #         <br/>
    #         </div>
    #         <div class='my_set_image_img' οnclick="$('.my_set_image_img').hide()" style="z-index:9999;position:fixed; left: 100px; top:100px;display:none;">
    #         <img src='/media/{}' style='width: 502px;height:500px;margin-left: 200px;' title='点击关闭'>
    #         </div>
    #         """.format(self.icon, self.icon)
    #         return mark_safe(html_img)
    #
    # image_data.short_description = '待处理图片'
