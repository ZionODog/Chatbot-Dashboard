import React, { useState, KeyboardEvent } from 'react';
import { FaPaperPlane } from 'react-icons/fa';
import '../App.css';

// Interface para definir o tipo de cada mensagem
interface Message {
  text: string;
  sender: 'user' | 'bot';
}

interface ChatPageProps {
  onSendMessage: (text: string) => void;
  loading: boolean;
  messages: Message[];
}

const ChatPage: React.FC<ChatPageProps> = ({ onSendMessage, loading, messages }) => {
  const [input, setInput] = useState('');

  const handleSubmit = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="main-content">
      {messages.length === 0 ? (
        // Estado inicial, centralizado
        <div className="chat-initial-state">
          <h1 className="welcome-message">Como eu posso ajudar?</h1>
          <div className="message-input-wrapper">
            <textarea
              className="message-input"
              placeholder="Envie uma mensagem..."
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
            />
            <div className="input-actions">
              <button onClick={handleSubmit} disabled={loading}>
                {loading ? '...' : <FaPaperPlane />}
              </button>
            </div>
          </div>
        </div>
      ) : (
        // Estado de conversa, mensagens no topo e input embaixo
        <>
          <div className="chat-window">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
          </div>
          <div className="message-input-wrapper">
            <textarea
              className="message-input"
              placeholder="Envie uma mensagem..."
              rows={1}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
            />
            <div className="input-actions">
              <button onClick={handleSubmit} disabled={loading}>
                {loading ? '...' : <FaPaperPlane />}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatPage;