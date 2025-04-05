from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import DefectInfo, RepairSuggestion


# def defect_entry(request):
#     if request.method == 'POST':
#         work_point_name = request.POST.get('work_point_name')
#         defect_name = request.POST.get('defect_name')
#         defect_level = request.POST.get('defect_level')
#         start_well_number = request.POST.get('start_well_number')
#         end_well_number = request.POST.get('end_well_number')
#         defect_start_position_m = float(request.POST.get('defect_start_position_m'))
#         defect_end_position_m = float(request.POST.get('defect_end_position_m'))
#         defect_start_position_clock = request.POST.get('defect_start_position_clock')
#         if defect_start_position_clock:
#             defect_start_position_clock = int(defect_start_position_clock)
#         defect_end_position_clock = request.POST.get('defect_end_position_clock')
#         if defect_end_position_clock:
#             defect_end_position_clock = int(defect_end_position_clock)
#         pipe_type = request.POST.get('pipe_type')
#         pipe_material = request.POST.get('pipe_material')
#         start_depth = float(request.POST.get('start_depth'))
#         end_depth = float(request.POST.get('end_depth'))
#         pipe_diameter = float(request.POST.get('pipe_diameter'))
#         area_type = request.POST.get('area_type')
#         structural_defect_parameter = float(request.POST.get('structural_defect_parameter'))
#         defect_density = float(request.POST.get('defect_density'))
#         soil_type = request.POST.get('soil_type')
#         wet_loess_level = request.POST.get('wet_loess_level')
#         expansive_soil_level = request.POST.get('expansive_soil_level')
#         silt_type = request.POST.get('silt_type')

#         defect_info = DefectInfo.objects.create(
#             work_point_name=work_point_name,
#             defect_name=defect_name,
#             defect_level=defect_level,
#             start_well_number=start_well_number,
#             end_well_number=end_well_number,
#             defect_start_position_m=defect_start_position_m,
#             defect_end_position_m=defect_end_position_m,
#             defect_start_position_clock=defect_start_position_clock,
#             defect_end_position_clock=defect_end_position_clock,
#             pipe_type=pipe_type,
#             pipe_material=pipe_material,
#             start_depth=start_depth,
#             end_depth=end_depth,
#             pipe_diameter=pipe_diameter,
#             area_type=area_type,
#             structural_defect_parameter=structural_defect_parameter,
#             defect_density=defect_density,
#             soil_type=soil_type,
#             wet_loess_level=wet_loess_level,
#             expansive_soil_level=expansive_soil_level,
#             silt_type=silt_type
#         )

#         # 计算修复建议，这里暂时模拟，实际需根据文档规则计算
#         repair_suggestion = "模拟修复建议"
#         RepairSuggestion.objects.create(defect_info=defect_info, repair_suggestion=repair_suggestion)

#         return redirect('repair_suggestion_view')

#     context = {
#         'defect_info': DefectInfo()
#     }
#     return render(request, 'defect_entry.html', context)


# def repair_suggestion_view(request):
#     repair_suggestions = RepairSuggestion.objects.all()
#     context = {
#       'repair_suggestions': repair_suggestions
#     }
#     return render(request,'repair_suggestion_view.html', context)


# def defect_detail(request, pk):
#     defect = get_object_or_404(DefectInfo, pk=pk)
#     repair_suggestion = RepairSuggestion.objects.filter(defect_info=defect).first()
#     context = {
#         'defect': defect,
#         'repair_suggestion': repair_suggestion
#     }
#     return render(request, 'defect_repair/defect_detail.html', context)


# @staff_member_required
# def defect_info_list(request):
#     defects = DefectInfo.objects.all().order_by('-id')
#     return render(request, 'admin/defect_repair/defectinfo/change_list.html', {'defects': defects})


# @staff_member_required
# def defect_info_create(request):
#     if request.method == 'POST':
#         # 处理表单提交
#         try:
#             DefectInfo.objects.create(**request.POST.dict())
#             messages.success(request, '缺陷信息创建成功！')
#             return redirect('admin:defect_repair_defectinfo_changelist')
#         except Exception as e:
#             messages.error(request, f'创建失败：{str(e)}')
#     return render(request, 'admin/defect_repair/defectinfo/change_form.html')


# @staff_member_required
# def defect_info_detail(request, pk):
#     defect = get_object_or_404(DefectInfo, pk=pk)
#     return render(request, 'admin/defect_repair/defectinfo/change_form.html', {'defect': defect})


# @staff_member_required
# def defect_info_edit(request, pk):
#     defect = get_object_or_404(DefectInfo, pk=pk)
#     if request.method == 'POST':
#         try:
#             for key, value in request.POST.items():
#                 if hasattr(defect, key):
#                     setattr(defect, key, value)
#             defect.save()
#             messages.success(request, '缺陷信息更新成功！')
#             return redirect('admin:defect_repair_defectinfo_changelist')
#         except Exception as e:
#             messages.error(request, f'更新失败：{str(e)}')
#     return render(request, 'admin/defect_repair/defectinfo/change_form.html', {'defect': defect})


# @staff_member_required
# def repair_suggestion_list(request):
#     suggestions = RepairSuggestion.objects.all().order_by('-id')
#     return render(request, 'admin/defect_repair/repairsuggestion/change_list.html', {'suggestions': suggestions})


# @staff_member_required
# def repair_suggestion_create(request):
#     if request.method == 'POST':
#         try:
#             RepairSuggestion.objects.create(**request.POST.dict())
#             messages.success(request, '修复建议创建成功！')
#             return redirect('admin:defect_repair_repairsuggestion_changelist')
#         except Exception as e:
#             messages.error(request, f'创建失败：{str(e)}')
#     return render(request, 'admin/defect_repair/repairsuggestion/change_form.html')


# @staff_member_required
# def repair_suggestion_detail(request, pk):
#     suggestion = get_object_or_404(RepairSuggestion, pk=pk)
#     return render(request, 'admin/defect_repair/repairsuggestion/change_form.html', {'suggestion': suggestion})


# @staff_member_required
# def repair_suggestion_edit(request, pk):
#     suggestion = get_object_or_404(RepairSuggestion, pk=pk)
#     if request.method == 'POST':
#         try:
#             for key, value in request.POST.items():
#                 if hasattr(suggestion, key):
#                     setattr(suggestion, key, value)
#             suggestion.save()
#             messages.success(request, '修复建议更新成功！')
#             return redirect('admin:defect_repair_repairsuggestion_changelist')
#         except Exception as e:
#             messages.error(request, f'更新失败：{str(e)}')
#     return render(request, 'admin/defect_repair/repairsuggestion/change_form.html', {'suggestion': suggestion})