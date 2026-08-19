from app.database.database import SessionLocal
from app.models.shortened_url import ShortenedURL
from app.repositories.url_repository import URLRepository


def main():
    db = SessionLocal()

    repository = URLRepository()

    url = ShortenedURL(
        original_url="https://google.com",
        short_code="abc123"
    )

    saved_url = repository.create(db, url)

    print("ID:", saved_url.id)
    print("Original URL:", saved_url.original_url)
    print("Short Code:", saved_url.short_code)
    print("Clicks:", saved_url.clicks)
    print("Created At:", saved_url.created_at)

    db.close()


if __name__ == "__main__":
    main()
