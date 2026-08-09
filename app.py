from generator import generate_text


def main():
    prompt = input("Enter your prompt: ").strip()

    if not prompt:
        print("Error: Prompt cannot be empty.")
        return

    try:
        result = generate_text(prompt)

        print("\nGenerated text:")
        print(result)

    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()