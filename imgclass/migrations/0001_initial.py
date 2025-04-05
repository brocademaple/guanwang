# Generated by Django 3.2.4 on 2023-04-01 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImgClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='请输入工点名称', max_length=15, verbose_name='工点名称')),
                ('image', models.ImageField(help_text='请上传需判断图像', upload_to='static/imgclass_img/', verbose_name='图像')),
                ('state', models.IntegerField(choices=[(0, '未知'), (1, '立即修复'), (2, '尽快修复'), (3, '无需修复')], default=0, editable=False, help_text='初步分类结果', verbose_name='分型')),
            ],
            options={
                'verbose_name': '缺陷分类',
                'verbose_name_plural': '辅助判断',
                'db_table': 'image_class',
            },
        ),
    ]
