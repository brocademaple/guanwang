# Generated by Django 3.2.4 on 2023-04-03 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emrecord', '0003_auto_20230402_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='morder',
            name='imgmo1',
            field=models.ImageField(blank=True, help_text='请上传患者临时医嘱', null=True, upload_to='static/morder/', verbose_name='临时医嘱'),
        ),
        migrations.AlterField(
            model_name='morder',
            name='imgmo2',
            field=models.ImageField(blank=True, help_text='请上传患者长期医嘱', null=True, upload_to='static/morder/', verbose_name='长期医嘱'),
        ),
    ]
