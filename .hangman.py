import random

HANGMAN_PICS = [
    """
       +---+
       |   |
           |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
           |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
       |   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|   |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
           |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      /    |
           |
    =========""",
    """
       +---+
       |   |
       O   |
      /|\\  |
      / \\  |
           |
    ========="""
]

def load_words():
    """Reads words from 'words.txt' if available, otherwise uses a default list."""
    try:
        with open("words.txt", "r") as file:
            words = file.read().splitlines()
            words = [word.strip().upper() for word in words if word.strip().isalpha()]
            if words:
                return words
    except FileNotFoundError:
        pass
    
    # Fallback word list if words.txt is not present
    return ["PYTHON", "DEVELOPER", "INTERNSHIP", "HANGMAN", "PROGRAMMING", "DATHEON"]

def play_hangman():
    words = load_words()
    secret_word = random.choice(words).upper()
    
    guessed_letters = set()
    incorrect_guesses = 0
    max_attempts = 6

    print("========================================")
    print("   WELCOME TO HANGMAN GAME (CONSOLE)   ")
    print("========================================\n")

    while incorrect_guesses < max_attempts:
        # Display current stage ASCII art
        print(HANGMAN_PICS[incorrect_guesses])
        
        # Display masked word (e.g. '_ A _ H E O N')
        display_word = [letter if letter in guessed_letters else "_" for letter in secret_word]
        print("\nWord: " + " ".join(display_word))
        print(f"Guessed Letters: {', '.join(sorted(guessed_letters)) if guessed_letters else 'None'}")
        print(f"Remaining Attempts: {max_attempts - incorrect_guesses}\n")

        # Check win condition
        if "_" not in display_word:
            print("🎉 CONGRATULATIONS! YOU WON! 🎉")
            print(f"The secret word was: {secret_word}\n")
            return

        # User Input
        guess = input("Guess a letter: ").strip().upper()

        # Input Validations
        if len(guess) != 1 or not guess.isalpha():
            print(" Invalid input. Please enter a single English letter.\n")
            continue
            
        if guess in guessed_letters:
            print(f" You already guessed '{guess}'. Try another letter!\n")
            continue

        # Process guess
        guessed_letters.add(guess)

        if guess in secret_word:
            print(f" Good guess! '{guess}' is in the word.\n")
        else:
            incorrect_guesses += 1
            print(f" Wrong guess! '{guess}' is not in the word.\n")

    # Defeat screen if max attempts reached
    print(HANGMAN_PICS[max_attempts])
    print("💥 GAME OVER! 💥")
    print(f"You ran out of attempts. The secret word was: {secret_word}\n")

if __name__ == "__main__":
    play_hangman()