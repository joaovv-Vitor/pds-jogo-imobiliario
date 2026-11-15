# Diagrama de classes inicial

Representa as classes centrais existentes nesta etapa. Métodos auxiliares,
exceções e funções livres foram omitidos para legibilidade. O diagrama deve
evoluir junto do código; não antecipa classes de efeitos especiais ausentes.

```mermaid
classDiagram
    direction TB

    class Terminal {
        +executar() None
        -_mostrar_situacao() None
        -_mostrar_historico() None
    }
    class ControladorPartida {
        +jogo Jogo
        +executar(comando) None
    }
    class Comando {
        <<abstract>>
        +executar(jogo) None
    }
    class InformarDados {
        +dados Dados
        +executar(jogo) None
    }
    class Comprar {
        +executar(jogo) None
    }
    class RecusarCompra {
        +executar(jogo) None
    }

    class Jogo {
        -_indice_atual int
        -_bonus_partida int
        +jogador_atual Jogador
        +estado EstadoPartida
        +vencedor Jogador
        +informar_dados(dados) None
        +comprar() None
        +recusar_compra() None
        +mover_e_resolver(dados) None
        +oferecer_compra(propriedade) None
        +adquirir(propriedade) None
        +cobrar(proprietario, valor, origem) None
        +concluir_turno() None
        +registrar(tipo, descricao) None
    }
    class EstadoPartida {
        <<abstract>>
        +nome str
        +informar_dados(jogo, dados) None
        +comprar(jogo) None
        +recusar_compra(jogo) None
    }
    class AguardandoDados {
        +informar_dados(jogo, dados) None
    }
    class AguardandoCompra {
        +propriedade Propriedade
        +comprar(jogo) None
        +recusar_compra(jogo) None
    }
    class Finalizada {
        +nome str
    }
    class Jogador {
        +nome str
        +saldo int
        +posicao int
        +eliminado bool
        +creditar(valor) None
        +debitar(valor) None
        +pagar_para(destinatario, valor) None
        +mover_para(posicao) None
        +eliminar() None
    }
    class Dados {
        +primeiro int
        +segundo int
        +soma int
    }
    class Tabuleiro {
        +casas tuple
        +avancar(posicao, passos) tuple
        +adquiridos_por(jogador) tuple
    }
    class Logradouro {
        <<abstract>>
        +nome str
        +receber_visita(jogo, dados) None
    }
    class Propriedade {
        <<abstract>>
        +preco int
        +proprietario Jogador
        +comprar(comprador) None
        +calcular_cobranca(dados) int
        +receber_visita(jogo, dados) None
    }
    class Imovel {
        -_aluguel int
        +calcular_cobranca(dados) int
    }
    class Empresa {
        -_estrategia EstrategiaTaxa
        +calcular_cobranca(dados) int
    }
    class LugarEspecial {
        <<abstract>>
    }
    class PontoPartida {
        +receber_visita(jogo, dados) None
    }

    class EstrategiaTaxa {
        <<abstract>>
        +calcular(dados) int
    }
    class TaxaFixa {
        +valor int
        +calcular(dados) int
    }
    class TaxaVariavel {
        +multiplicador int
        +calcular(dados) int
    }

    class Evento {
        +tipo str
        +descricao str
    }
    class Observador {
        <<abstract>>
        +atualizar(evento) None
    }
    class Publicador {
        -_observadores list
        +inscrever(observador) None
        +remover(observador) None
        +publicar(evento) None
    }
    class HistoricoTextual {
        +linhas tuple
        +atualizar(evento) None
    }
    class Configuracao {
        +saldo_inicial int
        +bonus_partida int
        +preco_imovel int
        +aluguel_imovel int
        +preco_empresa int
        +taxa_fixa int
        +multiplicador_variavel int
    }

    Terminal --> ControladorPartida
    Terminal --> HistoricoTextual : consulta
    Terminal ..> Comando : cria por interpretar_comando
    ControladorPartida --> Jogo : receptor
    ControladorPartida ..> Comando : invoca
    Comando <|-- InformarDados
    Comando <|-- Comprar
    Comando <|-- RecusarCompra
    Comando ..> Jogo
    InformarDados --> Dados

    Jogo "1" --> "2" Jogador : participantes
    Jogo --> Tabuleiro
    Jogo "1" *-- "1" EstadoPartida : estado atual
    EstadoPartida <|-- AguardandoDados
    EstadoPartida <|-- AguardandoCompra
    EstadoPartida <|-- Finalizada
    EstadoPartida ..> Jogo
    AguardandoCompra --> Propriedade : oferta

    Tabuleiro "1" o-- "2..*" Logradouro : percurso
    Logradouro <|-- Propriedade
    Logradouro <|-- LugarEspecial
    Propriedade <|-- Imovel
    Propriedade <|-- Empresa
    LugarEspecial <|-- PontoPartida
    Propriedade "0..*" --> "0..1" Jogador : proprietario
    Logradouro ..> Jogo : resolve visita
    Empresa --> EstrategiaTaxa : delega calculo
    EstrategiaTaxa <|-- TaxaFixa
    EstrategiaTaxa <|-- TaxaVariavel
    EstrategiaTaxa ..> Dados

    Jogo --> Publicador : publica fatos
    Publicador "1" o-- "0..*" Observador : inscritos
    Observador <|-- HistoricoTextual
    Publicador ..> Evento
    Observador ..> Evento
```

## Correspondência dos padrões

| Padrão | Participantes |
| --- | --- |
| Strategy | `Empresa`, `EstrategiaTaxa`, `TaxaFixa`, `TaxaVariavel`. |
| State | `Jogo`, `EstadoPartida`, `AguardandoDados`, `AguardandoCompra`, `Finalizada`. |
| Command | `Comando`, `InformarDados`, `Comprar`, `RecusarCompra`, `ControladorPartida`, `Jogo`; criação na CLI. |
| Observer | `Jogo`, `Publicador`, `Observador`, `Evento`, `HistoricoTextual`. |

As propriedades de leitura aparecem como atributos públicos para simplificar
a notação; não representam setters disponíveis. `vencedor` e `proprietario`
podem ser `None`. A enumeração das casas é imutável (`tuple`); as entidades
guardadas nela continuam mutáveis. `Configuracao` e `Dados` são dataclasses
imutáveis. A função livre `main.criar_jogo_demo` usa `Configuracao` e monta os
objetos, por isso não existe uma classe de composição no diagrama.
