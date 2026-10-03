import joblib, logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from Shemas import RecommendRequest, RecommendResponse, DriverRecommendation
from Clients import fetch_shipment_and_bids, fetch_all_drivers_and_vehicles
from feature import build_feature_matrix
from optimization import optimize_routes
from predictions import predict_delay, predict_demand

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log=logging.getLogger(__name__)
ml={"model":None,"features":None,"roc_auc":None}
@asynccontextmanager
async def lifespan(app):
    try:
        data=joblib.load("model.pkl"); ml.update(model=data["model"],features=data["features"],roc_auc=data["roc_auc"])
        log.info("Driver recommendation model loaded")
    except Exception as e: log.warning("Existing recommendation model unavailable: %s",e)
    yield
app=FastAPI(title="Intelligent Logistics ML & Optimization Service",version="2.0.0",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

@app.get("/health")
async def health(): return {"status":"ok","model_loaded":ml["model"] is not None,"features":ml["features"]}

@app.post("/api/recommend",response_model=RecommendResponse)
async def recommend(request:RecommendRequest):
    if ml["model"] is None: raise HTTPException(503,"Driver recommendation model not loaded")
    try: shipment,bids=await fetch_shipment_and_bids(request.shipmentId)
    except Exception as e: raise HTTPException(502,f"Could not reach Shipment Service: {e}")
    if not bids: raise HTTPException(404,f"No pending bids found for shipment {request.shipmentId}")
    driver_ids=list({b.driverId for b in bids})
    try: results=await fetch_all_drivers_and_vehicles(driver_ids)
    except Exception as e: raise HTTPException(502,f"Could not reach User Service: {e}")
    mp={i:(d,v) for i,d,v in results}
    matrix,ids=build_feature_matrix(bids,mp,shipment,ml["features"])
    if matrix.empty: raise HTTPException(422,"Could not build driver features")
    scores=ml["model"].predict_proba(matrix)[:,1]
    scored=sorted(zip(ids,scores),key=lambda x:x[1],reverse=True)[:3]
    return RecommendResponse(shipmentId=request.shipmentId,recommendations=[DriverRecommendation(driverId=i,score=round(float(s*100),1),rank=r) for r,(i,s) in enumerate(scored,1)],totalBidsEvaluated=len(ids))

class RouteRequest(BaseModel):
    locations: List[dict]
    vehicles: List[dict]
    depot: int=0
    distanceMatrix: List[List[int]]|None=None
    timeLimitSeconds: int=2
@app.post("/api/optimize-route")
async def optimize_route(req:RouteRequest):
    try: return optimize_routes(req.model_dump())
    except Exception as e: raise HTTPException(400,str(e))

class PredictionRequest(BaseModel):
    history: List[dict]=Field(min_length=6)
    sample: dict={}
@app.post("/api/predict-delay")
async def delay(req:PredictionRequest):
    try:return predict_delay(req.history,req.sample)
    except Exception as e:raise HTTPException(400,str(e))

class DemandRequest(BaseModel):
    history: List[dict]=Field(min_length=6)
    horizonDays: int=7
@app.post("/api/predict-demand")
async def demand(req:DemandRequest):
    try:return predict_demand(req.history,req.horizonDays)
    except Exception as e:raise HTTPException(400,str(e))
