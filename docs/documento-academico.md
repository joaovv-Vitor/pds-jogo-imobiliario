# Modelo do documento acadêmico

> Documento inicial em Markdown. Substituir os campos entre colchetes antes da
> entrega; acrescentar linhas até incluir todos os integrantes reais da equipe.

## Capa

**[NOME DA INSTITUIÇÃO]**

**[CURSO]**

**Projeto e Desenvolvimento de Software — [TURMA / PERÍODO]**

**Jogo de tabuleiro para dois jogadores: arquitetura orientada a objetos e
aplicação de padrões GoF em Python**

Integrantes:

- [NOME COMPLETO DO INTEGRANTE 1 — MATRÍCULA, SE EXIGIDA]
- [NOME COMPLETO DO INTEGRANTE 2 — MATRÍCULA, SE EXIGIDA]
- [ACRESCENTAR TODOS OS DEMAIS INTEGRANTES]

Docente: [NOME DA PROFESSORA]

[CIDADE]

[DATA / ANO]

---

## 1. Objetivo e contexto

Este trabalho organiza um jogo de tabuleiro para dois jogadores em Python,
com interação pelo terminal. A interface gráfica mencionada inicialmente no
enunciado foi dispensada posteriormente pela professora. A arquitetura aplica
Strategy, State, Command e Observer, buscando responsabilidades claras,
polimorfismo e baixo acoplamento.

Nesta etapa há uma base executável com oito casas demonstrativas. O fluxo
comum de turnos, compras opcionais, cobranças e eliminação é exercitável. O
catálogo final, os efeitos especiais de saldo e movimento e o balanceamento
permanecem pendentes. Não há persistência, rede, autenticação ou interface web.

## 2. Requisitos e delimitação

Os requisitos completos, com identificadores, estão em
[`requisitos.md`](requisitos.md). Os identificadores EX designam exigências;
INT designa interpretações provisórias; PEN registra definições pendentes;
ENT identifica os artefatos da entrega final.

Entre as interpretações adotadas estão o movimento pela soma dos dois dados,
a taxa variável calculada por multiplicador vezes essa soma e o crédito de
bônus antes da resolução da casa de destino. Essas interpretações precisam
ser confirmadas e não são apresentadas como citações do enunciado.

## 3. Organização da solução

`presentation/cli` interpreta entradas e exibe o jogo. `application` contém
os comandos, o controlador que os invoca e o observador do histórico. `domain`
contém entidades, regras, estados, contratos de observação e estratégias de
taxa. `main.py` faz a composição dos objetos.

O domínio não depende de componentes do terminal. O saldo fica protegido em
`Jogador`, a propriedade dos bens em `Propriedade`, e o portfólio é obtido por
consulta ao tabuleiro. Não há duplicação de listas de aquisições no jogador.

## 4. Aplicação dos padrões

### 4.1 Strategy

**Motivação:** variar o cálculo de cobrança das empresas sem adicionar
condicionais de algoritmo em `Empresa`.

**Participantes:** `Empresa` (contexto), `EstrategiaTaxa` (contrato),
`TaxaFixa` e `TaxaVariavel` (estratégias concretas).

**Localização:**
[`domain/taxas/estrategias.py`](../src/jogo_pds/domain/taxas/estrategias.py) e
[`domain/logradouros.py`](../src/jogo_pds/domain/logradouros.py).

**Trechos correspondentes:**

```python
# Empresa.calcular_cobranca
valor = self._estrategia.calcular(dados)
validar_inteiro(valor, "Taxa calculada")
return valor

# TaxaFixa.calcular
return self.valor

# TaxaVariavel.calcular
return self.multiplicador * dados.soma
```

**Decisão e consequência:** a estratégia é recebida no construtor de
`Empresa`; novas fórmulas podem ser introduzidas por uma nova implementação
de `EstrategiaTaxa`. Não há requisito atual de trocar a fórmula pelo terminal.

### 4.2 State

**Motivação:** permitir ações diferentes ao aguardar dados, aguardar uma
decisão de compra ou encerrar a partida.

**Participantes:** `Jogo` (contexto), `EstadoPartida` (contrato),
`AguardandoDados`, `AguardandoCompra` e `Finalizada` (estados concretos).

**Localização:**
[`domain/estados/partida.py`](../src/jogo_pds/domain/estados/partida.py) e
[`domain/jogo.py`](../src/jogo_pds/domain/jogo.py).

**Trechos correspondentes:**

```python
# Jogo.informar_dados
self.estado.informar_dados(self, dados)

# AguardandoDados.informar_dados
jogo.mover_e_resolver(dados)

# AguardandoCompra.comprar
jogo.adquirir(self.propriedade)

# EstadoPartida.comprar: rejeição padrão de uma ação não permitida
raise AcaoInvalida(f"Não é permitido comprar no estado {self.nome}.")
```

