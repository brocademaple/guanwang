from django.contrib import admin
from .models import FuncPipeSection, funcdefectinfo, funcrepairsuggestion


class FuncDefectInfoInline(admin.StackedInline):
    """在管段详情页中内联显示缺陷信息"""
    model = funcdefectinfo
    extra = 0
    fieldsets = [
        (None, {
            'fields': ('defect_name', 'defect_level', 'defect_start_position_m', 
                      'defect_end_position_m', 'defect_start_position_clock', 
                      'defect_end_position_clock')
        }),
    ]
    readonly_fields = []


@admin.register(FuncPipeSection)
class FuncPipeSectionAdmin(admin.ModelAdmin):
    """功能性缺陷的管段信息管理界面"""
    list_display = ('work_point_name', 'pipe_length', 'pipe_type', 'pipe_material', 
                   'pipe_diameter', 'get_E_value', 'start_well_number', 'end_well_number')
    search_fields = ('work_point_name', 'start_well_number', 'end_well_number')
    list_filter = ('pipe_type', 'pipe_material')
    fieldsets = [
        (None, {
            'fields': ('work_point_name', 'pipe_length', 'start_well_number', 'end_well_number',
                      'pipe_type', 'pipe_material', 'start_depth', 'end_depth', 'pipe_diameter')
        }),
    ]
    inlines = [FuncDefectInfoInline]
    
    def get_E_value(self, obj):
        """显示计算得到的E值"""
        return obj.calculate_E()
    get_E_value.short_description = 'E值'


# 移除这个类，因为我们不需要在缺陷表单中显示修复建议
# class FuncRepairSuggestionInline(admin.StackedInline):
#     """在缺陷详情页中内联显示修复建议"""
#     model = funcrepairsuggestion
#     extra = 0
#     fieldsets = [
#         (None, {
#             'fields': ('repair_suggestion',)
#         }),
#     ]
#     readonly_fields = ['repair_suggestion']


@admin.register(funcdefectinfo)
class FunctionalDefectInfoAdmin(admin.ModelAdmin):
    """功能性缺陷信息管理界面"""
    list_display = ('pipe_section', 'defect_name', 'defect_level', 
                   'defect_start_position_m', 'defect_end_position_m')
    search_fields = ('pipe_section__work_point_name', 'defect_name')
    list_filter = ('defect_name', 'defect_level')
    fieldsets = [
        (None, {
            'fields': ('pipe_section', 'defect_name', 'defect_level', 
                      'defect_start_position_m', 'defect_end_position_m', 
                      'defect_start_position_clock', 'defect_end_position_clock')
        }),
    ]
    # 移除内联编辑，不再显示修复建议部分
    # inlines = [FuncRepairSuggestionInline]
    
    # 自动验证和填充修复建议
    actions = ['auto_update_suggestions']
    
    def auto_update_suggestions(self, request, queryset):
        """批量更新选中缺陷的修复建议"""
        for defect in queryset:
            defect.save()  # 调用save方法会自动更新修复建议
        self.message_user(request, f"已成功更新{queryset.count()}个缺陷的修复建议")
    auto_update_suggestions.short_description = "更新选中缺陷的修复建议"


@admin.register(funcrepairsuggestion)
class FunctionalRepairSuggestionAdmin(admin.ModelAdmin):
    """功能性缺陷修复建议管理界面"""
    list_display = ('defect_info', 'repair_suggestion')
    search_fields = ('repair_suggestion', 'defect_info__pipe_section__work_point_name')
    readonly_fields = ['defect_info', 'repair_suggestion']
    fieldsets = [
        (None, {
            'fields': ('defect_info', 'repair_suggestion')
        }),
    ]
    
    # 不允许直接添加或修改修复建议，只能通过缺陷信息自动生成
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
