from models.events import Event
from io import BytesIO
from fastapi import APIRouter
import base64
from prisma.errors import UniqueViolationError
from fastapi import File, UploadFile, Form
import jwt
from fastapi import HTTPException, status, Request
from prismadb import prisma
from fastapi import Body

router = APIRouter(prefix='/event')


# CRIAR FUNCAO PARA AUTHORIZATION HEADER (USADA EM TODAS(QUASE TODAS) AS FUNCOES)

@router.post('/get_interested')
async def get_interested(request: Request, data: dict = Body(...)):
    try:
        json_data = data
        header_authorization = request.headers.get('authorization')
        token = header_authorization[7:] if header_authorization and header_authorization.startswith(
            "Bearer ") else None
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para acessar",
        )
    if token:
        try:
            decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
            user_email = decoded_token["sub"]
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token invalido",
            )
        try:
            user = await prisma.user.find_unique(
                where={
                    "email": user_email
                })
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )
        if user:
            try:
                event = await prisma.events.find_unique(where={"id": json_data["event_id"]})
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Evento nao encontrado",
                )
            try:
                await prisma.eventinterest.create(
                    data={"userId": user.id, "eventId": json_data["event_id"]})
                return f"{user.name} marcou interesse no evento: {event.name}"
            except UniqueViolationError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Usuario ja marcou interesse no evento: {event.name}",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Voce nao tem permissao para isso.",
            )


@router.post('/create_event')
async def create_event(event: Event, request: Request):
    try:
        header_authorization = request.headers.get('authorization')
        token = header_authorization[7:] if header_authorization and header_authorization.startswith(
            "Bearer ") else None
        decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
        user_email = decoded_token["sub"]
        print(user_email)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )
    try:
        user = await prisma.user.find_unique(
            where={
                "email": user_email
            })
        if user:
            event_dict = event.dict()
            print(event_dict)
            event_dict["creatorId"] = user.id
            print(event_dict)
            event = await prisma.events.create(data=event_dict)
            return event_dict
            pass
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao encontrado.",
        )


@router.post('/add_banner')
async def add_banner(request: Request, image: UploadFile = File(...), event_id: str = Form(...)):
    print(event_id)
    header_authorization = request.headers.get('authorization')
    token = header_authorization[7:] if header_authorization and header_authorization.startswith("Bearer ") else None
    decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
    user_email = decoded_token["sub"]
    print(user_email)

    try:
        image_in_bytes = BytesIO(await image.read())
        base64_encoded = base64.b64encode(image_in_bytes.getvalue()).decode()

        user = await prisma.user.find_unique(
            where={
                "email": str(user_email)

            })
        print(user.dict())

        if user:
            await prisma.events.update(where={"id": event_id}, data={"banner": base64_encoded})
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario nao encontrado.",
            )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )


@router.get("/get_events_interested")
async def get_events_interested(request: Request):
    try:
        authorization_header = request.headers.get("authorization")
        token = authorization_header[7:] if authorization_header and authorization_header.startswith(
            "Bearer ") else None
        decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
        user_email = decoded_token["sub"]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )
    try:
        user = await prisma.user.find_unique(
            where={
                "email": user_email
            },
            include={
                "eventsInterested": True
            }
        )
        dict_return = user.dict()
        return dict_return["eventsInterested"]
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Voce nao tem permissao para isso.",
        )


@router.get("/get_events_created")
async def get_events_created(request: Request):
    authorization_header = request.headers.get("authorization")
    token = authorization_header[7:] if authorization_header and authorization_header.startswith("Bearer ") else None
    decoded_token = jwt.decode(token, "batatafricacombanana", algorithms=["HS256"])
    user_email = decoded_token["sub"]
    user = await prisma.user.find_unique(
        where={
            "email": user_email
        },
        include={
            "eventsCreated": True
        }
    )


@router.get("/get_events")
async def get_events_created(request: Request):
    events = await prisma.events.find_many()
    print(events)
    return events
