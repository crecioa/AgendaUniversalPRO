# Agenda Universal PRO

**Versão:** 1.0.0  
**Plataforma de uso documentada:** Windows, PowerShell e Python 3  
**Interface:** menu interativo no terminal

## Objetivo

O Agenda Universal PRO atualiza agendas em formato Word (`.docx`) de um ano de origem para um ano de destino. O usuário seleciona o documento de entrada, informa o nome do documento de saída e confirma a operação antes de iniciar o processamento.

> **Importante:** confira as datas, os dias da semana, os feriados e a apresentação visual do Word gerado antes de utilizá-lo. A atualização automática não substitui a revisão de um calendário jurídico nem a consulta às regras de expediente e prazos dos tribunais.

## Requisitos e instalação

É necessário ter Python 3 e as dependências indicadas em `requirements.txt`.

No PowerShell, na pasta raiz do projeto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
```

Se o ambiente virtual já existir, basta ativá-lo. Caso o PowerShell bloqueie a ativação, verifique a política de execução aplicável ao seu computador antes de alterá-la.

## Como executar

Com o ambiente ativado, na raiz do projeto:

```powershell
py app.py
```

O programa apresenta:

```text
MENU PRINCIPAL

1 - Atualizar agenda para um novo ano
2 - Configurações
0 - Sair
```

A aplicação não possui uma opção `--help` implementada; `py app.py --help` também inicia o menu interativo.

## Atualizar uma agenda

1. No menu principal, escolha **1 — Atualizar agenda para um novo ano**.
2. Selecione um documento `.docx` listado na pasta de origem. Use **M** para informar manualmente o caminho completo de outro arquivo `.docx`, ou **0** para cancelar.
3. Informe **apenas o nome** do arquivo de destino, incluindo a extensão `.docx`, por exemplo `agenda_2027.docx`. O arquivo será direcionado à pasta de destino configurada. Digite **0** para voltar.
4. Informe o **ano atual da agenda** (ano de origem) e o **novo ano da agenda** (ano de destino). Os anos devem ser diferentes.
5. Confira o resumo exibido e digite **S** para iniciar a atualização. Qualquer outra resposta cancela a operação.
6. Ao concluir, o programa informa a quantidade de substituições realizadas e o caminho do arquivo gerado. Se ocorrer um erro, uma mensagem será exibida.

**Exemplo de uso:** selecione uma agenda de 2026, informe `agenda_2027.docx` como destino, escolha 2026 como ano de origem e 2027 como ano de destino.

**Atenção:** escolha um nome de saída novo; não dependa da substituição de um arquivo existente. Guarde uma cópia do documento de origem.

## Configurações

No menu principal, escolha **2 — Configurações**. O aplicativo exibe as pastas atuais e permite:

- **1 — Alterar diretório de origem:** informe uma pasta existente.
- **2 — Alterar diretório de destino:** informe uma pasta existente ou autorize a criação de uma nova.
- **0 — Voltar:** retorna ao menu principal.

As alterações são salvas pelo serviço de configurações do aplicativo. A localização exata do arquivo de configuração depende da configuração do projeto.

## Arquivos e diretórios

- `app.py`: ponto de entrada do aplicativo.
- `modelos/`: pasta de modelos utilizada no projeto; a origem efetiva pode ser alterada no menu de configurações.
- `output/`: pasta de documentos gerados utilizada no projeto; o destino efetivo pode ser alterado no menu de configurações.
- `config/`: módulos de configuração.
- `core/`: lógica central de atualização.
- `services/`: serviços de processamento, configuração e registros.
- `tests/`: testes automatizados.
- `logs/`: arquivos de registro, conforme a configuração da aplicação.
- `backup/`: cópias de segurança existentes no projeto; não confundir com o arquivo final de saída.

## Testes e verificação

Na raiz do projeto, com o ambiente virtual ativado:

```powershell
py -m pip check
py -m pytest -q
py -m mypy .
```

Na auditoria de 21/10/2026, foram informados **259 testes aprovados**, `pip check` sem conflitos e `mypy` sem erros em **58 arquivos-fonte**. Esses resultados se referem à versão auditada e devem ser repetidos após alterações.

## Cuidados com calendários jurídicos

- Verifique a correspondência entre datas e dias da semana.
- Diferencie feriados nacionais de pontos facultativos, datas religiosas e feriados locais.
- Confirme os calendários de funcionamento dos tribunais e eventuais suspensões de prazos nas fontes oficiais competentes.
- Revise a paginação, as tabelas e os campos de audiências e acordos no Microsoft Word antes da distribuição ou impressão.

## Versionamento e entrega

A versão indicada na interface é **1.0.0**. A criação da tag Git `v1.0.0` deve ocorrer somente após a conferência final dos arquivos, dos testes e do estado do repositório.
