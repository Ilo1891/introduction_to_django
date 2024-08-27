from django.core.management import BaseCommand
from catalog.models import Category, Product
import json
from pathlib import Path


class Command(BaseCommand):

    @staticmethod
    def json_read_categories(path):
        with open(path, 'r') as file:
            data = json.load(fp=file)
        categories = []
        for model in data:
            if model["model"] == "catalog.category":
                categories.append(model)
        return categories

    @staticmethod
    def json_read_products(path):
        with open(path, 'r') as file:
            data = json.load(fp=file)
        products = []
        for model in data:
            if model["model"] == "catalog.products":
                products.append(model)
        return products

    def handle(self, *args, **options):
        fixture_path = Path(Path(__file__).parent.parent.parent.parent, "all_data.json")

        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фиктсуры для получения информации об одном объекте
        for category in Command.json_read_categories(fixture_path):
            category_for_create.append(
                Category(name=category['fields']['name'],
                         description=category['fields']['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фиктсуры для получения информации об одном объекте
        for product in Command.json_read_products(fixture_path):
            product_for_create.append(
                Product(name=product['fields']['name'],
                        description=product['fields']['description'],
                        image=product['fields']['image'],
                        # получаем категорию из базы данных для корректной связки объектов
                        category=Category.objects.get(pk=product['fields']['category']),
                        price=product['fields']['price'],
                        created_at=product['fields']['created_at'],
                        updated_at=product['fields']['updated_at'],
                        )
            )

            # Создаем объекты в базе с помощью метода bulk_create()
            Product.objects.bulk_create(product_for_create)
