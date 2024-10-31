from fastcrud import FastCRUD
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.agent import Agent
from ..schemas.agent import AgentCreate, AgentRead, AgentUpdate

CRUDAgent = FastCRUD[Agent, AgentCreate, AgentUpdate, AgentRead, AsyncSession]
crud_agents = CRUDAgent(Agent)
