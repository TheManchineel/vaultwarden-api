# vaultwarden-api: a simple read-only API for for Vaultwarden Server (WIP)

This project implements a bare-bones API to monitor the status of a [Vaultwarden](https://github.com/dani-garcia/vaultwarden) instance.

## Installation (Docker)

```sh
docker run \ 
    -e VAULTWARDEN_URL=https://vaultwarden.example.com \
    -e VAULTWARDEN_TOKEN=your_vaultwarden_token \
    -e API_KEY=some_api_key \
    -p 8019:8019 \
    --name vaultwarden-api \
    --restart unless-stopped \
    ghcr.io/themanchineel/vaultwarden-api:main
```

Where `VAULTWARDEN_URL` is the main URL of your Vaultwarden instance (web vault), `VAULTWARDEN_TOKEN` is the administrator token, and `API_KEY` is the API key you want to use to access the API. If `API_KEY` is not set, the API will be accessible without authentication *(not a good idea!)*.

## Usage

The API is accessible at `http://localhost:8019/api` (or the port you mapped it to). If `API_KEY` is set, the `X-API-Key` header must be set to the same value.

### Example

#### Request:
```sh
curl "http://localhost:8019/api/stats" \
    -H 'X-API-Key: test'
```

#### Response:

```json
{
  "user_count": 10,
  "organization_count": 3,
  "total_entries": 250,
  "total_attachments": 16,
  "total_attachment_size": 3423624
}
```

### Endpoints

| Method | Endpoint | Description                                       |
| ------ | -------- | ------------------------------------------------- |
| GET    | `/stats` | Returns statistics from the Vaultwarden instance. |

More endpoints will be added in the future