# [ETAPA 1 DO PROJETO - Carregar a base Varejo.csv com pandas e mostrar: número de registros, colunas e tipos de dados.]
print("--- ETAPA 01 ---")
# 1.1 Importar biblioteca Pandas
import pandas as pd
import numpy as np

# 1.2 Carregar do dados da Base Varejo, e printar se estiver ok. 
df = pd.read_csv('Base Varejo.csv', sep=';')
print ("Dados lidos com sucesso")

# 1.3 Apresentando número de registros, colunas e tipos de dados
print("\n--- Registros, Colunas e Tipos de Dados ---")
print("\nTipos de Dados")
print(df.dtypes)

linhas, colunas = df.shape
print(f"\nNúmero de registros (linhas): {linhas}")
print(f"\nNúmero de colunas: {colunas}")

# 1.4 Visualização de 5 primeiras e 5 ultimas linhas
print("\n--- Visualizacao das 5 primeiras e 5 ultimas linhas ---")
print("\nPrimeiras 5 linhas da Base Varejo")
print(df.head(5))

print("\nUltimas 5 linhas da Base Varejo")
print(df.tail(5))
# logica: usando o head e tail para trazer primeiras e ultimas

# 1.5 Vizualizar 10 centrais 
print("\n--- Visualizacao das 10 linhas centrais ---")
meio_idx = len(df) // 2
df_centro = df.iloc[meio_idx - 5 : meio_idx + 5]
print(df_centro)
# logica: Pega o meio da tabela (total de linhas / 2) e filtra 5 linhas pra cima e 5 pra baixo pra ver o meio da base


# [ETAPA 2 DO PROJETO - Verificar e reportar ao menos dois problemas básicos: valores nulos por coluna, duplicatas e possíveis inconsistências (ex.: datas inválidas ou categorias vazias).]
print("\n--- ETAPA 02 ---")
# 2.1 - Verificação de nulos por coluna
print("\n--- Verificacao de nulos por coluna ---")
nulos = df.isnull().sum()
print(nulos[nulos > 0] 
      if nulos.sum() > 0 
      else "Sem valores nulos.")
# logica: Conta os nulos de cada coluna e mostra somente as que tem valores zerados/faltantes
# Resultado: 4 colunas com valores nulos (Unnamed: 10, Unnamed: 11, Unnamed: 12, Unnamed: 13), com todas as linhas nulas, necessário tratar.

# 2.2 - Verificação de Duplicidades
print("\n--- Verificacao de Duplicadas ---")
duplicadas = df.duplicated().sum()
print(f"Total de linhas duplicadas: {duplicadas}")
# logica: # Soma e mostra o total de linhas totalmente iguais da base
# Resultado: 96553 linhas duplicadas, necessário tratar.

# 2.3 - Verificação do tipo DATA
print("\n--- Verificacao de do tipo DATA ---")
if 'DATA' in df.columns:
    # Tenta converter para data sem alterar o dataframe original para testar validade
    datas_invalidas = pd.to_datetime(df['DATA'], errors='coerce').isnull().sum() - df['DATA'].isnull().sum()
    print(f"Total de registros com data, porém com formato inválido")
    print(f"Coluna 'DATA': {datas_invalidas} registro(s) com formato de data inválido.")
# logica: Testa a conversao para data em memoria para contar quantas datas estao em formato invalido sem alterar a base
# Resultado: 484735 registros com formato inválido na coluna DATA

# 2.4 - Verificar de quais categorias existem na base
print("\n--- Verificacao de quais categorias existentes ---")
if 'PR_CAT' in df.columns:
    print("Categorias encontradas na base:")
    print(df['PR_CAT'].unique())
# logica: Lista todas as categorias
# Resultado: verificado que existe uma categoria como "#N/D" que precisa ser tratada.

# 2.5 - Verificar campos 0(zero) nas colunas de int64 e float64 (numericos)
print("\n--- Verificacao de Campos com informacao 0(zero) ---")
colunas_numericas = df.select_dtypes(include=['int64', 'float64']).columns
for col in colunas_numericas:
    invalidos = (df[col] <= 0).sum()
    if invalidos > 0:
        print("Campos com valores negativos ou zerados:")
        print(f"Coluna '{col}': {invalidos} registro(s) com valor menor ou igual a zero.")
