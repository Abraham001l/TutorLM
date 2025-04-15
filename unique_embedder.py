from sentence_transformers import SentenceTransformer
import numpy as np
import math
# Load the model
model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
model = SentenceTransformer(model_name)

# Define the queries and documents
queries = ['how to do matrix multiplication', 'Where can I get the best tacos?']
documents = ['take the rows of the left matrix and multiply them by the columns of the right matrix', 'you subtract the first row from the second row is a way of performing gaussian reduction']

# Compute embeddings: use `prompt_name="query"` to encode queries!
query_embeddings = model.encode(queries)
document_embeddings = model.encode(documents)

print(query_embeddings.size)
print(document_embeddings.size)

def calculate_cosine_similarity(query_vector, vector):
    return np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))

def calculate_angle(vector1, vector2):
    # Normalize the vectors to unit length
  unit_vector1 = vector1 / np.linalg.norm(vector1)
  unit_vector2 = vector2 / np.linalg.norm(vector2)

  # Calculate the dot product of the unit vectors
  dot_product = np.dot(unit_vector1, unit_vector2)

  # Clip the dot product to ensure it's within the valid range of arccos (-1 to 1)
  clipped_dot_product = np.clip(dot_product, -1.0, 1.0)

  # Calculate the angle in radians using arccos
  angle_radians = np.arccos(clipped_dot_product)

  return angle_radians*(180/(math.pi))

print(calculate_angle(query_embeddings[0], document_embeddings[0]))
print(calculate_angle(query_embeddings[0], document_embeddings[1]))

# Compute cosine similarity scores
scores = model.similarity(query_embeddings, document_embeddings)
print(scores)