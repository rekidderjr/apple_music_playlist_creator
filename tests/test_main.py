"""
Comprehensive tests for the main module.

This test suite demonstrates:
- Unit testing best practices
- Security testing
- Error handling validation
- Input validation testing
- Mocking and fixtures

Author: rekidderjr
"""

from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest

from apple_music_playlist_creator.main import PlaylistCreator, main


class TestPlaylistCreator:
    """Test suite for PlaylistCreator."""

    def test_init_default_config(self) -> None:
        """Test initialization with default configuration."""
        instance = PlaylistCreator()
        assert instance.config == {}
        assert isinstance(instance.config, dict)

    def test_init_custom_config(self) -> None:
        """Test initialization with custom configuration."""
        config = {"key": "value", "debug": True}
        instance = PlaylistCreator(config)
        assert instance.config == config

    def test_init_invalid_config_type(self) -> None:
        """Test initialization with invalid configuration type."""
        with pytest.raises(ValueError, match="Configuration must be a dictionary"):
            PlaylistCreator("invalid_config")  # type: ignore

    def test_process_data_valid_dict(self) -> None:
        """Test processing valid dictionary data."""
        instance = PlaylistCreator()
        test_data = {"key1": "value1", "key2": "value2"}

        result = instance.process_data(test_data)

        assert result["status"] == "success"
        assert result["input_type"] == "dict"
        assert result["processed_count"] == 2
        assert "timestamp" in result

    def test_process_data_valid_list(self) -> None:
        """Test processing valid list data."""
        instance = PlaylistCreator()
        test_data = [1, 2, 3, 4, 5]

        result = instance.process_data(test_data)

        assert result["status"] == "success"
        assert result["input_type"] == "list"
        assert result["processed_count"] == 5
        assert "timestamp" in result

    def test_process_data_none_input(self) -> None:
        """Test processing None input raises ValueError."""
        instance = PlaylistCreator()

        with pytest.raises(ValueError, match="Input data cannot be None"):
            instance.process_data(None)  # type: ignore

    def test_process_data_invalid_type(self) -> None:
        """Test processing invalid data type raises TypeError."""
        instance = PlaylistCreator()

        with pytest.raises(TypeError, match="Input data must be a list or dictionary"):
            instance.process_data("invalid_string")  # type: ignore

    def test_validate_input_valid(self) -> None:
        """Test input validation with valid input."""
        instance = PlaylistCreator()

        assert instance.validate_input("test", str) is True
        assert instance.validate_input(42, int) is True
        assert instance.validate_input([1, 2, 3], list) is True

    def test_validate_input_invalid(self) -> None:
        """Test input validation with invalid input."""
        instance = PlaylistCreator()

        with pytest.raises(TypeError, match="Expected str, got int"):
            instance.validate_input(42, str)

        with pytest.raises(TypeError, match="Expected list, got str"):
            instance.validate_input("test", list)

    def test_get_status(self) -> None:
        """Test getting status information."""
        config = {"debug": True, "timeout": 30}
        instance = PlaylistCreator(config)

        status = instance.get_status()

        assert status["initialized"] is True
        assert set(status["config_keys"]) == {"debug", "timeout"}
        assert "timestamp" in status

    @patch("datetime.datetime")
    def test_get_timestamp_mocked(self, mock_datetime: MagicMock) -> None:
        """Test timestamp generation with mocked datetime."""
        mock_datetime.now.return_value.isoformat.return_value = "2023-01-01T12:00:00"

        instance = PlaylistCreator()
        timestamp = instance._get_timestamp()

        assert timestamp == "2023-01-01T12:00:00"
        mock_datetime.now.assert_called_once()

    def test_process_data_exception_handling(self) -> None:
        """Test exception handling in process_data method."""
        instance = PlaylistCreator()

        # Mock _get_timestamp to raise an exception
        with patch.object(instance, "_get_timestamp", side_effect=Exception("Timestamp error")):
            with pytest.raises(RuntimeError, match="Processing failed: Timestamp error"):
                instance.process_data({"test": "data"})