# logica: Percorre as colunas numericas para checar se existem valores zerados ou negativos
# Resultado: como a coluna CL_FHL, foi a unica que trouxe zerados, não tem problema, pois é a quantidade de filhos do cliente, sendo assim o 0 é sem filhos.

# 2.6 - Outliers na coluna DATA (valores fora do "padrao")
print("\n--- Verificacao de possiveis outliers(fora do padrao) na coluna data ---")
if 'DATA' in df.columns:
    # feito conversao para datatime, pra analisar os outliers
    datas_convertidas = pd.to_datetime(df['DATA'], errors='coerce')
    # Identificacao de data maior e menor
    data_minima = datas_convertidas.min()
    data_maxima = datas_convertidas.max()
    print(f"Data mais antiga encontrada: {data_minima.strftime('%d/%m/%Y') if pd.notnull(data_minima) else 'N/A'}")
    print(f"Data mais recente encontrada: {data_maxima.strftime('%d/%m/%Y') if pd.notnull(data_maxima) else 'N/A'}")
# logica: Converte a coluna DATA pra datetime temporariamente pra pegar a menor e a maior data e ver se tem datas fora do padrao
# Resultado: ao analisar as primeiras e ultimas 5 linhas, esta correto. Nada anormal


# [ETAPA 3 DO PROJETO - Fazer as três etapas de limpeza mínima necessária: remover ou imputar nulos (explique a escolha), eliminar duplicatas relevantes e ajustar tipos de dados (ex.: converter coluna DATA para datetime).]
print("\n--- ETAPA 03 ---")

# 3.1 Ajustar a coluna data, para formato datatime
print("\n--- Ajuste da coluna data para datatime ---")
if 'DATA' in df.columns:
    # 3.1.1 ver se ha nulos antes da conversao
    nulos_antes = df['DATA'].isnull().sum()
    # 3.1.2 conversao com errors='coerce' para substituir para NaT, caso haja nulos
    df['DATA'] = pd.to_datetime(df['DATA'], dayfirst=True, errors='coerce')
    # 3.1.3 quantos nulos apos conversao
    nulos_depois = df['DATA'].isnull().sum()
    # 3.1.4 quantidade de datas que eram invalidas e viraram NaT
    datas_invalidas = nulos_depois - nulos_antes
    if datas_invalidas > 0:
        print(f"{datas_invalidas} registro possuíam formato de data invalido e foram convertidos para NaT (nulo).")
    else:
        print("Coluna 'DATA' convertida com sucesso! Nenhuma data invalida foi encontrada.")
# logica: Converte a coluna DATA pra datetime pra ajustar o tipo de dado e depois um if/else com print, pra avisar quantas vieram nulo, ou se tudo ok


# 3.2 Remocao de espacos vazios em colunas de texto
print("\n--- Remocao de espacos vazios ---")
colunas_texto = df.select_dtypes(include=['str']).columns
for col in colunas_texto:
    df[col] = df[col].astype(str).str.strip()
print("Espaços removidos com sucesso!")
# logica: Passa por todas as colunas de texto e remove espaços ocultos que possam estar antes ou apos texto


# 3.3 Remocao de duplicatas
print("\n--- Remocao de duplicatas ---")
duplicadas_iniciais = df.duplicated().sum()
if duplicadas_iniciais > 0:
    df = df.drop_duplicates()
    print(f"{duplicadas_iniciais} linha(s) duplicada(s) exatamente igual(is) removida(s).")
else:
    print("Nenhuma linha duplicada encontrada na base.")
# logica: utilzei o drop_duplicates() para excluir as linhas iguais, usei a exclusao, pois nao ha nenhuma informacao no df que indique que sao 2 produtos ou algo assim 
#Exclusao feito pois se tratam de linhas exatamente iguais


# 3.4 Remocao das colunas unnamed (fantasmas)
print("\n--- Remocao de colunas fantasmas, identificadas anteriormente (unnamed) ---")
colunas_unnamed = [col for col in df.columns if 'Unnamed' in col]
if colunas_unnamed:
    df = df.drop(columns=colunas_unnamed)
    print(f"Colunas 'Unnamed' removidas com sucesso: {colunas_unnamed}")
