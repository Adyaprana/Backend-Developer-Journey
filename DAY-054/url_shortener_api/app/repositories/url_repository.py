from sqlalchemy.orm import Session
from app.models.shortened_url import ShortenedURL
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