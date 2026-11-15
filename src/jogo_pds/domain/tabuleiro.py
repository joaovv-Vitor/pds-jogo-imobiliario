from collections.abc import Sequence

from jogo_pds.domain.erros import ErroDeRegra
from jogo_pds.domain.jogador import Jogador
from jogo_pds.domain.logradouros import Logradouro, PontoPartida, Propriedade
from jogo_pds.domain.validacao import validar_inteiro


class Tabuleiro:
    def __init__(self, casas: Sequence[Logradouro]) -> None:
        if len(casas) < 2 or not isinstance(casas[0], PontoPartida):
            raise ErroDeRegra("O tabuleiro precisa de ao menos duas casas e Partida na posição zero.")
        if sum(isinstance(casa, PontoPartida) for casa in casas) != 1:
            raise ErroDeRegra("Deve existir exatamente um ponto de partida.")
        if len({id(casa) for casa in casas}) != len(casas):
            raise ErroDeRegra("Cada posição deve conter uma instância distinta de logradouro.")
        self._casas = tuple(casas)

    @property
    def casas(self) -> tuple[Logradouro, ...]:
        return self._casas

    def avancar(self, posicao: int, passos: int) -> tuple[int, int]:
        """Retorna (posição de destino, passagens pela Partida), apenas para avanço."""
        validar_inteiro(posicao, "Posição")
        validar_inteiro(passos, "Passos", minimo=1)
        if posicao >= len(self.casas):
            raise ErroDeRegra("Posição fora do tabuleiro.")
        voltas, destino = divmod(posicao + passos, len(self.casas))
        return destino, voltas

    def adquiridos_por(self, jogador: Jogador) -> tuple[Propriedade, ...]:
        return tuple(
            casa for casa in self.casas
            if isinstance(casa, Propriedade) and casa.proprietario is jogador
        )
