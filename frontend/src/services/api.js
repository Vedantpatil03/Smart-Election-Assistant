import axios from 'axios';

// API base URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://smart-election-assistantt.onrender.com/api/steps';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API endpoints
export const electionAPI = {
  // Data endpoints
  getSteps: () => api.get('/steps'),
  getTimeline: () => api.get('/timeline'),
  getFAQ: (language = 'en') => api.get(`/faq?language=${language}`),
  getFirstTimeVoterGuide: () => api.get('/first-time-voter-guide'),
  getQuiz: (language = 'en') => api.get(`/quiz?language=${language}`),

  // Translation endpoint
  translateText: (text, targetLanguage = 'en', sourceLanguage = 'en') =>
    api.post('/chat/translate', {
      text,
      target_language: targetLanguage,
      source_language: sourceLanguage,
    }),

  // Chat endpoint
  sendMessage: (userInput, language = 'en', isFirstTimeVoter = false, location = null) =>
    api.post('/chat/', {
      user_input: userInput,
      language,
      is_first_time_voter: isFirstTimeVoter,
      location,
    }),

  // Chat history
  getChatHistory: (limit = 10) => api.get(`/chat/history?limit=${limit}`),
};

export default api;
