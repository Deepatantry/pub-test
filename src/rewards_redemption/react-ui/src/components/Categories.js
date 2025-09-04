import React, { useState, useEffect } from 'react';
import { rewardsAPI } from '../services/api';

const Categories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadCategories = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await rewardsAPI.getActiveCategories();
      setCategories(response.data.data.categories || []);
    } catch (err) {
      setError('Failed to load categories');
      console.error('Error loading categories:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCategories();
  }, []);

  return (
    <div className="section">
      <h3>🎯 Active Categories</h3>
      <button className="button" onClick={loadCategories} disabled={loading}>
        {loading ? 'Loading...' : 'Refresh Categories'}
      </button>

      {error && (
        <div className="result error">
          <p>{error}</p>
        </div>
      )}

      {categories.length > 0 && (
        <div className="result success">
          <h4>Bonus Categories</h4>
          {categories.map(category => (
            <div key={category.id} className="card">
              <h5>{category.name}</h5>
              <p>{category.description}</p>
              <p><strong>Status:</strong> <span className="status-active">{category.status}</span></p>
              <p><strong>Spending Cap:</strong> ${category.spending_cap?.toLocaleString() || 'No limit'}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Categories;