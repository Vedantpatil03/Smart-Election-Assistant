import React, { useState } from 'react';
import ChatWindow from './components/ChatWindow';
import StepsCard from './components/StepsCard';
import TimelineCard from './components/TimelineCard';
import FAQCard from './components/FAQCard';
import FirstTimeVoterGuideCard from './components/FirstTimeVoterGuideCard';
import QuizCard from './components/QuizCard';
import LoginPage from './components/LoginPage';
import './App.css';

function App() {
  const [loggedInUser, setLoggedInUser] = useState(() => {
    const savedUser = localStorage.getItem('sea-user-session');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const scrollToSection = (sectionId) => (event) => {
    event.preventDefault();

    if (sectionId === 'hero') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
      targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const handleLogin = (user) => {
    setLoggedInUser(user);
    localStorage.setItem('sea-user-session', JSON.stringify(user));
  };

  const handleLogout = () => {
    setLoggedInUser(null);
    localStorage.removeItem('sea-user-session');
  };

  if (!loggedInUser) {
    return <LoginPage onLogin={handleLogin} />;
  }

  return (
    <div className="app">
      <div className="app-shell">
        <nav className="top-nav" aria-label="Primary navigation">
          <div className="top-nav-brand">
            <span className="top-nav-mark">SEA</span>
            <div>
              <strong>Smart Election Assistant</strong>
              <span>Voter support dashboard</span>
            </div>
          </div>

          <div className="top-nav-links">
            <a href="#hero" onClick={scrollToSection('hero')}>Home</a>
            <a href="#voting-steps" onClick={scrollToSection('voting-steps')}>Guide</a>
            <a href="#election-timeline" onClick={scrollToSection('election-timeline')}>Election Timeline</a>
            <a href="#faqs" onClick={scrollToSection('faqs')}>FAQ</a>
            <a href="#quiz" onClick={scrollToSection('quiz')}>Quiz</a>
            <a href="#assistant" onClick={scrollToSection('assistant')}>Election Assistant</a>
          </div>

          <button type="button" className="logout-btn top-nav-logout" onClick={handleLogout}>
            Logout ({loggedInUser.name})
          </button>
        </nav>

        <header className="hero" id="hero">
          <div className="hero-copy">
            <p className="eyebrow">Indian Election Guide</p>
            <h1><strong>Everything a voter needs in one place</strong></h1>
            <p>
              Explore the voting process, election timeline, FAQs, first-time voter guidance,
              and the AI chat assistant built into the same experience.
            </p>
          </div>

          <div className="hero-side">
            <div className="hero-stats">
              <div>
                <strong>5</strong>
                <span>core tools visible</span>
              </div>
              <div>
                <strong>3</strong>
                <span>supported languages</span>
              </div>
              <div>
                <strong>1</strong>
                <span>AI assistant</span>
              </div>
            </div>

          </div>
        </header>

        <main className="dashboard">
          <section id="voting-steps" className="feature-section" aria-label="Voting process steps">
            <StepsCard />
          </section>

          <section id="election-timeline" className="feature-section" aria-label="Election timeline">
            <TimelineCard />
          </section>

          <section id="faqs" className="feature-section" aria-label="Frequently asked questions">
            <FAQCard />
          </section>

          <section id="first-time-voter" className="feature-section" aria-label="First-time voter guide">
            <FirstTimeVoterGuideCard />
          </section>

          <section id="quiz" className="feature-section" aria-label="Election awareness quiz">
            <QuizCard />
          </section>

          <section id="assistant" className="chat-section" aria-label="Smart election assistant chat">
            <ChatWindow />
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;
