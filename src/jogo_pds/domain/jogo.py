from collections.abc import Sequence

from jogo_pds.domain.dados import Dados
from jogo_pds.domain.erros import ErroDeRegra, SaldoInsuficiente
from jogo_pds.domain.estados.partida import (
    AguardandoCompra, AguardandoDados, EstadoPartida, Finalizada,
)
from jogo_pds.domain.eventos.observacao import Evento, Publicador
from jogo_pds.domain.jogador import Jogador
from jogo_pds.domain.logradouros import Propriedade
from jogo_pds.domain.tabuleiro import Tabuleiro
from jogo_pds.domain.validacao import validar_inteiro


class Jogo:
    def __init__(
        self, jogadores: Sequence[Jogador], tabuleiro: Tabuleiro,
        publicador: Publicador, bonus_partida: int,
    ) -> None:
        if len(jogadores) != 2 or jogadores[0] is jogadores[1]:
            raise ErroDeRegra("A partida exige exatamente dois jogadores distintos.")
        if jogadores[0].nome.casefold() == jogadores[1].nome.casefold():
            raise ErroDeRegra("Os jogadores precisam de nomes distintos.")
        validar_inteiro(bonus_partida, "Bônus da Partida")
        self._jogadores = tuple(jogadores)
        self._tabuleiro = tabuleiro
        self._publicador = publicador
        self._bonus_partida = bonus_partida
        self._indice_atual = 0
        self._estado: EstadoPartida = AguardandoDados()
        self._vencedor: Jogador | None = None
        self.registrar("inicio", "Demonstração iniciada com dois jogadores.")

    @property
    def jogadores(self) -> tuple[Jogador, ...]:
        return self._jogadores

    @property
    def tabuleiro(self) -> Tabuleiro:
        return self._tabuleiro

    @property
    def jogador_atual(self) -> Jogador:
        return self.jogadores[self._indice_atual]

    @property
    def estado(self) -> EstadoPartida:
        return self._estado

    @property
    def vencedor(self) -> Jogador | None:
        return self._vencedor

    def informar_dados(self, dados: Dados) -> None:
        self.estado.informar_dados(self, dados)

    def comprar(self) -> None:
        self.estado.comprar(self)

    def recusar_compra(self) -> None:
        self.estado.recusar_compra(self)

    # Operações de colaboração do domínio, acionadas pelos estados e logradouros.
    # A interface e os comandos devem usar somente as três ações acima.
    def mover_e_resolver(self, dados: Dados) -> None:
        jogador = self.jogador_atual
        destino, passagens = self.tabuleiro.avancar(jogador.posicao, dados.soma)
        jogador.mover_para(destino)
        self.registrar("dados", f"{jogador.nome} informou {dados.primeiro} e {dados.segundo} (soma {dados.soma}).")
        if passagens:
            bonus = passagens * self._bonus_partida
            jogador.creditar(bonus)
            self.registrar("bonus", f"{jogador.nome} recebeu {bonus} por {passagens} passagem(ns) pela Partida.")
        casa = self.tabuleiro.casas[destino]
        self.registrar("movimento", f"{jogador.nome} chegou à posição {destino}: {casa.nome}.")
        casa.receber_visita(self, dados)

    def oferecer_compra(self, propriedade: Propriedade) -> None:
        self._estado = AguardandoCompra(propriedade)
        self.registrar("oferta", f"{propriedade.nome} disponível por {propriedade.preco} créditos; compra opcional.")

    def adquirir(self, propriedade: Propriedade) -> None:
        try:
            propriedade.comprar(self.jogador_atual)
        except SaldoInsuficiente:
            self.registrar("compra_sem_saldo", "Saldo insuficiente para comprar. Você pode recusar a oferta; não há eliminação.")
            return
        self.registrar("compra", f"{self.jogador_atual.nome} comprou {propriedade.nome} por {propriedade.preco}.")
        self.concluir_turno()

    def cobrar(self, proprietario: Jogador, valor: int, origem: str) -> None:
        jogador = self.jogador_atual
        try:
            jogador.pagar_para(proprietario, valor)
        except SaldoInsuficiente:
            jogador.eliminar()
            self._vencedor = proprietario
            self._estado = Finalizada()
            self.registrar("eliminacao", f"{jogador.nome} não conseguiu pagar {valor} por {origem} e foi eliminado.")
            self.registrar("vitoria", f"{proprietario.nome} venceu a demonstração.")
            return
        self.registrar("pagamento", f"{jogador.nome} pagou {valor} a {proprietario.nome} por {origem}.")
        self.concluir_turno()

    def concluir_turno(self) -> None:
        self._indice_atual = 1 - self._indice_atual
        self._estado = AguardandoDados()
        self.registrar("turno", f"Vez de {self.jogador_atual.nome}.")

    def registrar(self, tipo: str, descricao: str) -> None:
        self._publicador.publicar(Evento(tipo, descricao))
