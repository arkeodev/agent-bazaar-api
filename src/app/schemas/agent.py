from pydantic import BaseModel


# Define Agent model using Pydantic
class AgentBase(BaseModel):
    name: str
    image_path: str
    description: str
    version: str
    creator: str
    port: int
    status: str  # e.g., 'running', 'stopped'


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    description: str | None = None
    version: str | None = None
    port: int | None = None
    status: str | None = None


class AgentRead(AgentBase):
    id: int
