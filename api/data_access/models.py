from django.db import models
from django.contrib.auth.models import User

class Presentacion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentaciones")
    titulo = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='presentaciones/')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"
