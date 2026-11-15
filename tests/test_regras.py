import unittest

from jogo_pds.application.historico import HistoricoTextual
from jogo_pds.domain.configuracao import Configuracao
from jogo_pds.domain.dados import Dados
from jogo_pds.domain.erros import AcaoInvalida, ErroDeRegra, SaldoInsuficiente
from jogo_pds.domain.estados.partida import AguardandoCompra, AguardandoDados, Finalizada
from jogo_pds.domain.eventos.observacao import Evento, Publicador
from jogo_pds.domain.jogador import Jogador
from jogo_pds.domain.jogo import Jogo
from jogo_pds.domain.logradouros import Empresa, Imovel, PontoPartida
from jogo_pds.domain.tabuleiro import Tabuleiro
from jogo_pds.domain.taxas.estrategias import TaxaFixa, TaxaVariavel


class TestValores(unittest.TestCase):
    def test_dados_validos_e_soma(self):
        for primeiro in range(1, 7):
            for segundo in range(1, 7):
                dados = Dados(primeiro, segundo)
                self.assertEqual(dados.soma, primeiro + segundo)

    def test_dados_rejeitam_fora_da_faixa_e_nao_inteiros(self):
        for invalido in (0, 7, -1, True, False, 2.0, "2", None):
            for par in ((invalido, 1), (1, invalido)):
                with self.subTest(par=par), self.assertRaises(ErroDeRegra):
                    Dados(*par)

    def test_taxas_fixa_e_variavel(self):
        for dados in (Dados(1, 1), Dados(2, 5), Dados(6, 6)):
            self.assertEqual(TaxaFixa(15).calcular(dados), 15)
            self.assertEqual(TaxaVariavel(3).calcular(dados), 3 * dados.soma)

    def test_valores_monetarios_invalidos(self):
        for invalido in (-1, True, 1.5):
            for construir in (
                lambda: Jogador("Ana", invalido),
                lambda: Imovel("Rua", invalido, 10),
                lambda: Imovel("Rua", 10, invalido),
                lambda: TaxaFixa(invalido),
                lambda: TaxaVariavel(invalido),
                lambda: Configuracao(bonus_partida=invalido),
            ):
                with self.subTest(valor=invalido, construir=construir), self.assertRaises(ErroDeRegra):
                    construir()

    def test_saldo_nao_fica_negativo_nem_aceita_debito_negativo(self):
        jogador = Jogador("Ana", 10)
        with self.assertRaises(SaldoInsuficiente):
            jogador.debitar(11)
        with self.assertRaises(ErroDeRegra):
            jogador.debitar(-5)
        with self.assertRaises(ErroDeRegra):
            jogador.creditar(-5)
        self.assertEqual(jogador.saldo, 10)
        jogador.debitar(10)
        self.assertEqual(jogador.saldo, 0)

    def test_pagamento_sem_saldo_nao_faz_transferencia_parcial(self):
        origem, destino = Jogador("Ana", 10), Jogador("Beto", 20)
        with self.assertRaises(SaldoInsuficiente):
            origem.pagar_para(destino, 11)
        self.assertEqual((origem.saldo, destino.saldo), (10, 20))

    def test_tabuleiro_valida_partida_e_posicao(self):
        rua = Imovel("Rua", 10, 1)
        for casas in ([], [PontoPartida()], [rua, PontoPartida()], [PontoPartida(), PontoPartida()], [PontoPartida(), rua, rua]):
            with self.subTest(casas=casas), self.assertRaises(ErroDeRegra):
                Tabuleiro(casas)
        tabuleiro = Tabuleiro([PontoPartida(), rua])
        with self.assertRaises(ErroDeRegra):
            tabuleiro.avancar(2, 1)
        with self.assertRaises(ErroDeRegra):
            tabuleiro.avancar(0, -1)


