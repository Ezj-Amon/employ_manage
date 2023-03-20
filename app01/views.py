from django.shortcuts import render, redirect
from app01 import models
from django import forms


# Create your views here.
def depart_list(request):
    """ 部门列表 """
    # [对象，对象，对象]每个对象是一行数据
    queryset = models.Department.objects.all()
    return render(request, "depart_list.html", {'queryser': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request, "depart_add.html")

    title = request.POST.get('title')

    models.Department.objects.create(title=title)

    return redirect("/depart/list/")
    # return render(request, "depart_list.html")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID
    nid = request.GET.get('nid')
    # 删除ID
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect("/depart/list/")


def depart_edit(request, nid: int):
    """ 部门编辑 """
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id,row_object.title)

        return render(request, "depart_edit.html", {'row_object': row_object})
    else:  # POST
        new_title = request.POST.get('title')
        models.Department.objects.filter(id=nid).update(title=new_title)
        return redirect('/depart/list/')


def user_list(request):
    """ 用户列表 """
    user_query = models.UserInfo.objects.all()

    return render(request, 'user_list.html', {'user_query': user_query})


def user_add(request):
    if request.method == 'GET':
        context = {
            'gender_choices': models.UserInfo.gender_choice
            , "depart_list": models.Department.objects.all()
        }
        return render(request, 'user_add.html', context)
    else:
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        gd = request.POST.get('gd')
        age = request.POST.get('age')
        ac = request.POST.get('ac')
        ctime = request.POST.get('ctime')
        dp = request.POST.get('dp')
        models.UserInfo.objects.create(name=name, password=pwd, age=age, gender=gd, account=ac, create_time=ctime,
                                       depart_id=dp)
        return redirect('/user/list/')


##############################################


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", 'account', 'create_time', "gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_modelform_add(request):
    """ 添加用户（ModelForm版本）"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_modelform_add.html', {"form": form})

    # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        # {'name': '123', 'password': '123', 'age': 11, 'account': Decimal('0'), 'create_time': datetime.datetime(2011, 11, 11, 0, 0, tzinfo=<UTC>), 'gender': 1, 'depart': <Department: IT运维部门>}
        # print(form.cleaned_data)
        # models.UserInfo.objects.create(..)
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_modelform_add.html', {"form": form})