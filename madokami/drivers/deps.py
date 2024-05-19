from collections.abc import Generator
from typing import Annotated
from sqlmodel import Session
from ..db import engine
from fastapi import Depends, HTTPException, status, Header
from ..crud import get_oauth2_client


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]


def get_client_id(session: SessionDep, x_token: str = Header(...)) -> str:
    client = get_oauth2_client(session=session, token=x_token)
    if not client:
        raise HTTPException(status_code=409, detail="Client not found")
    return client.client_id


CurrentClient = Annotated[str, Depends(get_client_id)]