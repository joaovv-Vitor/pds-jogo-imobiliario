from jogo_pds.domain.eventos.observacao import Evento, Observador


class HistoricoTextual(Observador):
    """Projeção em memória dos eventos; não faz entrada/saída nem persiste dados."""

    def __init__(self) -> None:
        self._linhas: list[str] = []

    @property
    def linhas(self) -> tuple[str, ...]:
        return tuple(self._linhas)

    def atualizar(self, evento: Evento) -> None:
        self._linhas.append(f"[{evento.tipo}] {evento.descricao}")
