import pytest

from security.guard import enforce_permission, PermissionDenied
from security.roles import Role, Capability


def test_operator_can_execute_workflow():
    # Should not raise — operator is granted execute_workflow in permissions.yaml.
    enforce_permission(role=Role.OPERATOR, capability=Capability.EXECUTE_WORKFLOW)


def test_viewer_cannot_execute_workflow():
    with pytest.raises(PermissionDenied):
        enforce_permission(role=Role.VIEWER, capability=Capability.EXECUTE_WORKFLOW)


def test_viewer_can_view_search_results():
    # Should not raise — every role is granted view_search_results.
    enforce_permission(role=Role.VIEWER, capability=Capability.VIEW_SEARCH_RESULTS)


def test_operator_cannot_manage_rules():
    with pytest.raises(PermissionDenied):
        enforce_permission(role=Role.OPERATOR, capability=Capability.MANAGE_RULES)
