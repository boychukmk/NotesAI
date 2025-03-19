import pytest
import requests
from app.services.gemini_summerizer import summarize_text, GEMINI_URL


@pytest.mark.parametrize(
    "mock_response, expected_summary",
    [
        (
            {"candidates": [{"content": {"parts": [{"text": "This is a summary"}]}}]},
            "This is a summary",
        ),
        (
            {"candidates": [{"content": {"parts": [{"text": "Short summary"}]}}]},
            "Short summary",
        ),
    ],
)
def test_summarize_text_success(mocker, mock_response, expected_summary):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = mock_response

    text = "Some long text to summarize."
    result = summarize_text(text)

    assert result == expected_summary
    mock_post.assert_called_once_with(
        GEMINI_URL,
        json={"contents": [{"parts": [{"text": mocker.ANY}]}]},
        headers={"Content-Type": "application/json"},
        params={"key": mocker.ANY},
        timeout=10,
    )


def test_summarize_text_empty_response(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {}

    text = "Some text."
    result = summarize_text(text)

    assert result == "API response error"


def test_summarize_text_invalid_json(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.side_effect = ValueError("Invalid JSON")

    text = "Some text."
    result = summarize_text(text)

    assert result == "API response error"


def test_summarize_text_timeout(mocker):
    mock_post = mocker.patch("requests.post", side_effect=requests.Timeout)

    text = "Some text."
    result = summarize_text(text)

    assert result == "API request timed out"
    mock_post.assert_called_once()


def test_summarize_text_request_error(mocker):
    mock_post = mocker.patch("requests.post", side_effect=requests.RequestException("Network error"))

    text = "Some text."
    result = summarize_text(text)

    assert result == "Generation failed"
    mock_post.assert_called_once()


def test_summarize_text_api_error(mocker):
    mock_post = mocker.patch("requests.post")
    mock_post.return_value.status_code = 500
    mock_post.return_value.json.return_value = {"error": "Something went wrong"}

    text = "Some text."
    result = summarize_text(text)

    assert result == "API response error"
    mock_post.assert_called_once()
