import math

from .rules import *
from .score import ScoreEngine
from .crack_time import estimate_crack_time


class PasswordAnalyzer:

    def __init__(self, password):

        self.password = password
        self.engine = ScoreEngine()
        self.problems = []
        self.suggestions = []
        self.risk_score = 0
        # self.pattern_penalty = 0

    def calculate_entropy(self):

        pool = 0

        if has_lower(self.password):
            pool += 26

        if has_upper(self.password):
            pool += 26

        if has_digit(self.password):
            pool += 10

        if has_symbol(self.password):
            pool += 32

        if pool == 0:
            return 0

        entropy = len(self.password) * math.log2(pool)
        # predictable suffix penalty

        # if re.search(r"\d{4}[^A-Za-z0-9]?$", self.password):
        #     entropy -= 15

        return round(entropy, 2)

    def calculate_effective_entropy(self):

        entropy = self.calculate_entropy()

        password = self.password.lower()

        penalty = 0

        # word + year
        # if re.search(r"^[a-z]+\d{4}$", password):
        #     penalty += 25

        if re.search(r"^[a-z]+\d{4}[!@#$%^&*]$", password):
            penalty += 15


        # sequential
        if has_sequential_pattern(password):
            penalty += 30


        # famous passwords
        if password in [
            "abc123!",
            "password",
            "qwerty123"
        ]:
            penalty += 50


        return round(
            max(1, entropy - penalty),
            2
        )
    def analyze(self, common_passwords):

        password = self.password

        # Length

        if len(password) >= 16:

            self.engine.add(
                25,
                "Excellent password length"
            )

        elif len(password) >= 12:

            self.engine.add(
                20,
                "Good password length"
            )

        elif len(password) >= 8:

            self.engine.add(
                10,
                "Acceptable password length"
            )

        else:

            self.problems.append(
                "Password is too short"
            )

            self.suggestions.append(
                "Use at least 12 characters"
            )

        # Character types

        checks = [

            (
                has_upper(password),
                10,
                "Contains uppercase letters",
                "Add uppercase letters"
            ),

            (
                has_lower(password),
                10,
                "Contains lowercase letters",
                "Add lowercase letters"
            ),

            (
                has_digit(password),
                10,
                "Contains numbers",
                "Add numbers"
            ),

            (
                has_symbol(password),
                10,
                "Contains special characters",
                "Add special characters"
            )

        ]

        for result, score, good, bad in checks:

            if result:

                self.engine.add(
                    score,
                    good
                )

            else:

                self.suggestions.append(
                    bad
                )

        # Leaked passwords

        if password.lower() in common_passwords:

            self.engine.remove(
                40,
                "Password found in leaked database"
            )

            self.risk_score += 50

            self.problems.append(
                "Password is commonly used"
            )

        # Repeated characters

        if has_repeated_chars(password):

            self.engine.remove(
                20,
                "Repeated characters detected"
            )

            self.risk_score += 20

            self.problems.append(
                "Repeated characters detected"
            )
        if has_repeated_pattern(password):

            self.engine.remove(
                35,
                "Repeated pattern detected"
            )

            self.risk_score += 60

            self.problems.append(
                "Repeated word pattern detected"
            )
            # Sequential patterns

        if has_sequential_pattern(password):

            self.engine.remove(
                30,
                "Predictable sequence detected"
            )

            self.risk_score += 30

            self.problems.append(
                "Password contains predictable sequences"
            )

        # Common words

        # if has_common_word_pattern(password):

        #     self.engine.remove(
        #         30,
        #         "Common word pattern detected"
        #     )

        #     self.risk_score += 35

        #     self.problems.append(
        #         "Password contains common words"
        #     )
        if has_dictionary_match(
            password,
            common_passwords
        ):
            self.engine.remove(
                30,
                "Common word detected"
            )

            self.risk_score += 25

            self.problems.append(
                "Password contains common words"
            )
        return self.result()

    def result(self):

        score_data = self.engine.get_score()

        entropy = self.calculate_entropy()

        effective_entropy = self.calculate_effective_entropy()

        print("DEBUG RAW ENTROPY:", entropy)
        print("DEBUG EFFECTIVE:", effective_entropy)
        print("DEBUG RISK:", self.risk_score)

        return {

            "score": score_data["score"],

            "level": score_data["level"],

            "details": score_data["details"],

            "entropy": entropy,

            "effective_entropy": effective_entropy,
            "crack_time": estimate_crack_time(
                effective_entropy,
                self.risk_score
            ),

            "problems": self.problems,

            "suggestions": self.suggestions
        }
