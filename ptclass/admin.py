from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.urls import reverse  # 确保从Django导入


from ptclass.models import PtClass
from django.shortcuts import render, redirect


# 自定义视图函数来显示医学影像报告
def show_medical_report(request):
    queryset_ids = request.GET.get('queryset_ids', '')
    queryset = PtClass.objects.filter(id__in=queryset_ids.split(','))
    context = {
        'queryset': queryset,
    }
    return render(request, 'admin/ptclass/medical_report.html', context)


# 注册URL
@admin.register(PtClass)
class PtClassAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'defect_type', 'image_1', 'repair_type', 'diagnosis_data',
    )
    list_filter = ('state',)
    search_fields = ('name',)
    list_per_page = 6

    @admin.display(description='缺陷图像', ordering='image_1')
    def image_1(self, obj):
        if obj.image:
            image_url = obj.image.url
            return mark_safe(f'<img src="{image_url}" width="100" height="100" alt="暂无图像" />')
        else:
            return "暂无"

    @admin.display(description='修复/养护建议', ordering='name')
    def diagnosis_data(self, obj):
        if obj.state == 3:
            html_text = "<p>(整体缺陷)管道存在重大缺陷，管道损坏严重或即将导致破坏。结构已经发生或即将发生破坏，应立即修复。</p>"
            return mark_safe(html_text)
        else:
            return mark_safe(obj.diagnosis)

    @admin.display(description='修复类型', ordering='state')
    def repair_type(self, obj):
        if obj.state == 3:
            return mark_safe('<span style="color: red;">立即修复</span>')
        elif obj.state == 2:
            return mark_safe('<span style="color: orange;">尽快修复</span>')
        elif obj.state == 0:
            return mark_safe('<span style="color: green;">无需修复</span>')
        else:
            return mark_safe('<span>未知</span>')

    @admin.action(description="查看报告")
    def view_report(self, request, queryset):
        if queryset:
            ids = ','.join(str(obj.id) for obj in queryset)
            url = reverse('ptclass_medical_report') + f'?queryset_ids={ids}'
            messages.add_message(request, messages.INFO, f'请点击此处查看报告: <a href="{url}">查看报告</a>')
        else:
            messages.warning(request, '没有选择任何项目。')
        return redirect(request.META.get('HTTP_REFERER', 'admin:ptclass_ptclass_changelist'))

    def work(self, request, queryset):
        queryset.update(state="3")
        messages.add_message(request, messages.SUCCESS, '建议完成！')

    work.short_description = "辅助建议"
    work.type = 'success'
    actions = [work, view_report]

