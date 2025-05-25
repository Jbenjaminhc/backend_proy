from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import FileResponse, Http404
from api.data_access.generator import generar_contenido, generar_pptx
from api.data_access.models import Presentacion
from api.business_logic.presentaciones.serializers import PresentacionSerializer
from api.models import User
from api.data_access.models.presentacion import Presentacion, VersionPresentacion

class GenerarPresentacionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        prompt = request.data.get('prompt')

        # Verifica si es cliente con límite
        if user.has_role("Cliente") and Presentacion.objects.filter(creada_por=user).count() >= 1:
            return Response({"error": "Solo se permite una presentación para cuentas gratuitas"}, status=403)

        # Genera contenido usando OpenAI
        slides = generar_contenido(prompt)

        # Guarda archivo pptx
        nombre_archivo = f"presentacion_{user.id}"
        ruta_archivo = generar_pptx(slides, nombre_archivo)

        # Crear la presentación
        presentacion = Presentacion.objects.create(
            titulo=prompt,
            contenido=slides,
            creada_por=user
        )
        #  Asigna solo la parte relativa
        presentacion.archivo.name = f"presentaciones/{nombre_archivo}.pptx"
        presentacion.save()

        # Guarda versión inicial
        VersionPresentacion.objects.create(
            presentacion=presentacion,
            contenido=slides
        )

        serializer = PresentacionSerializer(presentacion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListarPresentacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        presentaciones = Presentacion.objects.filter(creada_por=request.user)
        serializer = PresentacionSerializer(presentaciones, many=True)
        return Response(serializer.data)


class DescargarPresentacionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            presentacion = Presentacion.objects.get(pk=pk)
            if request.user != presentacion.creada_por and not request.user in presentacion.colaboradores.all():
                return Response({"error": "No autorizado."}, status=403)

            ruta = presentacion.archivo.path
            return FileResponse(open(ruta, 'rb'), as_attachment=True, filename=presentacion.titulo + ".pptx")
        except Presentacion.DoesNotExist:
            raise Http404("Presentación no encontrada")


class AgregarColaboradorView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        email = request.data.get('email')
        try:
            colaborador = User.objects.get(email=email)
            presentacion = Presentacion.objects.get(pk=pk, creada_por=request.user)
            presentacion.colaboradores.add(colaborador)
            return Response({"message": "Colaborador añadido"})
        except:
            return Response({"error": "No se pudo añadir colaborador"}, status=400)


class ActualizarContenidoView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            presentacion = Presentacion.objects.get(pk=pk, creada_por=request.user)
            nuevo_contenido = request.data.get('contenido')

            if not isinstance(nuevo_contenido, list):
                return Response({"error": "Formato inválido."}, status=400)

            # Guardar versión anterior
            VersionPresentacion.objects.create(presentacion=presentacion, contenido=presentacion.contenido)

            presentacion.contenido = nuevo_contenido
            presentacion.save()
            return Response({"message": "Cambios guardados y versión anterior registrada."})

        except Presentacion.DoesNotExist:
            return Response({"error": "Presentación no encontrada."}, status=404)