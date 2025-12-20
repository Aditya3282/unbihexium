"""Tests for CLI module."""

import pytest
from click.testing import CliRunner


class TestCLI:
    """Tests for command-line interface."""
    
    @pytest.fixture
    def runner(self):
        return CliRunner()
    
    def test_version_command(self, runner):
        """Test version command."""
        from unbihexium.cli import cli
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
    
    def test_help_command(self, runner):
        """Test help command."""
        from unbihexium.cli import cli
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Unbihexium" in result.output
