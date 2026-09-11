from workflow.router import WorkflowRouter


def test_route_matches_by_classification():
    router = WorkflowRouter()

    decision = router.route(
        classification="payment_request",
        text="please chase this arrears payment",
    )

    assert decision == {"queue": "finance_ops", "priority": "high"}


def test_route_matches_by_keyword():
    router = WorkflowRouter()

    decision = router.route(
        classification="general",
        text="please review the attached contract",
    )

    assert decision == {"queue": "legal_review", "priority": "normal"}


def test_route_falls_back_to_default_route():
    router = WorkflowRouter()

    decision = router.route(
        classification="general",
        text="just checking in, no action needed",
    )

    assert decision == {"queue": "general_review", "priority": "normal"}
