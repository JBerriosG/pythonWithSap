from typing import Any

from pydantic import BaseModel, Field


class SoapCallRequest(BaseModel):
    endpoint: str = Field(
        ...,
        description="Ruta relativa o absoluta del servicio SOAP en SAP.",
        examples=["/sap/bc/srt/scs_ext/some_service"],
    )
    soap_action: str | None = Field(
        default=None,
        description="Header SOAPAction, opcional dependiendo del servicio SAP.",
    )
    payload: dict[str, Any] = Field(
        ...,
        description="Diccionario que representa el XML SOAP Envelope completo.",
    )


class SoapCallResponse(BaseModel):
    status_code: int
    headers: dict[str, str]
    parsed_xml: dict[str, Any]
    raw_xml: str


class ODataQueryParams(BaseModel):
    top: int | None = Field(default=None, ge=1, le=5000)
    skip: int | None = Field(default=None, ge=0)
    filter: str | None = Field(default=None, alias="$filter")
    select: str | None = Field(default=None, alias="$select")


class ODataResponse(BaseModel):
    status_code: int
    data: dict[str, Any]
