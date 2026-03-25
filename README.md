# SAP Integration API (Python)

API base (muy simple) para equipos junior que necesitan:

1. **Enviar información a SAP con SOAP**.
2. **Obtener información desde SAP con OData**.
3. **Mapear XML de request y response de forma sencilla** usando `dict <-> xml`.

## Stack

- FastAPI
- httpx
- xmltodict
- pydantic

## Estructura

```txt
app/
  clients/
    sap_client.py
  utils/
    xml_mapper.py
  config.py
  models.py
  main.py
tests/
  test_xml_mapper.py
```

## Configuración

Crea un archivo `.env` basado en este ejemplo:

```env
SAP_BASE_URL=https://tu-servidor-sap.example.com
SAP_USERNAME=mi_usuario
SAP_PASSWORD=mi_password
REQUEST_TIMEOUT_SECONDS=30
```

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar API

```bash
uvicorn app.main:app --reload
```

Documentación Swagger:

- <http://127.0.0.1:8000/docs>

---

## Endpoint 1: SOAP

`POST /sap/soap/call`

Ejemplo de body:

```json
{
  "endpoint": "/sap/bc/srt/scs_ext/mi_servicio",
  "soap_action": "urn:ZGetCustomer",
  "payload": {
    "soapenv:Envelope": {
      "@xmlns:soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
      "soapenv:Header": null,
      "soapenv:Body": {
        "n0:ZGetCustomer": {
          "@xmlns:n0": "urn:sap-com:document:sap:rfc:functions",
          "CustomerId": "1000"
        }
      }
    }
  }
}
```

Respuesta:

- `status_code`
- `headers`
- `parsed_xml` (XML ya mapeado a dict)
- `raw_xml` (respuesta original)

---

## Endpoint 2: OData

`GET /sap/odata/{entity_set}`

Ejemplo:

```bash
curl "http://127.0.0.1:8000/sap/odata/ZCUSTOMER_SRV?
$top=10&$filter=Country eq 'MX'&$select=CustomerId,Name"
```

> `entity_set` se concatena a `/sap/opu/odata/sap/{entity_set}`.

---

## XML Mapper simple

En `app/utils/xml_mapper.py`:

- `dict_to_xml(payload)` transforma un `dict` a XML.
- `xml_to_dict(xml_content)` transforma XML a `dict`.

Esto permite construir y leer SOAP sin pelearse con clases XML complejas.

## Tests

```bash
pytest
```

