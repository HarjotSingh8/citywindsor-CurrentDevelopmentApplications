import torch
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
def generate_embeddings_fastembed(texts):
    """
    Generate embeddings for a list of texts using FastEmbed.
    
    Args:
        texts (list): List of texts to generate embeddings for.
    
    Returns:
        list: List of embeddings.
    """

    embeddings = FastEmbedEmbeddings(providers=["CUDAExecutionProvider"])
    document_embeddings = embeddings.embed_documents(texts)
    return document_embeddings


def generate_embeddings_cohere(chunks, api_key, input_type='text'):
    """
    Generate embeddings for a list of texts using Cohere API.
    
    Args:
        chunks (list): List of texts to generate embeddings for.
        api_key (str): Cohere API key.
    
    Returns:
        list: List of embeddings.
    """
    import cohere
    import time
    tries = 5
    embeddings = []
    co = cohere.ClientV2(api_key)
    while True:
        tries-=1
        try:
            while i<len(chunks):
                current_chunks = chunks[i:i+96]
                response = co.embed(
                    texts=current_chunks,
                    model="embed-v4.0",
                    input_type=input_type,
                    embedding_types=['float'],
                    output_dimension=1536,
                )
                embeddings.extend(response.embeddings.float)
                i+=96
            return embeddings
        except cohere.error.CohereError as e:
            print(f"Error: {e}")
            if tries == 0:
                raise e
            print("Retrying in 65 seconds...")
            time.sleep(65)