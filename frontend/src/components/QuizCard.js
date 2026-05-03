import React, { useEffect, useMemo, useState } from 'react';
import { electionAPI } from '../services/api';
import './QuizCard.css';

const QuizCard = (props) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResult, setShowResult] = useState(false);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        setLoading(true);
        const response = await electionAPI.getQuiz('en');
        setQuestions(response.data.data || []);
      } catch (err) {
        setError('Failed to load quiz');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuiz();
  }, []);

  const currentQuestion = questions[currentIndex];

  const score = useMemo(() => {
    return questions.reduce((total, q) => {
      const selected = answers[q.question_id];
      return selected === q.correct_option_index ? total + 1 : total;
    }, 0);
  }, [answers, questions]);

  const answeredCount = Object.keys(answers).length;
  const isAnswered = currentQuestion
    ? answers[currentQuestion.question_id] !== undefined
    : false;

  const handleSelect = (optionIndex) => {
    if (!currentQuestion || showResult) return;

    setAnswers((prev) => ({
      ...prev,
      [currentQuestion.question_id]: optionIndex,
    }));
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      return;
    }

    setShowResult(true);
  };

  const restartQuiz = () => {
    setAnswers({});
    setCurrentIndex(0);
    setShowResult(false);
  };

  if (loading) return <div className="quiz-card loading">Loading quiz...</div>;
  if (error) return <div className="quiz-card error">{error}</div>;
  if (questions.length === 0) return <div className="quiz-card">No quiz questions available.</div>;

  if (showResult) {
    const percentage = Math.round((score / questions.length) * 100);

    return (
      <div className="quiz-card" {...props}>
        <h2>Election Awareness Quiz</h2>
        <div className="quiz-result">
          <p className="result-score">Your Score: {score}/{questions.length}</p>
          <p className="result-percent">{percentage}%</p>
          <p className="result-message">
            {percentage >= 80
              ? 'Excellent! You are well-informed about voting basics.'
              : percentage >= 50
              ? 'Good effort. Review key voting points and try again.'
              : 'Keep learning. Read the guide cards and retry the quiz.'}
          </p>
          <button type="button" className="quiz-btn" onClick={restartQuiz}>
            Retry Quiz
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="quiz-card" {...props}>
      <h2>Election Awareness Quiz</h2>
      <p className="quiz-progress">
        Question {currentIndex + 1} of {questions.length}
      </p>
      <p className="quiz-question">{currentQuestion.question}</p>

      <div className="quiz-options">
        {currentQuestion.options.map((option, idx) => {
          const selected = answers[currentQuestion.question_id] === idx;
          return (
            <button
              type="button"
              key={`${currentQuestion.question_id}-${idx}`}
              className={`quiz-option ${selected ? 'selected' : ''}`}
              onClick={() => handleSelect(idx)}
            >
              {option}
            </button>
          );
        })}
      </div>

      {isAnswered && (
        <p className="quiz-explanation">{currentQuestion.explanation}</p>
      )}

      <div className="quiz-footer">
        <span>Answered: {answeredCount}/{questions.length}</span>
        <button
          type="button"
          className="quiz-btn"
          onClick={handleNext}
          disabled={!isAnswered}
        >
          {currentIndex < questions.length - 1 ? 'Next' : 'Finish'}
        </button>
      </div>
    </div>
  );
};

export default QuizCard;
