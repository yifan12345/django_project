from django import forms
from django.forms import widgets
from app_manage.models import Project


# 项目新增表单
class ProjectForm(forms.Form):
    name = forms.CharField(label="名称", max_length=100,
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    describe = forms.CharField(label="描述",
                               widget=widgets.Textarea(attrs={"class": "form-control"}))
    status = forms.BooleanField(label="状态", required=False,
                                widget=widgets.CheckboxInput(attrs={"class": "checkbox"}))


class ProjectEditForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'describe', 'status']
