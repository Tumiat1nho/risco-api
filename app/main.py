from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from app import database, regras, schemas

app = FastAPI(
    title="Risco API",
    description=(
        "Calcula o nível de risco de fornecedores/terceiros com base em dados "
        "cadastrais e mantém um histórico das avaliações realizadas."
    ),
    version="1.0.0",
)


@app.on_event("startup")
def startup() -> None:
    database.init_db()


@app.post("/risco/calcular", response_model=schemas.Avaliacao, status_code=201)
def calcular_risco(payload: schemas.RiscoInput):
    nivel, pontos, motivos = regras.calcular_score(
        payload.situacao_cadastral, payload.capital_social, payload.data_inicio_atividade
    )

    conn = database.get_connection()
    cursor = conn.execute(
        """INSERT INTO avaliacoes_risco
           (situacao_cadastral, capital_social, data_inicio_atividade, nivel_risco, pontuacao, observacao)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            payload.situacao_cadastral,
            payload.capital_social,
            payload.data_inicio_atividade,
            nivel,
            pontos,
            "; ".join(motivos),
        ),
    )
    conn.commit()
    novo_id = cursor.lastrowid

    row = conn.execute("SELECT * FROM avaliacoes_risco WHERE id = ?", (novo_id,)).fetchone()
    conn.close()
    return dict(row)


@app.get("/risco/historico", response_model=List[schemas.Avaliacao])
def listar_historico(
    nivel_risco: Optional[str] = None,
    order_by: str = Query("id", enum=["id", "pontuacao", "data_avaliacao"]),
    order_dir: str = Query("desc", enum=["asc", "desc"]),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    conn = database.get_connection()

    query = "SELECT * FROM avaliacoes_risco WHERE 1=1"
    params: list = []

    if nivel_risco:
        query += " AND nivel_risco = ?"
        params.append(nivel_risco)

    query += f" ORDER BY {order_by} {order_dir.upper()} LIMIT ? OFFSET ?"
    params.extend([limit, skip])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@app.get("/risco/historico/{avaliacao_id}", response_model=schemas.Avaliacao)
def obter_avaliacao(avaliacao_id: int):
    conn = database.get_connection()
    row = conn.execute("SELECT * FROM avaliacoes_risco WHERE id = ?", (avaliacao_id,)).fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return dict(row)


@app.put("/risco/historico/{avaliacao_id}", response_model=schemas.Avaliacao)
def atualizar_avaliacao(avaliacao_id: int, payload: schemas.AvaliacaoUpdate):
    conn = database.get_connection()

    row = conn.execute("SELECT * FROM avaliacoes_risco WHERE id = ?", (avaliacao_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    campos = payload.dict(exclude_unset=True)
    if campos:
        set_clause = ", ".join(f"{campo} = ?" for campo in campos)
        valores = list(campos.values()) + [avaliacao_id]
        conn.execute(f"UPDATE avaliacoes_risco SET {set_clause} WHERE id = ?", valores)
        conn.commit()

    row = conn.execute("SELECT * FROM avaliacoes_risco WHERE id = ?", (avaliacao_id,)).fetchone()
    conn.close()
    return dict(row)


@app.delete("/risco/historico/{avaliacao_id}", status_code=204)
def remover_avaliacao(avaliacao_id: int):
    conn = database.get_connection()

    row = conn.execute("SELECT id FROM avaliacoes_risco WHERE id = ?", (avaliacao_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    conn.execute("DELETE FROM avaliacoes_risco WHERE id = ?", (avaliacao_id,))
    conn.commit()
    conn.close()
    return None
