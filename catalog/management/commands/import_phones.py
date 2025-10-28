import csv
import os
from django.core.management.base import BaseCommand
from catalog.models import Phone


class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def handle(self, *args, **options):
        csv_file_path = r'D:/hw_projects_py/ORM1/phones.csv'

        self.stdout.write(f"Ищем файл: {csv_file_path}")

        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR('Файл phones.csv не найден по указанному пути!')
            )
            return

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file, delimiter=';')

                phones_created = 0
                for row in csv_reader:
                    phone, created = Phone.objects.get_or_create(
                        id=int(row['id']),
                        defaults={
                            'name': row['name'],
                            'price': int(row['price']),
                            'image': row['image'],
                            'release_date': row['release_date'],
                            'lte_exists': row['lte_exists'] == 'True',
                        }
                    )

                    if created:
                        phones_created += 1
                        self.stdout.write(f'Добавлен: {row["name"]}')
                    else:
                        self.stdout.write(f'Уже существует: {row["name"]}')

                self.stdout.write(
                    self.style.SUCCESS(f'Импорт завершен! Добавлено: {phones_created} телефонов')
                )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {e}'))