else:
    print("Nenhuma coluna 'Unnamed' encontrada.")
# logica: remocao das colunas unnamed identificadas anteriormente, que foram criadas ao importar o csv pro vscode
# após remoção das colunas nulas, rodar novamente o verificar campos nulos

# 3.5 Verificacao de existe algum nulo ainda
print("\n--- Verificar se xiste algum nulo ainda ---")
nulos = df.isnull().sum()
print(nulos[nulos > 0] 
      if nulos.sum() > 0 
      else "Sem valores nulos.")
# logica: uma verificacao se existe algum nulo ainda
# não trouxe nenhum nulo.


# 3.6 Renomeando as colunas, para que fique de melhor entendimento.
print("\n--- Renomeando as colunas ---")
mapeamento_colunas = {
    'DATA': 'Data_Compra',
    'CO_ID': 'NF',
    'CL_ID': 'Nr_Cliente',
    'CL_GENERO': 'Sexo',
    'CL_EC': 'Estado_Civil',
    'CL_FHL': 'Qtd_Filhos',
    'CL_SEG': 'Segmento_Economico',
    'PR_ID': 'ID_Produto',
    'PR_CAT': 'Categoria_Produto',
    'PR_NOME': 'Nome_Produto'
}
# logica: Renomeação no DataFrame para melhor entendimento
df = df.rename(columns=mapeamento_colunas)

print("Colunas renomeadas com sucesso!")
print("\nNovos nomes das colunas:")
print(df.columns.tolist())

# 3.7 Renomeacoo das numeracao para a descricao do campo Estado_civil, de acordo com documento anexo a base.
print("\n--- Renomeando os numeros de Estado Civil para descrição ---")
mapa_estado_civil = {
    1: 'Casado(a) ou Uniao Estavel',
    2: 'Divorciado(a)',
    3: 'Separado(a)',
    4: 'Solteiro(a)',
    5: 'Viúvo(a)'}

if 'Estado_Civil' in df.columns:
    df['Estado_Civil'] = df['Estado_Civil'].map(mapa_estado_civil).fillna('Outros/Não Informado')
    print("Códigos de Estado Civil substituídos com sucesso!")
    print("\nDistribuição atualizada:")
    print(df['Estado_Civil'].value_counts())
# logica: renomeia os codigos de estado civil de acordo com a informacao que veio no doumento anexo a base

# 3.8 Ajustando o #N/D descoberto anteriormente
print("\n--- Ajuste dos campos com informacao #N/D ---")
padroes_erro = ['#N/D']
relatorio_erros = {}
for col in df.columns:
    qtd = df[col].astype(str).str.strip().isin(padroes_erro).sum()
    if qtd > 0:
        relatorio_erros[col] = qtd
print("Quantos foram encontrados por coluna")
if relatorio_erros:
    for col, qtd in relatorio_erros.items():
        percentual = (qtd / len(df)) * 100
        print(f"• Coluna '{col}': {qtd} registros ({percentual:.2f}%)")
else:
    print("Nenhum texto '#N/D' foi encontrado nas colunas.")

if 'Categoria_Produto' in df.columns:
    df['Categoria_Produto'] = (
        df['Categoria_Produto']
        .astype(str)
        .str.strip()
        .replace('#N/D', 'SEM DIFINICAO'))

if 'Nome_Produto' in df.columns:
    df['Nome_Produto'] = (
        df['Nome_Produto']
        .astype(str)
        .str.strip()
        .replace('#N/D', 'SEM DEFINICAO'))
# logica: Mapeia e conta em todas as colunas a presenca de textos com erro de carga identificada anteriormente ('#N/D') mostrando a quantidade e a porcentagem afetada.
# Em seguida, substitui esse texto por 'SEM DEFINICAO' nas colunas de categoria e nome do produto para padronizar os dados sem perder o registro.

# consulta nova de categorias
if 'Categoria_Produto' in df.columns:
    print("Categorias ajustadas:")
    print(df['Categoria_Produto'].unique())


# 3.9 rodando novamente o print, para verificar como ficou a apresentacao dos dados
print("\n--- Apresentacao dos dados atualizada ---")
print("\nPrimeiras 5 linhas da Base Varejo")
print(df.head(5))

