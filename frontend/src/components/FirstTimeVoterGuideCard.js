import React, { useEffect, useState } from 'react';
import { electionAPI } from '../services/api';
import './FirstTimeVoterGuideCard.css';

const FirstTimeVoterGuideCard = () => {
  const [guide, setGuide] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchGuide = async () => {
      try {
        setLoading(true);
        const response = await electionAPI.getFirstTimeVoterGuide();
        setGuide(response.data.data || null);
      } catch (err) {
        setError('Failed to load first-time voter guide');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchGuide();
  }, []);

  if (loading) return <div className="guide-card loading">Loading guide...</div>;
  if (error) return <div className="guide-card error">{error}</div>;
  if (!guide) return null;

  return (
    <div className="guide-card">
      <h2>{guide.title}</h2>
      <p className="guide-description">{guide.description}</p>

      <div className="guide-sections">
        {guide.sections?.map((section, index) => (
          <div key={`${section.title}-${index}`} className="guide-section">
            <h3>{section.title}</h3>
            <ul>
              {section.tips?.map((tip, tipIndex) => (
                <li key={`${tip}-${tipIndex}`}>{tip}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>

      <div className="guide-questions">
        <h3>Common Questions</h3>
        {guide.common_questions?.map((item, index) => (
          <details key={`${item.q}-${index}`} className="guide-question">
            <summary>{item.q}</summary>
            <p>{item.a}</p>
          </details>
        ))}
      </div>
    </div>
  );
};

export default FirstTimeVoterGuideCard;