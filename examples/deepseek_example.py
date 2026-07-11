import os
from deepseek_client import search_deepseek


def main():
    # Ensure you have set DEEPSEEK_API_KEY in your environment or GitHub Secrets
    query = "example astrology resources"
    try:
        res = search_deepseek(query)
        print("Found:", res)
    except Exception as e:
        print("Deepseek request failed:", e)


if __name__ == "__main__":
    main()
