from jogo_pds.application.controllers.partida import ControladorPartida
from jogo_pds.application.historico import HistoricoTextual
from jogo_pds.domain.configuracao import Configuracao
from jogo_pds.domain.eventos.observacao import Publicador
from jogo_pds.domain.jogador import Jogador
from jogo_pds.domain.jogo import Jogo
from jogo_pds.domain.logradouros import Empresa, Imovel, PontoPartida
from jogo_pds.domain.tabuleiro import Tabuleiro
from jogo_pds.domain.taxas.estrategias import TaxaFixa, TaxaVariavel
from jogo_pds.presentation.cli.terminal import Terminal


def criar_jogo_demo(
    configuracao: Configuracao | None = None,
) -> tuple[ControladorPartida, HistoricoTextual]:
    config = configuracao if configuracao is not None else Configuracao()
    jogadores = (
        Jogador("Jogador 1", config.saldo_inicial),
        Jogador("Jogador 2", config.saldo_inicial),
    )
    tabuleiro = Tabuleiro([
        PontoPartida(),
        Imovel("Rua das Flores", config.preco_imovel, config.aluguel_imovel),
        Empresa("Companhia de Água", config.preco_empresa, TaxaFixa(config.taxa_fixa)),
        Imovel("Avenida Central", config.preco_imovel, config.aluguel_imovel),
        Imovel("Rua do Sol", config.preco_imovel, config.aluguel_imovel),
        Empresa("Companhia de Energia", config.preco_empresa, TaxaVariavel(config.multiplicador_variavel)),
        Imovel("Rua da Praça", config.preco_imovel, config.aluguel_imovel),
        Imovel("Alameda Verde", config.preco_imovel, config.aluguel_imovel),
    ])
    publicador = Publicador()
    historico = HistoricoTextual()
    publicador.inscrever(historico)
    jogo = Jogo(jogadores, tabuleiro, publicador, config.bonus_partida)
    return ControladorPartida(jogo), historico


def main() -> int:
    controlador, historico = criar_jogo_demo()
    Terminal(controlador, historico).executar()
    return 0
