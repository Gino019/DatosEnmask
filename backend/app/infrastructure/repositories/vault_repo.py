from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from app.domain.interfaces.vault_repository import VaultRepository

class MemoryVaultRepository(VaultRepository):
    def __init__(self):
        # job_id -> list of backup records
        self._data: Dict[str, List[Dict[str, Any]]] = {}

    async def save_backup(self, job_id: str, table_name: str, record_pk: str, original_data: Dict[str, Any]) -> None:
        if job_id not in self._data:
            self._data[job_id] = []
        
        self._data[job_id].append({
            "job_id": job_id,
            "table_name": table_name,
            "record_pk": record_pk,
            "original_data": original_data
        })

    async def get_backups_for_job(self, job_id: str) -> List[Dict[str, Any]]:
        return self._data.get(job_id, [])

    async def delete_backups_for_job(self, job_id: str) -> None:
        if job_id in self._data:
            del self._data[job_id]

    # --- MÉTODOS ABSTRACTOS OBLIGATORIOS (SANGRE DE 4 ESPACIOS) ---
    async def bulk_delete_backups(self, *args, **kwargs):
        pass

    async def bulk_save_backups(self, *args, **kwargs):
        pass

    async def decrypt_value(self, *args, **kwargs):
        return ""

    async def encrypt_value(self, *args, **kwargs):
        return ""

    async def purge_expired(self, *args, **kwargs):
        pass

    async def set_retention_policy(self, *args, **kwargs):
        pass


class MongoVaultRepository(VaultRepository):
    def __init__(self, uri: str, database_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database_name]
        self.collection = self.db["vault_backups"]

    async def save_backup(self, job_id: str, table_name: str, record_pk: str, original_data: Dict[str, Any]) -> None:
        doc = {
            "job_id": job_id,
            "table_name": table_name,
            "record_pk": record_pk,
            "original_data": original_data
        }
        await self.collection.insert_one(doc)

    async def get_backups_for_job(self, job_id: str) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"job_id": job_id})
        results = []
        async for document in cursor:
            if "_id" in document:
                del document["_id"]
            results.append(document)
        return results

    async def delete_backups_for_job(self, job_id: str) -> None:
        await self.collection.delete_many({"job_id": job_id})

    # --- TAMBIÉN SE LOS AGREGAMOS AQUÍ PARA EVITAR ERRORES EN PRODUCCIÓN ---
    async def bulk_delete_backups(self, *args, **kwargs):
        pass

    async def bulk_save_backups(self, *args, **kwargs):
        pass

    async def decrypt_value(self, *args, **kwargs):
        return ""

    async def encrypt_value(self, *args, **kwargs):
        return ""

    async def purge_expired(self, *args, **kwargs):
        pass

    async def set_retention_policy(self, *args, **kwargs):
        pass


# Initialize memory fallback instance (Al final de todo)
memory_vault_repository = MemoryVaultRepository()