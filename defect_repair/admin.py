from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import defectinfo, repairsuggestion
from django.contrib import messages
from django import forms

# 新加的代码
class DefectInfoAdminForm(forms.ModelForm):
    class Meta:
        model = defectinfo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wet_loess_level'].widget.attrs['style'] = 'display:none;'
        self.fields['expansive_soil_level'].widget.attrs['style'] = 'display:none;'
        self.fields['silt_type'].widget.attrs['style'] = 'display:none;'

    def clean(self):
        cleaned_data = super().clean()
        soil_type = cleaned_data.get('soil_type')
        if soil_type == '湿陷性黄土' and not cleaned_data.get('wet_loess_level'):
            self.add_error('wet_loess_level', '请选择湿陷性黄土等级')
        elif soil_type == '膨胀土' and not cleaned_data.get('expansive_soil_level'):
            self.add_error('expansive_soil_level', '请选择膨胀土等级')
        elif soil_type == '淤泥类土' and not cleaned_data.get('silt_type'):
            self.add_error('silt_type', '请选择淤泥类土类型')
        return cleaned_data



@admin.register(defectinfo)
class DefectInfoAdmin(admin.ModelAdmin):
    list_display = ('work_point_name', 'defect_name', 'defect_level', 'pipe_type', 'pipe_material')
    # 以下为测试加按钮功能的代码
    # # 增加自定义按钮
    # actions = ['make_copy', 'custom_button']
    #
    # def custom_button(self, request, queryset):
    #     pass
    #
    # # 显示的文本，与django admin一致
    # custom_button.short_description = '测试按钮'
    # # icon，参考element-ui icon与https://fontawesome.com
    # custom_button.icon = 'fas fa-audio-description'
    #
    # # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    # custom_button.type = 'danger'
    #
    # # 给按钮追加自定义的颜色
    # custom_button.style = 'color:black;'
    #
    # def make_copy(self, request, queryset):
    #     pass
    #
    # make_copy.short_description = '复制员工'
    # 以上为测试加按钮功能的代码

    list_filter = ('defect_level', 'pipe_type', 'pipe_material')
    search_fields = ('work_point_name', 'defect_name', 'start_well_number', 'end_well_number')
    ordering = ('-id',)

    @admin.display(description='待判别图像', ordering='name')
    def auto_detect_level(self, obj, queryset):
        for obj in queryset:
            if '破裂' in obj.defect_name or '渗漏' in obj.defect_name or '脱节' in obj.defect_name:
                obj.defect_level = '3级'  # 假设这类缺陷为3级
            elif '变形' in obj.defect_name or '错口' in obj.defect_name:
                obj.defect_level = '2级'  # 假设这类缺陷为2级
            elif '腐蚀' in obj.defect_name or '接口材料脱落' in obj.defect_name:
                obj.defect_level = '1级'  # 假设这类缺陷为1级
            elif '异物刺入' in obj.defect_name or '支管暗接' in obj.defect_name or '起伏' in obj.defect_name:
                obj.defect_level = '4级'  # 假设这类缺陷为4级
            else:
                obj.defect_level = '1级'  # 默认为1级

            obj.save()  # 保存状态变化

        messages.add_message(request, messages.SUCCESS, '缺陷等级自动判断已完成！')

    auto_detect_level.short_description = "自动判断缺陷等级"  # 显示的名称
    auto_detect_level.type = 'success'
    actions = [auto_detect_level]

    list_per_page = 10

    class Media:
        js = ('js/defect_info_admin.js',)


@admin.register(repairsuggestion)
class RepairSuggestionAdmin(admin.ModelAdmin):
    list_display = ('defect_info', 'repair_suggestion')
    search_fields = ('repair_suggestion', 'defect_info__work_point_name')
    ordering = ('-id',)


# 自定义菜单
def get_app_list(self, request):
    app_list = super().get_app_list(request)
    for app in app_list:
        if app['app_label'] == 'defect_repair':
            app['name'] = '缺陷修复'
            app['icon'] = 'fas fa-tools'
            app['models'].sort(key=lambda x: x['name'])
    return app_list
