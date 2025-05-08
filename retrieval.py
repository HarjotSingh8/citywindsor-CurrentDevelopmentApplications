# tests chunking, retrieval, and referencing the data
import os
import cohere
# import numpy as np
# import re
# import pandas as pd
# from tqdm import tqdm
# from datasets import load_dataset
# import umap
# import altair as alt
# from sklearn.metrics.pairwise import cosine_similarity
# from annoy import AnnoyIndex
# import warnings
# import random
import json

# read file:
file_name = "response.json"
file_path = os.path.join(os.path.dirname(__file__), file_name)
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        data = f.read()
else:
    raise FileNotFoundError(f"File {file_name} not found in the directory {os.path.dirname(__file__)}")

# load json
def load_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data
    

loaded_data = load_json(file_path)
# print(loaded_data)
'''
loaded_data = {
    "pages": [
        {
            "index": 0,
            "markdown": "<page contents in markdown>",
            "images": []
        }
    ]
}
'''

# create chunks from pages
def create_chunks(data, chunk_size = 512, overlap=128):
    chunks = []
    for page in data["pages"]:
        # split the markdown into chunks
        text = page["markdown"]
        # split the text into chunks of size chunk_size
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i+chunk_size]
            chunks.append(chunk)
    return chunks

# create smart chunks
def create_smart_chunks(data, chunk_size=512, overlap=128):
    import re
    chunks = []
    page_numbers = {}
    # for page in data["pages"]:
    for page_number, page in enumerate(data["pages"]):
        text = page["markdown"]
        table_start_pattern = r"(\n\|)"
        table_end_pattern = r"(\|\n(?!\|))"
        
        # Find table starts and ends
        table_starts = [m.start() for m in re.finditer(table_start_pattern, text)]
        table_ends = [m.start() for m in re.finditer(table_end_pattern, text)]
        
        char_index = 0
        i = 0
        j = 0
        # for i in range(len(table_starts)):
        temp_chunks = []
        while i < len(table_starts) and j < len(table_ends):
            
            # Capture non-table text before the current table
            if table_starts[i] > char_index:
                non_table_chunk = text[char_index:table_starts[i]].strip()
                if non_table_chunk:
                    # call create_chunks on the non-table chunk
                    non_table_chunks = create_chunks({"pages": [{"index": page_number, "markdown": non_table_chunk}]}, chunk_size, overlap)
                    for chunk in non_table_chunks:
                        if chunk not in page_numbers:
                            page_numbers[chunk] = []
                        page_numbers[chunk].append(page_number+1)
                    temp_chunks.extend(non_table_chunks)
                    # char_index = table_starts[i]
                # continue
            
            # Capture the table chunk
            start = table_starts[i]
            end = table_ends[j] if j < len(table_ends) else len(text)
            char_index = end + 1
            j += 1
            i += 1
            # check if table_starts[i] is greater than table_ends[j]
            # if not skip table starts until it is
            while i < len(table_starts) and j < len(table_ends) and table_starts[i] < table_ends[j]:
                i += 1
            # add some pre-start context to the table:
            table_chunk = text[start:end+1].strip()
            if table_chunk:
                temp_chunks.append(table_chunk)
        
        # Capture any remaining non-table text after the last table
        if char_index < len(text):
            remaining_chunk = text[char_index:].strip()
            if remaining_chunk:
                # temp_chunks.append(remaining_chunk)
                # call create_chunks on the remaining chunk
                remaining_chunks = create_chunks({"pages": [{"index": page_number, "markdown": remaining_chunk}]}, chunk_size, overlap)
                for chunk in remaining_chunks:
                    if chunk not in page_numbers:
                        page_numbers[chunk] = []
                    page_numbers[chunk].append(page_number+1)
                temp_chunks.extend(remaining_chunks)
        # add page number to each chunk
        for chunk in temp_chunks:
            if chunk not in page_numbers:
                page_numbers[chunk] = []
                page_numbers[chunk].append(page_number+1)
        
        chunks.extend(temp_chunks)

    return chunks, page_numbers

    

