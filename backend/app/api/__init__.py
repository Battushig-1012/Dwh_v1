from fastapi import APIRouter

from . import auth, bcbs, dictionary, dq, export, lineage, rdarr, srep

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(srep.router, prefix="/srep", tags=["srep"])
api_router.include_router(lineage.router, prefix="/lineage", tags=["lineage"])
api_router.include_router(dictionary.router, prefix="/dictionary", tags=["dictionary"])
api_router.include_router(dq.router, prefix="/dq", tags=["data-quality"])
api_router.include_router(export.router, prefix="/export", tags=["export"])
api_router.include_router(rdarr.router, prefix="/rdarr", tags=["rdarr-ssm"])
api_router.include_router(bcbs.router, prefix="/bcbs", tags=["bcbs-239"])
