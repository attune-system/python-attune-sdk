from enum import Enum


class RbacResource(str, Enum):
    ACTIONS = "actions"
    ARTIFACTS = "artifacts"
    AUDIT_LOG = "audit_log"
    CACHES = "caches"
    DASHBOARDS = "dashboards"
    ENFORCEMENTS = "enforcements"
    EVENTS = "events"
    EXECUTIONS = "executions"
    IDENTITIES = "identities"
    INQUIRIES = "inquiries"
    KEYS = "keys"
    PACKS = "packs"
    PERMISSIONS = "permissions"
    POLICIES = "policies"
    QUEUES = "queues"
    QUEUE_ITEMS = "queue_items"
    RETENTION = "retention"
    RULES = "rules"
    RUNTIMES = "runtimes"
    TRIGGERS = "triggers"
    WORKERS = "workers"

    def __str__(self) -> str:
        return str(self.value)
