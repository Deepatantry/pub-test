import React, { useState } from 'react';
import { rewardsAPI } from '../services/api';

const ValueAnalysis = () => {
  const [analysis, setAnalysis] = useState(null);
  const [tier, setTier] = useState('');
  const [availablePoints, setAvailablePoints] = useState(10000);
  const [loading, setLoading] = useState(false);

  const loadValueAnalysis = async () => {
    setLoading(true);
    try {
      const params = {
        available_points: availablePoints
      };
      if (tier) params.member_tier = tier;

      const response = await rewardsAPI.getValueAnalysis(params);
      setAnalysis(response.data.data);
    } catch (error) {
      console.error('Error loading value analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const getValueRatingColor = (rating) => {
    switch (rating) {
      case 'Excellent': return '#28a745';
      case 'Good': return '#007bff';
      case 'Fair': return '#ffc107';
      case 'Poor': return '#dc3545';
      default: return '#6c757d';
    }
  };

  return (
    <div className="section">
      <h3>💎 Value Analysis</h3>
      
      <div className="input-group">
        <label>Member Tier:</label>
        <select value={tier} onChange={(e) => setTier(e.target.value)}>
          <option value="">Standard</option>
          <option value="gold">Gold</option>
          <option value="platinum">Platinum</option>
          <option value="diamond">Diamond</option>
        </select>
      </div>

      <div className="input-group">
        <label>Available Points:</label>
        <input 
          type="number" 
          value={availablePoints}
          onChange={(e) => setAvailablePoints(Number(e.target.value))}
          min="0"
          step="1000"
        />
      </div>

      <button className="button" onClick={loadValueAnalysis} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze Values'}
      </button>

      {analysis && (
        <div className="result success">
          <h4>Value Analysis Results</h4>
          
          {analysis.recommendations && analysis.recommendations.length > 0 && (
            <div>
              <h5>Best Value Recommendations</h5>
              {analysis.recommendations.map((rec, index) => (
                <div key={index} className="card">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h6>{rec.name}</h6>
                      <p><strong>Type:</strong> {rec.type}</p>
                      <p><strong>Points Required:</strong> <span className="points">{rec.points_required?.toLocaleString()}</span></p>
                      <p><strong>Cash Value:</strong> ${rec.cash_value?.toFixed(2)}</p>
                      <p><strong>Value per Point:</strong> ${rec.effective_value_per_point?.toFixed(4)}</p>
                      <p><strong>Reason:</strong> {rec.recommendation_reason}</p>
                    </div>
                    <div style={{ textAlign: 'center' }}>
                      <div 
                        style={{ 
                          color: getValueRatingColor(rec.value_rating),
                          fontWeight: 'bold',
                          fontSize: '18px'
                        }}
                      >
                        {rec.value_rating}
                      </div>
                      <div style={{ fontSize: '12px', color: '#666' }}>
                        Rating
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {analysis.analysis && analysis.analysis.length > 0 && (
            <div>
              <h5>Complete Analysis (Top 10)</h5>
              <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
                {analysis.analysis.slice(0, 10).map((item, index) => (
                  <div key={index} className="card" style={{ margin: '5px 0' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                      <div>
                        <strong>{item.name}</strong> ({item.type})
                      </div>
                      <div style={{ textAlign: 'right' }}>
                        <div>${item.effective_value_per_point?.toFixed(4)}/pt</div>
                        <div style={{ 
                          color: getValueRatingColor(item.value_rating),
                          fontSize: '12px'
                        }}>
                          {item.value_rating}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ValueAnalysis;