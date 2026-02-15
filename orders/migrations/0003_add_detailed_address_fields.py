# Generated migration for detailed address fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='street_address',
            field=models.CharField(blank=True, help_text='e.g., 123 Osu Street', max_length=250),
        ),
        migrations.AddField(
            model_name='order',
            name='building_number',
            field=models.CharField(blank=True, help_text='House/Building number', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='region',
            field=models.CharField(blank=True, help_text='Region/District', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Postal or ZIP code', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, help_text='Kept for backward compatibility', max_length=250),
        ),
    ]
