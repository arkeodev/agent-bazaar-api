from pydantic import BaseModel, ConfigDict

from src.app.models.agent import AgentStatus


# Define Agent model using Pydantic
class AgentBase(BaseModel):
    name: str
    image_path: str
    description: str
    version: str
    creator: str
    port: int
    status: AgentStatus

    model_config = ConfigDict(from_attributes=True)


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    description: str | None = None
    version: str | None = None
    port: int | None = None
    status: AgentStatus | None = None

    model_config = ConfigDict(from_attributes=True)


class AgentRead(AgentBase):
    id: int
