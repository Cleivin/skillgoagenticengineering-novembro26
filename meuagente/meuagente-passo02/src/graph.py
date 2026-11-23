"""Montagem do grafo.

START -> atendimento -> dermatologico -> dermatologista  -> END
                     -> cardiologico  -> cardiologista   -> END
                     -> neurologico   -> neurologista    -> END
                     -> urgente       -> agente_urgencia -> END
                     -> clinicogeral  -> clinicogeral    -> END
"""

from langgraph.graph import END, START, StateGraph

from src.edges.roteamento import rotear_por_urgencia
from src.nodes.agente_urgencia import agente_urgencia
from src.nodes.atendimento import atendimento
from src.nodes.cardiologista import cardiologista
from src.nodes.clinicogeral import clinicogeral
from src.nodes.dermatologista import dermatologista
from src.nodes.neurologista import neurologista
from src.state import State

builder = StateGraph(State)

builder.add_node("atendimento", atendimento)
builder.add_node("agente_urgencia", agente_urgencia)
builder.add_node("cardiologista", cardiologista)
builder.add_node("dermatologista", dermatologista)
builder.add_node("neurologista", neurologista)
builder.add_node("clinicogeral", clinicogeral)

builder.add_edge(START, "atendimento")
builder.add_conditional_edges(
    "atendimento",
    rotear_por_urgencia,
    {
        "dermatologico": "dermatologista",
        "cardiologico": "cardiologista",
        "neurologico": "neurologista",
        "urgente": "agente_urgencia",
        "clinicogeral": "clinicogeral",
    },
)
builder.add_edge("agente_urgencia", END)
builder.add_edge("cardiologista", END)
builder.add_edge("dermatologista", END)
builder.add_edge("neurologista", END)
builder.add_edge("clinicogeral", END)

grafo = builder.compile()
