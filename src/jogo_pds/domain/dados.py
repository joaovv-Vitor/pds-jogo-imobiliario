from dataclasses import dataclass

from jogo_pds.domain.erros import ErroDeRegra


@dataclass(frozen=True)
class Dados:
    primeiro: int
    segundo: int

    def __post_init__(self) -> None:
        for valor in (self.primeiro, self.segundo):
            if type(valor) is not int or not 1 <= valor <= 6:
                raise ErroDeRegra("Cada dado deve ser um inteiro entre 1 e 6.")

    @property
    def soma(self) -> int:
        return self.primeiro + self.segundo
