from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from jogo_pds.domain.dados import Dados
from jogo_pds.domain.erros import AcaoInvalida

if TYPE_CHECKING:
    from jogo_pds.domain.jogo import Jogo
    from jogo_pds.domain.logradouros import Propriedade


class EstadoPartida(ABC):
    @property
    @abstractmethod
    def nome(self) -> str:
        raise NotImplementedError

    def informar_dados(self, jogo: Jogo, dados: Dados) -> None:
        raise AcaoInvalida(f"Não é permitido informar dados no estado {self.nome}.")

    def comprar(self, jogo: Jogo) -> None:
        raise AcaoInvalida(f"Não é permitido comprar no estado {self.nome}.")

    def recusar_compra(self, jogo: Jogo) -> None:
        raise AcaoInvalida(f"Não há compra a recusar no estado {self.nome}.")


class AguardandoDados(EstadoPartida):
    nome = "aguardando dados"

    def informar_dados(self, jogo: Jogo, dados: Dados) -> None:
        jogo.mover_e_resolver(dados)


class AguardandoCompra(EstadoPartida):
    nome = "aguardando compra"

    def __init__(self, propriedade: Propriedade) -> None:
        self.propriedade = propriedade

    def comprar(self, jogo: Jogo) -> None:
        jogo.adquirir(self.propriedade)

    def recusar_compra(self, jogo: Jogo) -> None:
        jogo.registrar("compra_recusada", f"{jogo.jogador_atual.nome} recusou {self.propriedade.nome}.")
        jogo.concluir_turno()


class Finalizada(EstadoPartida):
    nome = "finalizada"
    # As três ações herdam a rejeição explícita do contrato; a partida terminou.
