from abc import ABC, abstractmethod
from dataclasses import dataclass

from jogo_pds.domain.dados import Dados
from jogo_pds.domain.jogo import Jogo


class Comando(ABC):
    @abstractmethod
    def executar(self, jogo: Jogo) -> None:
        """Solicita uma ação; o estado da partida decide se ela é permitida."""
        raise NotImplementedError


@dataclass(frozen=True)
class InformarDados(Comando):
    dados: Dados

    def executar(self, jogo: Jogo) -> None:
        jogo.informar_dados(self.dados)


class Comprar(Comando):
    def executar(self, jogo: Jogo) -> None:
        jogo.comprar()


class RecusarCompra(Comando):
    def executar(self, jogo: Jogo) -> None:
        jogo.recusar_compra()
