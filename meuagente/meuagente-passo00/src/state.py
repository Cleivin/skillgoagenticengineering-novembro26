from typing import Literal
from pydantic import BaseModel, Field

class State(BaseModel):
    """Atendimento de Prontuarios medicos"""
    
    identificador_id: str = Field(..., description="ID do paciente")
    data_atualizacao: str = Field(..., description="Data da ultima atualizacao do prontuario")

    