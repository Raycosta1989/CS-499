from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from typing import Dict, Any, Optional, List


class ValidationError(Exception):
    """Custom exception for schema validation errors."""
    pass


class AnimalSchema:
    """Lightweight schema validator for AAC animal documents."""

    REQUIRED_FIELDS = {"name", "animal_type", "breed", "age_upon_outcome", "outcome_type"}

    @staticmethod
    def validate(document: Dict[str, Any]) -> None:
        if not isinstance(document, dict):
            raise ValidationError("Document must be a dictionary.")

        missing = AnimalSchema.REQUIRED_FIELDS - document.keys()
        if missing:
            raise ValidationError(f"Missing required fields: {missing}")


class MongoConfig:
    """Configuration object for MongoDB connection."""

    def __init__(self,
                 host: str = "nv-desktop-services.apporto.com",
                 port: int = 30273,
                 db: str = "AAC",
                 collection: str = "animals"):
        self.host = host
        self.port = port
        self.db = db
        self.collection = collection


class AnimalShelter:
    """Secure, validated CRUD operations for the AAC MongoDB collection."""

    def __init__(self, username: str, password: str, config: MongoConfig = MongoConfig()):
        try:
            uri = f"mongodb://{username}:{password}@{config.host}:{config.port}"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            self.database = self.client[config.db]
            self.collection = self.database[config.collection]

            # Test connection
            self.client.server_info()

        except errors.ServerSelectionTimeoutError:
            raise ConnectionError("Failed to connect to MongoDB server.")
        except Exception as e:
            raise ConnectionError(f"Unexpected error during connection: {e}")

    # -----------------------------
    # CREATE
    # -----------------------------
    def create(self, data: Dict[str, Any]) -> bool:
        if not data:
            raise ValueError("Data cannot be empty.")

        try:
            AnimalSchema.validate(data)
            self.collection.insert_one(data)
            return True
        except ValidationError as ve:
            print(f"Validation error: {ve}")
            return False
        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    # -----------------------------
    # READ
    # -----------------------------
    def read(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        try:
            criteria = criteria or {}
            results = list(self.collection.find(criteria, {"_id": False}))
            return results
        except Exception as e:
            print(f"Read failed: {e}")
            return []

    # -----------------------------
    # UPDATE
    # -----------------------------
    def update(self, filter_criteria: Dict[str, Any], update_values: Dict[str, Any]) -> int:
        if not filter_criteria or not update_values:
            raise ValueError("Filter criteria and update values cannot be empty.")

        try:
            result = self.collection.update_many(filter_criteria, {"$set": update_values})
            return result.modified_count
        except Exception as e:
            print(f"Update failed: {e}")
            return 0

    # -----------------------------
    # DELETE
    # -----------------------------
    def delete(self, delete_criteria: Dict[str, Any]) -> int:
        if not delete_criteria:
            raise ValueError("Delete criteria cannot be empty.")

        try:
            result = self.collection.delete_many(delete_criteria)
            return result.deleted_count
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0
