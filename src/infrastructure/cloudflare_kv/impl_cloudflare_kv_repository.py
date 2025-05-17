from ...domain.db.repository.nosql_repository import NoSqlRepository
from typing import Any, List, Optional, Dict
import httpx
import json

class CloudflareKvRepository(NoSqlRepository):
    """Cloudflare KV implementation of the NoSqlRepository abstract class."""

    def __init__(self, account_id: str, namespace_id: str, api_token: str):
        self.account_id = account_id
        self.namespace_id = namespace_id
        self.api_token = api_token
        self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/storage/kv/namespaces/{self.namespace_id}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.client = httpx.AsyncClient()

    async def create(self, key: str, value: Any) -> None:
        """Concrete method for creating data (key-value pair) in Cloudflare KV."""
        url = f"{self.base_url}/values/{key}"
        # Cloudflare KV stores values as strings, so we need to serialize complex types
        if not isinstance(value, (str, bytes)):
            value = json.dumps(value)
        await self.client.put(url, headers=self.headers, content=value)

    async def read_single(self, key: str) -> Optional[Any]:
        """Concrete method for reading a single value by key from Cloudflare KV."""
        url = f"{self.base_url}/values/{key}"
        response = await self.client.get(url, headers=self.headers)
        if response.status_code == 200:
            try:
                # Attempt to deserialize if it looks like JSON
                return json.loads(response.text)
            except json.JSONDecodeError:
                return response.text
        return None

    async def read_list(self, prefix: str) -> List[Dict[str, Any]]:
        """Concrete method for reading a list of values by prefix from Cloudflare KV."""
        url = f"{self.base_url}/keys"
        params = {"prefix": prefix}
        response = await self.client.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            keys_data = response.json()
            results = []
            # Cloudflare KV list endpoint only returns keys, not values.
            # To get values, we need to fetch each key individually.
            for item in keys_data.get('result', []):
                key = item['name']
                value = await self.read_single(key)
                if value is not None:
                    results.append({"key": key, "value": value})
            return results
        return []

    async def delete(self, key: str) -> None:
        """Concrete method for deleting data by key from Cloudflare KV."""
        url = f"{self.base_url}/values/{key}"
        await self.client.delete(url, headers=self.headers)
