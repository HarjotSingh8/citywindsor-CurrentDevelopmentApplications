import os
import cohere
def query(message, documents=None, history=[], model="command-a-03-2025", system_prompt=None):
    model = "command-r"
    """
    Query the Cohere API with a message and conversation history.
    """
    # Initialize the Cohere client with the API key
    co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))
    messages = []
    # Add the system prompt to the messages if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    # Add the conversation history to the messages
    for role, content in history:
        messages.append({"role": role, "content": content})
    print(messages)
    # Add the current message to the messages
    messages.append({"role": "user", "content": message})
    # print("yolo")
    # print(messages)
    # print(documents)
    if documents is not None:
        response = co.chat(
            model=model,
            messages=messages,
            documents=documents,
        )
    else:
        response = co.chat(
            model=model,
            messages=messages
        )
    try:
        references = [
            source.id
            for citation in response.message.citations
            for source in citation.sources
        ]
        citation_range = [
            (citation.start, citation.end)
            for citation in response.message.citations
        ]
    except Exception as e:
        print(f"Error: {e}")
        references = []
        citation_range = []
    markdown_text = response.message.content[0].text
    return response, markdown_text, references, citation_range