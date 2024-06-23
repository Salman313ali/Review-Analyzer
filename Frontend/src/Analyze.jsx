import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import './Analyze.css';
import ReactStars from 'react-rating-stars-component';

const Analyze = () => {
  const [review, setReview] = useState('');
  const [inputStars, setInputStars] = useState(1); 
  const [predictedStars, setPredictedStars] = useState(null);
  const [sentiment, setSentiment] = useState(null);
  const [department, setDepartment] = useState(null);
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
      if (response.data.sentiment === 'negative') {
        setDepartment(response.data.department);
      } else {
        setDepartment(null);
      }
      const receivedStars = response.data.stars;
      setPredictedStars(receivedStars < 1 ? 1 : receivedStars); 
      setShowResults(true);
    } catch (error) {
      setError("An error occurred. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setReview('');
    setInputStars(1); 
    setPredictedStars(null);
    setSentiment(null);
    setDepartment(null);
    setShowResults(false);
    setError(null);
  };

  return (
    <div className="container">
      <motion.div
        className={`content-container ${showResults ? 'shift-left' : ''}`}
        initial={{ opacity: 1 }}
        animate={{ x: showResults ? '-20%' : '0%' }}
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
          <div className="stars-input">
            <span className="label">Your Rating:</span>
            <ReactStars
              count={5}
              value={inputStars}
              onChange={(newRating) => setInputStars(newRating)} 
              size={24}
              isHalf={true}
              activeColor="#ffd700"
            />
          </div>
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
          animate={{ opacity: 1, x: '20%' }}
          transition={{ duration: 0.2 }}
        >
          <div className="result">
            <p><span className="label">Sentiment:</span> {sentiment}</p>
            <p><span className="label">Sentiment:</span> {department}</p>
            {sentiment === 'negative' && department && (
              <p><span className="label">Complaint:</span> The complaint is generated for this department '{department}'</p>
            )}
            <div>
              <span className="label">Actual Rating:</span>
              <ReactStars
                count={5}
                value={inputStars}
                size={24}
                isHalf={true}
                edit={false}
                activeColor="#ffd700"
              />
            </div>
            {predictedStars !== null && (
              <div>
                <span className="label">Predicted Rating:</span>
                <ReactStars
                  count={5}
                  value={predictedStars}
                  size={24}
                  isHalf={true}
                  edit={false}
                  activeColor="#ffd700"
                />
              </div>
            )}
            <button className="button" onClick={resetForm}>
              Try again
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default Analyze;