chunks = create_chunks(loaded_data)
smart_chunks, page_numbers = create_smart_chunks(loaded_data)
# print sizes of smart chunks
print(f"smart chunks sizes: {[len(chunk) for chunk in smart_chunks]}")
print(f"Number of chunks: {len(chunks)}")
print(f"Number of smart chunks: {len(smart_chunks)}")
# print(smart_chunks)
i = 0
# while True:
#     print(smart_chunks[i])
#     i += 1
#     if i >= len(smart_chunks):
#         break
#     # wait for user input
#     print("---------------------")
#     input("Press Enter to continue...")

def extract_embeddings(chunks):
    import cohere
    model_name = "embed-v4.0"
    api_key = os.getenv("COHERE_API_KEY")
    input_type = 'search_document'
    embedding_types = ['float']
    embedding_dimensions = 1536

    co = cohere.ClientV2(api_key)

    response = co.embed(
        texts = chunks,
        model = model_name,
        input_type = input_type,
        embedding_types=embedding_types,
        output_dimension=embedding_dimensions,
    )

    return response.embeddings.float

# create vector store
def create_vector_store(embeddings, chunks, force_rebuild=False):
    from annoy import AnnoyIndex
    index_file = "testing.ann"
    search_index = AnnoyIndex(1536, "angular")

    if force_rebuild or not os.path.exists(index_file):
        for i, embedding in enumerate(embeddings):
            search_index.add_item(i, embedding)
        search_index.build(10)
        search_index.save(index_file)
    else:
        search_index.load(index_file)

    return search_index

# vector_store = create_vector_store(extract_embeddings(smart_chunks), chunks, force_rebuild=True)
vector_store = create_vector_store(None, None, force_rebuild=False)

# take user input and return the most similar chunk
def get_similar_chunks(query, vector_store, chunks, n=5):
    import numpy as np
    # get the embedding for the query
    query_embedding = extract_embeddings([query])[0]
    # get the top n most similar chunks
    similar_items = vector_store.get_nns_by_vector(query_embedding, n, include_distances=True)
    indices, distances = similar_items
    # get the chunks
    similar_chunks = [chunks[index] for index in indices]
    # also get distances
    return similar_chunks, indices, distances

# get user input
def get_user_input():
    query = input("Enter your query: ")
    return query
import cohere
api_key = os.getenv("COHERE_API_KEY")
co = cohere.ClientV2(api_key)

while True:
    query = get_user_input()
    if query.lower() == "exit":
        break
    chunk = get_similar_chunks(query, vector_store, smart_chunks, 10)
    similar_chunks, indices, distances = chunk
    # get page number from index
    page_number = []
    for index in indices:
        for chunk in smart_chunks:
            if chunk == smart_chunks[index]:
                page_number.append(page_numbers[chunk])
    # print(f"Page number: {page_number}")
    # print(f"Most similar chunk: {similar_chunks[0]}")
    # print(f"distances: {distances}")
    context_string = ""
    documents = []
    for id, chunk in zip(indices, similar_chunks):
        context_string += f"chunk {id}: {chunk}\n"
        documents.append({"id": str(id), "data": chunk})
    response = co.chat(
        model="command-r",
        messages=[
            {"role": "system", "content": "must return any used references inline in the response as [chunkid], do not return output without any reference"},
            {"role": "user", "content": "" + context_string + "\nuser query:" + query}
            # {"role": "user", "content": query}
            ],
        # documents=documents,
    )
    # print the response
    # print(f"Response: {response}")
    # find inline references
    response_text = response.message.content[0].text
    print (f"Response: {response_text}")
    # find inline references
    # references can be single references [0] or multiple [0, 1, 2]
    # references may or may not be separated by spaces, but there will always be a comma if there are multiple references
    references = []
    for i in range(len(response_text)):
        if response_text[i] == "[":
            j = i
            while response_text[j] != "]":
                j += 1
            references.append(response_text[i+1:j])
    # remove duplicates
    # separate references by comma
    references = [ ref.split(",") for ref in references ]
    # convert to int
    references = [int(ref) for sublist in references for ref in sublist]
    references = list(set(references))
    # print the references
    print(references)
