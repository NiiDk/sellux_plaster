from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    base_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"

class ShippingSetting(models.Model):
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter percentage, e.g., 15 for 15%")
    delivery_fee_per_100 = models.DecimalField(max_digits=10, decimal_places=2, help_text="Additional fee per 100 GHS worth of goods")

    def __str__(self):
        return "General Shipping and Tax Settings"

    class Meta:
        verbose_name_plural = "Shipping Settings"
