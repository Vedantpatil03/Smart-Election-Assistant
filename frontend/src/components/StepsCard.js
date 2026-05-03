import React, { useState, useEffect } from 'react';
import { electionAPI } from '../services/api';
import './StepsCard.css';

const StepsCard = () => {
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [completedSteps, setCompletedSteps] = useState({});

  useEffect(() => {
    const saved = localStorage.getItem('completedVotingSteps');
    if (saved) {
      try {
        setCompletedSteps(JSON.parse(saved));
      } catch (e) {
        console.error('Failed to parse saved completed steps', e);
      }
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('completedVotingSteps', JSON.stringify(completedSteps));
  }, [completedSteps]);

  useEffect(() => {
    const fetchSteps = async () => {
      try {
        setLoading(true);
        const response = await electionAPI.getSteps();
        setSteps(response.data.data);
      } catch (err) {
        setError('Failed to load voting steps');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchSteps();
  }, []);

  const toggleStepCompletion = (stepNumber) => {
    setCompletedSteps((prev) => ({
      ...prev,
      [stepNumber]: !prev[stepNumber],
    }));
  };

  const completedCount = steps.filter((step) => completedSteps[step.step_number]).length;

  if (loading) return <div className="card loading">Loading steps...</div>;
  if (error) return <div className="card error">{error}</div>;

  return (
    <div className="steps-card">
      <h2>Voting Process Steps</h2>
      <p className="steps-progress">
        Completed: {completedCount}/{steps.length}
      </p>
      <div className="steps-list">
        {steps.map((step) => {
          const isCompleted = Boolean(completedSteps[step.step_number]);

          return (
            <div key={step.step_number} className={`step-item ${isCompleted ? 'completed' : ''}`}>
              <div className="step-number">{step.step_number}</div>
              <div className="step-content">
                <h3>{step.title}</h3>
                <p>{step.description}</p>
                <button
                  type="button"
                  className={`read-toggle ${isCompleted ? 'done' : ''}`}
                  onClick={() => toggleStepCompletion(step.step_number)}
                >
                  {isCompleted ? 'Mark as unread' : 'Mark as read'}
                </button>
                <details>
                  <summary>More Details</summary>
                  <p>{step.details}</p>
                </details>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default StepsCard;
