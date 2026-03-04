# Guia Descomplicado: Como Usar as APIs Agrícolas 🌾💻

Este guia foi feito para você que não é programador, mas precisa entender como os dados chegam no nosso sistema `AJUDAGRO` através do arquivo `integracao_apis.py`.

As APIs são como **"garçons"**: o nosso sistema (cliente) faz um pedido (pergunta algo), a API vai até a cozinha (servidor do governo/meteorologia), pega a informação e entrega de volta pra gente em formato de texto.

---

## 1. Previsão do Tempo (Open-Meteo) 🌤️
**O que ela faz:** Traz a previsão do clima para os próximos dias (temperatura, chuvas e evapotranspiração).
- **É gratuita?** Sim, totalmente!
- **Precisa de senha/cadastro?** Não.
- **Como usamos:** Basta dizermos para qual Latitude e Longitude (ex: `-17.79, -50.92`) queremos a previsão e para quantos dias.
- **No código:** Chamada através do `PrevisaoTempo.obter_previsao_open_meteo(...)`.

---

## 2. Dados do Governo (INMET e ANA) 🌧️
**O que elas fazem:** Trazem o **histórico** do que já aconteceu (chuvas passadas, temperaturas do ano passado, nível dos rios). Ideal para calcular qual o padrão de clima de uma fazenda ao longo de 10 a 30 anos.
- **É gratuita?** Sim, são redes públicas do governo.
- **Precisa de senha/cadastro?** Não.
- **Como usamos (INMET):** Precisamos saber o "Código da Estação" Meteorológica mais próxima da fazenda (ex: `A001` de Brasília) e passar as datas (ex: *quero dados de Jan/2023 a Dez/2023*). 
- **⚠️ Atenção:** Às vezes o site do governo cai ou fica lento, o que é normal. Se isso acontecer, o sistema avisa que deu erro.
- **No código:** `RedesPublicas.obter_dados_inmet(...)` e `obter_dados_ana(...)`.

---

## 3. Risco Climático (ZARC - MAPA) 📊
**O que é:** O **Z**oneamento **A**grícola de **R**isco **C**limático é um tabelão do governo que diz: *"Se plantar soja nesta cidade hoje, a chance de dar ruim por falta de chuva é de 20%, 30% ou 40%?"*.
- **É gratuita?** Sim.
- **Como usamos:** Lemos essas tabelas que o Ministério da Agricultura disponibiliza em portais de "Dados Abertos" e cruzamos com a cidade do produtor.
- **No código:** `RedesPublicas.obter_tabela_risco_zarc_mapa(...)`.

---

## 4. O Coração de Ouro: Embrapa (AgroAPI) 🌱💎
**O que ela faz:** É a fonte de dados mais inteligente. Onde o sistema pergunta coisas como *"Qual a melhor janela de plantio para essa cidade?"* ou *"Me recomende sementes de soja para cá"*.
- **É gratuita?** Sim, porém...
- **Precisa de senha/cadastro?** **SIM.** Esta é a única que não funciona sem a gente criar um cadastro oficial no site deles.
- **Como usar (Passo a Passo Burocrático):**
  1. Temos que entrar no site `api.cnptia.embrapa.br` e nos cadastrar (criar uma "Alinea/App" lá dentro).
  2. Eles vão nos dar um **Token** (que é basicamente uma senha gigante e secreta).
  3. Com essa senha, ativamos essa parte no sistema AJUDAGRO.
- **No código:** Sem esse *Token*, as chamadas `Embrapa.obter_janela_plantio(...)` ou `obter_zoneamento_agricola(...)` não vão buscar os dados reais de jeito nenhum, elas apenas dão *"Acesso Negado"*.

---

### Resumo prático para não ter dor de cabeça:
Tudo que for **Clima Futuro (Open-Meteo)** e **Médias Antigas (Governo)** vai funcionar sozinho a partir de agora! 

Para destravar os dados chiques da **Embrapa**, a única pendência é criar a conta na AgroAPI deles e jogar a chave dentro do sistema posteriormente.
