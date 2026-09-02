from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.url import URLCreate, URLResponse
from app.services.url_service import URLService

router = APIRouter(
    prefix="/shorten",
    tags=["URL Shortener"]
)

@router.post(
    "",
    response_model=URLResponse,
    status_code=201
)
def create_short_url(
    url: URLCreate,
    db: Session = Depends(get_db)
):
    service = URLService()

    return service.create_short_url(
        db=db,
        original_url=str(url.original_url)
    )