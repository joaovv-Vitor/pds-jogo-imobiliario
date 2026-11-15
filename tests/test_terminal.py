import importlib
import pkgutil
import unittest

import jogo_pds
from jogo_pds.application.commands.acoes import Comprar, InformarDados, RecusarCompra
from jogo_pds.domain.configuracao import Configuracao
from jogo_pds.domain.dados import Dados
from jogo_pds.domain.estados.partida import Finalizada
from jogo_pds.main import criar_jogo_demo
from jogo_pds.presentation.cli.terminal import Terminal


class TestIntegracao(unittest.TestCase):
    def test_imports_dos_pacotes_sem_abrir_terminal(self):
        for modulo in pkgutil.walk_packages(jogo_pds.__path__, jogo_pds.__name__ + "."):
            if modulo.name != "jogo_pds.__main__":
                with self.subTest(modulo=modulo.name):
                    importlib.import_module(modulo.name)

    def test_comandos_coordenam_partida_e_historico(self):
        controlador, historico = criar_jogo_demo()
        controlador.executar(InformarDados(Dados(1, 1)))
        controlador.executar(Comprar())
        controlador.executar(InformarDados(Dados(1, 1)))
        self.assertEqual(tuple(j.saldo for j in controlador.jogo.jogadores), (215, 285))
        self.assertTrue(any("[pagamento]" in linha for linha in historico.linhas))
        controlador.executar(InformarDados(Dados(1, 1)))
        controlador.executar(RecusarCompra())
        self.assertTrue(any("[compra_recusada]" in linha for linha in historico.linhas))

    def test_terminal_recupera_entradas_invalidas_e_exibe_portfolios(self):
        controlador, historico = criar_jogo_demo()
        entradas = iter([
            "", "dados x 2", "dados 0 6", "dados 1", "comprar",
            "ajuda", "dados 1 1", "dados 2 2", "comprar", "sair",
        ])
        saidas = []
        Terminal(controlador, historico, lambda _: next(entradas), saidas.append).executar()
        texto = "\n".join(saidas)
        self.assertIn("Entrada inválida", texto)
        self.assertIn("Ação rejeitada", texto)
        self.assertIn("Jogador da vez: Jogador 2", texto)
        self.assertIn("empresas: Companhia de Água", texto)
        self.assertIn("saldo 200", texto)
        self.assertIn("sem declarar vencedor", texto)
        self.assertEqual(texto.count("[compra]"), 1)

    def test_terminal_finaliza_apos_eliminacao(self):
        config = Configuracao(saldo_inicial=100, preco_empresa=20, taxa_fixa=101)
        controlador, historico = criar_jogo_demo(config)
        entradas = iter(["dados 1 1", "comprar", "dados 1 1"])
        saidas = []
        Terminal(controlador, historico, lambda _: next(entradas), saidas.append).executar()
        self.assertIsInstance(controlador.jogo.estado, Finalizada)
        self.assertIn("Vencedor: Jogador 1", "\n".join(saidas))

    def test_terminal_trata_fim_da_entrada_e_interrupcao(self):
        for interrupcao in (EOFError, KeyboardInterrupt):
            with self.subTest(interrupcao=interrupcao):
                controlador, historico = criar_jogo_demo()
                saidas = []

                def entrada(_):
                    raise interrupcao

                Terminal(controlador, historico, entrada, saidas.append).executar()
                self.assertIn("sem declarar vencedor", saidas[-1])
                self.assertIsNone(controlador.jogo.vencedor)


if __name__ == "__main__":
    unittest.main()
