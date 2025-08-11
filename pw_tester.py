#!/usr/bin/env python3
"""
pw_tester - Password Complexity and Brute Force Time Analyzer

This tool analyzes password complexity and estimates the time
for brute force attacks based on different attack scenarios.
"""

import re
import math
import string
import argparse
import sys
from typing import Dict, Tuple, List
from dataclasses import dataclass
from enum import Enum

# Color and platform-specific imports
from colorama import init, Fore, Back, Style

init(autoreset=True)  # Initialize colorama

# Platform-specific imports
if sys.platform == "win32":
    import msvcrt
else:
    import termios
    import tty


class AttackScenario(Enum):
    """Different attack scenarios with varying speeds"""

    BASIC_CPU = "basic_cpu"  # 1 million attempts/second
    MODERN_CPU = "modern_cpu"  # 100 million attempts/second
    GPU_SINGLE = "gpu_single"  # 10 billion attempts/second
    GPU_CLUSTER = "gpu_cluster"  # 1 trillion attempts/second
    QUANTUM_FUTURE = "quantum_future"  # 1 quadrillion attempts/second


@dataclass
class PasswordAnalysis:
    """Result of password analysis"""

    password_length: int
    character_space: int
    entropy_bits: float
    total_combinations: int
    complexity_score: str
    brute_force_times: Dict[str, str]
    recommendations: List[str]


class PasswordTester:
    """Main class for password complexity analysis"""

    # Attack scenarios with attempts per second
    ATTACK_SPEEDS = {
        AttackScenario.BASIC_CPU: 1_000_000,  # 1M/s
        AttackScenario.MODERN_CPU: 100_000_000,  # 100M/s
        AttackScenario.GPU_SINGLE: 10_000_000_000,  # 10B/s
        AttackScenario.GPU_CLUSTER: 1_000_000_000_000,  # 1T/s
        AttackScenario.QUANTUM_FUTURE: 1_000_000_000_000_000,  # 1P/s
    }

    # Character sets for different password types
    CHARACTER_SETS = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "special": "!@#$%^&*()_+-=[]{}|;:,.<>?",
        "space": " ",
    }

    def __init__(self):
        self.common_patterns = [
            r"\d{4,}",  # 4+ consecutive numbers
            r"[a-zA-Z]{8,}",  # 8+ consecutive letters
            r"(.)\1{2,}",  # 3+ same characters in a row
            r"(012|123|234|345|456|567|678|789|890)",  # number sequences
            r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)",  # letter sequences
        ]

    def analyze_character_space(self, password: str) -> int:
        """Determines the character space of the password"""
        character_space = 0

        if any(c in self.CHARACTER_SETS["lowercase"] for c in password):
            character_space += len(self.CHARACTER_SETS["lowercase"])

        if any(c in self.CHARACTER_SETS["uppercase"] for c in password):
            character_space += len(self.CHARACTER_SETS["uppercase"])

        if any(c in self.CHARACTER_SETS["digits"] for c in password):
            character_space += len(self.CHARACTER_SETS["digits"])

        if any(c in self.CHARACTER_SETS["special"] for c in password):
            character_space += len(self.CHARACTER_SETS["special"])

        if any(c in self.CHARACTER_SETS["space"] for c in password):
            character_space += len(self.CHARACTER_SETS["space"])

        return character_space

    def calculate_entropy(self, password: str, character_space: int) -> float:
        """Calculates the entropy of the password in bits"""
        if character_space == 0 or len(password) == 0:
            return 0.0

        # Base entropy
        base_entropy = len(password) * math.log2(character_space)

        # Reduction for common patterns
        pattern_penalty = 0
        for pattern in self.common_patterns:
            matches = re.findall(pattern, password, re.IGNORECASE)
            if matches:
                pattern_penalty += len("".join(matches)) * 0.5

        # Reduction for repetitions
        unique_chars = len(set(password.lower()))
        repetition_penalty = (len(password) - unique_chars) * 0.3

        adjusted_entropy = base_entropy - pattern_penalty - repetition_penalty
        return max(0, adjusted_entropy)

    def get_complexity_score(self, entropy: float) -> str:
        """Determines complexity rating based on entropy"""
        if entropy < 28:
            return "Very Weak"
        elif entropy < 36:
            return "Weak"
        elif entropy < 60:
            return "Medium"
        elif entropy < 128:
            return "Strong"
        else:
            return "Very Strong"

    def get_complexity_color(self, complexity: str) -> str:
        """Returns color code for complexity score"""
        colors = {
            "Very Weak": Fore.RED,
            "Weak": Fore.LIGHTRED_EX,
            "Medium": Fore.YELLOW,
            "Strong": Fore.LIGHTGREEN_EX,
            "Very Strong": Fore.GREEN,
        }
        return colors.get(complexity, Fore.WHITE)

    def calculate_brute_force_time(self, total_combinations: int) -> Dict[str, str]:
        """Calculates brute force time for different attack scenarios"""
        times = {}

        # On average, password is found after half of all attempts
        avg_attempts = total_combinations // 2

        for scenario, speed in self.ATTACK_SPEEDS.items():
            seconds = avg_attempts / speed
            times[scenario.value] = self.format_time(seconds)

        return times

    def format_time(self, seconds: float) -> str:
        """Formats time in readable form"""
        if seconds < 1:
            return f"{seconds:.3f} seconds"
        elif seconds < 60:
            return f"{seconds:.1f} seconds"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f} minutes"
        elif seconds < 86400:
            hours = seconds / 3600
            return f"{hours:.1f} hours"
        elif seconds < 31536000:
            days = seconds / 86400
            return f"{days:.1f} days"
        elif seconds < 31536000000:
            years = seconds / 31536000
            return f"{years:.1f} years"
        else:
            return "Practically uncrackable (> 1000 years)"

    def generate_recommendations(self, password: str, entropy: float) -> List[str]:
        """Generates recommendations for password improvement"""
        recommendations = []

        if len(password) < 12:
            recommendations.append("Use at least 12 characters")

        if not any(c.islower() for c in password):
            recommendations.append("Add lowercase letters")

        if not any(c.isupper() for c in password):
            recommendations.append("Add uppercase letters")

        if not any(c.isdigit() for c in password):
            recommendations.append("Add numbers")

        if not any(c in self.CHARACTER_SETS["special"] for c in password):
            recommendations.append("Add special characters")

        # Check for common patterns
        for pattern in self.common_patterns:
            if re.search(pattern, password, re.IGNORECASE):
                recommendations.append("Avoid predictable patterns and sequences")
                break

        if entropy < 60:
            recommendations.append("Increase complexity for better security")

        if not recommendations:
            recommendations.append("Your password has good complexity!")

        return recommendations

    def analyze_password(self, password: str) -> PasswordAnalysis:
        """Performs complete password analysis"""
        if not password:
            raise ValueError("Password cannot be empty")

        character_space = self.analyze_character_space(password)
        entropy = self.calculate_entropy(password, character_space)
        total_combinations = character_space ** len(password)
        complexity_score = self.get_complexity_score(entropy)
        brute_force_times = self.calculate_brute_force_time(total_combinations)
        recommendations = self.generate_recommendations(password, entropy)

        return PasswordAnalysis(
            password_length=len(password),
            character_space=character_space,
            entropy_bits=entropy,
            total_combinations=total_combinations,
            complexity_score=complexity_score,
            brute_force_times=brute_force_times,
            recommendations=recommendations,
        )


