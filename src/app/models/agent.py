from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Agent(Base):
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    image_path = Column(String)
    description = Column(String)
    version = Column(String)
    creator = Column(String)
    port = Column(Integer)
    status = Column(Enum("running", "stopped", name="status_enum"))
