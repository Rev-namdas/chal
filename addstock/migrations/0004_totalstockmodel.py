# Generated by Django 2.2.7 on 2020-01-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addstock', '0003_auto_20200119_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='totalStockModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('riceName', models.CharField(max_length=30)),
                ('amount', models.IntegerField()),
                ('bosta', models.IntegerField()),
            ],
        ),
    ]
