import React, { useState } from 'react';
import MemberDashboard from './components/MemberDashboard';
import Categories from './components/Categories';
import SpendingInsights from './components/SpendingInsights';
import RedemptionCatalog from './components/RedemptionCatalog';
import ValueAnalysis from './components/ValueAnalysis';

function App() {
  const [selectedMember, setSelectedMember] = useState('member1');

  return (
    <div className="container">
      <div className="header">
        <h1>🏆 Rewards & Redemption System</h1>
        <p>Interactive React Demo - Loyalty Program Backend</p>
      </div>

      <div className="grid">
        <MemberDashboard 
          selectedMember={selectedMember}
          onMemberChange={setSelectedMember}
        />
        <Categories />
      </div>

      <SpendingInsights selectedMember={selectedMember} />

      <RedemptionCatalog selectedMember={selectedMember} />

      <ValueAnalysis />

      <div className="section">
        <h3>ℹ️ System Information</h3>
        <div className="result">
          <h4>Demo Configuration</h4>
          <p><strong>API Server:</strong> http://localhost:8000</p>
          <p><strong>Demo Members:</strong> member1 (12,000 pts, Gold), member2 (8,500 pts, Standard)</p>
          <p><strong>Categories:</strong> Dining (3x), Gas (2x), Grocery (2.5x), Travel (5x)</p>
          <p><strong>Redemption Types:</strong> Cashback, Travel, Merchandise, Experience</p>
          
          <h5>Available Features:</h5>
          <ul>
            <li>✓ Real-time category and multiplier management</li>
            <li>✓ Spending insights with recommendations</li>
            <li>✓ Interactive redemption catalog</li>
            <li>✓ Manual redemption processing</li>
            <li>✓ Value optimization analysis</li>
            <li>✓ Tier-based benefits and pricing</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default App;