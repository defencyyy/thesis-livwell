# Generated by Django 5.1.2 on 2024-10-25 02:24


from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True)),
                ('reward', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('broker', 'Broker'), ('company', 'Company')], default='company', max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]