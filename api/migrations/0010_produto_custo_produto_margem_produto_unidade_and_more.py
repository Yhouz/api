# Generated by Django 5.2.2 on 2025-06-10 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_rename_dt_nacimento_funcionario_dt_nascimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='custo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='margem',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='unidade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='categoria',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
