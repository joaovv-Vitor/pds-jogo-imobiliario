from jogo_pds.domain.erros import ErroDeRegra, SaldoInsuficiente
from jogo_pds.domain.validacao import validar_inteiro


class Jogador:
    def __init__(self, nome: str, saldo_inicial: int) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise ErroDeRegra("O nome do jogador não pode estar vazio.")
        validar_inteiro(saldo_inicial, "Saldo inicial")
        self._nome = nome.strip()
        self._saldo = saldo_inicial
        self._posicao = 0
        self._eliminado = False

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def saldo(self) -> int:
        return self._saldo

    @property
    def posicao(self) -> int:
        return self._posicao

    @property
    def eliminado(self) -> bool:
        return self._eliminado

    def creditar(self, valor: int) -> None:
        validar_inteiro(valor, "Crédito")
        self._saldo += valor

    def debitar(self, valor: int) -> None:
        validar_inteiro(valor, "Débito")
        if valor > self._saldo:
            raise SaldoInsuficiente(f"{self.nome} não possui {valor} créditos.")
        self._saldo -= valor

    def pagar_para(self, destinatario: "Jogador", valor: int) -> None:
        self.debitar(valor)
        destinatario.creditar(valor)

    def mover_para(self, posicao: int) -> None:
        validar_inteiro(posicao, "Posição")
        self._posicao = posicao

    def eliminar(self) -> None:
        self._eliminado = True
