from fastapi import FastAPI, HTTPException, Query
from httpx import HTTPStatusError

from app.clients.sap_client import SAPClient
from app.models import ODataResponse, SoapCallRequest, SoapCallResponse

app = FastAPI(
    title="SAP Integration API (SOAP + OData)",
    description="API base para equipos junior: envío SOAP y lectura OData hacia SAP.",
    version="1.0.0",
)

sap_client = SAPClient()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/sap/soap/call", response_model=SoapCallResponse)
async def sap_soap_call(request: SoapCallRequest) -> SoapCallResponse:
    try:
        status_code, headers, parsed_xml, raw_xml = await sap_client.call_soap(
            endpoint=request.endpoint,
            payload=request.payload,
            soap_action=request.soap_action,
        )
        return SoapCallResponse(
            status_code=status_code,
            headers=headers,
            parsed_xml=parsed_xml,
            raw_xml=raw_xml,
        )
    except HTTPStatusError as exc:
        detail = {
            "message": "Error HTTP al consumir servicio SOAP SAP.",
            "status_code": exc.response.status_code,
            "response": exc.response.text,
        }
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc


@app.get("/sap/odata/{entity_set}", response_model=ODataResponse)
async def sap_odata_get(
    entity_set: str,
    top: int | None = Query(default=None, ge=1, le=5000),
    skip: int | None = Query(default=None, ge=0),
    filter_expr: str | None = Query(default=None, alias="$filter"),
    select_expr: str | None = Query(default=None, alias="$select"),
) -> ODataResponse:
    try:
        status_code, data = await sap_client.get_odata_entities(
            entity_set=entity_set,
            top=top,
            skip=skip,
            filter_expr=filter_expr,
            select_expr=select_expr,
        )
        return ODataResponse(status_code=status_code, data=data)
    except HTTPStatusError as exc:
        detail = {
            "message": "Error HTTP al consumir endpoint OData SAP.",
            "status_code": exc.response.status_code,
            "response": exc.response.text,
        }
        raise HTTPException(status_code=exc.response.status_code, detail=detail) from exc
