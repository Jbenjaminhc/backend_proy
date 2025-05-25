from rest_framework import serializers
from api.data_access.models.presentacion import Presentacion

class PresentacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentacion
        fields = ['id', 'titulo', 'contenido', 'archivo', 'creada_en', 'colaboradores']
