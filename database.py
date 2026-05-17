"""
MongoDB database operations for storing monitored links and settings.
"""
from datetime import datetime
from typing import Optional

from pymongo import MongoClient


class Database:
    def __init__(self, mongo_uri: str, db_name: str):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.links = self.db["links"]
        self.settings = self.db["settings"]
        self.counters = self.db["counters"]

        # Ensure unique index on url
        self.links.create_index("url", unique=True)
        self.settings.create_index("key", unique=True)

    def _next_id(self) -> int:
        """Auto-increment ID for links."""
        result = self.counters.find_one_and_update(
            {"_id": "link_id"},
            {"$inc": {"seq": 1}},
            upsert=True,
            return_document=True,
        )
        return result["seq"]

    def add_link(self, url: str, app_name: str = "Unknown App", status: str = "unknown") -> bool:
        """
        Add a new TestFlight link. Returns True if added, False if already exists.
        """
        try:
            self.links.insert_one({
                "id": self._next_id(),
                "url": url,
                "app_name": app_name,
                "status": status,
                "added_at": datetime.now().isoformat(),
                "last_checked": None,
                "last_status_change": None,
            })
            return True
        except Exception:
            # Duplicate url
            return False

    def remove_link(self, link_id: int) -> Optional[dict]:
        """
        Remove a link by ID. Returns the removed link info or None if not found.
        """
        doc = self.links.find_one_and_delete({"id": link_id})
        if doc:
            doc.pop("_id", None)
            return doc
        return None

    def get_all_links(self) -> list[dict]:
        """Get all monitored links."""
        docs = list(self.links.find({}, {"_id": 0}).sort("id", 1))
        return docs

    def get_link_count(self) -> int:
        """Get the total number of monitored links."""
        return self.links.count_documents({})

    def update_link_status(
        self, link_id: int, status: str, app_name: Optional[str] = None,
        status_changed: bool = False,
    ):
        """Update the status and last_checked time of a link.

        Args:
            status_changed: If True, also updates last_status_change timestamp.
        """
        now = datetime.now().isoformat()
        update = {
            "$set": {
                "status": status,
                "last_checked": now,
            }
        }

        if app_name:
            update["$set"]["app_name"] = app_name

        if status_changed:
            update["$set"]["last_status_change"] = now

        self.links.update_one({"id": link_id}, update)

    def update_link_checked(self, link_id: int):
        """Update only the last_checked timestamp."""
        self.links.update_one(
            {"id": link_id},
            {"$set": {"last_checked": datetime.now().isoformat()}},
        )

    def get_setting(self, key: str, default: str = "") -> str:
        """Get a setting value by key."""
        doc = self.settings.find_one({"key": key})
        return doc["value"] if doc else default

    def set_setting(self, key: str, value: str):
        """Set a setting value (upsert)."""
        self.settings.update_one(
            {"key": key},
            {"$set": {"key": key, "value": value}},
            upsert=True,
        )
