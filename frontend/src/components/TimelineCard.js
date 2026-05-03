import React, { useState, useEffect } from 'react';
import { electionAPI } from '../services/api';
import './TimelineCard.css';

const TimelineCard = () => {
  const [phases, setPhases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchTimeline = async () => {
      try {
        setLoading(true);
        const response = await electionAPI.getTimeline();
        setPhases(response.data.data);
      } catch (err) {
        setError('Failed to load election timeline');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchTimeline();
  }, []);

  if (loading) return <div className="card loading">Loading timeline...</div>;
  if (error) return <div className="card error">{error}</div>;

  return (
    <div className="timeline-card">
      <h2>Election Timeline</h2>
      <div className="timeline">
        {phases.map((phase, index) => (
          <div key={index} className="timeline-item">
            <div className="timeline-marker"></div>
            <div className="timeline-content">
              <h3>{phase.phase}</h3>
              <p className="duration">{phase.duration}</p>
              <p>{phase.description}</p>
              <details>
                <summary>More Info</summary>
                <p>{phase.details}</p>
              </details>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TimelineCard;
