from jogo_pds.domain.erros import ErroDeRegra


def validar_inteiro(valor: int, nome: str, minimo: int = 0) -> None:
    # bool é subclasse de int em Python, mas não é um valor válido neste domínio.
    if type(valor) is not int or valor < minimo:
        raise ErroDeRegra(f"{nome} deve ser inteiro maior ou igual a {minimo}.")
