# FreightIQ Architecture

## Application flow

React.js frontend -> Spring Boot services -> MySQL
                              |
                              +-> Python ML service
                                      |- Scikit-learn: delivery-time prediction
                                      |- XGBoost: demand forecasting
                                      |- OR-Tools: capacity-constrained route optimization

## Spring Boot

- User Service: companies, drivers and vehicles.
- Shipment Service: shipments, bids, reviews and status workflow.
- Both services use MySQL through Spring Data JPA.

## Python ML service

- `/api/recommend`: existing driver suitability ranking.
- `/api/predict-delay`: Scikit-learn delivery-time prediction.
- `/api/predict-demand`: XGBoost demand forecasting.
- `/api/optimize-route`: Google OR-Tools vehicle routing with vehicle capacities.

## Database migration

The project has been changed from PostgreSQL to MySQL. Set `DB_URL`, `DB_USERNAME`, and `DB_PASSWORD` in `.env` when running without Docker.
