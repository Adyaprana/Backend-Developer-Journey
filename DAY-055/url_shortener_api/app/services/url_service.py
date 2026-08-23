import random
import string
from sqlalchemy.orm import Session
from app.models.shortened_url import ShortenedURL
from app.repositories.url_repository import URLRepository


class URLService:
    """
    Handles business logic for URL shortening.
    """
    CODE_LENGTH = 6
    def __init__(self):
        self.repository = URLRepository()
    def generate_short_code(self) -> str:
        """
        Generate a unique short code.
        """
        characters = string.ascii_letters + string.digits
        return "".join(
            random.choice(characters)
            for _ in range(self.CODE_LENGTH)
        )
    def create_short_url(
        self,
        db: Session,
        original_url: str
    ) -> ShortenedURL:
        while True:
            short_code = self.generate_short_code()
            existing_url = self.repository.get_by_short_code(
                db,
                short_code
            )
            if existing_url is None:
                break
        url = ShortenedURL(
            original_url=original_url,
            short_code=short_code
        )
        return self.repository.create(db, url)