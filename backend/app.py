import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import sqlite3
import json
import pandas as pd
import plotly.express as px

# Carrega a chave de API do arquivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Chave de API do Google não encontrada no arquivo .env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-pro')
app = Flask(__name__)
CORS(app)

# Função para buscar todos os dados do banco de dados
def get_database_content():
    conn = sqlite3.connect('chamados.db')
    cursor = conn.cursor()
    
    # Retorna apenas um resumo dos dados para evitar excesso de tokens
    cursor.execute("SELECT COUNT(*) FROM chamados")
    total = cursor.fetchone()[0]

    cursor.execute("PRAGMA table_info(chamados)")
    columns = [col[1] for col in cursor.fetchall()]

    cursor.execute("SELECT * FROM chamados LIMIT 5")
    amostra = cursor.fetchall()

    conn.close()
    return {
        "total_chamados": total,
        "colunas": columns,
        "amostra": amostra
    }

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_prompt = data.get("prompt")
    
    if not user_prompt:
        return jsonify({"error": "Prompt não fornecido"}), 400

    try:
        # Obter apenas um resumo dos dados do banco de dados
        db_content = get_database_content()
        full_prompt = (
            "Você é um agente de análise de dados altamente qualificado. "
            "Nunca tente trazer todos os registros do banco de dados de uma só vez. "
            "Se precisar mostrar exemplos, use apenas os primeiros registros da amostra. "
            "Prefira sempre responder com estatísticas, agregados ou resumos. "
            "Se o usuário pedir todos os chamados, explique que o resultado foi limitado para melhor desempenho.\n\n"
            "Esquema do banco de dados:\n"
            f"Colunas: {db_content['colunas']}\n"
            f"Total de chamados: {db_content['total_chamados']}\n"
            f"Amostra dos primeiros chamados: {db_content['amostra']}\n\n"
            f"Pergunta do usuário: {user_prompt}"
        )

        response = model.generate_content(full_prompt)
        
        if response and response.text:
            return jsonify({"message": response.text})
        else:
            return jsonify({"error": "Resposta vazia da IA."}), 500

    except Exception as e:
        print(f"Erro detalhado: {e}")
        return jsonify({"error": "Ocorreu um erro interno. Verifique o log do servidor."}), 500


@app.route('/dashboard-analysis', methods=['GET'])
def dashboard_analysis():
    try:
        conn = sqlite3.connect('chamados.db')
        df = pd.read_sql_query("SELECT * FROM chamados", conn)
        conn.close()

        # Cria os cards de resumo
        total_chamados = len(df)
        chamados_abertos = len(df[df['status'] == 'Em Andamento'])
        analistas_unicos = df['analista'].nunique()

        # Prepara a lista de gráficos para retorno
        graphs = []
        
        # Distribuição de Chamados por Status (Colunas)
        status_counts = df['status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Quantidade']
        fig_status = px.bar(status_counts, x='Status', y='Quantidade', title='Distribuição de Chamados por Status')
        graphs.append({"title": "Distribuição de Chamados por Status", "data": json.loads(fig_status.to_json())['data']})

        # Chamados por Canal de Abertura (Colunas)
        canal_counts = df['tipo_abertura'].value_counts().reset_index()
        canal_counts.columns = ['Canal', 'Quantidade']
        fig_canal = px.bar(canal_counts, x='Canal', y='Quantidade', title='Chamados por Canal de Abertura')
        graphs.append({"title": "Chamados por Canal de Abertura", "data": json.loads(fig_canal.to_json())['data']})
        
        # Distribuição de Chamados por Tipo (Colunas)
        tipo_counts = df['tipo_chamado'].value_counts().reset_index()
        tipo_counts.columns = ['Tipo', 'Quantidade']
        fig_tipo = px.bar(tipo_counts, x='Tipo', y='Quantidade', title='Distribuição de Chamados por Tipo')
        graphs.append({"title": "Distribuição de Chamados por Tipo", "data": json.loads(fig_tipo.to_json())['data']})

        # Distribuição de Chamados por Prioridade (Pizza)
        prioridade_counts = df['prioridade'].value_counts().reset_index()
        prioridade_counts.columns = ['Prioridade', 'Quantidade']
        fig_prioridade = px.pie(prioridade_counts, values='Quantidade', names='Prioridade', title='Distribuição de Chamados por Prioridade')
        graphs.append({"title": "Distribuição de Chamados por Prioridade", "data": json.loads(fig_prioridade.to_json())['data']})

        # Top 5 Analistas (Colunas)
        analista_counts = df['analista'].value_counts().nlargest(5).reset_index()
        analista_counts.columns = ['Analista', 'Quantidade']
        fig_analista = px.bar(analista_counts, x='Analista', y='Quantidade', title='Top 5 Analistas com Mais Chamados Atribuídos')
        graphs.append({"title": "Top 5 Analistas com Mais Chamados Atribuídos", "data": json.loads(fig_analista.to_json())['data']})

        # Top 5 Categorias (Colunas)
        categoria_counts = df['categoria'].value_counts().nlargest(5).reset_index()
        categoria_counts.columns = ['Categoria', 'Quantidade']
        fig_categoria = px.bar(categoria_counts, x='Categoria', y='Quantidade', title='Top 5 Categorias de Chamados')
        graphs.append({"title": "Top 5 Categorias de Chamados", "data": json.loads(fig_categoria.to_json())['data']})

        # Retorna todos os dados para o front-end
        return jsonify({
            "cards": [
                {"title": "Total de Chamados", "value": total_chamados},
                {"title": "Chamados em Andamento", "value": chamados_abertos},
                {"title": "Analistas Únicos", "value": analistas_unicos}
            ],
            "graphs": graphs
        })

    except Exception as e:
        print(f"Erro ao gerar a análise: {e}")
        return jsonify({"error": "Ocorreu um erro interno ao processar a análise."}), 500

if __name__ == '__main__':
    app.run(debug=True)