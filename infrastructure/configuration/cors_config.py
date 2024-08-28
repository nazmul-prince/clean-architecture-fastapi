from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_cors_middleware(app: FastAPI):
    allowed_origins = ["*"]
    allowed_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers = ["*", "Authorization", "Content-Type"]

    return CORSMiddleware(
        app=app,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=allowed_methods,
        allow_headers=allowed_headers,
    )
