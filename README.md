
# Инструкция по настройке и выполнению проекта по домашней работе

**Задание 1: Подключение СУБД PostgreSQL**

1. **Создайте базу данных PostgreSQL вручную.**
2. **Настройки подключения:**
   - В файле `settings.py` вашего проекта Django внесите изменения в раздел `DATABASES` на следующие:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_database_name',  # имя вашей базы данных
             'USER': 'your_database_user',  # имя пользователя базы данных
             'PASSWORD': 'your_database_password',  # пароль пользователя
             'HOST': 'localhost',  # или IP адрес вашего сервера
             'PORT': '5432',  # стандартный порт для PostgreSQL
         }
     }
     ```

**Задание 2: Создание моделей**

1. **Модели Product и Category:**
   - В приложении каталога (`catalog`) создайте файл `models.py` с содержимым:
     ```python
     from django.db import models

     class Category(models.Model):
         name = models.CharField(max_length=255, verbose_name="Наименование")
         description = models.TextField(verbose_name="Описание")

         def __str__(self):
             return self.name

         class Meta:
             verbose_name = "Категория"
             verbose_name_plural = "Категории"

     class Product(models.Model):
         name = models.CharField(max_length=255, verbose_name="Наименование")
         description = models.TextField(verbose_name="Описание")
         image = models.ImageField(upload_to='products/', verbose_name="Изображение")
         category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
         price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена за покупку")
         created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
         updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

         def __str__(self):
             return self.name

         class Meta:
             verbose_name = "Продукт"
             verbose_name_plural = "Продукты"
     ```

**Задание 3: Настройки полей и связи**

1. **Поля моделей описаны в `models.py` выше.**
2. **Связь «Один ко многим» реализована с помощью ForeignKey.**

**Задание 4: Миграции и изменения в модели**

1. **Создание и применение миграций:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **Добавление поля `manufactured_at`:**
   ```python
   class Product(models.Model):
       # предыдущее содержание
       manufactured_at = models.DateField(verbose_name="Дата производства продукта", null=True, blank=True)
   ```
   - **Создание и применение миграций:**
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
3. **Откат миграции и удаление лишней:**
   ```bash
   python manage.py migrate catalog 0001
   ```

**Задание 5: Настройка отображения в административной панели**

1. **Файл `admin.py` вашего приложения `catalog`:**
   ```python
   from django.contrib import admin
   from .models import Product, Category

   @admin.register(Category)
   class CategoryAdmin(admin.ModelAdmin):
       list_display = ('id', 'name')

   @admin.register(Product)
   class ProductAdmin(admin.ModelAdmin):
       list_display = ('id', 'name', 'price', 'category')
       list_filter = ('category',)
       search_fields = ('name', 'description')
   ```

**Задание 6: Заполнение данных через shell и фикстуры**

1. **Установка ipython и обновление зависимостей:**
   ```bash
   pip install ipython
   pip freeze > requirements.txt
   ```
2. **Заполнение категорий и их фильтрация:**
   ```bash
   python manage.py shell

   from catalog.models import Category
   Category.objects.create(name="Электроника", description="Описание для электроники")
```

```

   Category.objects.create(name="Книги", description="Описание для книг")
   categories = Category.objects.filter(name__icontains="Электро")

   print(categories)
   ```
3. **Создание фикстур:**
   ```bash
   python -Xutf8 manage.py dumpdata catalog > fixtures/catalog_data.json
   ```

4. **Кастомная команда для заполнения данных:**
   - Создайте файл `management/commands/populate_db.py` в вашем приложении `catalog` и добавьте следующий код:
     ```python
     from django.core.management.base import BaseCommand
     from catalog.models import Category, Product

     class Command(BaseCommand):
         help = 'Заполняет базу данных начальными данными'

         def handle(self, *args, **kwargs):
             # Удаляем все старые данные
             Category.objects.all().delete()
             Product.objects.all().delete()

             # Создаем новые категории
             electronics = Category.objects.create(name="Электроника", description="Описание для электроники")
             books = Category.objects.create(name="Книги", description="Описание для книг")

             # Создаем новые продукты
             Product.objects.create(name="Смартфон", description="Описание смартфона", image="path/to/image.jpg", category=electronics, price=1000)
             Product.objects.create(name="Книга", description="Описание книги", image="path/to/image2.jpg", category=books, price=500)

             self.stdout.write(self.style.SUCCESS('Данные успешно заполнены'))
     ```

**Дополнительное задание: Вывод последних пяти товаров и контактные данные**

1. **Вывод последних пяти товаров:**
   - В контроллере главной страницы:
     ```python
     from catalog.models import Product

     def home(request):
         latest_products = Product.objects.all().order_by('-created_at')[:5]
         for product in latest_products:
             print(product)
         # остальной код контроллера
     ```

2. **Модель для хранения контактных данных:**
   - Создайте новую модель `Contact`:
     ```python
     class Contact(models.Model):
         name = models.CharField(max_length=255, verbose_name="Имя")
         email = models.EmailField(verbose_name="Электронная почта")
         phone = models.CharField(max_length=20, verbose_name="Телефон")
         message = models.TextField(verbose_name="Сообщение")

         def __str__(self):
             return self.name

         class Meta:
             verbose_name = "Контакт"
             verbose_name_plural = "Контакты"
     ```

   - Вывод контактов на страницу с контактами:
     ```python
     from catalog.models import Contact

     def contact_view(request):
         contacts = Contact.objects.all()
         return render(request, 'contact_page.html', {'contacts': contacts})
     ```

Не забудьте добавить все миграции в ваш коммит:

```bash
git add .
git commit -m "Configured database, created models, applied migrations, and added administrative panel settings"
git push origin main
```
```