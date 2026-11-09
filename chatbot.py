import re
import sys

# Intent response dictionary containing patterns and corresponding answers
INTENT_RESPONSES = [
    {
        'tag': 'greeting',
        'patterns': [r'\b(hi|hello|hey|greetings|good morning|good evening)\b'],
        'responses': [
            "Hello! Welcome to our customer support. How can I help you today?",
            "Hi there! How can I assist you with our products or services?"
        ]
    },
    {
        'tag': 'business_hours',
        'patterns': [r'\b(hours|timing|timings|open|close|working hours|time)\b'],
        'responses': [
            "Our business hours are Monday through Friday, 9:00 AM to 6:00 PM.",
            "We are open Mon-Fri from 9:00 AM to 6:00 PM. Closed on weekends!"
        ]
    },
    {
        'tag': 'product_faq',
        'patterns': [r'\b(product|item|price|cost|buy|purchase|catalog|features)\b'],
        'responses': [
            "You can explore our product catalog on our website or ask me about specific items!",
            "Our products come with a 1-year warranty and free shipping on orders over $50."
        ]
    },
    {
        'tag': 'support_help',
        'patterns': [r'\b(help|support|contact|issue|problem|assist)\b'],
        'responses': [
            "I'm here to help! You can ask me about our business hours, product details, or shipping info.",
            "If you need further human assistance, you can email our support team at support@example.com."
        ]
    },
    {
        'tag': 'shipping_delivery',
        'patterns': [r'\b(shipping|delivery|ship|deliver|track|order status)\b'],
        'responses': [
            "Standard delivery usually takes 3-5 business days.",
            "We offer worldwide shipping. Tracking details are sent via email once your order ships."
        ]
    }
]

# Fallback responses when query confidence/match is low
FALLBACK_RESPONSES = [
    "I'm sorry, I didn't quite catch that. Could you please rephrase?",
    "Hmm, I'm not sure about that. Try asking about our business hours, products, or shipping.",
    "I don't have information on that specific query. Type 'help' to see what I can assist with!"
]

def get_bot_response(user_input):
    """
    Normalizes user input, matches it against intent patterns using regex,
    and returns an appropriate contextual response.
    """
    # 3. Normalize user input (lowercase, strip whitespace)
    normalized_input = user_input.lower().strip()

    # Check each intent pattern using regular expressions
    for intent in INTENT_RESPONSES:
        for pattern in intent['patterns']:
            if re.search(pattern, normalized_input):
                import random
                return random.choice(intent['responses'])

    # 5. Provide graceful fallbacks when query confidence is low
    import random
    return random.choice(FALLBACK_RESPONSES)

def main():
    print("=" * 60)
    print("       RULE-BASED INTERACTIVE TERMINAL ASSISTANT")
    print("=" * 60)
    print("Bot: Hello! I am your virtual assistant.")
    print("     (Type 'bye', 'exit', or 'quit' to end the chat)\n")

    # Conversational State Management loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            # Handle empty inputs
            if not user_input:
                continue

            # 4. Clean exit commands handling
            if user_input.lower() in ['bye', 'exit', 'quit']:
                print("Bot: Thank you for chatting with us. Goodbye!")
                break

            # Get and print bot response
            response = get_bot_response(user_input)
            print(f"Bot: {response}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nBot: Session interrupted. Goodbye!")
            sys.exit(0)

if __name__ == '__main__':
    main()