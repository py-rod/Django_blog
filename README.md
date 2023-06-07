El primer paso para que el proyecto funcione es crear un entorno virtual. Para ello, vamos a usar el siguiente comando en la terminal:

python -m venv venv

Presionamos enter y se creará la carpeta de nuestro entorno virtual. Ahora necesitamos activar nuestro entorno virtual.

Linux:
source ./venv/bin/activate

Windows:
venv\Scripts\activate.bat

Luego de eso, necesitamos instalar todos los pip de requirements.txt. Utilizaremos el siguiente comando:

pip install -r requirements.txt

Luego de eso, necesitamos crear dentro de la carpeta core un archivo llamado .env. Y dentro de este archivo irá lo siguiente:

En SECRET_KEY es necesario que generen una llave y ponerla aquí, después del signo igual.

SECRET_KEY=

En DEBUG podemos poner True.

DEBUG=True

Aquí necesitan crear sus propias llaves para poder utilizar el captcha. Para obtener las llaves pueden ir a este sitio y crearlas:

https://www.google.com/recaptcha/admin

Una vez ya creadas, las ponen abajo donde dice RECAPTCHA_PUBLIC_KEY y RECAPTCHA_PRIVATE_KEY. Después del signo igual.

RECAPTCHA_PUBLIC_KEY=

RECAPTCHA_PRIVATE_KEY=

Esta parte se encarga de enviar a nuestro correo un token de activación de cuenta. No es necesario que realicen esta configuración a no ser que quieran ver cómo funciona.

Para poder saltar esta parte, es necesario que modifiquemos nuestro modelo que se encuentra dentro de la carpeta users. Dentro de la carpeta, buscan el archivo .py que se llame models.py. Y dentro de este archivo está nuestro modelo de usuarios.

Dentro del archivo, buscar la clase llamada CustomUser y dentro, buscar la variable que se llama is_active. Por defecto, está en False, es de pasarlo a True y listo.

EMAIL_FROM=

EMAIL_HOST_USER=

EMAIL_HOST_PASSWORD=


Aquí van todos los datos relacionados con la base de datos para hacer la conexión (utilizamos Postgres).

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=


Por último, solo nos queda ejecutar los siguientes comandos:

python manage.py makemigrations

python manage.py migrate


Y para levantar nuestro sitio:


python manage.py runserver
