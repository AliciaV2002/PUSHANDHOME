# Generated by Django 5.0.2 on 2024-05-30 05:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Barrio',
            fields=[
                ('id_barrio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_barrio', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=100)),
                ('rol', models.CharField(choices=[('Arrendador', 'Arrendador'), ('Arrendatario', 'Arrendatario')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id_propiedad', models.AutoField(primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=200)),
                ('numero_contacto', models.CharField(max_length=20)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_bano', models.CharField(choices=[('Privado', 'Privado'), ('Compartido', 'Compartido')], max_length=20)),
                ('num_habitaciones', models.IntegerField()),
                ('tipo_propiedad', models.CharField(choices=[('Casa', 'Casa'), ('Apartamento', 'Apartamento'), ('Habitacion', 'Habitacion')], max_length=20)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('id_barrio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.barrio')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id_imagen', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.BinaryField()),
                ('id_propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pagina.propiedad')),
            ],
        ),
    ]
