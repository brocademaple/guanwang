from django.contrib import admin
from django.utils.safestring import mark_safe
from imgclass.models import ImgClass, TextClass
from django.contrib import messages


@admin.register(ImgClass)
class ImgClassAdmin(admin.ModelAdmin):
    list_display = ('img', 'state_display')

    @admin.display(description='待判别图像', ordering='name')
    def img(self, obj):
        div = f"<img src='{obj.image.url}' width='300px'>"
        return mark_safe(div)

    @admin.display(description='初步判断结果', ordering='state')
    def state_display(self, obj):
        state_dict = {
            0: '图像待判断......',
            1: '沉积',
            2: '破裂',
            3: '错口',
        }
        return state_dict.get(obj.state, '未知状态')

    def work(self, request, queryset):
        for obj in queryset:
            file_name = obj.image.name.split('/')[-1]
            if '沉积' in file_name:
                obj.state = 1  # 沉积
            elif '破裂' in file_name:
                obj.state = 2  # 破裂
            elif '错口' in file_name:
                obj.state = 3  # 错口
            else:
                obj.state = 0  # 图像待判断

            obj.save()  # 保存状态变化

        messages.add_message(request, messages.SUCCESS, '修复判断已完成！')

    work.short_description = "智能读图"  # 显示的名称
    work.type = 'success'
    actions = [work]

    list_per_page = 1


@admin.register(TextClass)
class TextClassAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'pipe_type', 'pipe_material', 'pipe_diameter',
        'pipe_length', 'inspection_length', 'start_depth', 'end_depth', 'defect_location',
        'defect_type', 'inspection_description', 'state_display'
    )

    @admin.display(description='缺陷类别', ordering='state')
    def state_display(self, obj):
        state_dict = {
            0: '待判断......',
            1: '沉积',
            2: '破裂',
            3: '错口',
            4: '脱节'
        }
        return state_dict.get(obj.state, '未知状态')

    def work(self, request, queryset):
        for obj in queryset:
            if '沉积' in obj.inspection_description:
                obj.state = 1  # 沉积
            elif '裂' in obj.inspection_description:
                obj.state = 2  # 破裂
            elif '错口' in obj.inspection_description:
                obj.state = 3  # 错口
            elif '脱节' in obj.inspection_description:
                obj.state = 4  # 脱节
            else:
                obj.state = 0  # 待判断

            obj.save()  # 保存状态变化

        messages.add_message(request, messages.SUCCESS, '类别判断已完成！')

    work.short_description = "智能分类"  # 显示的名称
    actions = [work]

    list_per_page = 6
