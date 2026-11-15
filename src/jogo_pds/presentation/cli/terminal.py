from collections.abc import Callable

from jogo_pds.application.commands.acoes import Comando, Comprar, InformarDados, RecusarCompra
from jogo_pds.application.controllers.partida import ControladorPartida
from jogo_pds.application.historico import HistoricoTextual
from jogo_pds.domain.dados import Dados
from jogo_pds.domain.erros import ErroDeRegra
from jogo_pds.domain.estados.partida import AguardandoCompra, Finalizada
from jogo_pds.domain.logradouros import Empresa, Imovel


def interpretar_comando(texto: str) -> Comando:
    partes = texto.lower().split()
    if len(partes) == 3 and partes[0] == "dados":
        try:
            primeiro, segundo = int(partes[1]), int(partes[2])
        except ValueError as erro:
            raise ValueError("Use dois inteiros: dados 2 3.") from erro
        return InformarDados(Dados(primeiro, segundo))
    if partes == ["comprar"]:
        return Comprar()
    if partes == ["recusar"]:
        return RecusarCompra()
    raise ValueError("Comando desconhecido. Use ajuda para ver os comandos.")


class Terminal:
    AJUDA = "Comandos: dados <1-6> <1-6> | comprar | recusar | ajuda | sair"

    def __init__(
        self, controlador: ControladorPartida, historico: HistoricoTextual,
        entrada: Callable[[str], str] = input,
        saida: Callable[[str], None] = print,
    ) -> None:
        self._controlador = controlador
        self._historico = historico
        self._entrada = entrada
        self._saida = saida
        self._linhas_exibidas = 0

    def executar(self) -> None:
        self._saida("Jogo PDS — base inicial de demonstração, regras especiais ainda pendentes.")
        self._saida(self.AJUDA)
        self._saida("Posições do tabuleiro (percurso circular):")
        for posicao, casa in enumerate(self._controlador.jogo.tabuleiro.casas):
            self._saida(f"  {posicao}: {casa.nome} ({type(casa).__name__})")
        while True:
            self._mostrar_historico()
            self._mostrar_situacao()
            if isinstance(self._controlador.jogo.estado, Finalizada):
                return
            try:
                texto = self._entrada("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                self._saida("\nDemonstração encerrada sem declarar vencedor; nada foi salvo.")
                return
            if texto == "sair":
                self._saida("Demonstração encerrada sem declarar vencedor; nada foi salvo.")
                return
            if texto == "ajuda":
                self._saida(self.AJUDA)
                continue
            try:
                self._controlador.executar(interpretar_comando(texto))
            except ErroDeRegra as erro:
                self._saida(f"Ação rejeitada: {erro}")
            except ValueError as erro:
                self._saida(f"Entrada inválida: {erro}")

    def _mostrar_historico(self) -> None:
        linhas = self._historico.linhas
        for linha in linhas[self._linhas_exibidas:]:
            self._saida(linha)
        self._linhas_exibidas = len(linhas)

    def _mostrar_situacao(self) -> None:
        jogo = self._controlador.jogo
        self._saida(f"\nEstado: {jogo.estado.nome}")
        if jogo.vencedor is None:
            self._saida(f"Jogador da vez: {jogo.jogador_atual.nome}")
        else:
            self._saida(f"Vencedor: {jogo.vencedor.nome}")
        for jogador in jogo.jogadores:
            adquiridos = jogo.tabuleiro.adquiridos_por(jogador)
            imoveis = ", ".join(casa.nome for casa in adquiridos if isinstance(casa, Imovel)) or "nenhum"
            empresas = ", ".join(casa.nome for casa in adquiridos if isinstance(casa, Empresa)) or "nenhuma"
            casa = jogo.tabuleiro.casas[jogador.posicao]
            self._saida(
                f"{jogador.nome}: posição {jogador.posicao} ({casa.nome}), saldo {jogador.saldo}; "
                f"imóveis: {imoveis}; empresas: {empresas}"
            )
        if isinstance(jogo.estado, AguardandoCompra):
            casa = jogo.estado.propriedade
            self._saida(f"Oferta: {casa.nome}, {casa.preco} créditos. Use comprar ou recusar.")