print("\nUltimas 5 linhas da Base Varejo")
print(df.tail(5))


# [ETAPA 4 DO PROJETO - Gerar estatísticas descritivas básicas para coluna de número de filhos do cliente (média; mediana; desvio padrão; moda; máximo; mínimo; e contagem).]
print("\n--- ETAPA 04 ---")

# 4.1 Estatisticas da coluna "Qnt_Filhos"
print("\n--- Estatisticas de quantidades de filhos por cliente ---")
if 'Qtd_Filhos' in df.columns and 'Nr_Cliente' in df.columns:
    # Agrupando por cliente, e pagendo primeiro registro, pois mesmo que tenham mais NF, o cliente pode ser o mesmo
    df_clientes_unicos = df.groupby('Nr_Cliente')['Qtd_Filhos'].first().reset_index()
    # Calculo da moda
    moda_filhos = df_clientes_unicos['Qtd_Filhos'].mode()[0]
    # Demais metricas
    estatisticas_filhos = df_clientes_unicos['Qtd_Filhos'].agg(
        Contagem='count',
        Média='mean',
        Mediana='median',
        Desvio_Padrão='std',
        Mínimo='min',
        Máximo='max')
    estatisticas_filhos['Moda'] = moda_filhos
    print("\nResumo Estatistico de Filhos dos Clientes:")
    print(estatisticas_filhos.to_frame(name='Valor').round(2))
# logica: Isolamos os clientes unicos (pegando so o primeiro registro de cada um) pra nao distorcer a media com compras repetidas. Depois, calculamdo as principais metricas estatisticas (media, mediana, moda, desvio padrao, min e max) do numero de filhos por cliente.

# [ETAPA 5 DO PROJETO - Explorar padrões de agrupamento com pelo menos dois agrupamentos (por exemplo: gênero com mais vendas, compras), usando groupby() ou pivot_table().]
print("\n--- ETAPA 05 ---")

# 5.1 Total de vendas por sexo, usando a NF como base
col_nf = 'NF' if 'NF' in df.columns else 'NF'
print("\n--- Quantidade de NF emitida por Sexo, com percentual ---")
if 'Sexo' in df.columns and col_nf in df.columns:
    # Agrupa por sexo levando em consideracao a NF
    vendas_por_sexo = df.groupby('Sexo')[col_nf].nunique().reset_index()
    vendas_por_sexo.columns = ['Sexo', 'Qtd_Vendas_NF']
    # Percentual
    total_vendas = vendas_por_sexo['Qtd_Vendas_NF'].sum()
    vendas_por_sexo['Percentual (%)'] = ((vendas_por_sexo['Qtd_Vendas_NF'] / total_vendas) * 100).round(2)
    print(vendas_por_sexo.to_string(index=False))
else:
    print(f"Verifique se as colunas 'Sexo' e '{col_nf}' estão presentes no DataFrame.")
# logica: Agrupa os dados por sexo contando o numero unico de Notas Fiscais (NF) e calcula a porcentagem de vendas de cada grupo sobre o total.

