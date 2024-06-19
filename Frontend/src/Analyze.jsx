import React, { useState } from 'react';
import axios from 'axios';

const Analyze = () => {
    const [review, setReview] = useState('');
    const [sentiment, setSentiment] = useState(null);
    const [department, setDepartment] = useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      setError(null); // Clear any previous errors
      setIsLoading(true);
  
      try {
        const response = await axios.post('http://127.0.0.1:5000/analyze', { review });
        setSentiment(response.data.sentiment);
        setDepartment(response.data.department);
      } catch (error) {
        setError("An error occurred. Please try again later.");
      } finally {
        setIsLoading(false);
      }
    };
  
    return (
      <div>
        <h2>Review Analyzer</h2>
        <form onSubmit={handleSubmit}>
          <textarea
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="Enter your review here..."
          />
          <button type="submit" disabled={isLoading}>
            {isLoading ? 'Analyzing...' : 'Analyze'}
          </button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </form>
        {sentiment && department && (
          <div>
            <p>Sentiment: {sentiment}</p>
            <p>Department: {department}</p>
          </div>
        )}
      </div>
    );
  };
  
  export default Analyze;
  
