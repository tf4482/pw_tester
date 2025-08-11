#!/usr/bin/env python3
"""
Tests for pw_tester module
"""

import pytest
from pw_tester import PasswordTester, PasswordAnalysis


class TestPasswordTester:
    """Test cases for PasswordTester class"""

    def setup_method(self):
        """Set up test fixtures"""
        self.tester = PasswordTester()

    def test_analyze_character_space(self):
        """Test character space analysis"""
        # Only lowercase
        assert self.tester.analyze_character_space("abc") == 26

        # Lowercase + uppercase
        assert self.tester.analyze_character_space("Abc") == 52

        # Lowercase + uppercase + digits
        assert self.tester.analyze_character_space("Abc1") == 62

        # All character types
        assert self.tester.analyze_character_space("Abc1!") == 88

    def test_calculate_entropy(self):
        """Test entropy calculation"""
        # Simple password
        entropy = self.tester.calculate_entropy("abc", 26)
        assert entropy > 0

        # More complex password should have higher entropy
        entropy_complex = self.tester.calculate_entropy("Abc123!", 88)
        assert entropy_complex > entropy

    def test_get_complexity_score(self):
        """Test complexity scoring"""
        assert self.tester.get_complexity_score(20) == "Very Weak"
        assert self.tester.get_complexity_score(30) == "Weak"
        assert self.tester.get_complexity_score(50) == "Medium"
        assert self.tester.get_complexity_score(80) == "Strong"
        assert self.tester.get_complexity_score(150) == "Very Strong"

    def test_format_time(self):
        """Test time formatting"""
        assert "seconds" in self.tester.format_time(0.5)
        assert "minutes" in self.tester.format_time(120)
        assert "hours" in self.tester.format_time(7200)
        assert "days" in self.tester.format_time(172800)
        assert "years" in self.tester.format_time(31536000)
        assert "uncrackable" in self.tester.format_time(31536000000)

    def test_analyze_password_weak(self):
        """Test analysis of weak password"""
        analysis = self.tester.analyze_password("123456")

        assert analysis.password_length == 6
        assert analysis.character_space == 10
        assert analysis.complexity_score == "Very Weak"
        assert len(analysis.recommendations) > 0
        assert "Use at least 12 characters" in analysis.recommendations

    def test_analyze_password_strong(self):
        """Test analysis of strong password"""
        analysis = self.tester.analyze_password("MyS3cur3P@ssw0rd!")

        assert analysis.password_length == 17
        assert analysis.character_space == 88
        assert analysis.complexity_score in ["Strong", "Very Strong"]
        assert "Your password has good complexity!" in analysis.recommendations

    def test_analyze_password_empty(self):
        """Test analysis of empty password"""
        with pytest.raises(ValueError, match="Password cannot be empty"):
            self.tester.analyze_password("")

    def test_generate_recommendations(self):
        """Test recommendation generation"""
        # Short password
        recs = self.tester.generate_recommendations("abc", 20)
        assert "Use at least 12 characters" in recs
        assert "Add uppercase letters" in recs
        assert "Add numbers" in recs
        assert "Add special characters" in recs

        # Good password
        recs = self.tester.generate_recommendations("MyS3cur3P@ssw0rd!", 100)
        assert "Your password has good complexity!" in recs

    def test_brute_force_time_calculation(self):
        """Test brute force time calculation"""
        times = self.tester.calculate_brute_force_time(1000000)

        assert "basic_cpu" in times
        assert "modern_cpu" in times
        assert "gpu_single" in times
        assert "gpu_cluster" in times
        assert "quantum_future" in times

        # All should be valid time strings
        for time_str in times.values():
            assert isinstance(time_str, str)
            assert len(time_str) > 0


def test_password_analysis_dataclass():
    """Test PasswordAnalysis dataclass"""
    analysis = PasswordAnalysis(
        password_length=8,
        character_space=26,
        entropy_bits=37.6,
        total_combinations=208827064576,
        complexity_score="Medium",
        brute_force_times={"basic_cpu": "1.2 days"},
        recommendations=["Add numbers"],
    )

    assert analysis.password_length == 8
    assert analysis.character_space == 26
    assert analysis.complexity_score == "Medium"


if __name__ == "__main__":
    pytest.main([__file__])
