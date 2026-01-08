// src/components/MessageInput.tsx
import React, { useState, KeyboardEvent } from 'react';
import { FaPaperPlane } from 'react-icons/fa';

// Definindo os tipos das props
interface MessageInputProps {
  onSendMessage: (text: string) => void;
  loading: boolean;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSendMessage, loading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput(''); // Limpa o input
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
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
  );
};

export default MessageInput;