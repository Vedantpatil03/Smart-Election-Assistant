import React, { useState, useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import LoadingIndicator from './LoadingIndicator';
import { electionAPI } from '../services/api';
import './ChatWindow.css';

const ChatWindow = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'नमस्ते! Hello! I am your Election Assistant. I can help you understand voting steps, timelines, FAQs, and more. What would you like to know about elections?',
      isUser: false,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [language, setLanguage] = useState('en');
  const [isFirstTimeVoter, setIsFirstTimeVoter] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (userInput) => {
    if (!userInput.trim()) return;

    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: userInput,
      isUser: true,
    };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await electionAPI.sendMessage(
        userInput,
        language,
        isFirstTimeVoter
      );

      const botResponse = response.data.data.response;
      const botMessage = {
        id: messages.length + 2,
        text: botResponse,
        isUser: false,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        id: messages.length + 2,
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
  };

  const toggleFirstTimeVoter = () => {
    setIsFirstTimeVoter(!isFirstTimeVoter);
  };

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h1>Smart Election Assistant</h1>
        <div className="chat-controls">
          <label>
            Language:
            <select value={language} onChange={handleLanguageChange}>
              <option value="en">English</option>
              <option value="hi">हिंदी (Hindi)</option>
              <option value="mr">मराठी (Marathi)</option>
            </select>
          </label>
          <label>
            <input
              type="checkbox"
              checked={isFirstTimeVoter}
              onChange={toggleFirstTimeVoter}
              aria-label="First-time voter mode"
            />
            First-time Voter Mode
          </label>
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <MessageBubble
            key={message.id}
            message={message.text}
            isUser={message.isUser}
          />
        ))}
        {isLoading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <InputBox onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatWindow;
