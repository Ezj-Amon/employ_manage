# Generated by Django 4.1.7 on 2023-03-21 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_alter_userinfo_create_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=11, verbose_name='手机号')),
                ('price', models.IntegerField(default=0, verbose_name='价格')),
                ('level', models.SmallIntegerField(choices=[(5, '黑铁'), (2, '黄金'), (1, '钻石'), (3, '白银'), (4, '青铜')], default=5, verbose_name='级别')),
                ('status', models.SmallIntegerField(choices=[(1, '已使用'), (2, '未使用')], default=2, verbose_name='状态')),
            ],
        ),
    ]