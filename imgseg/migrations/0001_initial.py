# Generated by Django 3.2.4 on 2023-03-29 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='工点名称')),
                ('icon', models.ImageField(upload_to='static/icon/', verbose_name='图像')),
                # ('crack_width', models.FloatField(blank=True, null=True, verbose_name='裂隙宽度')),  # 添加裂隙宽度字段
                # ('crack_area', models.FloatField(blank=True, null=True, verbose_name='裂隙面积')),  # 添加裂隙面积字段
            ],
            options={
                'verbose_name': '缺陷识别',
                'verbose_name_plural': '图像处理',
                'db_table': 'imgseg_image',
            },
        ),
    ]
