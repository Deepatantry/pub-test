import React, { useState, useEffect } from 'react';
import { rewardsAPI } from '../services/api';

const RedemptionCatalog = ({ selectedMember }) => {
  const [catalog, setCatalog] = useState([]);
  const [loading, setLoading] = useState(false);
  const [typeFilter, setTypeFilter] = useState('');
  const [processing, setProcessing] = useState(false);
  const [redemptionResult, setRedemptionResult] = useState(null);

  const loadCatalog = async () => {
    setLoading(true);
    try {
      const params = typeFilter ? { type: typeFilter } : {};
      const response = await rewardsAPI.getRedemptionCatalog(params);
      setCatalog(response.data.data.items || []);
    } catch (error) {
      console.error('Error loading catalog:', error);
    } finally {
      setLoading(false);
    }
  };

  const processRedemption = async (catalogId) => {
    if (!selectedMember) {
      alert('Please select a member first');
      return;
    }

    setProcessing(true);
    setRedemptionResult(null);
    try {
      const response = await rewardsAPI.processManualRedemption({
        member_id: selectedMember,
        catalog_id: catalogId,
        quantity: 1
      });
      setRedemptionResult(response.data);
      loadCatalog(); // Refresh catalog
    } catch (error) {
      setRedemptionResult({
        success: false,
        message: error.response?.data?.detail || 'Redemption failed'
      });
    } finally {
      setProcessing(false);
    }
  };

  useEffect(() => {
    loadCatalog();
  }, [typeFilter]);

  return (
    <div className="section">
      <h3>🛍️ Redemption Catalog</h3>
      
      <div className="input-group">
        <label>Type Filter:</label>
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          <option value="">All Types</option>
          <option value="cashback">Cashback</option>
          <option value="travel">Travel</option>
          <option value="merchandise">Merchandise</option>
          <option value="experience">Experience</option>
        </select>
      </div>

      <button className="button" onClick={loadCatalog} disabled={loading}>
        {loading ? 'Loading...' : 'Browse Catalog'}
      </button>

      {redemptionResult && (
        <div className={`result ${redemptionResult.success ? 'success' : 'error'}`}>
          <h4>Redemption Result</h4>
          <p>{redemptionResult.message}</p>
          {redemptionResult.success && redemptionResult.data && (
            <div>
              <p><strong>Transaction ID:</strong> {redemptionResult.data.transaction_id}</p>
              <p><strong>Points Used:</strong> {redemptionResult.data.points_used?.toLocaleString()}</p>
              <p><strong>Remaining Balance:</strong> {redemptionResult.data.remaining_balance?.toLocaleString()}</p>
            </div>
          )}
        </div>
      )}

      {catalog.length > 0 && (
        <div className="result">
          <h4>Available Redemptions</h4>
          {catalog.map(item => (
            <div key={item.id} className="card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h5>{item.name}</h5>
                  <p>{item.description}</p>
                  <p><strong>Type:</strong> {item.type}</p>
                  <p><strong>Points:</strong> <span className="points">{item.points_required?.toLocaleString()}</span></p>
                  <p><strong>Value:</strong> ${item.cash_value?.toFixed(2)}</p>
                  <p><strong>Stock:</strong> {item.in_stock ? '✓ Available' : '✗ Out of Stock'}</p>
                </div>
                <button 
                  className="button" 
                  onClick={() => processRedemption(item.id)}
                  disabled={!item.in_stock || processing || !selectedMember}
                >
                  {processing ? 'Processing...' : 'Redeem'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RedemptionCatalog;