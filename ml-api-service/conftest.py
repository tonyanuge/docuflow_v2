import os
import sys
import tempfile
from pathlib import Path

# The application modules (workflow, security, audit, app, ...) use absolute
# imports written for running from inside ml-api-service/ (e.g. as the
# Dockerfile/uvicorn WORKDIR). Make that importable regardless of the
# directory pytest is invoked from.
THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

# audit/logger.py creates its log directory as a side effect of import.
# Redirect it to a throwaway temp directory so running the test suite never
# writes into (or depends on) the real audit_logs/ directory.
os.environ.setdefault("DOCUFLOW_AUDIT_LOG_DIR", tempfile.mkdtemp(prefix="docuflow_test_audit_"))
