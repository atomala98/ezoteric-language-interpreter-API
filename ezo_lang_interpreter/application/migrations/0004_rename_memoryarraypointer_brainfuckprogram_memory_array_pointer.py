# Generated by Django 4.2.4 on 2023-08-21 21:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_remove_brainfuckprogram_length'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brainfuckprogram',
            old_name='memoryArrayPointer',
            new_name='memory_array_pointer',
        ),
    ]
