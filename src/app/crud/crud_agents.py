from fastcrud import FastCRUD

from ..models.agent import Agent
from ..schemas.agent import AgentCreate, AgentRead, AgentUpdate

CRUDAgent = FastCRUD[Agent, AgentCreate, AgentUpdate, AgentRead]
crud_agents = CRUDAgent(Agent)
