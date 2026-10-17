# Automação de testes: interface, API e carga

[![Testes automatizados](https://github.com/GabrielMonteiroCosta/qa-automacao-python/actions/workflows/testes.yml/badge.svg)](https://github.com/GabrielMonteiroCosta/qa-automacao-python/actions/workflows/testes.yml)

Projeto de portfólio com testes automatizados em Python, rodando a cada alteração no GitHub Actions.
São 32 testes de interface e de API e um teste de carga com critérios de aceite.

## O que é testado

| Tipo | Sistema testado | Ferramentas | Testes |
| --- | --- | --- | --- |
| Interface (ponta a ponta) | [Sauce Demo](https://www.saucedemo.com), loja de demonstração | Playwright, pytest | 14 |
| API REST | [ServeRest](https://serverest.dev), API pública para estudo de testes | requests, pytest, JSON Schema | 18 |
| Carga | ServeRest | JMeter | 1 cenário |

**Interface**
- Login: acesso com sucesso, campos obrigatórios, senha errada, usuário bloqueado e logout.
- Produtos: adicionar e remover do carrinho, ordenar por menor e maior preço.
- Checkout: compra completa, conferindo as regras do resumo (subtotal = soma dos itens, total = subtotal + imposto), e validação dos dados do comprador.

**API**
- Usuários: cadastro, e-mail repetido, campos obrigatórios, e-mail inválido, busca por id com validação de contrato, id inexistente, filtro por e-mail, atualização e exclusão.
- Login: token gerado com sucesso e recusa de credenciais erradas.
- Produtos: cadastro por administrador, validação de contrato, acesso sem token (401), usuário sem permissão (403), nome repetido e exclusão.

**Carga**
- 5 usuários virtuais, 10 repetições cada, consultando `GET /produtos` e `GET /usuarios`.
- Critérios de aceite: no máximo 1% de erros e percentil 95 de até 2 segundos.

## Estrutura

```
├── pages/                  # Page Objects das telas do Sauce Demo
├── api/                    # Cliente da API ServeRest e contratos (JSON Schema)
├── tests/
│   ├── ui/                 # Testes de interface
│   └── api/                # Testes de API
├── jmeter/                 # Plano do teste de carga
├── scripts/                # Conferência dos critérios de aceite da carga
├── .github/workflows/      # Pipelines do GitHub Actions
├── rodar_testes.bat        # Windows: prepara o ambiente e roda os testes com dois cliques
├── pytest.ini              # Configuração do pytest e do Playwright
└── requirements.txt        # Dependências com versões fixas
```

## Como rodar

Pré-requisito: Python 3.12 ou mais novo.

No Windows, o jeito mais fácil é dar dois cliques em `rodar_testes.bat`. Na primeira vez, ele prepara o ambiente. Depois, roda os testes com o Chrome visível e abre o relatório.

Em qualquer sistema, pelo terminal:

```bash
python -m venv .venv
.venv\Scripts\activate          # no Linux/Mac: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
pytest
```

Outras formas úteis:

| Comando | O que faz |
| --- | --- |
| `pytest -m ui` | Só os testes de interface |
| `pytest -m api` | Só os testes de API |
| `pytest -m ui --headed --slowmo 500` | Mostra o navegador executando os passos |
| `pytest -m ui --headed --slowmo 500 --browser-channel chrome` | O mesmo, usando o Google Chrome instalado (útil se o Chromium do Playwright não abrir no Windows) |
| `playwright show-trace test-results/<pasta-do-teste>/trace.zip` | Abre o passo a passo de um teste que falhou |

O relatório fica em `reports/relatorio.html`. Quando um teste de interface falha, o print da tela e o trace ficam em `test-results/`.

### Teste de carga

Pelo GitHub: aba **Actions** > **Teste de carga (JMeter)** > **Run workflow**. Dá para escolher a quantidade de usuários e de repetições.

Na máquina (precisa de Java 8 ou mais novo e do [JMeter](https://jmeter.apache.org/download_jmeter.cgi), arquivo `apache-jmeter-5.6.3.zip`). No Windows, troque `jmeter` pelo caminho do `bin\jmeter.bat` da pasta onde o JMeter foi extraído:

```bash
jmeter -n -t jmeter/carga-serverest.jmx -l reports/jmeter/resultados.jtl -e -o reports/jmeter/html
python scripts/verificar_carga.py reports/jmeter/resultados.jtl --max-erros 1 --p95 2000
```

## Integração contínua

- **testes.yml**: a cada push na `main` e em todo pull request, instala tudo, roda os 32 testes e publica o relatório como artefato.
- **carga-jmeter.yml**: disparo manual. Roda o JMeter, confere os critérios de aceite e publica o relatório HTML do JMeter.

## Decisões do projeto

- **Page Objects**: os testes usam ações com nome de negócio (`entrar`, `adicionar_ao_carrinho`). Se a tela mudar, só a classe da página muda.
- **Seletores `data-test`**: não quebram quando o layout ou o texto da tela muda.
- **Espera automática**: as verificações com `expect` do Playwright esperam o elemento ficar pronto. Não há `sleep`, o que evita testes instáveis.
- **Dados de teste**: Faker em português e e-mails únicos. Como a API é pública e compartilhada, as fixtures apagam tudo o que o teste criou, mesmo quando ele falha.
- **Contrato**: as respostas da API são validadas com JSON Schema, que acusa campo faltando, tipo errado ou campo novo.
- **Evidências só na falha**: print e trace são guardados apenas quando um teste falha.
- **Carga com critério objetivo**: o script `verificar_carga.py` reprova a execução se os limites forem ultrapassados, e o pipeline fica vermelho.

## Próximos passos

- Rodar os testes de interface também no Firefox e no WebKit.
- Versão dos testes de interface em Robot Framework.
- Relatório com Allure e histórico de execuções.

---

Feito por Gabriel Costa · [LinkedIn](https://www.linkedin.com/in/gabriel-monteiro-da-costa-69775a28a)
