"""Tests for attune.action module."""

import json
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from attune.action import read_params, run_action


class TestReadParams:
    def test_reads_json_from_stdin(self):
        with patch("sys.stdin", StringIO('{"name": "World", "count": 3}')):
            params = read_params()
        assert params == {"name": "World", "count": 3}

    def test_empty_stdin_returns_empty_dict(self):
        with patch("sys.stdin", StringIO("")):
            params = read_params()
        assert params == {}

    def test_whitespace_only_returns_empty_dict(self):
        with patch("sys.stdin", StringIO("   \n  ")):
            params = read_params()
        assert params == {}


class TestRunAction:
    def test_simple_action_with_kwargs(self, capsys):
        def my_action(name: str, greeting: str = "Hello"):
            return {"message": f"{greeting}, {name}!"}

        with patch("sys.stdin", StringIO('{"name": "Attune", "greeting": "Hi"}')):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output == {"message": "Hi, Attune!"}

    def test_extra_params_are_dropped(self, capsys):
        def my_action(name: str):
            return {"name": name}

        with patch("sys.stdin", StringIO('{"name": "Test", "extra": "ignored"}')):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output == {"name": "Test"}

    def test_kwargs_receives_all_params(self, capsys):
        def my_action(**kwargs):
            return {"keys": sorted(kwargs.keys())}

        with patch("sys.stdin", StringIO('{"a": 1, "b": 2, "c": 3}')):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output == {"keys": ["a", "b", "c"]}

    def test_action_returning_none_emits_empty_dict(self, capsys):
        def my_action():
            return None

        with patch("sys.stdin", StringIO("{}")):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 0
        output = json.loads(capsys.readouterr().out)
        assert output == {}

    def test_missing_required_param_produces_error(self, capsys):
        def my_action(url: str):
            return {"url": url}

        with patch("sys.stdin", StringIO("{}")):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 1
        output = json.loads(capsys.readouterr().out)
        assert output["success"] is False
        assert "url" in output["error"]

    def test_action_exception_produces_error(self, capsys):
        def my_action(name: str = "x"):
            raise ValueError("something went wrong")

        with patch("sys.stdin", StringIO("{}")):
            with pytest.raises(SystemExit) as exc_info:
                run_action(my_action)
        assert exc_info.value.code == 1
        output = json.loads(capsys.readouterr().out)
        assert output["success"] is False
        assert "something went wrong" in output["error"]

    def test_catch_exceptions_false_raises(self):
        def my_action():
            raise RuntimeError("boom")

        with patch("sys.stdin", StringIO("{}")):
            with pytest.raises(RuntimeError, match="boom"):
                run_action(my_action, catch_exceptions=False)
