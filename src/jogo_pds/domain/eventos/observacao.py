from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Evento:
    tipo: str
    descricao: str


class Observador(ABC):
    @abstractmethod
    def atualizar(self, evento: Evento) -> None:
        """Recebe um acontecimento já produzido pelo domínio."""
        raise NotImplementedError


class Publicador:
    def __init__(self) -> None:
        self._observadores: list[Observador] = []

    def inscrever(self, observador: Observador) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover(self, observador: Observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def publicar(self, evento: Evento) -> None:
        for observador in tuple(self._observadores):
            observador.atualizar(evento)
