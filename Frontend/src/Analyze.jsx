import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import './Analyze.css';
import ReactStars from 'react-rating-stars-component';


const Analyze = () => {
  const [review, setReview] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [department, setDepartment] = useState(null);
  const [stars, setStars] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:5000/analyze', { review });
      setSentiment(response.data.sentiment);
      setDepartment(response.data.department);
      setStars(response.data.stars);
      setShowResults(true);
    } catch (error) {
      setError("An error occurred. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setReview('');
    setSentiment(null);
    setDepartment(null);
    setStars(null);
    setShowResults(false);
    setError(null);
  };

  return (
    <div className="container">
      <motion.div
        className={`content-container ${showResults ? 'shift-left' : ''}`}
        initial={{ opacity: 1 }}
        animate={{ x: showResults ? '-30%' : '0%' }}
        transition={{ duration: 0.2 }}
      >
        <h2 className="title">Review Analyzer</h2>
        <form onSubmit={handleSubmit} className="form">
          <textarea
            className="textarea"
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="Enter your review here..."
            rows="6"
          />
          <motion.button
            type="submit"
            className={`button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </motion.button>
          {error && <p className="error">{error}</p>}
        </form>
      </motion.div>

      {showResults && (
        <motion.div
          className="results-container"
          initial={{ opacity: 0, x: '-100%' }}
          animate={{ opacity: 1, x: '30%' }}
          transition={{ duration: 0.2 }}
        >
          <div className="result">
            <p><span className="label">Sentiment:</span> {sentiment}</p>
            <p><span className="label">Department:</span> {department}</p>
            {stars !== null && (
              <div>
                <span className="label">Stars:</span>
                <ReactStars
                  count={5}
                  value={stars}
                  size={24}
                  isHalf={true}
                  edit={false}
                  activeColor="#ffd700"
                />
              </div>
            )}
            <button className="button" onClick={resetForm}>
             try again
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Analyze;
