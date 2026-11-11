from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from typing_extensions import Self

from ..models.output_visibility import OutputVisibility
from ..models.stdout_policy import StdoutPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="OutputPolicy")


@_attrs_define
class OutputPolicy:
    """Optional authoring choices. Resolve against the stored output contract once.

    Attributes:
        error (None | OutputVisibility | Unset):
        stderr (None | OutputVisibility | Unset):
        stdout (None | StdoutPolicy | Unset):
    """

    error: None | OutputVisibility | Unset = UNSET
    stderr: None | OutputVisibility | Unset = UNSET
    stdout: None | StdoutPolicy | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        error: None | str | Unset
        if isinstance(self.error, Unset):
            error = UNSET
        elif isinstance(self.error, OutputVisibility):
            error = self.error.value
        else:
            error = self.error

        stderr: None | str | Unset
        if isinstance(self.stderr, Unset):
            stderr = UNSET
        elif isinstance(self.stderr, OutputVisibility):
            stderr = self.stderr.value
        else:
            stderr = self.stderr

        stdout: None | str | Unset
        if isinstance(self.stdout, Unset):
            stdout = UNSET
        elif isinstance(self.stdout, StdoutPolicy):
            stdout = self.stdout.value
        else:
            stdout = self.stdout

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if error is not UNSET:
            field_dict["error"] = error
        if stderr is not UNSET:
            field_dict["stderr"] = stderr
        if stdout is not UNSET:
            field_dict["stdout"] = stdout

        return field_dict

    @classmethod
    def from_dict(cls, src_dict: Mapping[str, Any]) -> Self:
        d = dict(src_dict)

        def _parse_error(data: object) -> None | OutputVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                error_type_1 = OutputVisibility(data)

                return error_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OutputVisibility | Unset, data)

        error = _parse_error(d.pop("error", UNSET))

        def _parse_stderr(data: object) -> None | OutputVisibility | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stderr_type_1 = OutputVisibility(data)

                return stderr_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | OutputVisibility | Unset, data)

        stderr = _parse_stderr(d.pop("stderr", UNSET))

        def _parse_stdout(data: object) -> None | StdoutPolicy | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                stdout_type_1 = StdoutPolicy(data)

                return stdout_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | StdoutPolicy | Unset, data)

        stdout = _parse_stdout(d.pop("stdout", UNSET))

        output_policy = cls(
            error=error,
            stderr=stderr,
            stdout=stdout,
        )

        return output_policy
