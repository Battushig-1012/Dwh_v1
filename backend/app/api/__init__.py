from fastapi import APIRouter

from . import (
    auth,
    bcbs,
    dictionary,
    dpm,
    dq,
    export,
    governance,
    ict,
    lineage,
    ops_report_catalog,
    rdarr,
    srep,
)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(srep.router, prefix="/srep", tags=["srep"])
api_router.include_router(lineage.router, prefix="/lineage", tags=["lineage"])
api_router.include_router(dictionary.router, prefix="/dictionary", tags=["dictionary"])
api_router.include_router(dq.router, prefix="/dq", tags=["data-quality"])
api_router.include_router(export.router, prefix="/export", tags=["export"])
api_router.include_router(rdarr.router, prefix="/rdarr", tags=["rdarr-ssm"])
api_router.include_router(bcbs.router, prefix="/bcbs", tags=["bcbs-239"])
api_router.include_router(ict.router, prefix="/ict", tags=["eba-ict-security"])
api_router.include_router(dpm.router, prefix="/dpm", tags=["eba-dpm"])
api_router.include_router(governance.router, prefix="/governance", tags=["eba-internal-governance"])
# Catalog for many small/source reports — do not add one nav item per report
api_router.include_router(ops_report_catalog.router, prefix="/ops-reports", tags=["ops-reports"])
