"""
Pytest test cases for the Flask app model schema validation

Schemas for reference:

class Answer_Format(BaseModel):
    feedback: str = Field(..., min_length=1)
    total_mark: int = Field(..., gt=-1, le=30)
    
class Question_Format(BaseModel):
    question: str = Field(..., min_length=1)
    level: int = Field(..., gt=0)
"""

import pytest
from pydantic import ValidationError
from flask_app.routes.model.check_gen import Answer_Format, Question_Format

"""
Test cases for Schema validation - Answer_Format
"""


def test_valid_feedback():
    response = {"feedback": "Code is correct", "total_mark": 15}
    answer = Answer_Format(
        feedback=response["feedback"], total_mark=response["total_mark"]
    )

    assert answer.total_mark == 15
    assert len(answer.feedback) > 0


def test_valid_mark_upper_bound():
    response = {"feedback": "Code is incorrect", "total_mark": 30}
    answer = Answer_Format(
        feedback=response["feedback"], total_mark=response["total_mark"]
    )

    assert answer.total_mark == 30
    assert len(answer.feedback) > 0


def test_valid_mark_lower_bound():
    response = {"feedback": "Code is incorrect", "total_mark": 0}
    answer = Answer_Format(
        feedback=response["feedback"], total_mark=response["total_mark"]
    )

    assert answer.total_mark == 0
    assert len(answer.feedback) > 0


def test_invalid_mark_greater():
    response = {"feedback": "Code is correct", "total_mark": 31}
    with pytest.raises(ValidationError):
        Answer_Format(**response)


def test_invalid_mark_less():
    response = {"feedback": "Code is correct", "total_mark": -1}
    with pytest.raises(ValidationError):
        Answer_Format(**response)


def test_invalid_empty_feedback():
    response = {"feedback": "", "total_mark": 4}
    with pytest.raises(ValidationError):
        Answer_Format(**response)


def test_invalid_feedback_missing_field():
    response = {"total_mark": 4}
    with pytest.raises(ValidationError):
        Answer_Format(**response)


"""
Test cases for Schema validation - Question_Format
"""


def test_valid_question():
    response = {"question": "this is a question", "level": 1}
    answer = Question_Format(question=response["question"], level=response["level"])

    assert answer.level == 1
    assert len(answer.question) > 0


def test_invalid_level_less():
    response = {"question": "Code is correct", "level": 0}
    with pytest.raises(ValidationError):
        Question_Format(**response)


def test_invalid_empty_question():
    response = {"question": "", "level": 4}
    with pytest.raises(ValidationError):
        Question_Format(**response)


def test_invalid_feedback_missing_field():
    response = {"level": 4}
    with pytest.raises(ValidationError):
        Question_Format(**response)
