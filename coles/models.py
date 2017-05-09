from django.db import models

class Product(models.Model):
    '''
    Product model stores recorded data for a product special
    '''
    # Type of special
    MULTI_BUY = "MB"
    REDUCED_PRICE = "RP"
    SPECIAL_TYPE_CHOICES=(
        (MULTI_BUY, "Multi Buy"),
        (REDUCED_PRICE, "Reduced Price")
    )
    # Members
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qty = models.IntegerField()
    pkg_qty = models.IntegerField()
    special_type = models.CharField(max_length=2, choices=SPECIAL_TYPE_CHOICES, default = REDUCED_PRICE)
    date_recorded = models.DateField(auto_now_add = True)

    def __str__(self):
        return "{brand} {name}".format(brand = self.brand, name = self.name)
