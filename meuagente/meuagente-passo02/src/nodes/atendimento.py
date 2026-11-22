"""No de atendimento: faz a triagem do prontuario e escolhe o destino."""

from typing import Literal

from pydantic import BaseModel, Field

from src.services.llm import modelo
from src.state import State

PROMPT_TRIAGEM = """Voce e um profissional de triagem em um servico de saude.
Leia o prontuario e classifique o destino do atendimento:

- "dermatologico": queixa ou achado predominantemente de pele ou anexos.
  Exemplos: rash, prurido, lesoes cutaneas, urticaria, queimadura cutanea,
  infeccao de pele, erupcao, eczema, psoriasis.
- "cardiologico": queixa ou achado predominantemente cardiaco. Exemplos: dor
  toracica, palpitacao, sincope suspeita cardiaca, edema com dispneia sugestiva
  de insuficiencia cardiaca, sinais de sindrome coronariana aguda.
- "urgente": risco imediato a vida ou de agravamento rapido, sem predominancia
  cardiaca nem dermatologica. Exemplos: rebaixamento de consciencia, sinais de
  AVC, sangramento ativo, trauma grave, reacao alergica grave sistemica, dor
  intensa e subita nao toracica, sinais vitais instaveis por causa nao tipicamente
  cardiologica nem cutanea.
- "nao_urgente": quadro estavel, queixas leves ou cronicas, rotina, renovacao de
  receita, acompanhamento.

Prioridade na duvida: sinal cardiaco claro -> "cardiologico"; senao, queixa de
pele clara -> "dermatologico"; senao, entre urgente e nao_urgente, prefira "urgente".
Tambem informe se o caso e "urgente" ou "nao_urgente" no nivel de urgencia geral
(cardiologico e dermatologico contam como urgente quando houver risco clinico).
Justifique em uma ou duas frases, citando os achados do prontuario."""


class Classificacao(BaseModel):
    """Resultado da triagem."""

    destino: Literal["dermatologico", "cardiologico", "urgente", "nao_urgente"] = Field(
        description="Destino do atendimento apos a triagem"
    )
    urgencia: Literal["urgente", "nao_urgente"] = Field(
        description="Nivel de urgencia geral"
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
