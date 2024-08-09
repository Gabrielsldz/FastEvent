from fastapi import APIRouter
from prisma.errors import UniqueViolationError
from prisma.errors import FieldNotFoundError
from datetime import timedelta
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from utils.utils import create_access_token
from prismadb import prisma
from models.user import User
from utils.utils import encrypt_password
from utils.utils import check_password
from utils.utils import validate_token

router = APIRouter(prefix='/user')

@router.post('/register_new_account')
async def create_user(user: User):
    try:
        user.password = encrypt_password(user.password)
        await prisma.user.create(data=user.dict())
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email ja existe",
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro durante a criacao do usuario.",
        )
    return {'name': user.name, 'age': user.age, 'password': user.password, 'email': user.email}


@router.post("/edit_user")
async def edit_user(user: User, request: Request):
    token = validate_token(request.headers)
    print(token)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )
    else:
        try:
            decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
            print(decoded_token)
            print(f"Token é válido! Decodificado: {decoded_token}")
            if decoded_token["sub"] != user.email:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Voce nao tem permissao para isso.",
                )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )

    try:
        print('SEXO')
        user.password = encrypt_password(user.password)
        await prisma.user.update(
            where={
                "email": user.email
            },
            data={
                "name": user.name,
                "age": user.age,
                "password": user.password,
                "email": user.email
            }
        )
    except FieldNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro durante a atualizacao do usuario.",
        )
    return {'name': user.name, 'age': user.age, 'password': user.password, 'email': user.email}


@router.get('/get_info')
async def get_info(request: Request):
    try:
        token = validate_token(request.headers)
        print(token)
        if token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        else:
            try:
                decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
                user_email = decoded_token["sub"]
                try:
                    user = await prisma.user.find_unique(
                        where={
                            "email": user_email
                        }
                    )
                    return {"name": user.name, "email": user.email, "age": user.age,
                            "eventsInterested": user.eventsInterested}
                except Exception as e:
                    print(e)
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Voce nao tem permissao para isso.",
                    )
            except ExpiredSignatureError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Voce nao tem permissao para isso.")
            except InvalidTokenError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Voce nao tem permissao para isso.")
                print("Token é inválido")
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )


@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        password = encrypt_password(form_data.password)
        try:
            user = await prisma.user.find_unique(
                where={
                    "email": form_data.username
                }
            )

        except FieldNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
            )

        if not check_password(user.password, form_data.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos"
            )
        access_token = create_access_token(
            data={"sub": form_data.username}, expires_delta=timedelta(hours=1)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
        )


@router.post("/delete_user")
async def delete_user(request: Request):
    try:
        token = validate_token(request.headers)
        decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
        try:

            await prisma.user.delete(where={
                "email": decoded_token["sub"]
            })

        except Exception as e:
            print("Could not find user")
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )

