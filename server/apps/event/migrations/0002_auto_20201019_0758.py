# Generated by Django 3.0.5 on 2020-10-19 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crisis', '0002_auto_20201019_0758'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_event', to=settings.AUTH_USER_MODEL, verbose_name='Created By'),
        ),
        migrations.AddField(
            model_name='event',
            name='crisis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='crisis.Crisis', verbose_name='Crisis'),
        ),
        migrations.AddField(
            model_name='event',
            name='disaster_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.DisasterCategory', verbose_name='Disaster Category'),
        ),
        migrations.AddField(
            model_name='event',
            name='disaster_sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.DisasterSubCategory', verbose_name='Disaster Sub-Type'),
        ),
        migrations.AddField(
            model_name='event',
            name='disaster_sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.DisasterSubType', verbose_name='Disaster Sub-Type'),
        ),
        migrations.AddField(
            model_name='event',
            name='disaster_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.DisasterType', verbose_name='Disaster Type'),
        ),
        migrations.AddField(
            model_name='event',
            name='last_modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Last Modified By'),
        ),
        migrations.AddField(
            model_name='event',
            name='trigger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.Trigger', verbose_name='Trigger'),
        ),
        migrations.AddField(
            model_name='event',
            name='trigger_sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.TriggerSubType', verbose_name='Trigger Sub-Type'),
        ),
        migrations.AddField(
            model_name='event',
            name='violence',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.Violence', verbose_name='Violence'),
        ),
        migrations.AddField(
            model_name='event',
            name='violence_sub_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='event.ViolenceSubType', verbose_name='Violence Sub-Type'),
        ),
        migrations.AddField(
            model_name='disastertype',
            name='disaster_sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='event.DisasterSubCategory', verbose_name='Disaster Sub Category'),
        ),
        migrations.AddField(
            model_name='disastersubtype',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_types', to='event.DisasterType', verbose_name='Disaster Sub Type'),
        ),
        migrations.AddField(
            model_name='disastersubcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='event.DisasterCategory', verbose_name='Disaster Category'),
        ),
    ]