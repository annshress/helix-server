# Generated by Django 3.0.5 on 2020-09-18 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entry', '0007_merge_20200909_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sourcepreview',
            name='pdf',
            field=models.FileField(blank=True, null=True, upload_to='source/previews', verbose_name='Rendered Pdf'),
        ),
    ]
