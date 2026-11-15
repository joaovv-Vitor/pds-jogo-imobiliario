class ErroDeRegra(ValueError):
    """Uma ação viola uma regra do domínio."""


class AcaoInvalida(ErroDeRegra):
    """A etapa atual da partida não permite a ação solicitada."""


class SaldoInsuficiente(ErroDeRegra):
    """O jogador não dispõe do valor necessário."""
