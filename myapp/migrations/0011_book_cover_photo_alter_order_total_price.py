# Generated by Django 5.1.3 on 2024-12-17 11:29

import django.db.models.deletion
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

        migrations.RenameField(
            model_name='bookgenre',
            old_name='book',
            new_name='books',
        ),
        migrations.CreateModel(
            name='BookAuthors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.author')),
                ('books', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.book')),
            ],
        ),
    ]
