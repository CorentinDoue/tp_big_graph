# Generated by Django 2.1.4 on 2018-12-16 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unions', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='contibuted_unions',
            field=models.ManyToManyField(related_name='contributors', to='unions.Union'),
        ),
        migrations.AddField(
            model_name='user',
            name='personal_unions',
            field=models.ManyToManyField(related_name='members', to='unions.Union'),
        ),
    ]
