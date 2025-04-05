from django.contrib import admin, messages
from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.http import HttpResponseRedirect
from emrecord.models import Patient, PatientRecord


# 注册 Patient 模型
@admin.register(Patient)
class PatientShow(admin.ModelAdmin):
    list_display = ('serial_number', 'segment_type', 'material', 'diameter', 'length', 'defect_type',
                    'defect_name', 'defect_code',  'display_defect_image', 'defect_density')
    list_per_page = 5

    def display_defect_image(self, obj):
        if obj.defect_image:
            return mark_safe(f'<img src="{obj.defect_image.url}" style="max-height: 100px; max-width: 100px;"/>')
        return "无图片"

    display_defect_image.short_description = '缺陷图片'

    def import_data(self, request, queryset):
        # 这里可以根据需要设置其他缺陷相关的数据
        # messages.add_message(request, messages.INFO, '缺陷识别界面即将打开！')
        return HttpResponseRedirect('/imgseg/image/')  # 直接重定向到缺陷识别界面

    import_data.short_description = "缺陷识别"  # 显示的名称
    import_data.type = 'success'
    actions = [import_data]

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ('img', 'before_text')
    list_per_page = 1

    tag = False

    # 在list页面显示图像
    @admin.display(description='缺陷图像', ordering='name')
    def img(self, obj):
        div = f"<img src='{obj.image.url}' width='350px'>"
        return mark_safe(div)

    def jaccard(self, request, queryset):
        self.tag = not self.tag  # 取反tag
        if self.tag:
            self.list_display += ('after_text',)  # 显示after_text
            messages.add_message(request, messages.SUCCESS, '已对病历信息进行摘要抽取！')
        else:
            self.list_display = tuple([item for item in self.list_display if item != 'after_text'])  # 不显示after_text

    @staticmethod
    @admin.display(description='报告总结')
    def after_text(obj):
        html_text = f'<p>肺部有散在的多发片状和条索影，呈毛玻璃样改变，但其他结构正常，与2020年2月16日扫描相比，全肺和两肺病灶感染比例显著降低，新冠肺炎治疗后病灶有明显吸收好转。</p>'
        return mark_safe(html_text)

    def toshow(self, request, queryset):
        return redirect('/ptclass/ptclass/')

    jaccard.short_description = "摘要抽取"  # 显示的名称
    toshow.short_description = "结构化显示病历信息"
    jaccard.type = 'success'
    toshow.type = 'secondary'