class ScoreEngine:

    def __init__(self):
        self.score = 0
        self.details = []


    def add(self, value, reason):
        self.score += value

        self.details.append({
            "value": value,
            "reason": reason
        })


    def remove(self, value, reason):
        self.score -= value

        self.details.append({
            "value": -value,
            "reason": reason
        })


    def get_score(self):

        self.score = max(0, min(100, self.score))

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
            "details": self.details
        }