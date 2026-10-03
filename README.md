# FreightIQ — Intelligent Logistics & Delivery Optimization Platform

FreightIQ is a full-stack logistics and delivery management platform designed as an academic/product engineering project. It combines shipment operations with machine-learning predictions and constraint-based route optimization.

## What this project demonstrates

- Full-stack development with React and Java Spring Boot
- MySQL-backed shipment, driver and vehicle management
- Role-based company and driver workflows
- Shipment posting, bidding, assignment and delivery status tracking
- Scikit-learn-based delivery-time/delay prediction
- XGBoost-based demand forecasting
- Google OR-Tools vehicle-routing optimization with vehicle capacity constraints
- Docker Compose for running the complete stack locally

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js, JavaScript, Tailwind CSS, React Router, Axios |
| Backend | Java 21, Spring Boot, Spring Data JPA, OpenFeign |
| Database | MySQL 8 |
| ML Service | Python, FastAPI, Scikit-learn, XGBoost, Pandas, NumPy |
| Optimization | Google OR-Tools |
| DevOps | Docker, Docker Compose |

## Repository Structure

```text
FreightIQ-main/
├── User_Service/          # Company, driver and vehicle management
├── ShipmentService/       # Shipments, bids, reviews and status workflow
├── ML_Service/            # ML predictions + OR-Tools optimization
├── freightIQ-frontend/    # React web application
├── docker-compose.yaml    # Complete local stack
├── .env.example           # Environment template
├── ARCHITECTURE.md        # System architecture
└── PRODUCT_ROADMAP.md     # Suggested product-level improvements
```

## Run the project locally

### Prerequisites

- Docker Desktop
- Git

### Start everything

```bash
git clone <your-github-repository-url>
cd FreightIQ-main
docker compose up --build
```

Open:

- Frontend: http://localhost:5173
- User Service: http://localhost:8080
- Shipment Service: http://localhost:8081
- ML Service / Swagger: http://localhost:8000/docs

### Stop

```bash
docker compose down
```

### Reset MySQL data

```bash
docker compose down -v
```

## ML and Optimization Endpoints

The Python service currently exposes:

- `POST /api/recommend` — existing driver suitability recommendation flow
- `POST /api/predict-delay` — delivery-time/delay prediction
- `POST /api/predict-demand` — demand forecasting
- `POST /api/optimize-route` — OR-Tools route optimization with vehicle capacities
- `GET /health` — service/model health check

The React application already contains API wrappers for the prediction and optimization endpoints. The next product step is to expose these capabilities through dedicated dashboard pages and connect them to realistic operational data.

## Current Product Areas

### Company

- Register/login
- Company profile
- Post shipments
- View shipments
- View shipment details
- Review driver bids
- Driver recommendation flow
- Accept bids
- Submit reviews

### Driver

- Register/login
- Driver profile
- Vehicle information
- Browse available shipments
- Place bids
- View submitted bids
- Track ongoing shipments
- Update delivery progress

## Important Development Note

This repository is a development base for a larger portfolio project. Do not claim a feature on your resume until you have implemented and tested it end-to-end. In particular, the current ML/optimization service contains the backend capabilities, while the frontend still needs additional dashboard screens to present all of them as a polished logistics product.

## Suggested next milestone

Build an Operations Dashboard with:

1. KPI cards — total orders, active deliveries, completed deliveries, delayed deliveries
2. Orders table with filters and status chips
3. Driver & vehicle management
4. Delivery delay prediction screen
5. Demand forecasting charts
6. OR-Tools route optimization screen
7. Alerts and exception management
8. Analytics and reports
9. Better navigation/sidebar and responsive UI
10. Demo data and loading/error/empty states

See `PRODUCT_ROADMAP.md` for the suggested implementation sequence.
