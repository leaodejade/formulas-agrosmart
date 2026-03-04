# AJUDAGRO - Fórmulas Agronômicas

Este repositório documenta as fórmulas matemáticas que embasam o sistema **AJUDAGRO**, baseando-se nas metodologias agronômicas mais renomadas (IAC, CFSEMG, Embrapa, FAO). Abaixo está a descrição teórica pormenorizada de cada modelo matemático empregado.

---

## 1. Correção de Solo (Calagem)

A correção do pH e eliminação da acidez ativa e trocável é feita de formas diferentes dependendo da região do país.

### A. Método da Saturação por Bases (IAC - Boletim 100 / Região Sudeste-SP)

Este método visa aplicar uma quantidade de calcário que seja capaz de elevar o percentual da saturação por bases atual para um nível ideal desejado pela cultura.

**Fórmulas:**
- **Necessidade de Calcário (NC)** em toneladas por hectare ($t/ha$):
  $$NC = \frac{(V_2 - V_1) \times CTC_{pH7}}{PRNT}$$

Onde os parâmetros intermediários são obtidos da análise do solo:
- **$V_2$**: Saturação por bases desejada pela cultura a ser plantada (%). Exemplo: Para soja normalmente exige-se cerca de 70%.
- **$V_1$**: Saturação por bases atual, calculada por:
  $$V_1 = \left( \frac{SB}{CTC_{pH7}} \right) \times 100$$
- **$CTC_{pH7}$**: Capacidade de Troca Catiônica do solo em pH 7, dada por:
  $$CTC_{pH7} = SB + (H+Al)$$
- **$SB$**: Soma das Bases, calculada por:
  $$SB = Ca^{2+} + Mg^{2+} + K^{+}$$
- **$PRNT$**: Poder Relativo de Neutralização Total do calcário, avalia a qualidade do calcário que o agricultor está utilizando.

### B. Método da Neutralização do $Al^{3+}$ e Elevação de Cálcio e Magnésio (CFSEMG - 5ª Aproximação / MG e Cerrado)

O cerrado brasileiro, em geral, é mais ácido e com a presença comum de níveis tóxicos de Alumínio. Este método prioriza anular a toxidez.

**Fórmula:**
$$NC (t/ha) = Y \times Al^{3+} + [X - (Ca^{2+} + Mg^{2+})]$$

* **$Y$**: É o fator de correção baseado na capacidade tampão (textura) do solo. Normalmente, $Y$ cresce com o teor de argila do solo (0 a 1 para solos arenosos, 1 a 2 em textura média e 2 a 3 para solos argilosos).
* **$Al^{3+}$**: Nível de alumínio trocável atual ($cmol_{c}/dm^{3}$).
* **$X$**: Nível almejado (a exigência mínima) de Cálcio e Magnésio combinados da cultura ($cmol_{c}/dm^{3}$).
* **$(Ca^{2+} + Mg^{2+})$**: Teor atual medido. 
*Atenção: A parcela referente ao cálcio/magnésio só é somada se $X$ for maior que $(Ca^{2+} + Mg^{2+})$.*

### C. Método do Índice SMP (SBCS / Região Sul)

Na região sul adota-se o cálculo a partir da medição do Índice SMP (método tampão). A correlação na tabela pode ser interpolada usando logaritmo/função exponencial (cuja calibração, as constantes "a" e "b", variam conforme publicações de SC/RS).

**Fórmula referencial (Estimativa Analítica):**
$$NC_{100\%} = \frac{e^{(a - b \times pH_{SMP})}}{1000}$$

* **$a$ e $b$**: Parâmetros constantes que refletem a calibração com o bioma/região (a regressão linear do laboratório).

---

## 2. Adubação (Fosfatagem, Potassagem e Gessagem)