class TestSecurityCompliance:
    """Security and compliance tests."""

    def test_no_hardcoded_secrets(self) -> None:
        """Test that no hardcoded secrets are present in the class."""
        instance = PlaylistCreator()

        # Check that no common secret patterns exist in the instance
        instance_vars = vars(instance)
        for key, value in instance_vars.items():
            if isinstance(value, str):
                # Check for common secret patterns
                assert "password" not in value.lower()
                assert "api_key" not in value.lower()
                assert "secret" not in value.lower()
                assert "token" not in value.lower()

    def test_input_sanitization(self) -> None:
        """Test that inputs are properly sanitized."""
        instance = PlaylistCreator()

        # Test with potentially malicious input
        malicious_data = {
            "script": "<script>alert('xss')</script>",
            "sql": "'; DROP TABLE users; --",
            "path": "../../../etc/passwd",
        }

        # Should process without executing malicious content
        result = instance.process_data(malicious_data)
        assert result["status"] == "success"
        assert result["input_type"] == "dict"

    def test_error_message_security(self) -> None:
        """Test that error messages don't leak sensitive information."""
        instance = PlaylistCreator()

        try:
            instance.validate_input("test", int)
        except TypeError as e:
            error_msg = str(e)
            # Ensure error message doesn't contain sensitive paths or system info
            assert "/home/" not in error_msg
            assert "/usr/" not in error_msg
            assert "password" not in error_msg.lower()


class TestPerformanceAndReliability:
    """Performance and reliability tests."""

    def test_large_data_processing(self) -> None:
        """Test processing of large datasets."""
        instance = PlaylistCreator()

        # Create large dataset
        large_data = {f"key_{i}": f"value_{i}" for i in range(1000)}

        result = instance.process_data(large_data)

        assert result["status"] == "success"
        assert result["processed_count"] == 1000

    def test_empty_data_handling(self) -> None:
        """Test handling of empty data structures."""
        instance = PlaylistCreator()

        # Test empty dict
        result = instance.process_data({})
        assert result["status"] == "success"
        assert result["processed_count"] == 0

        # Test empty list
        result = instance.process_data([])
        assert result["status"] == "success"
        assert result["processed_count"] == 0

    def test_unicode_handling(self) -> None:
        """Test proper handling of unicode characters."""
        instance = PlaylistCreator()

        unicode_data = {
            "emoji": "rocket-lock-check",
            "chinese": "你好世界",
            "arabic": "مرحبا بالعالم",
            "special": "àáâãäåæçèéêë",
        }

        result = instance.process_data(unicode_data)
        assert result["status"] == "success"
        assert result["processed_count"] == 4


@pytest.fixture
def sample_instance() -> PlaylistCreator:
    """Fixture providing a sample PlaylistCreator instance."""
    return PlaylistCreator({"test_mode": True})


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Fixture providing sample test data."""
    return {"name": "Test Data", "count": 42, "active": True, "items": ["item1", "item2", "item3"]}


def test_fixture_usage(sample_instance: PlaylistCreator, sample_data: Dict[str, Any]) -> None:
    """Test using pytest fixtures."""
    result = sample_instance.process_data(sample_data)

    assert result["status"] == "success"
    assert result["input_type"] == "dict"
    assert result["processed_count"] == 4


@pytest.mark.parametrize(
    "input_data,expected_type,expected_count",
    [
        ({"a": 1, "b": 2}, "dict", 2),
        ([1, 2, 3, 4], "list", 4),
        ({"single": "item"}, "dict", 1),
        ([], "list", 0),
    ],
)
def test_parametrized_processing(input_data: Any, expected_type: str, expected_count: int) -> None:
    """Test data processing with parametrized inputs."""
    instance = PlaylistCreator()
    result = instance.process_data(input_data)

    assert result["status"] == "success"
    assert result["input_type"] == expected_type
    assert result["processed_count"] == expected_count

class TestMainFunction:
    """Test suite for the main function."""

    def test_main_function_success(self) -> None:
        """Test main function executes successfully."""
        # Just run main function - it should complete without error
        main()

    @patch("apple_music_playlist_creator.main.PlaylistCreator")
    def test_main_function_exception_handling(self, mock_playlist_creator: MagicMock) -> None:
        """Test main function handles exceptions properly."""
        # Make PlaylistCreator raise an exception
        mock_playlist_creator.side_effect = Exception("Test error")
        
        # Run main function and expect it to raise
        with pytest.raises(Exception, match="Test error"):
            main()
