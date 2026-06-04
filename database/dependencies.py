from database.connection import SessionLocal

# db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()