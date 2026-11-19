
from openai import OpenAI
import numpy as np

def cosine_similarity(vector_a, vector_b):
    a = np.array(vector_a)
    b = np.array(vector_b)

    dot_product = np.dot(a, b)

    magnitude_a = np.linalg.norm(a)
    magnitude_b = np.linalg.norm(b)

    return dot_product / (magnitude_a * magnitude_b)


client = OpenAI()

errors = [
    "Loan API returned HTTP 503",
    "Loan service is temporarily unavailable",
    "Customer email address is invalid"
]

response = client.embeddings.create(
    model = 'text-embedding-3-small',
    input = errors
)
embeddings = [items.embedding for items in response.data]

# for i,embedding in enumerate(embeddings):
#     print (i+1,f"{len(embedding)} dimensions")

similarity = cosine_similarity(response.data[0].embedding,response.data[2].embedding)
print(similarity)
    
