# Generated by Django 3.2.4 on 2023-04-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgseg', '0002_image_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='icon',
            field=models.ImageField(help_text='请上传需处理图像', upload_to='static/icon/', verbose_name='图像'),
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(help_text='请输入工点名称', max_length=15, verbose_name='工点名称'),
        ),
    ]
