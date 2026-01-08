import { useState, useEffect } from 'react';
import Plotly from 'react-plotly.js';
import './Dashboard.css';

// Interface para os dados de análise que a IA vai retornar
interface AnalysisData {
  cards: { title: string; value: string | number }[];
  graphs: { title: string; data: any[] }[];
}

const Dashboard = () => {
  const [analysis, setAnalysis] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/dashboard-analysis');
        if (!response.ok) {
          throw new Error('Falha ao buscar os dados da análise.');
        }
        const data: AnalysisData = await response.json();
        setAnalysis(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, []);

  if (loading) {
    return (
      <div className="dashboard-container">
        <h2>Dashboard de Análise</h2>
        <p>O Gemini está preparando as análises...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <h2 className="error-message">Erro ao carregar o dashboard:</h2>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">Dashboard de Análise de Chamados</h1>
      <p className="dashboard-summary">
        Aqui está uma análise completa dos seus dados.
      </p>
      
      {/* Seção de Cards */}
      <div className="cards-grid">
        {analysis?.cards.map((card, index) => (
          <div key={index} className="card">
            <h3>{card.title}</h3>
            <p>{card.value}</p>
          </div>
        ))}
      </div>

      {/* Seção de Gráficos */}
      <div className="charts-grid">
        {analysis?.graphs.map((graph, index) => (
          <div key={index} className="chart-wrapper">
            <h3>{graph.title}</h3>
            <Plotly
              data={graph.data}
              layout={{ 
                title: {
                  text: graph.title, // Mude o title para um objeto
                  font: { color: 'white' }
                },
                paper_bgcolor: 'rgba(0,0,0,0)', 
                plot_bgcolor: 'rgba(0,0,0,0)', 
                font: { color: 'white' }
              }}
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;