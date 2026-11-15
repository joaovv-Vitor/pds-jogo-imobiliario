# Requisitos e rastreabilidade

## Origem e leitura

Referência: requisitos fornecidos pela equipe nesta etapa, incluindo a dispensa
posterior da interface gráfica pela professora. Não foi fornecido um documento
original para comparação. Os identificadores abaixo são locais a este projeto.

- **EX**: exigência informada, sem acrescentar interpretação ao enunciado.
- **INT**: escolha provisória da implementação; precisa ser validada pela equipe.
- **PEN**: definição ou funcionalidade ainda pendente.
- **ENT**: item exigido para a entrega acadêmica.

“Implementado” indica comportamento disponível no tabuleiro de demonstração;
não significa que o jogo final está concluído. Os testes citados estão em
[`tests/test_regras.py`](../tests/test_regras.py) e
[`tests/test_terminal.py`](../tests/test_terminal.py).

## Exigências funcionais

| ID | Exigência | Situação nesta etapa / evidência |
| --- | --- | --- |
| EX-01 | Exatamente dois jogadores, com ações por turnos. | Implementado: `Jogo` valida a dupla; estados delimitam as ações e alternam a vez. Testes de quantidade, alternância e bloqueio de ações. |
| EX-02 | Tabuleiro circular com ponto de partida. | Implementado: `Tabuleiro.avancar`; `PontoPartida` na posição zero. |
| EX-03 | Entrada manual de dois dados de seis lados. | Implementado: comando `dados`; `Dados` valida cada inteiro entre 1 e 6. |
| EX-04 | Mostrar jogador da vez, posição e portfólio dos dois jogadores. | Implementado: `Terminal._mostrar_situacao`; saldo, imóveis e empresas separados. |
| EX-05 | Portfólio contém saldo, imóveis e empresas adquiridos. | Implementado: saldo em `Jogador`; aquisições consultadas em `Tabuleiro.adquiridos_por`. |
| EX-06 | Três categorias: imóvel, empresa e lugar especial. | Modeladas por `Imovel`, `Empresa` e `LugarEspecial`. O único lugar especial concreto é `PontoPartida`; outros efeitos estão pendentes. |
| EX-07 | Imóveis e empresas sem dono podem ser comprados pelo visitante; compra opcional. | Implementado: `Propriedade.receber_visita`, `AguardandoCompra`, `Comprar` e `RecusarCompra`. |
| EX-08 | Logradouro sem proprietário não cobra taxa. | Implementado: a visita apenas abre uma oferta, sem debitar. |
| EX-09 | Imóvel adversário cobra aluguel. | Implementado: `Imovel.calcular_cobranca` e `Jogo.cobrar`. |
| EX-10 | Empresa adversária cobra taxa fixa ou dependente dos dados. | Implementado: `Empresa`, `TaxaFixa` e `TaxaVariavel`; fórmula variável é INT-02. |
| EX-11 | Pagamentos são creditados ao proprietário. | Implementado: `Jogador.pagar_para`; testes de aluguel e dos dois tipos de empresa. |
| EX-12 | Visita à própria propriedade não gera pagamento. | Implementado em `Propriedade.receber_visita`. |
| EX-13 | Imóveis e empresas adquiridos não podem ser transferidos. | Implementado: proprietário somente pode ser definido na primeira compra; nova compra é rejeitada antes de debitar. Não há comando de transferência. |
| EX-14 | Lugares especiais não são compráveis e podem alterar posição ou saldo. | Compra impedida pela hierarquia; `PontoPartida` não oferece compra. Efeitos adicionais de saldo/movimento não implementados (PEN-01 a PEN-03). |
| EX-15 | Passar pela Partida gera crédito, mesmo sem parar. | Implementado para avanço comum pelos dados; testes de passagem, parada e múltiplas voltas. Ver INT-04 e PEN-02. |
| EX-16 | Nenhum saldo pode ser negativo. | Implementado em `Jogador.debitar`; créditos, preços e taxas também são validados. |
| EX-17 | Cobrança obrigatória sem saldo elimina; o outro jogador vence. | Implementado: `Jogo.cobrar` e `Finalizada`; novas ações são rejeitadas. |
| EX-18 | Saldo igual à cobrança permite pagamento e saldo final zero. | Implementado e testado; zero sozinho não causa eliminação. |
| EX-19 | Falta de saldo para compra impede aquisição, sem eliminar. | Implementado e testado; a oferta permanece aberta (INT-06). |
| EX-20 | Valores de compra, taxas, saldo inicial e bônus devem permitir calibração para partidas rápidas. | Centralizados em `Configuracao`; duração e balanceamento ainda não validados (PEN-04). |
| EX-21 | Interação pelo terminal, dispensada a interface gráfica. | Implementado; não há frontend, servidor HTTP ou API. |

## Exigências de arquitetura e escopo

