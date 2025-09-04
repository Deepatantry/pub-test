# Rewards & Redemption System

A complete implementation of the Rewards & Redemption microservice for the PremiumCard Loyalty Program.

## Features

### Core Services
- **Category Management**: Bonus categories with multipliers and spending caps
- **Spending Insights**: Analytics and recommendations based on transaction patterns  
- **Redemption Catalog**: Browse and manage redemption options (cashback, travel, merchandise)
- **Redemption Processing**: Manual and automatic redemption workflows
- **Value Optimization**: Point value analysis and recommendations

### Technical Implementation
- **In-Memory Repositories**: All data stored in memory for demo purposes
- **Event-Driven Architecture**: Async event handling for real-time updates
- **REST API**: Complete API coverage for all functionality
- **Mock External Services**: Simulated travel, merchandise, and payment providers

## Quick Start

### 1. Install Dependencies
```bash
cd workdir/src/rewards_redemption
pip install -r requirements.txt
```

### 2. Run Demo
```bash
python run_demo.py
```

Choose from:
- **CLI Demo**: Interactive command-line interface
- **Web API**: FastAPI server at http://localhost:8000
- **Web UI**: Browser-based demo interface
- **Integration Tests**: Automated system validation

### 3. API Documentation
When running the web server, visit:
- API Docs: http://localhost:8000/docs
- Demo UI: http://localhost:8000

## API Endpoints

- `GET /categories/active` - View active bonus categories
- `GET /categories/{member_id}/insights` - Get spending insights
- `GET /redemptions/catalog` - Browse redemption options
- `POST /redemptions/manual` - Process manual redemption
- `GET /redemptions/{member_id}/history` - View redemption history
- `GET /redemptions/value-analysis` - Get value recommendations

## Demo Data

The system comes pre-loaded with:
- **4 Categories**: Dining (3x), Gas (2x), Grocery (2.5x), Travel (5x)
- **6 Redemption Options**: Cashback, travel, merchandise, experiences
- **2 Demo Members**: member1 (12,000 pts), member2 (8,500 pts)
- **Sample Analytics**: Historical spending and earning patterns

## Architecture

```
├── models/           # Pydantic data models
├── repositories/     # In-memory data access
├── services/         # Business logic services
├── events/          # Event handling system
├── api/             # FastAPI endpoints
├── demo/            # Demo interfaces and data
└── config/          # Application settings
```

## Event System

The system publishes/subscribes to events:
- **Inbound**: TransactionProcessed, PointsEarned, BalanceUpdated, TierAdvanced
- **Outbound**: CategoryUpdated, RedemptionProcessed, AutoRedemptionTriggered

## Testing

Run integration tests:
```bash
python run_demo.py
# Select option 4
```

Tests validate:
- System initialization
- All core services
- API functionality
- Event handling
- Data consistency

## Configuration

Environment variables (optional):
- `DEBUG=true` - Enable debug mode
- `HOST=0.0.0.0` - Server host
- `PORT=8000` - Server port
- `CACHE_TTL=300` - Cache timeout seconds