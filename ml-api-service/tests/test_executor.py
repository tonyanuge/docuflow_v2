from workflow.executor import WorkflowExecutor


def test_queue_decision_drives_queue_action():
    """
    rules.yaml decisions carry `queue`/`priority`, not `action`. The executor
    must treat a `queue` decision as a "queue" action (not silently fall
    back to log-only) and reflect the queue/priority in the result.
    """
    executor = WorkflowExecutor()

    result = executor.execute(
        decision={"queue": "finance_ops", "priority": "high"},
        context={"query": "chase this payment"},
    )

    assert result["action"] == "queue"
    assert result["status"] == "completed"
    assert result["queue"] == "finance_ops"
    assert result["priority"] == "high"
    assert "finance_ops" in result["message"]


def test_decision_with_no_queue_or_action_falls_back_to_log():
    executor = WorkflowExecutor()

    result = executor.execute(decision={}, context={"query": "n/a"})

    assert result["action"] == "log"
    assert result["status"] == "completed"


def test_explicit_action_overrides_queue_inference():
    executor = WorkflowExecutor()

    result = executor.execute(
        decision={"action": "tag", "queue": "finance_ops"},
        context={"query": "n/a"},
    )

    assert result["action"] == "tag"
    assert result["status"] == "completed"
