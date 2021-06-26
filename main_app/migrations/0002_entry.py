# Generated by Django 3.2.4 on 2021-06-26 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('date', models.DateField(null=True)),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.journal')),
            ],
        ),
    ]
