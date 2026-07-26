from app.analyzer import PasswordAnalyzer


def load_passwords():

    with open(
        "database/common_passwords.txt",
        "r"
    ) as file:

        return [
            x.strip()
            for x in file.readlines()
        ]


print("""
=========================
   ErrorLover Shield 🛡️
 Password Security Tool
=========================
""")


password = input(
    "Enter password: "
)


database = load_passwords()


analyzer = PasswordAnalyzer(password)


result = analyzer.analyze(database)


print("\n========= REPORT =========")


print(
    f"Score: {result['score']}/100"
)


print(
    f"Level: {result['level']}"
)


print(
    f"Entropy: {result['entropy']} bits"
)


if result["details"]:

    print("\nScore Details:")

    for item in result["details"]:

        sign = "+" if item["value"] > 0 else ""

        print(
            f"{sign}{item['value']} : {item['reason']}"
        )


if result["problems"]:

    print("\nProblems:")

    for item in result["problems"]:
        print("-", item)


if result["suggestions"]:

    print("\nSuggestions:")

    for item in result["suggestions"]:
        print("-", item)
