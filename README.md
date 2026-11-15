# pds-jogo-imobiliario

Projeto acadêmico de Projeto e Desenvolvimento de Software (PDS): jogo de
tabuleiro para **exatamente dois jogadores**, com interação pelo terminal e
aplicação de quatro padrões GoF.

Esta é uma **base inicial executável**, com tabuleiro reduzido de demonstração.
Há turnos, dados manuais, compras opcionais, cobranças, bônus de passagem e
eliminação por cobrança impagável. O catálogo definitivo de casas, os efeitos
especiais de movimento/saldo e o balanceamento ainda estão pendentes. Não há
interface gráfica, serviço web, banco de dados ou persistência.

## Execução

Requer Python **3.11 ou superior**. Não há dependências externas em execução.
A partir da raiz do repositório, sem instalar pacotes:

```sh
PYTHONPATH=src python3 -m jogo_pds
```

Alternativamente, em ambiente virtual:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
jogo-pds
```

A instalação usa `setuptools` apenas para empacotamento. A primeira forma de
execução e os testes usam somente a biblioteca padrão e dispensam instalação.

Comandos no terminal: `dados 2 3`, `comprar`, `recusar`, `ajuda` e `sair`.
Informe os dois dados somente quando solicitado; a compra pode ser aceita ou
recusada. Uma compra sem saldo mantém a oferta aberta para que seja recusada.
`sair` encerra a demonstração sem declarar vencedor e sem salvar a partida.

O terminal mostra o estado, o jogador da vez, a posição, o saldo e as aquisições
dos dois jogadores, além do histórico de acontecimentos.

## Organização

```text
src/jogo_pds/
  domain/                   Entidades, regras e configuração da demonstração
    taxas/                  Strategy: taxa fixa e variável das empresas
    estados/                State: etapas e ações permitidas
    eventos/                Observer: evento, publicador e contrato do observador
  application/
    commands/               Command: informar dados, comprar, recusar
    controllers/            Encaminhamento dos comandos ao domínio
    historico.py            Observador que acumula o histórico textual
  presentation/cli/         Entrada, validação textual e saída pelo terminal
  main.py                   Composição dos objetos e ponto de entrada
docs/                       Requisitos, arquitetura, decisões e entrega acadêmica
tests/                      Testes das regras efetivamente implementadas
```

As dependências apontam da apresentação para a aplicação e para o domínio.
O domínio não importa apresentação nem aplicação. Os padrões ficam junto das
responsabilidades que atendem; não existe uma pasta genérica de padrões.

## Verificação

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 -m compileall -q src tests
printf 'dados 1 1\nrecusar\nsair\n' | PYTHONPATH=src python3 -m jogo_pds
```

Os parâmetros de valores ficam em `domain/configuracao.py`; a montagem do
tabuleiro de demonstração está em `main.py`. Os valores são créditos inteiros.
Não há promessa de duração ou equilíbrio das partidas nesta etapa.

## Documentação e entrega

- [Requisitos e pendências](docs/requisitos.md).
- [Arquitetura e participantes dos quatro padrões](docs/arquitetura.md).
- [Decisões e limites da etapa](docs/decisoes.md).
- [Diagrama de classes Mermaid](docs/diagrama-classes.md).
- [Modelo do documento acadêmico e capa](docs/documento-academico.md).

A entrega final deverá reunir código, diagrama e documento com os nomes reais
de todos os integrantes em um ZIP. O modelo ainda precisa ser preenchido e
revisado pela equipe; o ZIP final não é produzido nesta etapa.

## Contribuição

Use mensagens de commit no formato `tipo(escopo): descrição`, com descrição em
português. Os tipos, escopos e exemplos estão no [guia de contribuição](CONTRIBUTING.md).
