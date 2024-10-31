from typing import Literal

from pydantic import BaseModel, ConfigDict


# Define Agent model using Pydantic
class AgentBase(BaseModel):
    name: str
    image_path: str
    description: str
    version: str
    creator: str
    port: int
    status: Literal["running", "stopped"]

    model_config = ConfigDict(from_attributes=True)


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    description: str | None = None
    version: str | None = None
    port: int | None = None
    status: Literal["running", "stopped"] | None = None

    model_config = ConfigDict(from_attributes=True)


class AgentRead(AgentBase):
    id: int
