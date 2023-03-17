# 管理系统
## Django+bootstrap+jquery

### django有两种传值方式
- '/depart/delete/?nid={{ obj.id }}'<br>
 这样需要用get方法：
 request.GET.get('nid')
- html:/depart/{{ obj.id }}/edit/"<br>
  urls:'depart/<int:nid>/edit/'<br>
  view:就可以将nid作为函数的参数传入，不需要get方法

### 模板的继承
重复拷贝组件，JS，十分麻烦，在三个页面中我们都使用了导航栏,JS等内容
新建立一个layout.html里面放入公用部分，在需要更改的地方加入block
```html
<div>
    {% block content %}{% endblock %}
</div>
```
新建立一个index.html，里面使用extends关键字，就会自动将对应的content的内容填充
```html
{% extends 'layout.html' %}
{% block content %}
    <h1>首页</h1>
{% endblock %}
```
### 选择框和筛选内容的绑定
- 原始方式：通过字典传值
  - 用户提交数据没有校验
  - 如果出现错误，在页面上应该有错误提示
  - 页面上每一个字段都需要重写书写
  - 如果出现关联数据，需要手动从其他表取值循环展示
- Form组件(小简便)
  - 1.views.py<br>
  ```python
    class MyForm(Form):
      user = forms.CharField(widget=forms.Input)
      #这里用了input，在html中就会自动生产Input
      pwd = form.CharFiled(widget=forms.Input)
      email = form.CharFiled(widget=forms.Input)
      account = form.CharFiled(widget=forms.Input)
      create_time = form.CharFiled(widget=forms.Input)
      depart = form.CharFiled(widget=forms.Input)
      gender = form.CharFiled(widget=forms.Input)


    def user_add(request):
        if request.method == &quot;GET&quot;:
            form = MyForm()
            return render(request, &apos;user_add.html&apos;,{&quot;form&quot;:form})
  ```
  - 2.user_add.html<br>
  ```html
  &lt;form method=&quot;post&quot;&gt;
  {% for field in form%}
      {{ field }}
  {% endfor %}
  &lt;!-- &lt;input type=&quot;text&quot;  placeholder=&quot;姓名&quot; name=&quot;user&quot; /&gt; --&gt;
  &lt;/form&gt;
  ```
- ModelForm
  - models.py
  ```python
    class UserInfo(models.Model):
        """ 员工表 """
        name = models.CharField(verbose_name="姓名", max_length=16)
        password = models.CharField(verbose_name="密码", max_length=64)
        age = models.IntegerField(verbose_name="年龄")
        account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
        create_time = models.DateTimeField(verbose_name="入职时间")
        depart = models.ForeignKey(to="Department", to_field="id", on_delete=models.CASCADE)
        gender_choices = (
            (1, "男"),
            (2, "女"),
        )
        gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    ```
  - views.py
  ```python
    class MyForm(ModelForm):
        xx = form.CharField*("...")
        class Meta:
            model = UserInfo
            fields = ["name","password","age","xx"]
     
     
    def user_add(request):
        if request.method == "GET":
            form = MyForm()
            return render(request, 'user_add.html',{"form":form})
    ```
  - user_add.html
  ```html
    <form method="post">
        {% for field in form%}
            {{ field }}
        {% endfor %}
        <!-- <input type="text"  placeholder="姓名" name="user" /> -->
    </form>
    ```
     
    ```html
    <form method="post">
        {{ form.user }}
        {{ form.pwd }}
        {{ form.email }}
        <!-- <input type="text"  placeholder="姓名" name="user" /> -->
    </form>
    ```