# Generated by Django 4.2.4 on 2023-08-28 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0009_whitespaceprogram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='befungeprogram',
            name='status_code',
            field=models.CharField(choices=[('Run', 'Running'), ('Fin', 'Finished'), ('Wfc', 'Waiting for character input'), ('Wfn', 'Waiting for numeric input'), ('Oot', 'Out of time'), ('Ool', 'Loop stack out of memory'), ('Oom', 'Out of memory'), ('Mcb', 'Missing closing bracket'), ('Mob', 'Missing opening bracket'), ('Ooo', 'Output out of memory'), ('Wpc', 'Wrong program code'), ('Nei', 'No end instruction')], max_length=3),
        ),
        migrations.AlterField(
            model_name='brainfuckprogram',
            name='status_code',
            field=models.CharField(choices=[('Run', 'Running'), ('Fin', 'Finished'), ('Wfc', 'Waiting for character input'), ('Wfn', 'Waiting for numeric input'), ('Oot', 'Out of time'), ('Ool', 'Loop stack out of memory'), ('Oom', 'Out of memory'), ('Mcb', 'Missing closing bracket'), ('Mob', 'Missing opening bracket'), ('Ooo', 'Output out of memory'), ('Wpc', 'Wrong program code'), ('Nei', 'No end instruction')], default='Run', max_length=3),
        ),
        migrations.AlterField(
            model_name='whitespaceprogram',
            name='status_code',
            field=models.CharField(choices=[('Run', 'Running'), ('Fin', 'Finished'), ('Wfc', 'Waiting for character input'), ('Wfn', 'Waiting for numeric input'), ('Oot', 'Out of time'), ('Ool', 'Loop stack out of memory'), ('Oom', 'Out of memory'), ('Mcb', 'Missing closing bracket'), ('Mob', 'Missing opening bracket'), ('Ooo', 'Output out of memory'), ('Wpc', 'Wrong program code'), ('Nei', 'No end instruction')], max_length=3),
        ),
    ]