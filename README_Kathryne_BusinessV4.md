

Este repositório contém o script em Python desenvolvido para a análise, tratamento, limpeza e exploração estatística de uma base de dados de vendas de varejo (`Base Varejo.csv`).

---

# Como Executar o Projeto

1. Certifique-se de ter o **Python 3** e as bibliotecas **pandas** e **numpy** instaladas no seu ambiente.
2. Mantenha o arquivo da base de dados (`Base Varejo.csv`) na mesma pasta do script.
3. Abra o projeto no **VS Code** ou na IDE de sua preferência.
4. No terminal, execute o comando:
   ```bash
   python Miniprojeto_Kathryne_BusinessV4.py

---

# Requisitos para rodar o código: 

- Python 3
- Biblioteca Pandas (tratamento e manipulação de dados) 
- Biblioteca NumPy (suporte a operações numéricas) 
- VS Code (software para desenvolvimento do código)

---

# Etapas do Projeto realizadas

O script foi organizado em 5 etapas principais:

1. Diagnóstico Inicial da Base
- Carregamento da base original com separador `;`.
- Verificação do número de linhas, colunas e tipos de dados (`dtypes`).
- Inspeção visual das primeiras, últimas e 10 linhas centrais do DataFrame.

2. Identificação de Problemas
- Mapeamento de colunas nulas ou fantasmas (`Unnamed`).
- Identificação de **96.553 linhas duplicadas**.
- Verificação da coluna Data com 484735 registros com formato inválido.
- Identificação de inconsistências nas colunas Categorias e Nome Produto com a presença do valor `#N/D`
- Verificação de valores 0(zero) em colunas numéricas. Sem resultado encontrado.
- Verificação de outliers na coluna data, a fim de identificar data fora do comum no DF.

3. Limpeza e Tratamento dos Dados
- Conversão da coluna `DATA` para o formato `datetime`.
- Remoção de espaços em branco antes/depois nos textos (`strip()`).
- Exclusão das linhas 100% duplicadas e remoção das colunas desnecessárias (`Unnamed`), optei por excluir pois não há nada que indique que foram 2 compras do mesmo produto.
- Remoção das colunas unnamed, pois foram criadas na importação do csv.
- Renomeação das colunas para nomes mais claros e intuitivos (ex: `DATA` -> `Data_Compra`, `CL_GENERO` -> `Sexo`).
- Mapeamento do código numérico de `Estado_Civil` para suas descrições reais (Solteiro, Casado, etc.), usando como base o documento que veio anexo a base pelo Kaggle.
- Tratamento dos registros com `#N/D`, substituindo-os por `SEM DEFINICAO`. Optei pela substituição da descrição, pois acredito ser algum produto sem cadastro ou algo no sentido.

4. Estatística Descritiva dos filhos dos clientes
- Análise da quantidade de filhos por cliente (isolando clientes únicos para evitar repetição de compras, fazendo com que as estatísticas sejam falhas).
- Cálculo de métricas: Média, Mediana, Moda, Desvio Padrão, Valor Mínimo e Valor Máximo.

5. Análise de Agrupamentos e Exportação
- Contagem do total de vendas (NFs únicas) por **Sexo**, optei por usar as NFs, pois se usasse cliente não seria por vendas e sim sexo dos clientes em si. Porém a contagem realizada foi Sexo/Venda.
- Ranking de **Categorias** mais compradas.
- **Top 10 Produtos mais vendidos** com percentual de participação.
- Distribuição de filhos por cliente único.

FINALIZAÇÃO DO PROJETO 
- Exportação da base limpa final para o arquivo `base_varejo_limpa.csv` (utilizando separador `;` e codificação `utf-8-sig` para compatibilidade com o Excel).

# Possiveis problemas na base

Ao analisar os dados e seguir com os tratamentos, identificado que:
- Seria ideal que houvesse colunas como quantidade, tirando a dúvida se as linhas exclusas de fato eram duplicidade, ou indicava a quantidade, ex: 2 linhas repetidas = 2 unidades do produto. 
- Ter um numero sequencial identificando o produto na venda, talvés seria outra opção pra sanar a dúvida da duplicidade.
- Ter os valores também seria uma opção para que pudesse ser feito uma analise em cima de valores de venda, e consumo por sexo ou ate mesmo consumo por categoria.

---

# **Conclusão**

A realização deste projeto demonstrou na prática a importância da etapa de limpeza de dados. Trabalhar com dados brutos sem tratamento pode levar a análises incorretas, por exemplo, contar compras repetidas como clientes diferentes ou ignorar linhas duplicadas alterando o volume real de vendas.

O uso da biblioteca **Pandas** facilitou a padronização dos tipos de dados, o tratamento de erros de carga como `#N/D` e a geração rápida de relatórios estatísticos. Como resultado, a base tratada está pronta para ser consumida de forma confiável por ferramentas de BI ou relatórios de gestão.