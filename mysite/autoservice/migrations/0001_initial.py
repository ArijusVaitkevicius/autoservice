# Generated by Django 3.2.7 on 2021-10-05 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AutomobilioModelis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marke', models.CharField(help_text='Įveskite automobilio markę (pvz. Audi)', max_length=200, verbose_name='Marke')),
                ('modelis', models.CharField(help_text='Įveskite automobilio modelį (pvz. A6)', max_length=200, verbose_name='Modelis')),
            ],
        ),
        migrations.CreateModel(
            name='Automobilis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valstybinis_nr', models.CharField(help_text='Įveskite automobilio valstybinį numerį', max_length=200, verbose_name='Valstybinis numeris')),
                ('vin_kodas', models.CharField(help_text='Įveskite automobilio VIN kodą', max_length=200, verbose_name='VIN kodas')),
                ('klientas', models.CharField(help_text='Įveskite kliento vardą ir pavardę', max_length=200, verbose_name='Klientas')),
                ('automobilio_modelis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.automobiliomodelis')),
            ],
        ),
        migrations.CreateModel(
            name='Paslauga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pavadinimas', models.CharField(help_text='Įveskite pavadinimą', max_length=200, verbose_name='Pavadinimas')),
                ('kaina', models.FloatField(help_text='Įveskite kainą', verbose_name='Kaina')),
            ],
        ),
        migrations.CreateModel(
            name='Uzsakymas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(help_text='Įveskite datą', max_length=200, verbose_name='Data')),
                ('suma', models.FloatField(help_text='Įveskite sumą', null=True, verbose_name='Suma')),
                ('automobilis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.automobilis')),
            ],
        ),
        migrations.CreateModel(
            name='UzsakymoEilute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kiekis', models.IntegerField(help_text='Įveskite kiekį', verbose_name='Kiekis')),
                ('kaina', models.FloatField(help_text='Įveskite kainą', null=True, verbose_name='Kaina')),
                ('paslauga', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.paslauga')),
                ('uzsakymas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='autoservice.uzsakymas')),
            ],
        ),
    ]
