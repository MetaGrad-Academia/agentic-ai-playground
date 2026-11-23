def process_refund():
    return "To get a refund, please contact our support team with your order details."


def process_exchange():
    return "To process an exchange, please provide your order details and the item you wish to exchange."


def process_return():
    return "To process a return, please provide your order details and the item you wish to return."


def main():
    user_input = input("You: ").strip().lower()

    if "refund" in user_input:
        response = process_refund()
    elif "exchange" in user_input:
        response = process_exchange()
    elif "return" in user_input:
        response = process_return()
    else:
        response = "Sorry, I can only help with refunds, exchanges, or returns."

    print(f"Bot: {response}")


if __name__ == "__main__":
    main()
