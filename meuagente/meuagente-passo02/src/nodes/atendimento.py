"""No de atendimento: faz a triagem do prontuario e escolhe o destino."""

from typing import Literal

from pydantic import BaseModel, Field

from src.services.llm import modelo
from src.state import State

PROMPT_TRIAGEM = """Voce e um profissional de triagem em um servico de saude.
Leia o prontuario e classifique o destino do atendimento:

- "cardiologico": queixa ou achado predominantemente cardiaco. Exemplos: dor
  toracica, palpitacao, sincope suspeita cardiaca, edema com dispneia sugestiva
  de insuficiencia cardiaca, sinais de sindrome coronariana aguda.
- "urgente": risco imediato a vida ou de agravamento rapido, sem predominancia
  cardiaca. Exemplos: rebaixamento de consciencia, sinais de AVC, sangramento
  ativo, trauma grave, reacao alergica grave, dor intensa e subita nao toracica,
  sinais vitais instaveis por causa nao tipicamente cardiologica.
- "nao_urgente": quadro estavel, queixas leves ou cronicas, rotina, renovacao de
  receita, acompanhamento.

Se houver sinal cardiaco claro, prefira "cardiologico" em vez de "urgente".
Na duvida entre urgente e nao_urgente (sem quadro cardiaco), classifique como "urgente".
Tambem informe se o caso e "urgente" ou "nao_urgente" no nivel de urgencia geral
(cardiologico conta como urgente).
Justifique em uma ou duas frases, citando os achados do prontuario."""


class Classificacao(BaseModel):
    """Resultado da triagem."""

    destino: Literal["cardiologico", "urgente", "nao_urgente"] = Field(
        description="Destino do atendimento apos a triagem"
    )
    urgencia: Literal["urgente", "nao_urgente"] = Field(
        description="Nivel de urgencia geral (cardiologico e urgente)"
    )
    justificativa: str = Field(description="Motivo da classificacao")


def atendimento(state: State) -> dict:
    """Classifica o prontuario e devolve so os campos que altera no state."""
    triador = modelo().with_structured_output(Classificacao)
    resultado = triador.invoke(
        [
            ("system", PROMPT_TRIAGEM),
            ("human", state.prontuario),
        ]
    )
    return {
        "destino": resultado.destino,
        "urgencia": resultado.urgencia,
        "justificativa": resultado.justificativa,
    }
