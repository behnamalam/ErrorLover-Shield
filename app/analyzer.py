import math

from .rules import *
from .score import ScoreEngine



class PasswordAnalyzer:

    def __init__(self, password):

        self.password = password

        self.engine = ScoreEngine()

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


        return round(entropy, 2)




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




        # Common passwords

        if password.lower() in common_passwords:


            self.engine.remove(
                40,
                "Password found in leaked database"
            )


            self.problems.append(
                "Password is commonly used"
            )




        # Repeated characters

        if has_repeated_chars(password):


            self.engine.remove(
                20,
                "Repeated characters detected"
            )


            self.problems.append(
                "Repeated characters detected"
            )




        # Sequential patterns

        if has_sequential_pattern(password):


            self.engine.remove(
                20,
                "Sequential pattern detected"
            )


            self.problems.append(
                "Sequential pattern detected"
            )




        return self.result()




    def result(self):

        score_data = self.engine.get_score()


        return {

            "score": score_data["score"],

            "level": score_data["level"],

            "details": score_data["details"],

            "entropy": self.calculate_entropy(),

            "problems": self.problems,

            "suggestions": self.suggestions

        }