# 5.2 identifica quantidade de produto em cada categoria, fazendo um percentual por categoria, como nao existe quantidade, vai contar 1 produto como quantidade 1
print("\n--- Ranking de categorias mais vendidas ---")
if 'Categoria_Produto' in df.columns:
    # 1. Agrupamento por categoria, considerando 1 cada registro, pois nao ha coluna quantidade
    cat_vendidas = (
        df.groupby('Categoria_Produto')
        .size()
        .reset_index(name='Total_Unidades_Vendidas')
        .sort_values(by='Total_Unidades_Vendidas', ascending=False))
    # 2. Percentual
    total_geral_itens = cat_vendidas['Total_Unidades_Vendidas'].sum()
    cat_vendidas['Percentual (%)'] = ((cat_vendidas['Total_Unidades_Vendidas'] / total_geral_itens) * 100).round(2)
    # 3. Formata exibicao
    cat_vendidas_print = cat_vendidas.copy()
    cat_vendidas_print['Total_Unidades_Vendidas'] = cat_vendidas_print['Total_Unidades_Vendidas'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
    print(cat_vendidas_print.to_string(index=False))
else:
    print("A coluna 'Categoria_Produto' não foi encontrada no DataFrame.")
# logica: Conta os itens vendidos por categoria, ordena do mais vendido pro menos vendido e calcula a porcentagem de participacao de cada uma no total

# 5.3 top 10 produtos mais vendidos
print("\n --- Top 10 produtos mais vendidos ---")
if 'Nome_Produto' in df.columns:
    # 1. Agrupa por Produto e conta o total de unidades vendidas, usando 1 produto = quantidade 1
    prod_vendidos = (
        df.groupby('Nome_Produto')
        .size()
        .reset_index(name='Total_Unidades_Vendidas')
        .sort_values(by='Total_Unidades_Vendidas', ascending=False))
    # 2.Percentual
    total_geral_itens = prod_vendidos['Total_Unidades_Vendidas'].sum()
    prod_vendidos['Percentual (%)'] = ((prod_vendidos['Total_Unidades_Vendidas'] / total_geral_itens) * 100).round(2)
    # 3. filtra 10 top
    top10_produtos = prod_vendidos.head(10).copy()
    top10_produtos['Total_Unidades_Vendidas'] = top10_produtos['Total_Unidades_Vendidas'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
    print(top10_produtos.to_string(index=False))
else:
    print("A coluna 'Nome_Produto' não foi encontrada no DataFrame.")
# logica: Conta a quantidade vendida de cada produto, pega os 10 primeiros do ranking e calcula a porcentagem que eles representam no total

# 5.4 verifica qual a quantidade de filhos, mas considerando o nr_cliente, para nao haver duplicidade
print("\n --- Filhos por cliente único ---")
if 'Nr_Cliente' in df.columns and 'Qtd_Filhos' in df.columns:
    df_clientes_unicos = df.drop_duplicates(subset=['Nr_Cliente']).copy()
    distrib_filhos = (
        df_clientes_unicos.groupby('Qtd_Filhos', dropna=False)
        .size()
        .reset_index(name='Total_Clientes')
        .sort_values(by='Qtd_Filhos')
    )
    total_clientes_unicos = len(df_clientes_unicos)
    distrib_filhos['Percentual (%)'] = ((distrib_filhos['Total_Clientes'] / total_clientes_unicos) * 100).round(2)
    distrib_print = distrib_filhos.copy()
    distrib_print['Total_Clientes'] = distrib_print['Total_Clientes'].apply(lambda x: f"{x:,.0f}".replace(',', '.'))
    
    print(f"Total de Clientes Únicos na Base: {total_clientes_unicos:,.0f}".replace(',', '.'))
    print("\n" + distrib_print.to_string(index=False))
else:
    print("Verifique se as colunas 'Nr_Cliente' e 'Qtd_Filhos' estão presentes no DataFrame.")
# logica: Remove clientes repetidos pra analisar a base de pessoas únicas e mostra a distribuição da quantidade de filhos por cliente com a porcentagem de cada grupo


print("=" * 60)
print("       DIAGNÓSTICO DE INTEGRIDADE DA BASE DE DADOS")
print("=" * 60)


# 1. Informações da Base CSV ajustadas
total_linhas, total_colunas = df.shape
print(f" Total de Registros (Linhas):  {total_linhas:,.0f}".replace(',', '.'))
print(f" Total de Atributos (Colunas): {total_colunas}")
print("-" * 60)

# 2. Resumo de Tipos de Dados
resumo_base = pd.DataFrame({
    'Tipo': df.dtypes,
    'Qtd_Preenchidos': df.count(),
    'Qtd_Nulos': df.isnull().sum(),
    '%_Nulos': ((df.isnull().sum() / total_linhas) * 100).round(2)
}).reset_index().rename(columns={'index': 'Coluna'})

print("\n--- DETALHAMENTO POR COLUNA ---")
print(resumo_base.to_string(index=False))

print("-" * 60)

# 3. Verificacao de Duplicatas Totais
linhas_duplicadas = df.duplicated().sum()
print(f" Linhas 100% duplicadas no DataFrame: {linhas_duplicadas}")

# Salva a base limpa usando ponto e vírgula e utf-8-sig para abrir correto no Excel
df.to_csv('base_varejo_limpa.csv', sep=';', index=False, encoding='utf-8-sig')
print("\n Base limpa exportada com sucesso para 'base_varejo_limpa.csv'!")