def print_analysis(analysis: PasswordAnalysis, show_password: bool = False):
    """Prints analysis results in formatted output with colors and emojis"""
    tester = PasswordTester()
    complexity_color = tester.get_complexity_color(analysis.complexity_score)

    # Header with emoji
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.CYAN}🔐              PW_TESTER ANALYSIS              🔐")
    print(f"{Fore.CYAN}{'=' * 60}")

    # Password Properties
    print(f"\n{Fore.LIGHTBLUE_EX}📊 PASSWORD PROPERTIES:")
    print(
        f"  {Fore.WHITE}Length:          {Fore.LIGHTCYAN_EX}{analysis.password_length} characters"
    )
    print(
        f"  {Fore.WHITE}Character space: {Fore.LIGHTCYAN_EX}{analysis.character_space} possible characters"
    )
    print(
        f"  {Fore.WHITE}Entropy:         {Fore.LIGHTCYAN_EX}{analysis.entropy_bits:.2f} bits"
    )
    print(
        f"  {Fore.WHITE}Complexity:      {complexity_color}{analysis.complexity_score}"
    )
    print(
        f"  {Fore.WHITE}Combinations:    {Fore.LIGHTCYAN_EX}{analysis.total_combinations:,}"
    )

    # Brute Force Time Estimates
    print(f"\n{Fore.LIGHTBLUE_EX}⚡ BRUTE FORCE TIME ESTIMATES:")
    scenario_data = {
        "basic_cpu": ("💻 Basic CPU (1M/s)", Fore.LIGHTRED_EX),
        "modern_cpu": ("🖥️  Modern CPU (100M/s)", Fore.YELLOW),
        "gpu_single": ("🎮 Single GPU (10B/s)", Fore.LIGHTYELLOW_EX),
        "gpu_cluster": ("🔥 GPU Cluster (1T/s)", Fore.LIGHTMAGENTA_EX),
        "quantum_future": ("🚀 Quantum Computer (1P/s)", Fore.LIGHTRED_EX),
    }

    for scenario, time in analysis.brute_force_times.items():
        if scenario in scenario_data:
            name, color = scenario_data[scenario]
            # Color time based on security level
            if "uncrackable" in time.lower():
                time_color = Fore.GREEN
            elif "years" in time:
                time_color = Fore.LIGHTGREEN_EX
            elif "days" in time:
                time_color = Fore.YELLOW
            elif "hours" in time:
                time_color = Fore.LIGHTYELLOW_EX
            else:
                time_color = Fore.RED

            print(f"  {color}{name:<27}: {time_color}{time}")

    # Recommendations
    print(f"\n{Fore.LIGHTBLUE_EX}💡 RECOMMENDATIONS:")
    for i, rec in enumerate(analysis.recommendations, 1):
        if "good complexity" in rec.lower():
            emoji = "✅"
            color = Fore.GREEN
        else:
            emoji = "⚠️"
            color = Fore.YELLOW
        print(f"  {emoji} {color}{rec}")

    print(f"\n{Fore.CYAN}{'=' * 60}")


