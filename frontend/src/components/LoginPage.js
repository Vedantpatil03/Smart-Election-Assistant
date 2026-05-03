import React, { useState } from 'react';
import './LoginPage.css';

const LoginPage = ({ onLogin }) => {
  const [name, setName] = useState('');
  const [mobile, setMobile] = useState('');
  const [voterId, setVoterId] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();

    const trimmedName = name.trim();
    const trimmedMobile = mobile.trim();
    const trimmedVoterId = voterId.trim().toUpperCase();

    if (!trimmedName) {
      setError('Please enter your name.');
      return;
    }

    if (!/^\d{10}$/.test(trimmedMobile)) {
      setError('Please enter a valid 10-digit mobile number.');
      return;
    }

    if (!trimmedVoterId) {
      setError('Please enter your Voter ID.');
      return;
    }

    onLogin({
      name: trimmedName,
      mobile: trimmedMobile,
      voterId: trimmedVoterId,
    });
  };

  return (
    <div className="login-shell">
      <div className="login-card">
        <p className="login-tag">Smart Election Assistant</p>
        <h1>Welcome Voter</h1>
        <p className="login-subtitle">
          Login to access Voting steps, Timeline, Quiz, FAQs, and Chat Assistant.
        </p>

        <form className="login-form" onSubmit={handleSubmit}>
          <label htmlFor="name">Full Name</label>
          <input
            id="name"
            type="text"
            placeholder="Enter your full name"
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              setError('');
            }}
          />

          <label htmlFor="mobile">Mobile Number</label>
          <input
            id="mobile"
            type="tel"
            placeholder="10-digit mobile number"
            value={mobile}
            onChange={(e) => {
              setMobile(e.target.value.replace(/\D/g, ''));
              setError('');
            }}
            maxLength={10}
          />

          <label htmlFor="voter-id">Voter ID</label>
          <input
            id="voter-id"
            type="text"
            placeholder="Enter EPIC / Voter ID"
            value={voterId}
            onChange={(e) => {
              setVoterId(e.target.value.toUpperCase());
              setError('');
            }}
          />

          {error ? <p className="login-error">{error}</p> : null}

          <button type="submit" className="login-button">
            Continue
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginPage;
