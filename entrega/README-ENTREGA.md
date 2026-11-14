# Relatório de Entrega — Desafio Onfly

## 1. Defeitos corrigidos

### 1.1. Leitura incompleta dos dados

**Causa raiz:** Existia uma limitação de 200 linhas no arquivo `csv_reservation_repository.py`, impedindo a leitura de todas as reservas disponíveis no CSV.

**Investigação e solução:** Ao exibir os dados extraídos no terminal, identifiquei que apenas 200 das 300 reservas existentes estavam sendo processadas. Como não havia nenhuma limitação semelhante no `report_builder.py`, investiguei a origem da leitura dos dados e encontrei uma instrução `break` que interrompia o processamento ao atingir 200 linhas. Removi essa limitação para permitir a leitura de todas as reservas.

**Como validar:** Executar o CLI utilizando o arquivo principal de reservas e verificar se o relatório apresenta as 300 reservas em `total_reservations`.

### 1.2. Conversão incorreta dos valores das reservas

**Causa raiz:** Os valores monetários estavam sendo convertidos para `float` desnecessariamente, além de a operação de conversão cambial estar utilizando divisão em vez de multiplicação.

**Investigação e solução:** Analisei a função `convert_to_brl`, localizada no arquivo `currency_converter.py`, e identifiquei os problemas na operação de conversão. Removi a utilização de `float` e ajustei o cálculo para seguir a regra especificada:

`amount * rate_to_brl`

Dessa forma, os cálculos monetários passaram a utilizar `Decimal`, preservando a precisão dos valores.

**Como validar:** Executar os testes automatizados, especialmente `test_currency.py`, e utilizar o arquivo `data/exemplo-validacao.csv` para comparar os valores calculados com os resultados esperados na documentação.

### 1.3. Cálculo incorreto da quantidade de noites

**Causa raiz:** O cálculo utilizado para determinar a quantidade de noites não considerava corretamente a diferença entre as datas completas de check-in e check-out.

**Investigação e solução:** Analisei a função `calculate_room_nights`, localizada no arquivo `stay_calculator.py`, e identifiquei que o cálculo não seguia corretamente a regra de negócio especificada. Ajustei a implementação para subtrair a data de check-in da data de check-out, obtendo a diferença em dias e multiplicando o resultado pela quantidade de quartos.

A fórmula utilizada passou a seguir a especificação:

`(checkout_date - checkin_date).days * rooms`

**Como validar:** Executar o teste `test_nights.py`, que verifica o cálculo das noites na virada de mês, e comparar os resultados da amostra de validação com os valores esperados.

### 1.4. Verificação incorreta dos status das reservas

**Causa raiz:** A função `is_billable` estava considerando como faturáveis todos os status diferentes de `CANCELLED`, incluindo incorretamente as reservas `NO_SHOW`.

**Investigação e solução:** Analisei a função `is_billable`, localizada no arquivo `status_policy.py`, e identifiquei que a condição utilizada não correspondia à regra de negócio. Altereia verificação para considerar faturáveis exclusivamente as reservas com status `CONFIRMED`.

Dessa forma, reservas `CANCELLED` e `NO_SHOW` continuam sendo contabilizadas no total de reservas e nas respectivas contagens por status, mas não participam dos cálculos financeiros e das agregações.

**Como validar:** Executar o teste `test_status_rules.py`, que verifica a contabilização dos status e a exclusão de reservas canceladas e não comparecidas dos cálculos faturáveis.

### 1.5. Ordenação incorreta dos hotéis

**Causa raiz:** A ordenação dos hotéis estava sendo realizada em ordem crescente, contrariando a especificação, que exige ordem decrescente pelo valor total em reais.

**Investigação e solução:** Analisei o método `sorted`, responsável pela ordenação dos hotéis no relatório. Identifiquei que o parâmetro utilizado não configurava a ordenação decrescente. Ajustei a implementação para priorizar os hotéis com maior valor total em reais.

**Como validar:** Executar os testes `test_top_hotels.py` e `test_top_hotels_by_yallison.py`, verificando se os hotéis são apresentados em ordem decrescente de `total_brl`.

---

## 2. Validação do projeto

A validação foi realizada por meio da execução dos testes automatizados disponibilizados no projeto, utilizando o comando:

```bash
pytest -q
```

### Resultado dos testes

**Ambiente utilizado:**
- Sistema operacional: Windows
- Python: 3.12.10
- Pytest: 8.3.4

**Resultado:**

```text
platform win32 -- Python 3.12.10, pytest-8.3.4, pluggy-1.7.0 -- C:info-pessoal
cachedir: .pytest_cache
rootdir: C:info-pessoal
configfile: pyproject.toml
testpaths: tests
collected 6 items

tests/test_currency.py::test_currency_conversion_to_brl PASSED
tests/test_nights.py::test_nights_across_month_boundary PASSED
tests/test_regression_report.py::test_regression_report_on_sample PASSED
tests/test_status_rules.py::test_status_rules_exclude_cancelled_and_no_show PASSED
tests/test_top_hotels.py::test_top_hotels_are_ranked_descending PASSED
tests/test_top_hotels_by_yallison.py::test_top_hotels_are_ranked_descending PASSED

======================== 6 passed in 1.32s ========================
```

**Conclusão:** Todos os seis testes automatizados foram executados com sucesso, sem falhas.