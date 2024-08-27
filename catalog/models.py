from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name="name")
    description = models.CharField(max_length=64, verbose_name="description")

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Categy'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name="name")
    description = models.CharField(max_length=64, verbose_name="description")
    image = models.ImageField(upload_to="media/catalog", verbose_name="image")
    price = models.IntegerField(verbose_name="price")
    created_at = models.DateField(verbose_name="created", auto_now_add=True)
    update_at = models.DateField(verbose_name="updated", auto_now=True)
    manufactured_at = models.DateField(verbose_name="manufactured", auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="category")

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def __str__(self):
        return self.name
