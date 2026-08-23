from sqlalchemy.orm import Session
from app.models.shortened_url import ShortenedURL
from typing import Optional
class URLRepository:
    """
    Handles all database operations for shortened URLs.
    """
    def create(self, db: Session, url: ShortenedURL) -> ShortenedURL:
        """
        Save a new shortened URL to the database.
        """
        db.add(url)
        db.commit()
        db.refresh(url)
        return url

    def get_by_short_code(
        self,
        db: Session,
        short_code: str
    ) -> Optional[ShortenedURL]:
        """
        Return a URL by its short code.
        """
        return (
            db.query(ShortenedURL)
            .filter(ShortenedURL.short_code == short_code)
            .first()
        )