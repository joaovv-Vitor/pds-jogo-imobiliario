from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from jogo_pds.domain.dados import Dados
from jogo_pds.domain.erros import ErroDeRegra
from jogo_pds.domain.jogador import Jogador
from jogo_pds.domain.taxas.estrategias import EstrategiaTaxa
from jogo_pds.domain.validacao import validar_inteiro

if TYPE_CHECKING:
    from jogo_pds.domain.jogo import Jogo


class Logradouro(ABC):
    def __init__(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise ErroDeRegra("O logradouro precisa de um nome.")
        self._nome = nome.strip()

    @property
    def nome(self) -> str:
        return self._nome

    @abstractmethod
    def receber_visita(self, jogo: Jogo, dados: Dados) -> None:
        """Resolve a visita do jogador atual, conforme a categoria da casa."""
        raise NotImplementedError


class Propriedade(Logradouro, ABC):
    """Aquisição e propriedade comuns a imóveis e empresas."""

    def __init__(self, nome: str, preco: int) -> None:
        super().__init__(nome)
        validar_inteiro(preco, "Preço")
        self._preco = preco
        self._proprietario: Jogador | None = None

    @property
    def preco(self) -> int:
        return self._preco

    @property
    def proprietario(self) -> Jogador | None:
        return self._proprietario

    def comprar(self, comprador: Jogador) -> None:
        if self.proprietario is not None:
            raise ErroDeRegra("Propriedade já adquirida; transferências não são permitidas.")
        comprador.debitar(self.preco)
        self._proprietario = comprador

    @abstractmethod
    def calcular_cobranca(self, dados: Dados) -> int:
        """Calcula aluguel ou taxa, sem movimentar saldos."""
        raise NotImplementedError

    def receber_visita(self, jogo: Jogo, dados: Dados) -> None:
        if self.proprietario is None:
            jogo.oferecer_compra(self)
        elif self.proprietario is jogo.jogador_atual:
            jogo.registrar("visita_propria", f"Visita a {self.nome}: propriedade própria, sem cobrança.")
            jogo.concluir_turno()
        else:
            jogo.cobrar(self.proprietario, self.calcular_cobranca(dados), self.nome)


class Imovel(Propriedade):
    def __init__(self, nome: str, preco: int, aluguel: int) -> None:
        super().__init__(nome, preco)
        validar_inteiro(aluguel, "Aluguel")
        self._aluguel = aluguel

    def calcular_cobranca(self, dados: Dados) -> int:
        return self._aluguel


class Empresa(Propriedade):
    def __init__(self, nome: str, preco: int, estrategia: EstrategiaTaxa) -> None:
        super().__init__(nome, preco)
        self._estrategia = estrategia

    def calcular_cobranca(self, dados: Dados) -> int:
        valor = self._estrategia.calcular(dados)
        validar_inteiro(valor, "Taxa calculada")
        return valor


class LugarEspecial(Logradouro, ABC):
    """Categoria não comprável; novos efeitos exigem implementação concreta."""


class PontoPartida(LugarEspecial):
    def __init__(self) -> None:
        super().__init__("Partida")

    def receber_visita(self, jogo: Jogo, dados: Dados) -> None:
        jogo.registrar("visita_partida", "Parada na Partida, sem crédito adicional ao de passagem.")
        jogo.concluir_turno()
