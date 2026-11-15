from dataclasses import dataclass, fields

from jogo_pds.domain.validacao import validar_inteiro


@dataclass(frozen=True)
class Configuracao:
    """Valores de demonstração, em créditos inteiros; ainda sem balanceamento."""

    saldo_inicial: int = 300
    bonus_partida: int = 25
    preco_imovel: int = 80
    aluguel_imovel: int = 20
    preco_empresa: int = 100
    taxa_fixa: int = 15
    multiplicador_variavel: int = 3

    def __post_init__(self) -> None:
        for campo in fields(self):
            validar_inteiro(getattr(self, campo.name), campo.name)
