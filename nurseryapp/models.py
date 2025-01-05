from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    password=models.CharField(max_length=50)
    role=models.IntegerField()


class Contact(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    number=models.IntegerField()
    message=models.TextField(max_length=509)
    # def __str__(self):
    #     return self.name


class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=100, default="")
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    image = models.CharField(max_length=1000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    def __str__(self):
        return self.product_name

class ProductCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    qunatity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

