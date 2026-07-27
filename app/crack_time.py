def estimate_crack_time(entropy, risk=0):

    guesses_per_second = 10 ** 10

    guesses = 2 ** entropy

    # risk adjustment
    if risk >= 50:
        guesses *= 0.000001

    elif risk >= 20:
        guesses *= 0.001

    seconds = guesses / guesses_per_second

    return format_time(seconds)


def format_time(seconds):

    minute = 60
    hour = minute * minute
    day = hour * 24
    year = day * 365

    if seconds < minute:
        return "Instant"

    elif seconds < hour:
        return f"{round(seconds / minute)} minutes"

    elif seconds < day:
        return f"{round(seconds / hour)} hours"

    elif seconds < year:
        return f"{round(seconds / day)} days"

    elif seconds < year * 1000:
        return f"{round(seconds / year)} years"

    elif seconds < year * 1_000_000:
        return f"{round(seconds / year / 1000)} thousand years"

    elif seconds < year * 1_000_000_000:
        return f"{round(seconds / year / 1_000_000)} million years"

    else:
        return "Billions of years"