def get_password_with_asterisks(prompt: str = "Enter password: ") -> str:
    """Get password input with asterisks displayed for each character"""
    print(prompt, end="", flush=True)
    password = ""

    if sys.platform == "win32":
        # Windows implementation
        while True:
            char = msvcrt.getch()
            if char == b"\r":  # Enter key
                break
            elif char == b"\x08":  # Backspace
                if password:
                    password = password[:-1]
                    print("\b \b", end="", flush=True)
            elif char == b"\x03":  # Ctrl+C
                raise KeyboardInterrupt
            else:
                password += char.decode("utf-8", errors="ignore")
                print("*", end="", flush=True)
    else:
        # Unix/Linux/macOS implementation
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char == "\n" or char == "\r":  # Enter key
                    break
                elif char == "\x7f" or char == "\x08":  # Backspace/Delete
                    if password:
                        password = password[:-1]
                        print("\b \b", end="", flush=True)
                elif char == "\x03":  # Ctrl+C
                    raise KeyboardInterrupt
                elif char == "\x04":  # Ctrl+D (EOF)
                    break
                elif ord(char) >= 32:  # Printable characters
                    password += char
                    print("*", end="", flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print()  # New line after password input
    return password


def main():
    """Main function for CLI"""
    parser = argparse.ArgumentParser(
        description="pw_tester - Analyzes password complexity and brute force times",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pw_tester.py                          # Interactive mode (default)
  pw_tester.py --demo                   # Demo with example passwords
        """,
    )

    parser.add_argument(
        "--demo", action="store_true", help="Show demo with various example passwords"
    )
    parser.add_argument(
        "--show-password", action="store_true", help="Show password in output"
    )

    args = parser.parse_args()

    tester = PasswordTester()

    try:
        if args.demo:
            # Demo mode with various example passwords
            demo_passwords = [
                ("123456", "Very weak password"),
                ("password", "Common word"),
                ("Password123", "Basic complexity"),
                ("MyS3cur3P@ssw0rd!", "Strong password"),
                ("correct horse battery staple", "Passphrase"),
            ]

            print(f"{Fore.CYAN}🎯 PW_TESTER DEMO - Different Password Types 🎯")
            print(f"{Fore.CYAN}{'=' * 60}")

            for pwd, description in demo_passwords:
                print(f"\n{Fore.LIGHTMAGENTA_EX}📝 {description}: {Fore.WHITE}'{pwd}'")
                print(f"{Fore.LIGHTBLACK_EX}{'-' * 40}")
                analysis = tester.analyze_password(pwd)
                print_analysis(analysis, show_password=True)
        else:
            # Interactive mode - prompt user for password
            print(f"{Fore.CYAN}🔐 PW_TESTER - Password Complexity Analyzer 🔐")
            print(f"{Fore.CYAN}{'=' * 50}")
            print(
                f"{Fore.LIGHTBLUE_EX}🛡️  This tool analyzes password strength and estimates brute force times."
            )
            print(
                f"{Fore.LIGHTGREEN_EX}🔒 Your password will not be stored or logged.\n"
            )

            password = get_password_with_asterisks(
                f"{Fore.YELLOW}🔑 Enter password to analyze: {Style.RESET_ALL}"
            )

            if not password:
                print(f"{Fore.RED}❌ Error: Empty password entered.", file=sys.stderr)
                sys.exit(1)

            analysis = tester.analyze_password(password)
            print_analysis(analysis, show_password=args.show_password)

    except ValueError as e:
        print(f"{Fore.RED}❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Aborted.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}💥 Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
