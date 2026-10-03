"""Vehicle routing and driver assignment using Google OR-Tools."""
from typing import Any, Dict, List
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


def optimize_routes(request: Dict[str, Any]) -> Dict[str, Any]:
    locations = request.get("locations", [])
    vehicles = request.get("vehicles", [])
    depot = int(request.get("depot", 0))
    if len(locations) < 2 or not vehicles:
        raise ValueError("At least one depot, one delivery and one vehicle are required")
    distance_matrix = request.get("distanceMatrix")
    if not distance_matrix:
        # Manhattan-like fallback distance from x/y coordinates; replace with road distances in production.
        distance_matrix = []
        for a in locations:
            row=[]
            for b in locations:
                row.append(int(round((abs(a.get('lat',0)-b.get('lat',0))+abs(a.get('lng',0)-b.get('lng',0)))*1000)))
            distance_matrix.append(row)
    demands=[int(x.get("demand",0)) for x in locations]
    capacities=[int(v.get("capacity", 10**9)) for v in vehicles]
    manager=pywrapcp.RoutingIndexManager(len(distance_matrix), len(vehicles), depot)
    routing=pywrapcp.RoutingModel(manager)
    def dist_cb(i,j):
        return int(distance_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)])
    transit=routing.RegisterTransitCallback(dist_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)
    def demand_cb(i): return demands[manager.IndexToNode(i)]
    demand_idx=routing.RegisterUnaryTransitCallback(demand_cb)
    routing.AddDimensionWithVehicleCapacity(demand_idx,0,capacities,True,"Capacity")
    params=pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy=routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    params.local_search_metaheuristic=routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    params.time_limit.seconds=int(request.get("timeLimitSeconds",2))
    solution=routing.SolveWithParameters(params)
    if not solution:
        return {"status":"NO_SOLUTION","routes":[],"totalDistance":None}
    routes=[]; total=0
    for vehicle_id,v in enumerate(vehicles):
        idx=routing.Start(vehicle_id); stops=[]; route_dist=0; load=0
        while not routing.IsEnd(idx):
            node=manager.IndexToNode(idx); stops.append(locations[node].get("id",node)); load+=demands[node]
            nxt=solution.Value(routing.NextVar(idx)); route_dist+=routing.GetArcCostForVehicle(idx,nxt,vehicle_id); idx=nxt
        stops.append(locations[manager.IndexToNode(idx)].get("id",manager.IndexToNode(idx)))
        if len(stops)>2:
            routes.append({"vehicleId":v.get("id",vehicle_id),"stops":stops,"distance":route_dist,"load":load,"capacity":capacities[vehicle_id]})
            total+=route_dist
    return {"status":"OPTIMIZED","routes":routes,"totalDistance":total,"vehiclesUsed":len(routes)}
