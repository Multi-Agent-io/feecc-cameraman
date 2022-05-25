from fastapi import HTTPException, Header, status
from loguru import logger
from typed_getenv import getenv

from .database import MongoDbWrapper
from .models import Employee

TESTING_VALUE: str = "1111111111"
PRODUCTION_ENVIRONMENT: bool = getenv("PRODUCTION_ENVIRONMENT", optional=True, default=False, var_type=bool)


async def authenticate(rfid_card_id: str = Header(TESTING_VALUE)) -> Employee:
    try:
        if rfid_card_id == TESTING_VALUE and PRODUCTION_ENVIRONMENT:
            raise ValueError("Development credentials are not allowed in production environment")

        employee = await MongoDbWrapper().get_concrete_employee(rfid_card_id)
        logger.info(f"Authentication passed. {employee.name=}, {employee.rfid_card_id=}.")

        return employee

    except Exception as e:
        message = f"Authentication failed: {e}"
        logger.error(message)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
