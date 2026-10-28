"""Generated archive endpoints must accept successful gzip responses."""

import gzip
import importlib
import json
from pathlib import Path
import subprocess
import sys

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def archive_client(tmp_path_factory):
    """Exercise the pinned generator without replacing the checked-in SDK."""
    temp = tmp_path_factory.mktemp("archive-generation")
    paths = {}
    for path, operation, parameter, parameter_type, statuses in [
        (
            "/api/v1/internal/packs/{pack_ref}/archive",
            "download_pack_archive",
            "pack_ref",
            "string",
            [200, 206],
        ),
        (
            "/api/v1/internal/pack-installs/{pack_install_id}/archive",
            "download_pack_install_candidate_archive",
            "pack_install_id",
            "integer",
            [200],
        ),
    ]:
        parameters = [
            {
                "name": parameter,
                "in": "path",
                "required": True,
                "schema": {"type": parameter_type},
            }
        ]
        if parameter == "pack_install_id":
            parameters.append(
                {
                    "name": "x-attune-pack-candidate-token",
                    "in": "header",
                    "required": True,
                    "schema": {"type": "string"},
                }
            )
        paths[path] = {
            "get": {
                "operationId": operation,
                "tags": ["internal"],
                "parameters": parameters,
                "responses": {
                    str(status): {
                        "description": "Raw archive bytes",
                        "content": {
                            "application/gzip": {
                                "schema": {"type": "string", "format": "binary"}
                            }
                        },
                    }
                    for status in statuses
                },
            }
        }
    spec = temp / "openapi.json"
    spec.write_text(
        json.dumps(
            {
                "openapi": "3.1.0",
                "info": {"title": "Archive fixture", "version": "1.0.0"},
                "paths": paths,
            }
        )
    )
    package_name = "archive_response_test_client"
    result = subprocess.run(
        [
            str(Path(sys.executable).with_name("openapi-python-client")),
            "generate",
            "--path",
            str(spec),
            "--config",
            str(ROOT / "scripts/generator.config.json"),
            "--output-path",
            str(temp / package_name),
            "--meta",
            "none",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "WARNING" not in result.stderr
    assert (
        '--config "$SCRIPT_DIR/generator.config.json"'
        in (ROOT / "scripts/generate-client.sh").read_text()
    )
    with pytest.MonkeyPatch.context() as patch:
        patch.syspath_prepend(str(temp))
        yield importlib.import_module(package_name)


@pytest.mark.parametrize(
    "operation,target,status,path",
    [
        ("download_pack_archive", "demo", 200, "/api/v1/internal/packs/demo/archive"),
        ("download_pack_archive", "demo", 206, "/api/v1/internal/packs/demo/archive"),
        (
            "download_pack_install_candidate_archive",
            42,
            200,
            "/api/v1/internal/pack-installs/42/archive",
        ),
    ],
)
def test_archive_success_preserves_binary_bytes(
    archive_client, operation, target, status, path
):
    endpoint = importlib.import_module(
        f"{archive_client.__name__}.api.internal.{operation}"
    )
    file_type = importlib.import_module(f"{archive_client.__name__}.types").File
    archive = gzip.compress(b"\x00\xff archive bytes, not JSON or text", mtime=0)
    payload = archive[3:17] if status == 206 else archive

    def handler(request):
        assert request.method == "GET"
        assert request.url.path == path
        return httpx.Response(
            status,
            content=payload,
            headers={"Content-Type": "application/gzip"},
        )

    with httpx.Client(
        base_url="https://attune.test", transport=httpx.MockTransport(handler)
    ) as http_client:
        client = archive_client.AuthenticatedClient(
            base_url="https://attune.test",
            token="test-token",
            raise_on_unexpected_status=True,
        ).set_httpx_client(http_client)
        if operation == "download_pack_install_candidate_archive":
            response = endpoint.sync_detailed(
                target, client=client, x_attune_pack_candidate_token="test-candidate"
            )
        else:
            response = endpoint.sync_detailed(target, client=client)

    assert response.status_code == status
    assert response.content == payload
    assert isinstance(response.parsed, file_type)
    assert response.parsed.payload.read() == payload
