# Generated by Django 3.2.7 on 2021-10-05 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0002_auto_20211005_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('p', 'Patvirtinta'), ('v', 'Vykdoma'), ('a', 'Atlikta'), ('t', 'Atšaukta')], default='p', help_text='Status', max_length=1),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.FloatField(verbose_name='Price Eur.'),
        ),
    ]
