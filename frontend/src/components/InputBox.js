import React, { useState } from 'react';
import { FiSend } from 'react-icons/fi';
import './InputBox.css';

const InputBox = ({ onSendMessage, isLoading }) => {
  const [input, setInput] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form className="input-box" onSubmit={handleSubmit}>
      <textarea
        className="input-field"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Ask your question about elections..."
        disabled={isLoading}
        rows="2"
        aria-label="Message input"
      />
      <button
        type="submit"
        className="send-button"
        disabled={isLoading || !input.trim()}
        aria-label="Send message"
      >
        <FiSend />
      </button>
    </form>
  );
};

export default InputBox;
