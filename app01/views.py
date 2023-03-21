from django.core.validators import RegexValidator
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from app01 import models
from django import forms
from django.core.exceptions import ValidationError


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

    return redirect("/app01/depart/list/")
    # return render(request, "depart_list.html")


def depart_delete(request):
    """ 删除部门 """
    # 获取ID
    nid = request.GET.get('nid')
    # 删除ID
    models.Department.objects.filter(id=nid).delete()
    # 跳转回部门列表
    return redirect("/app01/depart/list/")


def depart_edit(request, nid: int):
    """ 部门编辑 """
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        # print(row_object.id,row_object.title)

        return render(request, "depart_edit.html", {'row_object': row_object})
    else:  # POST
        new_title = request.POST.get('title')
        models.Department.objects.filter(id=nid).update(title=new_title)
        return redirect('/app01/depart/list/')


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
        return redirect('/app01/user/list/')


##############################################


class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3, label="用户名")

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
        return redirect('/app01/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_modelform_add.html', {"form": form})


def user_edit(request, nid: int):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == 'GET':
        # 根据ID获取编辑行对应的内容
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})
        # 用户POST提交数据，数据校验。
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的数据
        # 单独保存其他指  form.instance.字段名=值
        form.save()
        return redirect('/app01/user/list/')


def user_delete(request, nid: int):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/app01/user/list/')


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, page_param="page", plus=3):
        """
        :param request: 请求的对象
        :param queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        :param page_size: 每页显示多少条数据
        :param page_param: 在URL中传递的获取分页的参数，例如：/etty/list/?page=12
        :param plus: 显示当前页的 前或后几页（页码）
        """

        from django.http.request import QueryDict
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        self.page_param = page_param
        page = request.GET.get(page_param, "1")

        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size

        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_queryset = queryset[self.start:self.end]

        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出，显示当前页的前5页、后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到11页。
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11页。

            # 当前页<5时（小极值）
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页 > 5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 页码
        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 页面
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_string = """
            <li>
                <form style="float: left;margin-left: -1px" method="get">
                    <input name="page"
                           style="position: relative;float:left;display: inline-block;width: 80px;border-radius: 0;"
                           type="text" class="form-control" placeholder="页码">
                    <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
                </form>
            </li>
            """

        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string



def pretty_list(request):

    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("level")

    page_object = Pagination(request, queryset)

    context = {
        "search_data": search_data,

        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }
    return render(request, 'pretty_list.html', context)


class PrettyModelForm(forms.ModelForm):
    # 验证：方式1
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误'), ],
    # )
    class Meta:
        model = models.PrettyNum
        fields = ["mobile", "price", "level", "status"]
        # fields = "__all__"
        # exclude = [".."]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            # if name == "password":
            #     continue
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
    # 方式2：
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile


def pretty_add(request):
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    # 用户POST提交数据，数据校验。
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        # 默认保存的是用户输入的数据
        # 单独保存其他指  form.instance.字段名=值
        form.save()
        return redirect('/app01/pretty/list/')
    return render(request, "pretty_add.html", {'form': form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ['mobile','price', 'level', 'status']

    # 验证：方式2
    def clean_mobile(self):
        # 当前编辑的哪一行的ID
        # print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")

        # 验证通过，用户输入的值返回
        return txt_mobile
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/app01/pretty/list/')

    return render(request, 'pretty_edit.html', {"form": form})


def pretty_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/app01/pretty/list/')
