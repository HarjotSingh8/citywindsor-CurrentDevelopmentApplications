from openai import OpenAI
from pydantic import BaseModel

class CrewReport(BaseModel):
    id: str
    report: str
    project: str
    relevant: bool
    category: str
    actionable: bool
    actionable_insight: str

class CrewReportResponse(BaseModel):
    reports: list[CrewReport]

client = OpenAI()

# response = client.responses.create(
#   model="gpt-4.1-nano",
#   input=[
#     {
#       "role": "system",
#       "content": [
#         {
#           "type": "input_text",
#           "text": "This GPT transforms user input into a list of optimized search query strings for a Retrieval-Augmented Generation (RAG) system. It is an expert assistant designed to maximize retriever hit rate by crafting precise, context-aware queries. Given minimal or ambiguous input, it infers intent, disambiguates phrasing, and applies domain-specific terminology where applicable.\n\nIt returns only a JSON list of relevant and distinct query strings—concise, high-quality, and tailored for effective retrieval. No additional explanation, formatting, or user interaction is included. The assistant defaults to generating multiple query variants to improve robustness unless otherwise specified. It avoids verbosity, generic phrasing, and low-precision queries. The agent does not introduce placeholders for anything that is ambiguous, it returns strings that can be directly used for a semantic search.\n\nThe output is strictly a flat list of strings in JSON format suitable for direct use in search pipelines."
#         }
#       ]
#     }
#   ],
#   text={
#     "format": {
#       "type": "text"
#     }
#   },
#   reasoning={},
#   tools=[],
#   temperature=1,
#   max_output_tokens=2048,
#   top_p=1,
#   store=True
# )

def query_strings(query):
    response = client.responses.create(
        model="gpt-4.1-nano",
        input=[
            {
            "role": "system",
            "content": [
                {
                "type": "input_text",
                "text": "This GPT transforms user input into a list of optimized search query strings for a Retrieval-Augmented Generation (RAG) system. It is an expert assistant designed to maximize retriever hit rate by crafting precise, context-aware queries. Given minimal or ambiguous input, it infers intent, disambiguates phrasing, and applies domain-specific terminology where applicable.\n\nIt returns only a JSON list of relevant and distinct query strings—concise, high-quality, and tailored for effective retrieval. No additional explanation, formatting, or user interaction is included. The assistant defaults to generating multiple query variants to improve robustness unless otherwise specified. It avoids verbosity, generic phrasing, and low-precision queries. The agent does not introduce placeholders for anything that is ambiguous, it returns strings that can be directly used for a semantic search.\n\nThe output is strictly a flat list of strings in JSON format suitable for direct use in search pipelines."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "input_text",
                "text": query
                }
            ]
            },
        ],
        text={
            "format": {
            "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True
        )
    return response

def crew_report(query):
    # query is a list of strings
    q_string = ""
    for q in query:
        q_string += q + "\n"
    class CrewReport(BaseModel):
        id: str
        report: str
        project: str
        relevant: bool
        category: str
        actionable: bool
        actionable_insight: str

    class CrewReportResponse(BaseModel):
        reports: list[CrewReport]

    response = client.responses.parse(
        model = "gpt-4.1-nano",
        input = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "This GPT transforms user input into a list of optimized search query strings for a Retrieval-Augmented Generation (RAG) system. It is an expert assistant designed to maximize retriever hit rate by crafting precise, context-aware queries. Given minimal or ambiguous input, it infers intent, disambiguates phrasing, and applies domain-specific terminology where applicable.\n\nIt returns only a JSON list of relevant and distinct query strings—concise, high-quality, and tailored for effective retrieval. No additional explanation, formatting, or user interaction is included. The assistant defaults to generating multiple query variants to improve robustness unless otherwise specified. It avoids verbosity, generic phrasing, and low-precision queries. The agent does not introduce placeholders for anything that is ambiguous, it returns strings that can be directly used for a semantic search.\n\nThe output is strictly a flat list of strings in JSON format suitable for direct use in search pipelines."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": q_string
                    }
                ]
            },
        ],
        text_format = CrewReportResponse,
        )
    return response