### A. Conversão de Unidades
Muitos laudos trazem Fósforo (P) e Potássio (K) puros. Os tratamentos vendidos na agroindústria representam formulações em seus óxidos comerciais ($P_2O_5$ e $K_2O$).
* **Fosfato:** $$P_2O_5 = P \times 2,29$$
* **Potássio:** $$K_2O = K \times 1,20$$

### B. Necessidade de Gessagem (Embrapa Cerrados / Sousa & Lobato)
Para carregar bases em profundidade (fazer raiz da planta descer até subsuperfície, muito útil contra secas).

**Fórmula (Geral para culturas anuais em cerrado):**
$$NG (kg/ha) = 50 \times (\%Argila)$$

* Uma via secundária, mais específica, observa a saturação de alumínio subsuperficial ($m\%$). O recomendável geral é usar proporção em massa baseada na leitura do teor de argila do solo.

---

## 3. Salinidade e Análise de Água (FAO 29 / Ayers & Westcot)

O excesso de sódio decompões a estrutura dos agregados clásticos do solo. O controle é feito através da **Razão de Adsorção de Sódio (RAS)** na avaliação da água usada para a irrigação.

**Fórmula:**
$$RAS = \frac{Na^{+}}{\sqrt{\frac{Ca^{2+} + Mg^{2+}}{2}}}$$

* Todos os valores devem estar na mesma unidade: $meq/L$ ou $mmol_{c}/L$.
* *Limites práticos:* RAS menor do que 3 está isento de restrições; acima de 9, representa fortíssimo risco para a aeração em nível de infiltração.

---

## 4. Clima e ZARC (Riscos Agrícolas)

O dimensionamento de risco à quebra de safra é baseado na medição da capacidade da lavoura em perder água ao meio ambiente.

### A. Evapotranspiração de Referência ($ETo$) – equação de Penman-Monteith (FAO 56)

Fórmula tida como padrão unificado para cálculos do Zoneamento Agrícola de Risco Climático (ZARC) operado pelo INMET e Embrapa:

$$ETo = \frac{0.408\Delta(R_n - G) + \gamma \frac{900}{T+273} u_2 (e_s - e_a)}{\Delta + \gamma(1 + 0.34u_2)}$$

* **$\Delta$**: Declividade da curva de pressão de vapor da atmosfera.
* **$R_n$ e $G$**: Radiação Líquida e o Fluxo térmico partindo do nível do solo.
* **$\gamma$**: Constante psicrométrica.
* **$T$**: Temperatura referencial diária ($ºC$).
* **$u_2$**: Velocidade do ar em escoamento a 2m.
* **($e_s - e_a$)**: O déficit saturado de pressão do vapor que rege como ocorre a troca de volume com a atmosfera.

### B. Balanço Hídrico Sequencial

Determina a necessidade de provisão contra estresses hídricos diários:
$$ARM_{atual} = ARM_{anterior} + (Precipitação - ETP)$$

* **Capacidade de Água Disponível ($CAD$):** Limite superior do sistema solo/planta. $0 \leq ARM \leq CAD$. A planta só aproveitará até a fronteira que marca a sua exigência hídrica momentaneamente.

---

## 5. Conservação e Erosão de Solo (Embrapa - EUPS)

A Equação Universal de Perda de Solo permite visualizar estimativas das perdas em massa orgânica geradas pelo impacto mecânico repetitivo da passagem das águas em declive. 

**Fórmula:**
$$A = R \times K \times L \times S \times C \times P$$

* **A**: Perda calculada de solo.
* **R**: Fator hidrológico (Poder de erosão gerado por chuvas correntes na região).
* **K**: Fator pedológico (Como o solo atual suporta erosão?).
* **L e S**: Comprimento do terreno e inclinação (rampa contínua e graus topográficos).
* **C**: Presença da cultura na proteção (uso/manejo do leito e resíduos orgânicos).
* **P**: Manejos conservacionistas de defesa empregados (por exemplo, uso de linhas em nível natural contra as encostas, plantio direto, etc).
