from pydantic import BaseModel


# Define Agent model using Pydantic
class Agent(BaseModel):
    name: str
    image_path: str
