from django.db import models
from django.conf import settings

class Presentacion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.JSONField()  # Estructura generada por OpenAI
    archivo = models.FileField(upload_to='presentaciones/', null=True, blank=True)
    creada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='presentaciones')
    colaboradores = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='colabora_en', blank=True)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
class VersionPresentacion(models.Model):
    presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE, related_name='versiones')
    contenido = models.JSONField()
    creado_en = models.DateTimeField(auto_now_add=True)