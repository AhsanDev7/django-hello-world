# Generated by Django 5.1.3 on 2024-12-17 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_remove_orderitem_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_photo',
            field=models.ImageField(default='/media/example.jpg', upload_to='covers/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]