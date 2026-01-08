import React from 'react';

// Definindo os tipos das props
interface SidebarProps {
  setView: (view: 'chat' | 'dashboard') => void;
}

const Sidebar: React.FC<SidebarProps> = ({ setView }) => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">Positivo Chatbot</div>
      <ul className="sidebar-menu">
        <li onClick={() => setView('chat')}>New Chat</li>
        <li onClick={() => setView('dashboard')}>Dashboard</li>
      </ul>
    </div>
  );
};

export default Sidebar;