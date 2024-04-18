from sqlmodel import Session, create_engine, select, SQLModel
from .config import basic_config
from .models import User
from .crud import create_user


engine = create_engine(str(basic_config.sqlite_uri))

DEFAULT_SUPERUSER_NAME = "root"
DEFAULT_SUPERUSER_PASSWORD = "123456"


def init_db() -> None:

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        super_user = session.exec(
            select(User).where(User.is_superuser == True)
        ).first()
        if not super_user:
            user = User(
                username=DEFAULT_SUPERUSER_NAME,
                password=DEFAULT_SUPERUSER_PASSWORD,
                is_superuser=True,
            )
            create_user(session=session, user=user)

