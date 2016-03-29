# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-28 18:22
from __future__ import unicode_literals

import colorfield.fields
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PosicionAnden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Shapefile',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('color', colorfield.fields.ColorField(max_length=10)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='ShapefileLine',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('color', colorfield.fields.ColorField(max_length=10)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='ShapefilePoint',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('color', colorfield.fields.ColorField(max_length=10)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='TipoEstaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='estaciones',
            name='anden',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geoportal.Shapefile'),
        ),
        migrations.AddField(
            model_name='estaciones',
            name='posicion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geoportal.PosicionAnden'),
        ),
    ]
