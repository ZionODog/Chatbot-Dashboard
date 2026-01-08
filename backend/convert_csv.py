import sqlite3
import csv

# Conexão com o banco de dados
conn = sqlite3.connect('chamados.db')
cursor = conn.cursor()

# Criação da tabela com as colunas do CSV
cursor.execute('''
CREATE TABLE IF NOT EXISTS chamados (
    chamado TEXT,
    tipo_abertura TEXT,
    data_abertura TEXT,
    nome TEXT,
    analista TEXT,
    tempo_resolucao TEXT,
    data_fechamento TEXT,
    analista_original TEXT,
    tipo_chamado TEXT,
    status TEXT,
    prioridade TEXT,
    agrupamento TEXT,
    categoria TEXT,
    produto TEXT,
    processo TEXT,
    problema TEXT,
    data_atualizacao TEXT,
    grupo_original TEXT,
    data_resolucao TEXT,
    grupo_atual TEXT,
    formulario TEXT
)
''')

# Importação dos dados do CSV
with open(r'E:\VSCode\Projetos\JavaScript_Projetos\Positivo_Chatbot\Chamados.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    print(reader.fieldnames)
    for row in reader:
        print(row)
        
        cursor.execute('''
            INSERT INTO chamados VALUES (
                :Chamado, :Tipo_abertura, :Data_Abertura, :Nome, :Analista, :Tempo_de_Resolução, :Data_Fechamento,
                :Analista_original, :Tipo_chamado, :Status, :Prioridade, :Agrupamento, :Categoria, :Produto,
                :Processo, :Problema, :Data_Atualização, :Grupo_Original, :Data_de_Resolução, :Grupo_atual, :Formulário
            )
        ''', {
            'Chamado': row['\ufeffChamado'],
            'Tipo_abertura': row['Tipo abertura'],
            'Data_Abertura': row['Data Abertura'],
            'Nome': row['Nome'],
            'Analista': row['Analista'],
            'Tempo_de_Resolução': row['Tempo de Resolução'],
            'Data_Fechamento': row['Data Fechamento'],
            'Analista_original': row['Analista original'],
            'Tipo_chamado': row['Tipo chamado'],
            'Status': row['Status'],
            'Prioridade': row['Prioridade'],
            'Agrupamento': row['Agrupamento'],
            'Categoria': row['Categoria'],
            'Produto': row['Produto'],
            'Processo': row['Processo'],
            'Problema': row['Problema'],
            'Data_Atualização': row['Data Atualização'],
            'Grupo_Original': row['Grupo Original'],
            'Data_de_Resolução': row['Data de Resolução'],
            'Grupo_atual': row['Grupo atual'],
            'Formulário': row['Formulário']
        })

conn.commit()
conn.close()