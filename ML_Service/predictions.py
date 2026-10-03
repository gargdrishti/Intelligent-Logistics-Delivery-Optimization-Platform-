"""Lightweight, reproducible ML prediction utilities for delivery analytics."""
from typing import Any, Dict, List
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, accuracy_score
from xgboost import XGBRegressor


def _records(data: List[Dict[str, Any]]):
    if not data or len(data)<6:
        raise ValueError("Provide at least 6 historical records")
    X=[]; y_delay=[]; y_demand=[]
    for r in data:
        X.append([float(r.get("distanceKm",0)), float(r.get("weightKg",0)), float(r.get("trafficIndex",0.5)), float(r.get("priority",1)), float(r.get("driverExperienceYears",0)), float(r.get("vehicleAgeYears",0))])
        y_delay.append(float(r.get("deliveryHours",0)))
        y_demand.append(float(r.get("demand",0)))
    return np.asarray(X), np.asarray(y_delay), np.asarray(y_demand)


def predict_delay(data: List[Dict[str,Any]], sample: Dict[str,Any]):
    X,y,_=_records(data)
    model=RandomForestRegressor(n_estimators=150,random_state=42)
    model.fit(X,y)
    sx=np.asarray([[float(sample.get("distanceKm",0)),float(sample.get("weightKg",0)),float(sample.get("trafficIndex",0.5)),float(sample.get("priority",1)),float(sample.get("driverExperienceYears",0)),float(sample.get("vehicleAgeYears",0))]])
    pred=float(model.predict(sx)[0])
    return {"predictedDeliveryHours":round(pred,2),"model":"Scikit-learn RandomForestRegressor"}


def predict_demand(data: List[Dict[str,Any]], horizon: int=7):
    X,_,y=_records(data)
    model=XGBRegressor(n_estimators=120,max_depth=4,learning_rate=0.06,subsample=.9,colsample_bytree=.9,objective="reg:squarederror",random_state=42)
    model.fit(X,y)
    base=float(np.mean(X[-min(7,len(X)):,0])) if len(X) else 0
    future=[]
    # Reuse representative operational features while varying distance slightly by horizon.
    for d in range(1,horizon+1):
        row=X[-1].copy(); row[0]=base + d*0.01
        future.append(max(0,float(model.predict(np.asarray([row]))[0])))
    return {"forecast":[round(x,2) for x in future],"model":"XGBoost","horizonDays":horizon}
