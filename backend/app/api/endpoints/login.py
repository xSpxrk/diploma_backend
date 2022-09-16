from datetime import timedelta
from typing import Any
import os
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend.app.core.security import hash_password
from backend.app import crud, models, schemas
from backend.app.api import deps
from backend.app.core import security
import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

router = APIRouter()


@router.post("/token", response_model=schemas.Token)
def login_access_token(
        *,
        db: Session = Depends(deps.get_db),
        login: schemas.Login
) -> Any:
    user = crud.customer.authenticate(db, email=login.username, password=login.password)
    type = "customer"
    if not user:
        user = crud.provider.authenticate(db, email=login.username, password=login.password)
        type = "provider"
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": security.create_access_token(
            user.customer_id if type == "customer" else user.provider_id,
            type,
            expires_delta=None
        ),
        "token_type": "bearer",
        "type": type
    }


@router.post("/reset-password")
def reset_password(
        *,
        email: schemas.Email,
        db: Session = Depends(deps.get_db)
) -> Any:
    def generate_new_password() -> str:
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(8))

    def send_new_password(user, new_password):
        def parse_template(file_name):
            with open(file_name, 'r', encoding='utf-8') as msg_template:
                content = msg_template.read()
                return Template(content)

        template = parse_template('backend/app/api/endpoints/reset_template.txt')

        FROM_EMAIL = os.getenv('FROM_EMAIL')
        PASSWORD = os.getenv('PASSWORD')

        smtp_server = smtplib.SMTP_SSL(host='smtp.mail.ru', port=465)
        smtp_server.login(FROM_EMAIL, PASSWORD)
        message = template.substitute(USER_NAME=user.name, PASSWORD=new_password)
        multipart_msg = MIMEMultipart()

        multipart_msg['From'] = FROM_EMAIL
        multipart_msg['To'] = user.email
        multipart_msg['Subject'] = 'Новый пароль'
        multipart_msg.attach(MIMEText(message, 'plain'))

        smtp_server.send_message(multipart_msg)
        smtp_server.quit()

    user = crud.customer.get_by_email(db, email.email)
    type = "customer"
    if not user:
        type = "provider"
        user = crud.provider.get_by_email(db, email.email)
        if not user:
            raise HTTPException(status_code=400, detail="User doesn't exist")

    new_password = generate_new_password()
    send_new_password(user, new_password)

    if type == 'customer':
        new_user = schemas.CustomerCreate(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            password=new_password
        )
        user = crud.customer.update(db, user, new_user)
    else:
        new_user = schemas.ProviderCreate(
            name=user.name,
            email=user.email,
            phone_number=user.phone_number,
            password=new_password
        )
        user = crud.provider.update(db, user, new_user)
    return 'success'