| ID | Exigência | Evidência |
| --- | --- | --- |
| EX-22 | Pelo menos quatro padrões GoF. | Strategy, State, Command e Observer com participantes descritos em `arquitetura.md`. |
| EX-23 | Separação entre apresentação, controladores e lógica. | Pacotes `presentation`, `application/controllers` e `domain`. |
| EX-24 | Polimorfismo, responsabilidades claras e baixo acoplamento. | Contratos abstratos de taxas, estados, comandos, logradouros e observadores; composição em `main.py`. |
| EX-25 | Observer com publicador e observadores explícitos; domínio sem conhecimento do terminal. | `Publicador`, `Observador` e `HistoricoTextual`; não há imports de aplicação/apresentação no domínio. |
| EX-26 | Não incluir banco, autenticação, rede ou persistência nesta etapa. | Dados e histórico somente em memória; nenhuma dependência externa em execução. |
| EX-27 | Não simular regras ausentes com métodos vazios. | Contratos abstratos lançam `NotImplementedError`; ações inválidas lançam `AcaoInvalida`; nenhum efeito especial fictício foi criado. |

## Interpretações adotadas

Estas escolhas **não foram dadas como texto explícito do enunciado**.

| ID | Interpretação provisória | Consequência |
| --- | --- | --- |
| INT-01 | Movimento normal avança pela soma dos dois dados, em um único sentido. | `Dados.soma` alimenta `Tabuleiro.avancar`. Não há recuo ou sorteio automático. |
| INT-02 | Taxa variável = multiplicador configurável × soma dos dados da jogada atual. | `TaxaVariavel.calcular`; não se informam dados novos para a cobrança. |
| INT-03 | Valores em créditos inteiros não negativos. | Sem centavos, juros ou arredondamentos. A configuração aceita zero para facilitar cenários de teste. |
| INT-04 | Cada passagem na movimentação comum credita um bônus, inclusive ao chegar exatamente à Partida; iniciar na casa zero não gera crédito. | Em tabuleiro curto pode haver mais de um bônus por jogada. Parar na Partida não gera um segundo crédito. |
| INT-05 | O bônus do movimento comum é creditado antes de resolver a casa de destino. | Pode compor o saldo usado para pagar uma cobrança ou realizar compra. |
| INT-06 | Compra sem saldo mantém a oferta aberta e permite recusá-la. | Não elimina nem alterna automaticamente o turno. |
| INT-07 | Cobrança impagável não faz pagamento parcial. | O jogador é eliminado com saldo preservado; o credor só recebe cobranças integralmente pagas. Não há liquidação de bens nesta base. |
| INT-08 | Jogador 1 inicia; ambos começam na Partida. Dados iguais não dão turno extra nesta demonstração. | Ordem e comportamento provisórios, sujeitos a confirmação (PEN-05). |
| INT-09 | Compra concluída, recusa, visita própria, pagamento ou parada na Partida encerram o turno. | A resolução de uma oferta integra o mesmo turno do movimento. |
| INT-10 | Preço de compra é debitado e sai da circulação; não há entidade “banco”. | Apenas cobranças entre jogadores geram crédito ao adversário. |

## Pendências

| ID | Questão ou trabalho pendente | Tratamento atual |
| --- | --- | --- |
| PEN-01 | Quais lugares especiais existirão e quais valores/efeitos de saldo terão? | Apenas `PontoPartida` concreto. Não há penalidades, prêmios ou cartas especiais. |
| PEN-02 | Movimentos especiais dão bônus? Recuos, teletransportes e saltos contam como passagem? | Não há movimentos especiais; `Tabuleiro.avancar` trata somente avanço pelos dados. Não reutilizar essa regra para outros efeitos sem decisão explícita. |
| PEN-03 | Movimento especial ativa a casa de destino? Pode encadear outros efeitos? Como evitar ciclos? | Não implementado; definir antes de criar esses efeitos. |
| PEN-04 | Catálogo final, número de casas, preços, taxas, saldo, bônus e duração desejada. | Oito casas e valores demonstrativos; precisam de calibração em partidas reais. |
| PEN-05 | Confirmar INT-01 a INT-10, inclusive fórmula variável, ordem inicial e dados iguais. | Escolhas documentadas, sem tratá-las como exigências originais. |
| PEN-06 | Efeito especial com perda obrigatória de saldo segue exatamente a eliminação por cobrança? Quem recebe eventual crédito? | Não implementar até definir; saldo negativo permanece proibido. |
| PEN-07 | Confirmar se o documento final deve registrar apenas padrões efetivamente aplicados ou também alternativas descartadas. | O modelo já descreve os quatro padrões existentes e suas evidências. |
| PEN-08 | Identificar todos os integrantes, instituição, disciplina/turma, docente, local e data; fechar formato da entrega. | Campos vazios no modelo; diagrama final e documento precisam ser revisados e incluídos no ZIP. |

## Entrega acadêmica

| ID | Item final | Situação |
| --- | --- | --- |
| ENT-01 | ZIP com código-fonte. | Estrutura criada; empacotamento final pendente. |
| ENT-02 | Diagrama de classes com os padrões. | Mermaid inicial em `diagrama-classes.md`, a atualizar conforme o código evoluir. |
| ENT-03 | Documento com decisões, classes participantes e trechos correspondentes. | Base em `arquitetura.md`, `decisoes.md` e `documento-academico.md`. |
| ENT-04 | Capa com nomes de todos os integrantes. | Modelo com campos a preencher, sem integrantes inventados. |
