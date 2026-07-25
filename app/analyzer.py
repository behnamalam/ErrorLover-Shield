import math
from .rules import *


class PasswordAnalyzer:

    def __init__(self, password):
        self.password = password
        self.score = 0
        self.problems = []
        self.suggestions = []


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

        return round(entropy,2)



    def analyze(self, common_passwords):

        password = self.password


        # Length

        if len(password) >= 16:
            self.score += 25

        elif len(password) >= 12:
            self.score += 20

        elif len(password) >= 8:
            self.score += 10

        else:
            self.problems.append(
                "Password is too short"
            )


        # Characters

        checks = [
            (has_upper(password),
             "Add uppercase letters"),

            (has_lower(password),
             "Add lowercase letters"),

            (has_digit(password),
             "Add numbers"),

            (has_symbol(password),
             "Add special characters")
        ]


        for result, suggestion in checks:

            if result:
                self.score += 10

            else:
                self.suggestions.append(suggestion)



        # Common passwords

        if password.lower() in common_passwords:

            self.score -= 40

            self.problems.append(
                "Password exists in leaked password database"
            )



        # Patterns

        if has_repeated_chars(password):

            self.score -= 20

            self.problems.append(
                "Repeated characters detected"
            )



        if has_sequential_pattern(password):

            self.score -= 20

            self.problems.append(
                "Sequential pattern detected"
            )


        self.score = max(0,min(100,self.score))


        return self.result()



    def result(self):

        if self.score < 30:
            level = "Very Weak"

        elif self.score < 60:
            level = "Weak"

        elif self.score < 80:
            level = "Strong"

        else:
            level = "Very Strong"


        return {

            "score": self.score,
            "level": level,
            "entropy": self.calculate_entropy(),
            "problems": self.problems,
            "suggestions": self.suggestions

        }