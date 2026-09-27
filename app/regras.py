from datetime import datetime, date
from typing import List, Optional, Tuple


def calcular_score(
    situacao_cadastral: Optional[str],
    capital_social: Optional[float],
    data_inicio_atividade: Optional[str],
) -> Tuple[str, int, List[str]]:
    """Calcula o score de risco e retorna (nivel, pontuacao, motivos)."""
    pontos = 0
    motivos: List[str] = []

    situacao = (situacao_cadastral or "").upper()
    if situacao and situacao != "ATIVA":
        pontos += 40
        motivos.append(f"Situação cadastral irregular: {situacao_cadastral}")
    elif not situacao:
        pontos += 20
        motivos.append("Situação cadastral não informada")

    capital = capital_social or 0
    if capital < 1000:
        pontos += 30
        motivos.append("Capital social muito baixo (< R$ 1.000)")
    elif capital < 10000:
        pontos += 15
        motivos.append("Capital social baixo (< R$ 10.000)")

    idade_anos = None
    if data_inicio_atividade:
        try:
            data_inicio = datetime.strptime(data_inicio_atividade, "%Y-%m-%d").date()
            idade_anos = (date.today() - data_inicio).days / 365.25
        except ValueError:
            motivos.append("Data de início de atividade em formato inválido")

    if idade_anos is not None:
        if idade_anos < 1:
            pontos += 30
            motivos.append("Empresa aberta há menos de 1 ano")
        elif idade_anos < 2:
            pontos += 15
            motivos.append("Empresa aberta há menos de 2 anos")

    if pontos >= 70:
        nivel = "critico"
    elif pontos >= 45:
        nivel = "alto"
    elif pontos >= 20:
        nivel = "medio"
    else:
        nivel = "baixo"

    if not motivos:
        motivos.append("Nenhum fator de risco identificado")

    return nivel, pontos, motivos
