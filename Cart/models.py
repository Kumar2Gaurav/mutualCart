from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    type =  models.CharField(max_length=256, blank=True, null=True)
    description =  models.CharField(max_length=2096, blank=True, null=True)
    filename = models.CharField(max_length=256, blank=True, null=True)
    height = models.CharField(max_length=256, blank=True, null=True)
    width = models.CharField(max_length=256, blank=True, null=True)
    price = models.FloatField(default=0)
    rating = models.FloatField(default=0)

    class Meta:
        db_table = "mutual_product"

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    product_map = models.ForeignKey(Product, db_column='created_by', blank=True, null=True,on_delete=models.CASCADE, related_name="products_cart")
    product_count = models.IntegerField(default=0)

    class Meta:
        db_table = "mutual_cart"

    def __str__(self):
        return str(self.product_map.title),(self.product_count)






