import math
import unittest

from ajudagro import AJUDAGRO


class TestAjudagroFormulas(unittest.TestCase):
    def test_formulas_correcao_solo(self) -> None:
        sb = AJUDAGRO.CorrecaoSolo.calcular_soma_bases(2.0, 1.0, 0.3)
        self.assertAlmostEqual(sb, 3.3)

        ca_mg = AJUDAGRO.CorrecaoSolo.calcular_calcio_magnesio(2.0, 1.0)
        self.assertAlmostEqual(ca_mg, 3.0)

        ctc = AJUDAGRO.CorrecaoSolo.calcular_ctc_ph7(sb, 4.0)
        self.assertAlmostEqual(ctc, 7.3)

        v1 = AJUDAGRO.CorrecaoSolo.calcular_v_atual(sb, ctc)
        self.assertAlmostEqual(v1, (3.3 / 7.3) * 100.0)

        nc_sp = AJUDAGRO.CorrecaoSolo.nc_saturacao_bases(70.0, v1, ctc, 80.0)
        self.assertAlmostEqual(nc_sp, ((70.0 - v1) * 7.3) / 80.0)

        nc_mg = AJUDAGRO.CorrecaoSolo.nc_neutralizacao_aluminio(2.0, 1.5, 2.5, 1.0, 0.5)
        self.assertAlmostEqual(nc_mg, (2.0 * 1.5) + (2.5 - (1.0 + 0.5)))

        nc_smp = AJUDAGRO.CorrecaoSolo.nc_indice_smp(10.0, 1.5, 5.5)
        self.assertAlmostEqual(nc_smp, math.exp(10.0 - (1.5 * 5.5)) / 1000.0)

    def test_formulas_adubacao(self) -> None:
        self.assertAlmostEqual(AJUDAGRO.Adubacao.fosforo_para_p2o5(15.0), 15.0 * 2.29)
        self.assertAlmostEqual(AJUDAGRO.Adubacao.potassio_para_k2o(50.0), 50.0 * 1.20)
        self.assertAlmostEqual(AJUDAGRO.Adubacao.necessidade_gessagem_por_argila(30.0), 50.0 * 30.0)

    def test_formula_ras(self) -> None:
        ras = AJUDAGRO.QualidadeAgua.razao_adsorcao_sodio(8.0, 2.0, 1.0)
        self.assertAlmostEqual(ras, 8.0 / math.sqrt((2.0 + 1.0) / 2.0))

    def test_formulas_clima(self) -> None:
        eto = AJUDAGRO.Clima.evapotranspiracao_penman_monteith(
            delta=0.2,
            rn=10.0,
            g=1.0,
            gamma=0.07,
            t=25.0,
            u2=2.0,
            es=3.2,
            ea=2.1,
        )
        esperado = (
            0.408 * 0.2 * (10.0 - 1.0)
            + 0.07 * (900.0 / (25.0 + 273.0)) * 2.0 * (3.2 - 2.1)
        ) / (0.2 + 0.07 * (1.0 + 0.34 * 2.0))
        self.assertAlmostEqual(eto, esperado)

        arm = AJUDAGRO.Clima.balanco_hidrico(40.0, 12.0, 5.0, 60.0)
        self.assertAlmostEqual(arm, 47.0)

    def test_formula_eups(self) -> None:
        perda = AJUDAGRO.ConservacaoSolo.perda_solo_eups(100.0, 0.2, 1.3, 1.1, 0.5, 0.8)
        self.assertAlmostEqual(perda, 100.0 * 0.2 * 1.3 * 1.1 * 0.5 * 0.8)


if __name__ == "__main__":
    unittest.main()
