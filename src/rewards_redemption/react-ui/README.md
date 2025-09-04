# Rewards & Redemption React UI

A modern React.js interface for the Rewards & Redemption System demo.

## Features

- **Member Dashboard**: Switch between demo members and view their data
- **Active Categories**: Display bonus categories with multipliers and caps
- **Spending Insights**: Generate analytics and recommendations
- **Redemption Catalog**: Browse and process redemptions with real-time inventory
- **Value Analysis**: Compare redemption values with tier-based pricing
- **Responsive Design**: Clean, modern interface with real-time updates

## Quick Start

### Prerequisites
- Node.js 16+ installed
- Python API server running on localhost:8000

### Installation
```bash
cd react-ui
npm install
```

### Development
```bash
npm start
```
Opens http://localhost:3000 with hot reload

### Production Build
```bash
npm run build
```

## API Integration

The React app connects to the Python FastAPI backend:
- **Development**: Proxied through package.json to localhost:8000
- **Production**: Direct connection to API server

### API Endpoints Used
- `GET /categories/active` - Category data
- `GET /categories/{member_id}/insights` - Spending analytics
- `GET /redemptions/catalog` - Redemption options
- `POST /redemptions/manual` - Process redemptions
- `GET /redemptions/value-analysis` - Value recommendations

## Components

### MemberDashboard
- Member selection dropdown
- Real-time balance and tier display
- Spending summary integration

### Categories
- Active bonus categories display
- Multiplier and cap information
- Auto-refresh functionality

### SpendingInsights
- Period-based analytics (monthly/quarterly/yearly)
- Category breakdown with recommendations
- Interactive charts and summaries

### RedemptionCatalog
- Filterable catalog by type
- Real-time inventory status
- One-click redemption processing
- Transaction confirmation

### ValueAnalysis
- Tier-based value calculations
- Best value recommendations
- Point optimization suggestions

## State Management

- React hooks for local component state
- Prop drilling for shared member selection
- API service layer for data fetching
- Error handling and loading states

## Styling

- CSS modules with responsive design
- Color-coded status indicators
- Card-based layout for data display
- Consistent button and form styling

## Demo Data

- **Members**: member1 (Gold, 12K pts), member2 (Standard, 8.5K pts)
- **Categories**: Dining, Gas, Grocery, Travel with different multipliers
- **Redemptions**: Cashback, travel credits, merchandise, experiences
- **Real-time Updates**: Inventory and balance changes reflected immediately

## Development Notes

- Uses axios for API calls with error handling
- Responsive grid layout for desktop and mobile
- Loading states for all async operations
- Form validation and user feedback
- Modular component architecture for maintainability