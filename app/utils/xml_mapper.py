from typing import Any

import xmltodict


class XmlMapper:
    """Mapeo XML <-> dict simple para request/response SOAP."""

    @staticmethod
    def dict_to_xml(payload: dict[str, Any]) -> str:
        return xmltodict.unparse(payload, full_document=True, pretty=True)

    @staticmethod
    def xml_to_dict(xml_content: str) -> dict[str, Any]:
        parsed = xmltodict.parse(xml_content)
        if not isinstance(parsed, dict):
            return {"value": parsed}
        return parsed
