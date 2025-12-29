from fastapi import FastAPI
# 1. Import the routers from your new DDD paths
from app.Domain.v1.Scan.route_scan import router as scan_router
from app.Domain.v1.Staff.route_staff import router as staff_router 
from app.Shared.Infra.reverse_proxy import proxy_handler, proxy_handler_staff

app = FastAPI(title="API Gateway (DDD)")

# 2. Include the routers correctly
app.include_router(scan_router)
app.include_router(staff_router)

@app.get("/")
async def health_check():
    return {"status": "Gateway is Healthy", "version": "v1-ddd"}

@app.on_event("shutdown")
async def shutdown_event():
    await proxy_handler.close()
    await proxy_handler_staff.close()