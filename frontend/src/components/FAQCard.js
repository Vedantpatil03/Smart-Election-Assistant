import React, { useEffect, useState } from 'react';
import { electionAPI } from '../services/api';
import './FAQCard.css';

const FAQCard = () => {
  const [faqs, setFaqs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchFaqs = async () => {
      try {
        setLoading(true);
        const response = await electionAPI.getFAQ('en');
        setFaqs(response.data.data || []);
      } catch (err) {
        setError('Failed to load FAQs');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchFaqs();
  }, []);

  if (loading) return <div className="faq-card loading">Loading FAQs...</div>;
  if (error) return <div className="faq-card error">{error}</div>;

  return (
    <div className="faq-card">
      <h2>Frequently Asked Questions</h2>
      <div className="faq-list">
        {faqs.map((faq, index) => (
          <details key={`${faq.question}-${index}`} className="faq-item">
            <summary>{faq.question}</summary>
            <div className="faq-answer">
              <p>{faq.answer}</p>
              <span className="faq-category">{faq.category}</span>
            </div>
          </details>
        ))}
      </div>
    </div>
  );
};

export default FAQCard;