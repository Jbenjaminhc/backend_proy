
from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # Ejecutar el seeder al finalizar la migración de la app
        post_migrate.connect(self.run_seed, sender=self)

    def run_seed(self, **kwargs):
        # Importar y ejecutar el seeder después de que las apps estén listas
        from .seeder.users import seed_users
        seed_users()  # Llama a tu script de seeding
