# Generated by Django 5.0.2 on 2024-06-02 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagina', '0006_alter_propiedad_servicios'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagen',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]