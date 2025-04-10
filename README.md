# Role Based Authorization and Authentication with DjangoRestFramework and SimpleJWT
##-----------activa el entorno virtual-----------
.\venv\Scripts\actívate
##-Ignorar el entorno virtual
venv/
__pycache__/
*.pyc
##------clonar usando el requirements.txt---------
pip install -r requirements.txt
  
/*
##--------activar entorno virtual----
.\venv\Scripts\activate
##---------- desactirvarlo-----------
deactivate

*/


##---correr el servidor para ver si conecta con posgret
python manage.py migrate
## -----------después para hacer funcionar el server...
python manage.py runserver