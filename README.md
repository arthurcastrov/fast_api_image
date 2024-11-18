# PoC Procesar imagen en Firebase o GCP

Recibir imagen validar authenticacion y devolver la imagen en escala de grises.

## Generar config.json en Firebase

- Ingrese a la consola de Firebase
- En settings⚙️ seleccione **Project settings**
- Seleccione la pestaña de **Service accounts**
- De click en el boton **Generate new private key**

**Nota: Almacene de forma segura la llave generada**

## Ejecucion local

Adicione un archivo .env con las siguientes variables, y reemplace el valor por los entregados en el config.json generado en el paso anterior.

```shell
SERVICE_ACCOUNT_PROJECT_ID="project_id"
SERVICE_ACCOUNT_PRIVATE_KEY_ID="private_key_id"
SERVICE_ACCOUNT_PRIVATE_KEY="private_key"
SERVICE_ACCOUNT_CLIENT_EMAIL="client_email"
SERVICE_ACCOUNT_CLIENT_ID="client_id"
SERVICE_ACCOUNT_CLIENT_X509_CERT_URL="client_x509_cert_url"
```

Ejecute los siguientes comandos para ejecutar la aplicacion


```shell
Python3 -m venv venv
source ./env/bin/activate
python -m pip install -r requirements.txt
uvicorn app.main:app
```
Nota: No se usa ```fastapi run env``` para ejecutar con las mismas condiciones del docker

## docker

Construir la imagen 

```shell
 docker build -t fastapi-app . 
```
Ejecutar la imagen


```shell

docker run --env-file .env -p 8000:8000 fastapi-app

docker run -it --entrypoint bash fastapi-app
```


## Tecnologias utilizadas
1. Python(FastApi) 
2. Firebase
3. Docker
4. Postman
