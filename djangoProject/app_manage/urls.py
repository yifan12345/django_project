from django.urls import path
from app_manage.views import project_view,module_view

urlpatterns = [
    # 项目管理
    path('1/', project_view.list_project),
    path('add/', project_view.add_project),
    path('edit/<int:pid>', project_view.edit_project),
    path('delete/<int:pid>', project_view.del_project),

    #模块管理
    path('2/', module_view.list_module),
]