class TestPartida(unittest.TestCase):
    def setUp(self):
        self.ana = Jogador("Ana", 100)
        self.beto = Jogador("Beto", 100)
        self.imovel = Imovel("Rua", 40, 20)
        self.fixa = Empresa("Água", 40, TaxaFixa(15))
        self.variavel = Empresa("Energia", 40, TaxaVariavel(3))
        self.tabuleiro = Tabuleiro([
            PontoPartida(), Imovel("Alameda", 40, 20), self.imovel,
            self.fixa, self.variavel, Imovel("Praça", 40, 20),
            Imovel("Avenida", 40, 20), Imovel("Travessa", 40, 20),
        ])
        self.publicador = Publicador()
        self.historico = HistoricoTextual()
        self.publicador.inscrever(self.historico)
        self.jogo = Jogo([self.ana, self.beto], self.tabuleiro, self.publicador, 25)

    def test_exatamente_dois_jogadores_distintos(self):
        terceiro = Jogador("Caio", 100)
        for jogadores in ([], [self.ana], [self.ana, self.ana], [self.ana, self.beto, terceiro], [self.ana, Jogador("ANA", 100)]):
            with self.subTest(jogadores=jogadores), self.assertRaises(ErroDeRegra):
                Jogo(jogadores, self.tabuleiro, Publicador(), 25)

    def test_inicio_sem_bonus_e_acoes_fora_de_estado_rejeitadas(self):
        self.assertEqual(self.ana.saldo, 100)
        for acao in (self.jogo.comprar, self.jogo.recusar_compra):
            with self.assertRaises(AcaoInvalida):
                acao()
        self.assertIs(self.jogo.jogador_atual, self.ana)

    def test_visita_sem_dono_oferece_compra_sem_cobrar(self):
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual(self.ana.posicao, 2)
        self.assertEqual((self.ana.saldo, self.beto.saldo), (100, 100))
        self.assertIsInstance(self.jogo.estado, AguardandoCompra)
        self.assertIs(self.jogo.jogador_atual, self.ana)
        with self.assertRaises(AcaoInvalida):
            self.jogo.informar_dados(Dados(2, 2))
        self.assertEqual(self.ana.posicao, 2)

    def test_recusa_nao_adquire_e_alterna_turno(self):
        self.jogo.informar_dados(Dados(1, 1))
        self.jogo.recusar_compra()
        self.assertIsNone(self.imovel.proprietario)
        self.assertEqual(self.ana.saldo, 100)
        self.assertIs(self.jogo.jogador_atual, self.beto)
        self.assertIsInstance(self.jogo.estado, AguardandoDados)
        self.jogo.informar_dados(Dados(1, 2))
        self.jogo.recusar_compra()
        self.assertIs(self.jogo.jogador_atual, self.ana)

    def test_compra_atualiza_saldo_portfolio_e_turno(self):
        self.jogo.informar_dados(Dados(1, 1))
        self.jogo.comprar()
        self.assertEqual(self.ana.saldo, 60)
        self.assertIs(self.imovel.proprietario, self.ana)
        self.assertEqual(self.tabuleiro.adquiridos_por(self.ana), (self.imovel,))
        self.assertIs(self.jogo.jogador_atual, self.beto)
        with self.assertRaises(ErroDeRegra):
            self.imovel.comprar(self.beto)
        self.assertEqual(self.beto.saldo, 100)

    def test_compra_sem_saldo_nao_elimina_e_permite_recusar(self):
        self.ana.debitar(61)
        self.jogo.informar_dados(Dados(1, 1))
        self.jogo.comprar()
        self.assertIsNone(self.imovel.proprietario)
        self.assertEqual(self.ana.saldo, 39)
        self.assertFalse(self.ana.eliminado)
        self.assertIsNone(self.jogo.vencedor)
        self.assertIsInstance(self.jogo.estado, AguardandoCompra)
        self.jogo.recusar_compra()
        self.assertIs(self.jogo.jogador_atual, self.beto)

    def test_compra_com_saldo_exato(self):
        self.ana.debitar(60)
        self.jogo.informar_dados(Dados(1, 1))
        self.jogo.comprar()
        self.assertEqual(self.ana.saldo, 0)
        self.assertFalse(self.ana.eliminado)
        self.assertIs(self.imovel.proprietario, self.ana)

    def test_propriedade_propria_nao_cobra(self):
        self.imovel.comprar(self.ana)
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual(self.ana.saldo, 60)
        self.assertIs(self.jogo.jogador_atual, self.beto)

    def test_aluguel_creditado_ao_adversario(self):
        self.imovel.comprar(self.beto)
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (80, 80))
        self.assertIs(self.jogo.jogador_atual, self.beto)

    def test_empresa_fixa_credita_taxa_ao_adversario(self):
        self.fixa.comprar(self.beto)
        self.jogo.informar_dados(Dados(1, 2))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (85, 75))

    def test_empresa_variavel_usa_dados_da_jogada(self):
        self.variavel.comprar(self.beto)
        self.jogo.informar_dados(Dados(1, 3))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (88, 72))

    def test_cobranca_com_saldo_exato_nao_elimina(self):
        self.imovel.comprar(self.beto)
        self.ana.debitar(80)
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (0, 80))
        self.assertFalse(self.ana.eliminado)
        self.assertIsNone(self.jogo.vencedor)
        self.assertIsInstance(self.jogo.estado, AguardandoDados)

    def test_cobranca_impagavel_finaliza_sem_deixar_saldo_negativo(self):
        self.imovel.comprar(self.beto)
        self.ana.debitar(81)
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (19, 60))
        self.assertTrue(self.ana.eliminado)
        self.assertIs(self.jogo.vencedor, self.beto)
        self.assertIsInstance(self.jogo.estado, Finalizada)
        for acao in (
            lambda: self.jogo.informar_dados(Dados(1, 1)),
            self.jogo.comprar, self.jogo.recusar_compra,
        ):
            with self.assertRaises(AcaoInvalida):
                acao()

    def test_passagem_credita_bonus_mesmo_sem_parar(self):
        self.ana.mover_para(7)
        self.jogo.informar_dados(Dados(1, 2))
        self.assertEqual(self.ana.posicao, 2)
        self.assertEqual(self.ana.saldo, 125)

    def test_parada_na_partida_nao_duplica_bonus_nem_oferece_compra(self):
        self.ana.mover_para(6)
        self.jogo.informar_dados(Dados(1, 1))
        self.assertEqual(self.ana.posicao, 0)
        self.assertEqual(self.ana.saldo, 125)
        self.assertIsInstance(self.jogo.estado, AguardandoDados)
        self.assertIs(self.jogo.jogador_atual, self.beto)
        with self.assertRaises(AcaoInvalida):
            self.jogo.comprar()

    def test_avanco_com_duas_passagens_paga_dois_bonus(self):
        self.ana.mover_para(7)
        self.jogo.informar_dados(Dados(6, 6))
        self.assertEqual(self.ana.posicao, 3)
        self.assertEqual(self.ana.saldo, 150)

    def test_bonus_e_creditado_antes_da_cobranca(self):
        self.imovel.comprar(self.beto)
        self.ana.debitar(100)
        self.ana.mover_para(7)
        self.jogo.informar_dados(Dados(1, 2))
        self.assertEqual((self.ana.saldo, self.beto.saldo), (5, 80))
        self.assertFalse(self.ana.eliminado)


class TestObservacao(unittest.TestCase):
    def test_publicador_notifica_varios_observadores_sem_duplicar_e_permite_remover(self):
        publicador = Publicador()
        primeiro, segundo = HistoricoTextual(), HistoricoTextual()
        publicador.inscrever(primeiro)
        publicador.inscrever(primeiro)
        publicador.inscrever(segundo)
        publicador.publicar(Evento("teste", "Primeiro acontecimento"))
        self.assertEqual(primeiro.linhas, segundo.linhas)
        self.assertEqual(len(primeiro.linhas), 1)
        publicador.remover(primeiro)
        publicador.publicar(Evento("teste", "Segundo acontecimento"))
        self.assertEqual(len(primeiro.linhas), 1)
        self.assertEqual(len(segundo.linhas), 2)


if __name__ == "__main__":
    unittest.main()
