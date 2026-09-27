from pydantic import BaseModel
from typing import Optional, List


class RiscoInput(BaseModel):
    situacao_cadastral: Optional[str] = None
    capital_social: Optional[float] = None
    data_inicio_atividade: Optional[str] = None  # formato YYYY-MM-DD


class AvaliacaoUpdate(BaseModel):
    nivel_risco: Optional[str] = None
    observacao: Optional[str] = None


class Avaliacao(BaseModel):
    id: int
    situacao_cadastral: Optional[str] = None
    capital_social: Optional[float] = None
    data_inicio_atividade: Optional[str] = None
    nivel_risco: str
    pontuacao: int
    observacao: Optional[str] = None
    data_avaliacao: str
