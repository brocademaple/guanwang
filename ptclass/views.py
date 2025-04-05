# views.py
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PtClass  # 导入你的模型


def export_report(request):
    queryset = PtClass.objects.all()  # 获取所有缺陷记录

    # 创建一个 HTTP 响应，设置内容类型为 PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # 创建一个 PDF 对象
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # 添加标题
    p.setFont("Helvetica-Bold", 24)
    p.drawString(100, height - 50, "管段缺陷报告")

    # 设置字体
    p.setFont("Helvetica", 12)

    # 记录开始位置
    y_position = height - 100

    for obj in queryset:
        if y_position < 50:  # 如果到达页面底部，就换页
            p.showPage()
            p.setFont("Helvetica-Bold", 24)
            p.drawString(100, height - 50, "管段缺陷报告")
            p.setFont("Helvetica", 12)
            y_position = height - 100

        # 添加缺陷信息
        p.drawString(100, y_position, f"名称: {obj.name}")
        y_position -= 20
        defect_type = {
            0: "未知",
            1: "沉积",
            2: "错口",
            3: "破裂"
        }.get(obj.defect_type, "未知")
        p.drawString(100, y_position, f"缺陷类型: {defect_type}")
        y_position -= 20
        p.drawString(100, y_position, f"缺陷描述: {obj.defect_density}")
        y_position -= 20
        p.drawString(100, y_position, "缺陷图像:")  # 这里可以添加图像处理
        y_position -= 20
        repair_type = {
            0: "无需修复",
            1: "立即修复",
            2: "尽快修复",
            3: "未知"
        }.get(obj.state, "未知")
        p.drawString(100, y_position, f"修复类型: {repair_type}")
        y_position -= 20
        p.drawString(100, y_position, f"修复/养护建议: {obj.diagnosis}")
        y_position -= 40  # 加大间距

    p.showPage()
    p.save()
    return response
