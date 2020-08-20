# Generated by Django 3.0.5 on 2020-08-19 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20200818_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='methodology',
            field=models.TextField(help_text='', verbose_name='Methodology'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_kind',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='organizations', to='organization.OrganizationKind', verbose_name='Organization Type'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_organizations', to='organization.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='source_detail_methodology',
            field=models.TextField(help_text='', verbose_name='Source detail and methodology'),
        ),
    ]