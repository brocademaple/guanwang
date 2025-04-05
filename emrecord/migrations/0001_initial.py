# Generated by Django 3.2.4 on 2023-04-01 23:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pno', models.CharField(db_index=True, help_text='患者的住院号应该唯一', max_length=25, unique=True, verbose_name='住院号')),
            ],
            options={
                'db_table': 'emr_pno',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=25, verbose_name='患者姓名')),
                ('gender', models.IntegerField(choices=[(0, '未知'), (1, '男'), (2, '女')], default=0, help_text='请选择患者性别', verbose_name='性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('pno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emrecord.pno', verbose_name='住院号')),
            ],
            options={
                'verbose_name': '住院清单',
                'verbose_name_plural': '住院清单',
                'db_table': 'emr_pt',
            },
        ),
        migrations.CreateModel(
            name='Morder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imgmo1', models.ImageField(upload_to='static/morder/', verbose_name='临时医嘱')),
                ('imgmo2', models.ImageField(upload_to='static/morder/', verbose_name='长期医嘱')),
                ('remarks', models.TextField(blank=True, default='暂无', max_length=400, null=True, verbose_name='备注')),
                ('state', models.IntegerField(choices=[(0, '暂无医嘱'), (1, '存在医嘱')], default=0, editable=False, verbose_name='医嘱情况')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emrecord.patient', verbose_name='患者姓名')),
                ('pno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emrecord.pno', verbose_name='住院号')),
            ],
            options={
                'verbose_name': '医嘱',
                'verbose_name_plural': '医嘱',
                'db_table': 'emr_mo',
            },
        ),
    ]
