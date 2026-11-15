from jogo_pds.application.commands.acoes import Comando
from jogo_pds.domain.jogo import Jogo


class ControladorPartida:
    """Invocador de comandos; não interpreta texto nem replica regras do domínio."""

    def __init__(self, jogo: Jogo) -> None:
        self._jogo = jogo

    @property
    def jogo(self) -> Jogo:
        return self._jogo

    def executar(self, comando: Comando) -> None:
        comando.executar(self.jogo)
