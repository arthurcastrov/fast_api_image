import os
from fastapi import FastAPI
from app.routers import process_image
import firebase_admin
from firebase_admin import credentials


service_account_info = {
    "type": "service_account",
    "project_id": os.getenv('SERVICE_ACCOUNT_PROJECT_ID'),
    "private_key_id": os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY_ID'),
    "private_key": os.getenv('SERVICE_ACCOUNT_PRIVATE_KEY').replace(r'\n', '\n'),
    "client_email": os.getenv('SERVICE_ACCOUNT_CLIENT_EMAIL'),
    "client_id": os.getenv('SERVICE_ACCOUNT_CLIENT_ID'),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv('SERVICE_ACCOUNT_CLIENT_X509_CERT_URL')
}

# Inicializa Firebase Admin con el archivo JSON de configuración
cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred)
app = FastAPI()

app.include_router(process_image.router, prefix='/api')