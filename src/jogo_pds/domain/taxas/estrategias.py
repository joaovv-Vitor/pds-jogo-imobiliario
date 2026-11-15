from abc import ABC, abstractmethod
from dataclasses import dataclass

from jogo_pds.domain.dados import Dados
from jogo_pds.domain.validacao import validar_inteiro


class EstrategiaTaxa(ABC):
    @abstractmethod
    def calcular(self, dados: Dados) -> int:
        """Retorna uma cobrança não negativa em créditos inteiros."""
        raise NotImplementedError


@dataclass(frozen=True)
class TaxaFixa(EstrategiaTaxa):
    valor: int

    def __post_init__(self) -> None:
        validar_inteiro(self.valor, "Taxa fixa")

    def calcular(self, dados: Dados) -> int:
        return self.valor


@dataclass(frozen=True)
class TaxaVariavel(EstrategiaTaxa):
    multiplicador: int

    def __post_init__(self) -> None:
        validar_inteiro(self.multiplicador, "Multiplicador")

    def calcular(self, dados: Dados) -> int:
        return self.multiplicador * dados.soma
