from typing import Any

import httpx

from app.config import settings
from app.utils.xml_mapper import XmlMapper


class SAPClient:
    def __init__(self) -> None:
        self.base_url = settings.sap_base_url.rstrip("/")
        self.auth = (
            (settings.sap_username, settings.sap_password)
            if settings.sap_username and settings.sap_password
            else None
        )
        self.timeout = settings.request_timeout_seconds

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{self.base_url}{endpoint}"

    async def call_soap(
        self,
        endpoint: str,
        payload: dict[str, Any],
        soap_action: str | None = None,
    ) -> tuple[int, dict[str, str], dict[str, Any], str]:
        xml_body = XmlMapper.dict_to_xml(payload)
        headers = {"Content-Type": "text/xml; charset=utf-8"}
        if soap_action:
            headers["SOAPAction"] = soap_action

        async with httpx.AsyncClient(timeout=self.timeout, auth=self.auth) as client:
            response = await client.post(self._build_url(endpoint), content=xml_body, headers=headers)
            response.raise_for_status()

        parsed_xml = XmlMapper.xml_to_dict(response.text)
        return response.status_code, dict(response.headers), parsed_xml, response.text

    async def get_odata_entities(
        self,
        entity_set: str,
        top: int | None = None,
        skip: int | None = None,
        filter_expr: str | None = None,
        select_expr: str | None = None,
    ) -> tuple[int, dict[str, Any]]:
        query_params: dict[str, Any] = {}
        if top is not None:
            query_params["$top"] = top
        if skip is not None:
            query_params["$skip"] = skip
        if filter_expr:
            query_params["$filter"] = filter_expr
        if select_expr:
            query_params["$select"] = select_expr

        endpoint = f"/sap/opu/odata/sap/{entity_set}"
        headers = {"Accept": "application/json"}

        async with httpx.AsyncClient(timeout=self.timeout, auth=self.auth, headers=headers) as client:
            response = await client.get(self._build_url(endpoint), params=query_params)
            response.raise_for_status()

        return response.status_code, response.json()
