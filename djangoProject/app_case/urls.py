from django.urls import path
from app_case import views

urlpatterns = [
    path('', views.case_list),
    path('new_case/', views.new_case),
    path('edit_case/<int:cid>/', views.edit_case),
    path('case_delete/<int:cid>/', views.case_delete),

    path('get_case_info/', views.get_case_info),
    # 用例详情
    # 发送请求
    path('send_req/', views.send_req),
    # 断言结果
    path('assert_result/', views.assert_result),
    # 查询二级联动需要的项目-模块数据
    path('get_select_data/', views.get_select_data),
    # 保存接口
    path('save_case/', views.save_case)
]
