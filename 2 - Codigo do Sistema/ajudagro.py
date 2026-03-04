import math
from typing import Optional

class AJUDAGRO:
    """
    Biblioteca de cálculos agronômicos AJUDAGRO.
    Contém módulos de correção de solo, adubação, salinidade, física do solo (erosão)
    e cálculos de clima/evapotranspiração.
    """

    class CorrecaoSolo:
        @staticmethod
        def calcular_soma_bases(ca: float, mg: float, k: float) -> float:
            """
            Calcula a Soma de Bases (SB).
            Unidades geralmente em cmolc/dm³.
            """
            return ca + mg + k

        @staticmethod
        def calcular_calcio_magnesio(ca: float, mg: float) -> float:
            """
            Calcula a soma de Cálcio e Magnésio (Ca + Mg).
            """
            return ca + mg

        @staticmethod
        def calcular_ctc_ph7(sb: float, h_al: float) -> float:
            """
            Calcula a Capacidade de Troca Catiônica (CTC) a pH 7.0.
            """
            return sb + h_al

        @staticmethod
        def calcular_v_atual(sb: float, ctc_ph7: float) -> float:
            """
            Calcula a Saturação por bases atual (V1) em porcentagem.
            """
            if ctc_ph7 <= 0:
                return 0.0
            return (sb / ctc_ph7) * 100.0

        @staticmethod
        def nc_saturacao_bases(v2: float, v1: float, ctc_ph7: float, prnt: float) -> float:
            """
            Método da Saturação por Bases (IAC / SP).
            :param v2: Saturação por bases desejada (Ex: 70%).
            :param v1: Saturação por bases atual (%).
            :param ctc_ph7: CTC a pH 7.0 (cmolc/dm³).
            :param prnt: Poder Relativo de Neutralização Total do calcário (%).
            :return: Necessidade de calcário em t/ha.
            """
            if v1 >= v2:
                return 0.0
            return ((v2 - v1) * ctc_ph7) / prnt

        @staticmethod
        def nc_neutralizacao_aluminio(y: float, al: float, x: float, ca: float, mg: float) -> float:
            """
            Método da Neutralização do Al3+ e Elevação de Ca+Mg (CFSEMG / MG e Cerrado).
            :param y: Fator da textura (Buffer capacity) do solo (0 a 3).
            :param al: Teor de alumínio trocável atual (cmolc/dm³).
            :param x: Exigência mínima de Ca+Mg da cultura (cmolc/dm³).
            :param ca: Teor atual medido de Ca no solo.
            :param mg: Teor atual medido de Mg no solo.
            :return: Necessidade de calcário em t/ha.
            """
            ca_mg_atual = AJUDAGRO.CorrecaoSolo.calcular_calcio_magnesio(ca, mg)
            falta_ca_mg = max(0.0, x - ca_mg_atual)
            nc = (y * al) + falta_ca_mg
            return max(0.0, nc)

        @staticmethod
        def nc_indice_smp(a: float, b: float, ph_smp: float) -> float:
            """
            Método do Índice SMP (Sul do Brasil).
            Dada a equação de regressão regional (NC = e^(a - b*pH) / 1000).
            :param a: Coeficiente 'a' da regressão do laboratório.
            :param b: Coeficiente 'b' da regressão do laboratório.
            :param ph_smp: Valor medido no pH SMP.
            :return: Necessidade de calcário usando produto PRNT 100% em t/ha.
            """
            # Implementação da tabela através da curva teórica
            nc = math.exp(a - (b * ph_smp)) / 1000.0
            return max(0.0, nc)

    class Adubacao:
        @staticmethod
        def fosforo_para_p2o5(p_puro: float) -> float:
            """
            Converte Fósforo Elementar puro para Óxido de Fósforo (P2O5).
            """
            return p_puro * 2.29

        @staticmethod
        def potassio_para_k2o(k_puro: float) -> float:
            """
            Converte Potássio Elementar puro para Óxido de Potássio (K2O).
            """
            return k_puro * 1.20

        @staticmethod
        def necessidade_gessagem_por_argila(argila_porcentagem: float) -> float:
            """
            Método da Embrapa Cerrados para Necessidade de Gesso baseada na Argila (textura).
            Ideal para carregar bases ao subsolo em culturas anuais.
            :param argila_porcentagem: Teor percentual da textura fina/argila (%).
            :return: Necessidade do Gesso (NG) em kg/ha.
            """
            return 50.0 * argila_porcentagem

    class QualidadeAgua:
        @staticmethod
        def razao_adsorcao_sodio(na: float, ca: float, mg: float) -> float:
            """
            Calcula o índice de RAS (Módulo de Salinidade, FAO 29).
            :param na: Lio/teores de Na+ da água investigada (meq/L).
            :param ca: Lio/teores de Ca2+ da água investigada (meq/L).
            :param mg: Lio/teores de Mg2+ da água investigada (meq/L).
            :return: Índice de RAS a-dimensional de alerta hídrico.
            """
            if ca + mg <= 0:
                return 0.0
            denominador = math.sqrt((ca + mg) / 2.0)
            return na / denominador

    class Clima:
        @staticmethod
        def evapotranspiracao_penman_monteith(
            delta: float, rn: float, g: float, gamma: float,
            t: float, u2: float, es: float, ea: float
        ) -> float:
            """
            Equação Penman-Monteith de Evapotranspiração referencial ETo (FAO 56).
            """
            parte_um = 0.408 * delta * (rn - g)
            parte_dois = gamma * (900.0 / (t + 273.0)) * u2 * (es - ea)
            
            numerador = parte_um + parte_dois
            denominador = delta + gamma * (1.0 + 0.34 * u2)
            
            return numerador / denominador

        @staticmethod
        def balanco_hidrico(arm_anterior: float, precipitacao: float,
                            etp: float, cad: float) -> float:
            """
            Calcula de maneira unidinâmica (1 dia) a cota ARM de água no solo.
            :param arm_anterior: Quantidade de água retida no solo no período anterior.
            :param precipitacao: Chuva real detectada.
            :param etp: Evapotranspiração programada ou diária da cultura.
            :param cad: Capacidade de Água Disponível da textura avaliada.
            """
            arm_atual = arm_anterior + (precipitacao - etp)
            
            # Limites físicos de porosidade no solo (0 <= ARM <= CAD)
            if arm_atual < 0:
                return 0.0
            elif arm_atual > cad:
                return cad
            return arm_atual

    class ConservacaoSolo:
        @staticmethod
        def perda_solo_eups(r: float, k: float, l: float, s: float, c: float, p: float) -> float:
            """
            Equação Universal de Perda de Solo (EUPS).
            Avalia o total cumulativo de terra orgânica mobilizada de cima da área.
            :param r: Fator erosividade (Chuvas).
            :param k: Erodibilidade relativa da matriz do solo.
            :param l: Fator linear da rampa.
            :param s: Factor declividade de descidas de águas.
            :param c: Retenção promovida pela cultura alvo da lavoura.
            :param p: Práticas conservacionistas inseridas em curva.
            :return: A estimativa escalar de perda da terra (em toneladas/hec/ano).
            """
            return r * k * l * s * c * p

    class ProcessadorArquivos:
        @staticmethod
        def processar_csv_analise_solo(caminho_csv: str) -> list[dict]:
            """
            Lê um arquivo CSV contendo os parâmetros de solo e calcula as fórmulas
            do AJUDAGRO para cada linha (amostra).
            """
            import csv
            resultados = []
            try:
                with open(caminho_csv, mode='r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        res = {"amostra": row.get("amostra", "Desconhecida")}
                        
                        # Função auxiliar para conversão segura
                        def safe_float(key: str) -> float:
                            try:
                                valor = row.get(key, "").strip()
                                return float(valor) if valor else 0.0
                            except ValueError:
                                return 0.0

                        # Leitura de parâmetros
                        ca = safe_float("ca")
                        mg = safe_float("mg")
                        k = safe_float("k")
                        h_al = safe_float("h_al")
                        al = safe_float("al")
                        v2 = safe_float("v2")
                        prnt = safe_float("prnt")
                        y = safe_float("y")
                        x = safe_float("x")
                        ph_smp = safe_float("ph_smp")
                        argila_perc = safe_float("argila_perc")
                        p_puro = safe_float("p_puro")
                        k_puro = safe_float("k_puro")
                        
                        # Opcional: Coeficientes da curva SMP (RS/SC)
                        a_smp = safe_float("a_smp") if row.get("a_smp") else 10.0
                        b_smp = safe_float("b_smp") if row.get("b_smp") else 1.5

                        # 1. Cálculos Base (IAC/SP)
                        sb = AJUDAGRO.CorrecaoSolo.calcular_soma_bases(ca, mg, k)
                        ctc = AJUDAGRO.CorrecaoSolo.calcular_ctc_ph7(sb, h_al)
                        v1 = AJUDAGRO.CorrecaoSolo.calcular_v_atual(sb, ctc)
                        res["v1_atual"] = round(v1, 2)
                        
                        if v2 > 0 and prnt > 0:
                            nc_sp = AJUDAGRO.CorrecaoSolo.nc_saturacao_bases(v2, v1, ctc, prnt)
                            res["nc_saturacao_bases_sp"] = round(nc_sp, 2)
                        
                        # 2. Cálculos (CFSEMG/Cerrado)
                        if y > 0 and x > 0:
                            nc_mg = AJUDAGRO.CorrecaoSolo.nc_neutralizacao_aluminio(y, al, x, ca, mg)
                            res["nc_neutralizacao_al_mg"] = round(nc_mg, 2)
                            
                        # 3. Cálculos SMP (Sul)
                        if ph_smp > 0:
                            nc_sul = AJUDAGRO.CorrecaoSolo.nc_indice_smp(a_smp, b_smp, ph_smp)
                            res["nc_indice_smp_sul"] = round(nc_sul, 2)
                            
                        # 4. Gessagem
                        if argila_perc > 0:
                            ng = AJUDAGRO.Adubacao.necessidade_gessagem_por_argila(argila_perc)
                            res["necessidade_gesso_kg_ha"] = round(ng, 2)
                            
                        # 5. Adubação Equivalente
                        if p_puro > 0:
                            res["fosfato_p2o5_eq"] = round(AJUDAGRO.Adubacao.fosforo_para_p2o5(p_puro), 2)
                        if k_puro > 0:
                            res["potassio_k2o_eq"] = round(AJUDAGRO.Adubacao.potassio_para_k2o(k_puro), 2)
                        
                        # Qualidade Água (Se houver parâmetros de sódio)
                        na_agua = safe_float("na_agua")
                        ca_agua = safe_float("ca_agua")
                        mg_agua = safe_float("mg_agua")
                        if na_agua > 0:
                            ras = AJUDAGRO.QualidadeAgua.razao_adsorcao_sodio(na_agua, ca_agua, mg_agua)
                            res["indice_ras_agua"] = round(ras, 2)

                        resultados.append(res)
            except Exception as e:
                print(f"Erro ao processar as análises: {e}")
                
            return resultados

# Execução Principal do Script
if __name__ == "__main__":
    import os
    import sys
    
    caminho_csv = ""
    if len(sys.argv) > 1:
        caminho_csv = sys.argv[1]
    else:
        print("\nDICA: Você pode arrastar o arquivo .csv para cá ou apenas apertar ENTER para rodar o exemplo.")
        caminho_csv = input("Digite o caminho do arquivo CSV com as amostras de solo: ").strip()
        
    # Se o usuário apenas der Enter, usamos o arquivo de modelo da pasta 1
    if not caminho_csv:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_csv = os.path.normpath(os.path.join(pasta_atual, "..", "1 - Planilhas", "modelo_planilha_solo.csv"))
        print(f"\nUsando o arquivo de exemplo padrão...")
        
    if not os.path.exists(caminho_csv):
        print(f"Erro: Arquivo '{caminho_csv}' não encontrado.")
    else:
        print(f"--- Processando Arquivo CSV: {caminho_csv} ---")
        resultados = AJUDAGRO.ProcessadorArquivos.processar_csv_analise_solo(caminho_csv)
        
        for r in resultados:
            print(f"\nResultados para: {r['amostra']}")
            for chave, valor in r.items():
                if chave != "amostra":
                    print(f"  - {chave}: {valor}")
