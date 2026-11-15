# Decisões iniciais

## DEC-01 — Adaptar a base encontrada

A inspeção inicial encontrou apenas `README.md`, com o título do projeto, e
nenhuma alteração local pendente. Não havia `AGENTS.md` no repositório ou nos
diretórios ancestrais consultados. Foram consideradas as instruções AGENTS.md
fornecidas na conversa. O título existente foi preservado e o README ampliado.

## DEC-02 — Pacote `src` e biblioteca padrão

Usar `src/jogo_pds`, Python 3.11+ e testes `unittest`. Não há dependências de
execução. `setuptools` é somente o backend de empacotamento para a instalação
opcional e o comando `jogo-pds`. A execução por `PYTHONPATH=src` dispensa essa
instalação. As verificações locais desta etapa foram executadas com Python
3.15.2; não foi executada uma matriz de versões.

## DEC-03 — Terminal e composição explícita

A dispensa de interface gráfica permite usar somente entrada e saída textuais.
`main.py` monta os objetos sem contêiner de injeção de dependências. O terminal
converte texto em comandos; o controlador os invoca, e o domínio valida as
ações. Não há comunicação em rede, servidor, autenticação ou persistência.

## DEC-04 — Uma fatia executável do jogo

O fluxo comum foi implementado para permitir demonstrar os padrões em uso:
dados, avanço, oferta opcional, pagamento e alternância. A cobrança impagável
encerra a demonstração com vencedor. Há oito casas com nomes fictícios de
logradouros e dois jogadores com nomes genéricos. Esses nomes não são nomes de
integrantes da equipe.

O catálogo final e os efeitos especiais não estão prontos. Nenhuma casa
anunciada como penalidade, prêmio ou teletransporte foi criada com efeito
vazio. `LugarEspecial` é abstrato; `PontoPartida` apenas encerra a visita,
pois o bônus de passagem do avanço comum já foi calculado.

## DEC-05 — Saldo e propriedade protegidos

Valores são créditos inteiros não negativos, rejeitando `bool` e frações.
Débito insuficiente lança `SaldoInsuficiente` antes de alterar o saldo.
Pagamento usa o mesmo limite; igualdade é permitida. Na cobrança obrigatória,
`Jogo` interpreta a insuficiência como eliminação. Na compra, registra a falha
e mantém a oferta aberta, sem eliminar.

`Propriedade` guarda um proprietário somente de leitura e impede nova compra.
O portfólio é consultado a partir desse vínculo, sem manter cópias no jogador.
Não há operação de venda, transferência, hipoteca ou liquidação. As entidades
são usadas em um processo síncrono, sem concorrência.

## DEC-06 — Quatro padrões em responsabilidades existentes

Strategy atende a variação de taxa; State delimita as ações por etapa; Command
separa solicitação e execução; Observer alimenta um histórico em memória.
Não foram acrescentados padrões GoF apenas para aumentar a contagem. Classes
abstratas tornam explícitos os contratos substituíveis. O controlador é pequeno
porque sua responsabilidade concreta é invocar os comandos; ele não duplica
a coordenação das regras que já pertence a `Jogo`.

## DEC-07 — Regras indefinidas são rastreadas

As interpretações INT-01 a INT-10 em `requisitos.md` são provisórias. Em
particular, soma dos dados, fórmula variável, bônus ao completar volta,
ordem de crédito e ausência de pagamento parcial precisam ser confirmados.

Não foi decidida a aplicação de bônus em movimentos especiais nem a ativação
da casa de destino ou de encadeamentos. A operação de avanço normal não deve
ser aplicada automaticamente a esses movimentos futuros. Também permanece
pendente definir perdas de saldo em efeitos especiais e sua relação com a
eliminação.

## DEC-08 — Entrega acadêmica evolutiva

Diagrama e documento inicial descrevem as classes existentes. Os trechos em
`arquitetura.md` e no modelo acadêmico são extraídos da implementação desta
etapa; precisam ser revistos quando ela mudar. O modelo usa campos vazios
para integrantes e dados institucionais. Documento final formatado, nomes,
diagrama revisado e ZIP pertencem à preparação da entrega final.
