# Generated by Django 4.1.1 on 2022-09-20 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicians', '0005_musician_organisation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicians.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='musician',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='musicians.category'),
        ),
    ]