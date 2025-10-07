# defect_repair/admin.py
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import defectinfo, repairsuggestion, PipeSection
from django.contrib import messages
from django import forms

# 注册PipeSection模型到admin
@admin.register(PipeSection)
class PipeSectionAdmin(admin.ModelAdmin):
    list_display = ('work_point_name', 'start_well_number', 'end_well_number', 'pipe_length', 'pipe_type', 'pipe_material')
    search_fields = ('work_point_name', 'start_well_number', 'end_well_number')
    list_filter = ('pipe_type', 'pipe_material', 'area_type', 'soil_type')
    ordering = ('-id',)
    list_per_page = 10
    
    # 详细表单布局
    fieldsets = (
        ('管段基本信息', {
            'fields': ('work_point_name', 'start_well_number', 'end_well_number', 'pipe_length')
        }),
        ('管道属性', {
            'fields': ('pipe_type', 'pipe_material', 'pipe_diameter', 'start_depth', 'end_depth')
        }),
        ('环境与地质信息', {
            'fields': ('area_type', 'soil_type', 'wet_loess_level', 'expansive_soil_level', 'silt_type')
        }),
        ('缺陷密度', {
            'fields': ('defect_density',),
            # 'classes': ('collapse',)
        })
    )

# 更新defectinfo表单，移除不再需要的字段
class DefectInfoAdminForm(forms.ModelForm):
    class Meta:
        model = defectinfo
        fields = '__all__'
        exclude = ('defect_density',)  # 移除不再需要的字段

@admin.register(defectinfo)
class DefectInfoAdmin(admin.ModelAdmin):
    form = DefectInfoAdminForm
    # list_display = ('defect_name', 'defect_level', 'defect_score', 'get_pipe_section_name', 'get_pipe_type', 'get_pipe_material', 'get_F_value', 'get_Sm_value', 'get_RI_value', 'get_repair_suggestion', 'get_repair_measures')
    list_display = ('defect_name', 'defect_level', 'defect_score', 'get_pipe_section_name', 'get_pipe_type', 'get_pipe_material', 'get_F_value', 'get_Sm_value', 'get_RI_value', 'get_repair_suggestion')

    list_filter = ('defect_level',)
    search_fields = ('pipe_section__work_point_name', 'pipe_section__start_well_number', 'pipe_section__end_well_number', 'defect_name')
    ordering = ('-id',)
    list_per_page = 10
    
    # 详细表单布局
    fieldsets = (
        ('关联信息', {
            'fields': ('pipe_section',)
        }),
        ('缺陷信息', {
            'fields': ('defect_name', 'defect_level', 'defect_start_position_m', 'defect_end_position_m')
        }),
        ('缺陷位置（钟表法）', {
            'fields': ('defect_start_position_clock', 'defect_end_position_clock')
        })
    )
    
    # 自定义显示字段，从pipe_section获取信息
    @admin.display(description='所属管段名称')
    def get_pipe_section_name(self, obj):
        return obj.pipe_section.work_point_name or '未命名'
    
    @admin.display(description='管道类型')
    def get_pipe_type(self, obj):
        return obj.pipe_section.pipe_type
    
    @admin.display(description='管段材质')
    def get_pipe_material(self, obj):
        return obj.pipe_section.pipe_material
    
    @admin.display(description='F值')
    def get_F_value(self, obj):
        return round(obj.pipe_section.calculate_F(), 2)
    
    @admin.display(description='Sm值')
    def get_Sm_value(self, obj):
        return f"{obj.pipe_section.calculate_Sm():.3f}"
    
    @admin.display(description='RI值')
    def get_RI_value(self, obj):
        return round(obj.pipe_section.calculate_RI(), 2)
    
    @admin.display(description='修复建议')
    def get_repair_suggestion(self, obj):
        return obj.get_repair_suggestion()
    
    # @admin.display(description='具体修复措施')
    # def get_repair_measures(self, obj):
    #     # 从defect_info获取实时计算的修复措施
    #     return obj.get_repair_measures()
    @admin.display(description='待判别图像', ordering='name')
    def auto_detect_level(self, request, queryset):
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

    class Media:
        js = ('js/defect_info_admin.js',)

@admin.register(repairsuggestion)
class RepairSuggestionAdmin(admin.ModelAdmin):
    list_display = ('get_defect_name',  'get_defect_level', 'get_pipe_section_name', 'get_F_value', 'get_Sm_value', 'get_RI_value', 'get_repair_suggestion', 'get_repair_measures')
    search_fields = ('repair_suggestion', 'defect_info__pipe_section__work_point_name', 'defect_info__defect_name')
    ordering = ('-id',)
    
    @admin.display(description='缺陷名称')
    def get_defect_name(self, obj):
        return obj.defect_info.defect_name
    

        
    
    @admin.display(description='缺陷等级')
    def get_defect_level(self, obj):
        return obj.defect_info.defect_level
    
    @admin.display(description='所属管段名称')
    def get_pipe_section_name(self, obj):
        return obj.defect_info.pipe_section.work_point_name or '未命名'
    
    @admin.display(description='F值')
    def get_F_value(self, obj):
        return round(obj.defect_info.pipe_section.calculate_F(), 2)
    
    @admin.display(description='Sm值')
    def get_Sm_value(self, obj):
        return f"{obj.defect_info.pipe_section.calculate_Sm():.3f}"
    
    @admin.display(description='RI值')
    def get_RI_value(self, obj):
        return round(obj.defect_info.pipe_section.calculate_RI(), 2)
    
    # @admin.display(description='修复建议')
    # def get_repair_suggestion_text(self, obj):
    #     return obj.repair_suggestion

    @admin.display(description='修复建议')
    def get_repair_suggestion(self, obj):
        # 与DefectInfoAdmin保持一致，从defect_info获取实时计算的修复建议
        return obj.defect_info.get_repair_suggestion()
        
    @admin.display(description='具体修复措施')
    def get_repair_measures(self, obj):
        # 与DefectInfoAdmin保持一致，从defect_info获取实时计算的修复措施
        return obj.defect_info.get_repair_measures()

# 自定义菜单
def get_app_list(self, request):
    app_list = super().get_app_list(request)
    for app in app_list:
        if app['app_label'] == 'defect_repair':
            app['name'] = '缺陷修复'
            app['icon'] = 'fas fa-tools'
            app['models'].sort(key=lambda x: x['name'])
    return app_list
