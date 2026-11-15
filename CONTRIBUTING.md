# Contribuição

## Padrão de commits

As mensagens de commit deste projeto seguem o formato:

```text
tipo(escopo): descrição
```

O escopo é opcional. Use os tipos em inglês e escreva a descrição em português.

### Tipos

| Tipo | Quando usar |
| --- | --- |
| `feat` | Adicionar uma funcionalidade ou regra do jogo. |
| `fix` | Corrigir um comportamento incorreto. |
| `docs` | Alterar requisitos, diagramas, README ou documento acadêmico. |
| `refactor` | Reorganizar código sem alterar seu comportamento. |
| `test` | Adicionar ou ajustar testes. |
| `style` | Ajustar formatação do código sem alterar seu comportamento. |
| `build` | Alterar empacotamento ou dependências do projeto. |
| `chore` | Fazer manutenção que não se enquadre nos tipos anteriores. |

### Escopos

Escolha a área principal afetada. Exemplos para este repositório:

- `domain`: entidades e regras do jogo.
- `taxas`, `estados` e `eventos`: responsabilidades específicas do domínio.
- `application`: comandos, controlador e histórico.
- `cli`: interação pelo terminal.
- `projeto`: estrutura e configuração geral.

Quando a alteração não tiver uma área clara, omita o escopo.

### Escrita e organização

- Comece a descrição com um verbo de ação, como `adiciona`, `corrige` ou
  `documenta`.
- Prefira títulos de até 72 caracteres, sem ponto final.
- Descreva o que mudou; evite mensagens como `ajustes`, `update` ou `final`.
- Mantenha cada commit focado em uma mudança coerente. Uma regra e seus testes
  podem fazer parte do mesmo commit.
- Separe mudanças independentes, como uma correção de cobrança e uma revisão
  da capa acadêmica.
- Quando necessário, acrescente um corpo separado do título por uma linha em
  branco, explicando o motivo da mudança e como ela foi verificada.

### Exemplos

```text
feat(cli): adiciona entrada manual dos dois dados
fix(domain): permite pagar cobrança com saldo exato
refactor(taxas): extrai contrato de cálculo das empresas
test(estados): cobre rejeição de compra fora da etapa permitida
docs: atualiza diagrama de classes
build(projeto): configura ponto de entrada do pacote
chore(projeto): ignora arquivos temporários do Python
```

Exemplo de mensagem com corpo:

```text
fix(domain): impede saldo negativo em cobranças

Valida o saldo antes de transferir o valor ao proprietário.
Uma cobrança impagável elimina o visitante sem pagamento parcial.

Verificação: testes de saldo insuficiente e saldo exatamente igual à cobrança.
```

## Verificação antes do commit

Para alterações de código, execute os testes indicados no
[README](README.md#verificação). Para alterações somente de documentação,
confira os links e a correspondência das descrições com o código existente.
