# FreightIQ — Product Roadmap

This file is intentionally practical: use it as the checklist for turning the current academic base into a polished portfolio-grade logistics product.

## Phase 1 — Operations Dashboard

- [ ] Add `/dashboard` route
- [ ] KPI cards: total orders, active deliveries, completed deliveries, delayed deliveries
- [ ] Delivery status distribution chart
- [ ] Orders trend chart
- [ ] Recent shipments table
- [ ] At-risk deliveries panel
- [ ] Loading, empty and error states

## Phase 2 — Shipment Operations

- [ ] Advanced search by shipment ID, origin and destination
- [ ] Filters for status, priority, cargo type and date
- [ ] Shipment timeline
- [ ] Assignment status
- [ ] Delivery ETA card
- [ ] Delay-risk badge
- [ ] Export shipment data to CSV

## Phase 3 — ML Features

- [ ] Dedicated delivery delay prediction page
- [ ] Form for distance, vehicle type, cargo type, driver experience, weather and historical features
- [ ] Show predicted delivery time
- [ ] Show delay probability/risk
- [ ] Dedicated demand forecast page
- [ ] Historical vs forecast chart
- [ ] 7/14/30-day forecast selection
- [ ] Explain the important operational factors used by the model

## Phase 4 — Route Optimization

- [ ] Dedicated route optimization page
- [ ] Add depot and delivery stops
- [ ] Add vehicle capacities
- [ ] Run OR-Tools optimization
- [ ] Display optimized vehicle routes
- [ ] Display distance and capacity utilization
- [ ] Add a map visualization later using a real mapping provider

## Phase 5 — Alerts & Exceptions

- [ ] Delayed delivery alerts
- [ ] Capacity exceeded alerts
- [ ] Unassigned shipment alerts
- [ ] High-risk delivery queue
- [ ] Alert acknowledgement state

## Phase 6 — Product Polish

- [ ] Professional sidebar navigation
- [ ] Responsive mobile/tablet layout
- [ ] Consistent empty/loading/error components
- [ ] Toast notifications
- [ ] Form validation
- [ ] Confirmation dialogs for destructive actions
- [ ] Better authentication/session handling
- [ ] Profile settings
- [ ] Activity/audit timeline

## Phase 7 — Portfolio Quality

- [ ] Add realistic demo seed data
- [ ] Add screenshots to README
- [ ] Add architecture diagram
- [ ] Add API documentation
- [ ] Add test coverage for important backend logic
- [ ] Add frontend component tests
- [ ] Add CI workflow for build/lint/test
- [ ] Deploy frontend and backend
- [ ] Add a public demo link

## Recommended Demo Flow

1. Login as a company
2. Open dashboard
3. Create a shipment
4. View available bids
5. Run driver recommendation
6. Open delay prediction
7. Run demand forecast
8. Open route optimizer
9. Assign a driver
10. Move shipment through delivery statuses
11. Show analytics/reporting

This sequence gives an interviewer a clear story: **operations → prediction → optimization → execution → analytics**.
