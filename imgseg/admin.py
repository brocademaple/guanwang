from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from imgseg.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('img', 'result')

    # 在list页面显示图像
    @admin.display(description='待处理图像', ordering='name')
    def img(self, obj):
        div = f"<img src='{obj.icon.url}' width='300px'>"
        return mark_safe(div)

    @admin.display(description='处理结果', ordering='name')
    def result(self, obj):
        if obj.state == 0:
            div0 = f"<img src='/static/icon/blank.jpg' width='300px'>"
            return mark_safe(div0)
        elif obj.state == 1:
            # 使用待处理图像的名称
            original_img_name = obj.icon.name.split('/')[-1].replace('.jpg', '')  # 假设原图为 .jpg 格式
            div1 = f"<img src='/static/icon/{original_img_name}.png' width='300px'>"
            return mark_safe(div1)
        else:
            return mark_safe(obj.tips)

    def work(self, request, queryset):
        queryset.update(state="1")
        messages.add_message(request, messages.SUCCESS, '处理成功！')

    work.short_description = "处理图像"  # 显示的名称
    work.type = 'success'

    def wrong(self, request, queryset):
        queryset.update(state="3")
        messages.add_message(request, messages.SUCCESS, '上报成功！点击图片即可前往修改')

    wrong.short_description = "结果有误"  # 显示的名称
    wrong.type = 'warning'
    actions = [work, wrong]

    list_per_page = 1