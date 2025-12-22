"""
Команда для ожидания готовности БД перед запуском приложения
"""
import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    """Django команда для ожидания БД"""
    
    def handle(self, *args, **options):
        self.stdout.write('Ожидание подключения к БД...')
        db_conn = None
        attempts = 0
        
        while not db_conn:
            try:
                connections['default'].ensure_connection()
                db_conn = True
            except OperationalError:
                attempts += 1
                self.stdout.write(f'Попытка {attempts}/30: БД недоступна, ждем 2 секунды...')
                time.sleep(2)
                
                if attempts > 30:
                    self.stdout.write(self.style.ERROR('Не удалось подключиться к БД!'))
                    return
        
        self.stdout.write(self.style.SUCCESS('БД доступна!'))