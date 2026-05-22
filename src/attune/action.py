"""
Action runner — handles stdin parameter parsing, output formatting, and error handling.

Usage::

    import attune

    def main(name: str, count: int = 1):
        return {"message": f"Hello, {name}!" * count}

    attune.run_action(main)

The entrypoint function declares whatever parameters it needs — they are
passed as keyword arguments from the parsed stdin JSON. Parameters not
declared by the function are silently ignored (via ``**kwargs`` or filtering).

Exit codes:
- 0: success (result is written to stdout as JSON)
- 1: failure (error details written to stdout as JSON with ``success: false``)
"""

from __future__ import annotations

import json
import sys
import traceback
from typing import Any, Callable


def read_params() -> dict[str, Any]:
    """Read action parameters from stdin (JSON format).

    The Attune worker delivers parameters as a single JSON object on stdin.
    """
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    return json.loads(raw)


def emit_result(payload: Any) -> None:
    """Write a JSON result to stdout."""
    print(json.dumps(payload, default=str))


def emit_error(message: str, *, details: Any | None = None) -> None:
    """Write a JSON error to stdout."""
    payload: dict[str, Any] = {"success": False, "error": message}
    if details is not None:
        payload["details"] = details
    print(json.dumps(payload, default=str))


def run_action(
    entrypoint: Callable[..., Any],
    *,
    catch_exceptions: bool = True,
) -> None:
    """Run an action entrypoint with automatic parameter parsing and output handling.

    The ``entrypoint`` is called with ``**params`` — each key in the JSON
    input becomes a keyword argument. Authors write functions that declare
    exactly the parameters they need::

        def main(url: str, method: str = "GET", timeout: int = 30):
            ...

    If the function accepts ``**kwargs``, all parameters are passed through.
    Otherwise, only parameters matching declared argument names are passed
    (extras are silently dropped).

    Args:
        entrypoint: The action function to execute.
        catch_exceptions: If True (default), uncaught exceptions are caught and
            reported as JSON errors on stdout with exit code 1. Set to False for
            development/debugging to let exceptions propagate.
    """
    try:
        params = read_params()

        # Filter params to only those the function accepts, unless it has **kwargs
        import inspect

        sig = inspect.signature(entrypoint)
        has_var_keyword = any(
            p.kind == p.VAR_KEYWORD for p in sig.parameters.values()
        )

        if has_var_keyword:
            call_params = params
        else:
            accepted = set(sig.parameters.keys())
            call_params = {k: v for k, v in params.items() if k in accepted}

        result = entrypoint(**call_params)

        # Emit result
        if result is None:
            result = {}
        emit_result(result)
        sys.exit(0)

    except SystemExit:
        raise
    except Exception as exc:
        if not catch_exceptions:
            raise
        emit_error(
            str(exc),
            details=traceback.format_exc() if sys.stderr.isatty() else None,
        )
        sys.exit(1)
