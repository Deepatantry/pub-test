import React, { useState } from 'react';
import { rewardsAPI } from '../services/api';

const SpendingInsights = ({ selectedMember }) => {
  const [insights, setInsights] = useState(null);
  const [period, setPeriod] = useState('monthly');
  const [loading, setLoading] = useState(false);

  const loadInsights = async () => {
    if (!selectedMember) {
      alert('Please select a member first');
      return;
    }

    setLoading(true);
    try {
      const response = await rewardsAPI.getSpendingInsights(selectedMember, period);
      setInsights(response.data.data);
    } catch (error) {
      console.error('Error loading insights:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="section">
      <h3>📈 Spending Insights</h3>
      
      <div className="input-group">
        <label>Period:</label>
        <select value={period} onChange={(e) => setPeriod(e.target.value)}>
          <option value="monthly">Monthly</option>
          <option value="quarterly">Quarterly</option>
          <option value="yearly">Yearly</option>
        </select>
      </div>

      <button 
        className="button" 
        onClick={loadInsights} 
        disabled={!selectedMember || loading}
      >
        {loading ? 'Generating...' : 'Generate Insights'}
      </button>

      {insights && (
        <div className="result success">
          <h4>Insights for {insights.member_id}</h4>
          <div className="grid">
            <div>
              <p><strong>Total Spending:</strong> ${insights.total_spending?.toFixed(2) || '0.00'}</p>
              <p><strong>Total Points:</strong> <span className="points">{insights.total_points?.toLocaleString() || '0'}</span></p>
              <p><strong>Top Category:</strong> {insights.top_category || 'None'}</p>
            </div>
          </div>

          {insights.category_breakdown && insights.category_breakdown.length > 0 && (
            <div>
              <h5>Category Breakdown</h5>
              {insights.category_breakdown.map((category, index) => (
                <div key={index} className="card">
                  <h6>{category.category_name}</h6>
                  <p><strong>Spending:</strong> ${category.spending?.toFixed(2)}</p>
                  <p><strong>Points:</strong> <span className="points">{category.points?.toLocaleString()}</span></p>
                  <p><strong>Transactions:</strong> {category.transactions}</p>
                  <p><strong>Avg Transaction:</strong> ${category.avg_transaction?.toFixed(2)}</p>
                </div>
              ))}
            </div>
          )}

          {insights.recommendations && insights.recommendations.length > 0 && (
            <div>
              <h5>Recommendations</h5>
              <ul>
                {insights.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SpendingInsights;