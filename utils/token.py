import tiktoken

def count_tokens(text: str, model: str) -> int:
    """
    Calculate the number of tokens in a given text using the specified model's encoding.

    Args:
        text (str): The input text to be tokenized.
        model (str): The model name for which to calculate tokens.

    Returns:
        int: The number of tokens in the input text.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    return len(tokens)