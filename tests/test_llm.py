import pytest
from unittest.mock import patch, MagicMock
from src.llm import generate_bullets

@patch("llm.genai.GenerativeModel")
def test_generate_bullets_with_mock(mock_model_class):
    # Mock response structure
    mock_response = MagicMock()
    mock_response.candidates[0].content.parts[0].text = "**1. Led a team to deliver a Java backend.** **2. Boosted performance by 25% using caching.**"

    # Mock Gemini model
    mock_model = MagicMock()
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model

    experience = "Managed a team of 5 engineers to deliver a Java backend."
    job_description = "Looking for leadership and backend experience."
    style = "metrics"

    bullets = generate_bullets(experience, job_description, style)

    assert len(bullets) == 2
    assert "Led a team" in bullets[0]
    assert "Boosted performance" in bullets[1]