**Decisão e consequência:** estados sobrescrevem apenas as ações permitidas;
as demais são rejeitadas explicitamente. O domínio coordena as transições.
O controlador e a CLI não precisam duplicar a tabela de permissões.

### 4.3 Command

**Motivação:** transformar solicitações em objetos, separando interpretação
textual e execução sobre a partida.

**Participantes:** `Comando` (contrato), `InformarDados`, `Comprar` e
`RecusarCompra` (comandos concretos), `ControladorPartida` (invocador),
`Jogo` (receptor) e `interpretar_comando` (cliente na apresentação).

**Localização:**
[`application/commands/acoes.py`](../src/jogo_pds/application/commands/acoes.py),
[`application/controllers/partida.py`](../src/jogo_pds/application/controllers/partida.py) e
[`presentation/cli/terminal.py`](../src/jogo_pds/presentation/cli/terminal.py).

**Trechos correspondentes:**

```python
# ControladorPartida.executar
comando.executar(self.jogo)

# InformarDados.executar
jogo.informar_dados(self.dados)

# RecusarCompra.executar
jogo.recusar_compra()
```

**Decisão e consequência:** o controlador aceita o contrato `Comando`, sem
selecionar tipos concretos. A validação da etapa fica no domínio. Não foram
incluídos desfazer, filas ou gravação de comandos.

### 4.4 Observer

**Motivação:** alimentar um histórico de acontecimentos sem acoplar as regras
a chamadas de saída pelo terminal.

**Participantes:** `Publicador` (sujeito explícito), `Observador` (contrato),
`HistoricoTextual` (observador concreto), `Evento` (informação publicada) e
`Jogo` (produtor dos fatos).

**Localização:**
[`domain/eventos/observacao.py`](../src/jogo_pds/domain/eventos/observacao.py),
[`application/historico.py`](../src/jogo_pds/application/historico.py) e
[`main.py`](../src/jogo_pds/main.py).

**Trechos correspondentes:**

```python
# Composição em criar_jogo_demo
publicador = Publicador()
historico = HistoricoTextual()
publicador.inscrever(historico)
jogo = Jogo(jogadores, tabuleiro, publicador, config.bonus_partida)

# Publicador.publicar
for observador in tuple(self._observadores):
    observador.atualizar(evento)

# HistoricoTextual.atualizar
self._linhas.append(f"[{evento.tipo}] {evento.descricao}")
```

**Decisão e consequência:** a publicação suporta vários observadores e
remoção de inscrições. O histórico acumula texto em memória; o terminal o
consulta e imprime. Não há persistência ou mecanismo de mensagens externo.

## 5. Diagrama de classes

O diagrama inicial está em [`diagrama-classes.md`](diagrama-classes.md), em
Mermaid, com os participantes dos quatro padrões e suas relações.

[INSERIR A REPRESENTAÇÃO RENDERIZADA DO DIAGRAMA NA VERSÃO FINAL DO DOCUMENTO]

Revisar a correspondência do diagrama com as classes após as próximas etapas.

## 6. Verificação desta etapa

Foram executados testes automatizados com a biblioteca padrão `unittest` para
dados válidos e inválidos, estratégias, estados, aquisições, cobranças,
pagamento com saldo exato, eliminação, bônus, observadores e interação textual.
Os testes de integração também verificam os imports dos módulos sem iniciar
uma sessão interativa. O comando do README permite reproduzir os testes.

[ACRESCENTAR RESULTADOS, VERSÃO DO PYTHON E EVIDÊNCIAS REVISADAS NA ENTREGA FINAL]

## 7. Decisões, limitações e próximos passos

As decisões iniciais estão em [`decisoes.md`](decisoes.md). Antes de implementar
novos lugares especiais, é necessário definir se seus movimentos dão bônus,
se ativam a casa de destino e se permitem encadeamentos. Também precisam ser
definidas perdas obrigatórias de saldo nesses lugares.

O catálogo e os valores precisam ser calibrados para partidas rápidas. As
interpretações provisórias precisam ser confirmadas. A base atual não
representa a conclusão do jogo final.

## 8. Referências

- Requisitos fornecidos para este trabalho, registrados em `requisitos.md`.
- [PREENCHER AS REFERÊNCIAS BIBLIOGRÁFICAS SOBRE GoF E ORIENTAÇÃO A OBJETOS
  REALMENTE CONSULTADAS PELA EQUIPE, NO FORMATO EXIGIDO PELA DISCIPLINA.]

## 9. Preparação da entrega final

- Preencher a capa com todos os integrantes reais e os dados institucionais.
- Confirmar requisitos e interpretações; atualizar o escopo implementado.
- Revisar os trechos de código e as classes participantes dos quatro padrões.
- Renderizar e inserir o diagrama coerente com a versão entregue.
- Reexecutar os testes e registrar os resultados.
- Reunir código, diagrama e documento no ZIP; excluir ambiente virtual, caches
  e metadados locais de desenvolvimento.
