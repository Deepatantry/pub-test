import React, { useState, useEffect } from 'react';
import { rewardsAPI } from '../services/api';

const MemberDashboard = ({ selectedMember, onMemberChange }) => {
  const [memberData, setMemberData] = useState(null);
  const [loading, setLoading] = useState(false);

  const members = [
    { id: 'member1', name: 'Member 1', points: '12,000', tier: 'Gold' },
    { id: 'member2', name: 'Member 2', points: '8,500', tier: 'Standard' }
  ];

  const loadMemberData = async () => {
    if (!selectedMember) return;
    
    setLoading(true);
    try {
      const insights = await rewardsAPI.getSpendingInsights(selectedMember);
      setMemberData({
        member_id: selectedMember,
        ...insights.data.data,
        tier: members.find(m => m.id === selectedMember)?.tier || 'Standard'
      });
    } catch (error) {
      console.error('Error loading member data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMemberData();
  }, [selectedMember]);

  return (
    <div className="section">
      <h3>📊 Member Dashboard</h3>
      <div className="input-group">
        <label>Member ID:</label>
        <select 
          value={selectedMember} 
          onChange={(e) => onMemberChange(e.target.value)}
        >
          <option value="">Select Member</option>
          {members.map(member => (
            <option key={member.id} value={member.id}>
              {member.name} ({member.points} pts)
            </option>
          ))}
        </select>
      </div>
      
      <button className="button" onClick={loadMemberData} disabled={!selectedMember || loading}>
        {loading ? 'Loading...' : 'Load Member Data'}
      </button>

      {memberData && (
        <div className="result success">
          <h4>Member Information</h4>
          <p><strong>Member ID:</strong> {memberData.member_id}</p>
          <p><strong>Tier:</strong> {memberData.tier}</p>
          <p><strong>Total Spending:</strong> ${memberData.total_spending?.toFixed(2) || '0.00'}</p>
          <p><strong>Total Points:</strong> <span className="points">{memberData.total_points?.toLocaleString() || '0'}</span></p>
          <p><strong>Top Category:</strong> {memberData.top_category || 'None'}</p>
        </div>
      )}
    </div>
  );
};

export default MemberDashboard;