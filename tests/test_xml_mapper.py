from app.utils.xml_mapper import XmlMapper


def test_dict_to_xml_and_back() -> None:
    payload = {
        "soapenv:Envelope": {
            "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            "soapenv:Header": None,
            "soapenv:Body": {
                "n0:ZGetCustomer": {
                    "@xmlns:n0": "urn:sap-com:document:sap:rfc:functions",
                    "CustomerId": "1000",
                }
            },
        }
    }

    xml_data = XmlMapper.dict_to_xml(payload)
    parsed = XmlMapper.xml_to_dict(xml_data)

    assert parsed["soapenv:Envelope"]["soapenv:Body"]["n0:ZGetCustomer"]["CustomerId"] == "1000"
