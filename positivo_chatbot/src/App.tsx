import React, { useState } from 'react';
import Sidebar from './components/Sidebar.tsx';
import ChatPage from './components/ChatPage.tsx';
import Dashboard from './components/Dashboard.tsx';
import './App.css';

// Interface para definir o tipo de cada mensagem
interface Message {
  text: string;
  sender: 'user' | 'bot';
}

function App() {
  const [view, setView] = useState<'chat' | 'dashboard'>('chat');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  // Função para lidar com o envio de mensagens para a IA
  const handleSendMessage = async (text: string) => {
    if (!text.trim()) return;

    const userMessage: Message = { text, sender: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: text }),
      });

      const data = await response.json();
      const botMessage: Message = { text: data.message, sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, botMessage]);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
      const errorMessage: Message = { text: "Ocorreu um erro. Tente novamente.", sender: 'bot' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <Sidebar setView={setView} />
      {view === 'chat' ? (
        <ChatPage
          onSendMessage={handleSendMessage}
          loading={loading}
          messages={messages}
        />
      ) : (
        <Dashboard />
      )}
    </div>
  );
}

export default App;