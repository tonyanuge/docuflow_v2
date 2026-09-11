# workflow/executor.py

from audit.logger import AuditLogger

class WorkflowExecutor:
    def __init__(self):
        self.logger = AuditLogger()

    def execute(self, *, decision: dict, context: dict) -> dict:
        """
        Execute a routing decision (simulated — no external side effects).
        Returns execution result.

        rules.yaml decisions carry `queue` / `priority` rather than an
        explicit `action`. If a rule does specify `action` directly, that
        takes precedence; otherwise a `queue` decision is treated as the
        "queue" action so the routing outcome actually drives simulated
        execution instead of silently falling back to log-only.
        """

        if "action" in decision:
            action = decision["action"]
        elif "queue" in decision:
            action = "queue"
        else:
            action = "log"

        result = {
            "action": action,
            "status": "completed"
        }

        # ---- Supported actions (simulated, no external side effects) ----

        if action == "queue":
            queue_name = decision.get("queue", "unspecified")
            priority = decision.get("priority", "normal")
            result["message"] = (
                f"Item queued to '{queue_name}' (priority: {priority})"
            )
            result["queue"] = queue_name
            result["priority"] = priority

        elif action == "tag":
            result["message"] = "Metadata tag applied"

        elif action == "log":
            result["message"] = "Logged only (no side effects)"

        elif action == "webhook":
            result["message"] = "Webhook execution placeholder"

        else:
            result["status"] = "ignored"
            result["message"] = f"Unknown action: {action}"

        # ---- Audit everything ----
        self.logger.log(
            event="workflow_execution",
            payload={
                "decision": decision,
                "context": context,
                "result": result
            }
        )

        return result
