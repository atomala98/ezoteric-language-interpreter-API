# Generated by Django 4.2.4 on 2023-08-24 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_brainfuckprogram_loop_stack_pointer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BefungeProgram',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('code', models.TextField()),
                ('name', models.CharField(max_length=30)),
                ('output', models.TextField(default='')),
                ('memory_stack', models.TextField()),
                ('memory_stack_pointer', models.IntegerField(default=-1)),
                ('ptr_x', models.IntegerField(default=0)),
                ('ptr_y', models.IntegerField(default=0)),
                ('max_x', models.IntegerField()),
                ('max_y', models.IntegerField()),
                ('current_direction', models.IntegerField(choices=[('0', 'up'), ('1', 'rigth'), ('2', 'down'), ('3', 'left')], default='1')),
                ('status_code', models.CharField(choices=[('Run', 'Running'), ('Fin', 'Finished'), ('Wfc', 'Waiting for character input'), ('Wfn', 'Waiting for numeric input'), ('Oot', 'Out of time'), ('Ool', 'Loop stack out of memory'), ('Oom', 'Out of memory'), ('Mcb', 'Missing closing bracket'), ('Mob', 'Missing opening bracket')], max_length=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='brainfuckprogram',
            name='status_code',
            field=models.CharField(choices=[('Run', 'Running'), ('Fin', 'Finished'), ('Wfc', 'Waiting for character input'), ('Wfn', 'Waiting for numeric input'), ('Oot', 'Out of time'), ('Ool', 'Loop stack out of memory'), ('Oom', 'Out of memory'), ('Mcb', 'Missing closing bracket'), ('Mob', 'Missing opening bracket')], default='Run', max_length=3),
        ),
    ]