"""Arestas condicionais: decidem o proximo passo a partir do state, sem chamar o LLM."""

from typing import Literal

from src.state import State

Destino = Literal["dermatologico", "cardiologico", "urgente", "nao_urgente"]


def rotear_por_urgencia(state: State) -> Destino:
    """Segue o ramo definido pelo atendimento. Sem classificacao, trata como urgente."""
    if state.destino in ("dermatologico", "cardiologico", "urgente", "nao_urgente"):
        return state.destino
    return "nao_urgente" if state.urgencia == "nao_urgente" else "urgente"
