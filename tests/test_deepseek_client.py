import os
from unittest.mock import MagicMock, patch

import pytest

import deepseek_client


def test_search_deepseek_success(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "testkey")

    mock_resp = MagicMock()
    mock_resp.json.return_value = {"results": [1]}
    mock_resp.raise_for_status.return_value = None

    mock_session = MagicMock()
    mock_session.post.return_value = mock_resp

    with patch("deepseek_client.requests.Session", return_value=mock_session):
        res = deepseek_client.search_deepseek("some query")
        assert res == {"results": [1]}
        mock_session.post.assert_called_once()


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(RuntimeError):
        deepseek_client._get_api_key(None)
