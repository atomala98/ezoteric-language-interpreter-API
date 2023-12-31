# Generated by Django 4.2.4 on 2023-08-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_befungeprogram_alter_brainfuckprogram_status_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='befungeprogram',
            name='string_mode',
            field=models.IntegerField(choices=[('0', 'on'), ('1', 'off')], default='1'),
        ),
        migrations.AlterField(
            model_name='befungeprogram',
            name='current_direction',
            field=models.IntegerField(choices=[('0', 'rigth'), ('1', 'down'), ('2', 'left'), ('3', 'up')], default='0'),
        ),
    ]
