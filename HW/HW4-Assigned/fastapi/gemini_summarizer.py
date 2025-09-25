import json

from google import genai
from google.genai import types

from user_definition import *


def return_gemini_summary(qualification: dict) -> list:
    """
    For the given qualification dictionary (outuput from
    retreive_google_career_qualification() and
    retreive_meta_career_qualification()),
    call Google GenAI API with the system instruction.
    See https://ai.google.dev/gemini-api/docs/text-generation
    for how to configure to add
    system instructions.
    This function should return a list of nouns that summarize
    the qualification.
    """
    system_instruction = """
    From the given dictionary formatted string,
    summarize technical skills in the values as a noun.
    For example,
    {"Minimum Qualification":
    ["7 years of experience leading technical project strategy,
    ML design, and optimizing ML infrastructure
    (e.g., model deployment, model evaluation, data processing,
    debugging, fine tuning).",
    "5 years of experience with one or more of the following:
    Speech/audio (e.g., technology duplicating and responding
    to the human voice), reinforcement learning
    (e.g., sequential decision making),
    ML infrastructure, or specialization in another ML field."]}
    This should be represented as an array of string
    ["Python", "Machine Learning Engineering", "MLOps", "MLFlow",
    "Generative AI", "Langchain", "Pinecone", "Machine Learning",
    "Scikit-Learn", "Reinforcement Learning"]
    What you need to provide is just a string formatted array, not codes.
    It would be desirable to provide tools or algorithms
    that are relevant to requirements.
    """
