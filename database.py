from sqlmodel import SQLModel, create_engine, Session

# 1) Define your SQLite file location
DATABASE_URL = "sqlite:///./data/kryptia.db"

# 2) Create the engine
engine = create_engine(DATABASE_URL, echo=True)

# 3) Initialize the database (call this once at startup)
def init_db():
    SQLModel.metadata.create_all(engine)

# 4) Dependency for sessions
def get_session():
    with Session(engine) as session:
        yield session
