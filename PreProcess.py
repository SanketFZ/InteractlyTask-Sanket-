import re
import pandas as pd
from sentence_transformers import SentenceTransformer

import faiss
import numpy as np

# Load the pre-trained SentenceTransformer model for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the Excel file
file_path = 'RecruterPilot candidate sample input dataset.xlsx'
df_candidates = pd.read_excel(file_path, sheet_name='candidate_profiles',engine='openpyxl')

# Clean and preprocess the data as before
def clean_text(text):
    if isinstance(text, str):
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
    return text

df_candidates['Name'] = df_candidates['Name'].apply(clean_text)
df_candidates['Contact Details (email)'] = df_candidates['Contact Details (email)'].apply(clean_text)
df_candidates['Location'] = df_candidates['Location'].apply(clean_text)
df_candidates['Job Skills'] = df_candidates['Job Skills'].apply(clean_text)
df_candidates['Projects'] = df_candidates['Projects'].apply(clean_text)
df_candidates['Comments'] = df_candidates['Comments'].apply(clean_text)
df_candidates['Experience'] = df_candidates['Experience'].apply(lambda x: int(re.search(r'\d+', x).group()))

# Generate embeddings for the candidate job skills
candidate_embeddings = model.encode(df_candidates['Job Skills'].tolist())


# Initialize a FAISS index for cosine similarity
d = candidate_embeddings.shape[1]  # Dimension of the embeddings
index = faiss.IndexFlatL2(d)  # Using L2 distance (Euclidean distance)

# Normalize the embeddings for cosine similarity
candidate_embeddings = candidate_embeddings / np.linalg.norm(candidate_embeddings, axis=1, keepdims=True)

# Add embeddings to the index
index.add(candidate_embeddings)

# Check if the index contains all embeddings
print(f"Number of vectors in the index: {index.ntotal}")


def find_candidates(job_description, top_k=10):
    # Generate embeddings for the job description
    job_embedding = model.encode([job_description])
    job_embedding = job_embedding / np.linalg.norm(job_embedding, axis=1, keepdims=True)

    # Search for the top_k most similar candidates
    distances, indices = index.search(job_embedding, top_k)
    
    # Retrieve the candidate profiles
    candidates = []
    for idx in indices[0]:
        candidate = df_candidates.iloc[idx]
        candidates.append({
            'Name': candidate['Name'],
            'Email': candidate['Contact Details (email)'],
            'Location': candidate['Location'],
            'Job Skills': candidate['Job Skills'],
            'Experience': candidate['Experience'],
            'Projects': candidate['Projects'],
            'Comments': candidate['Comments']
        })
    
    return candidates

# # Example usage
# job_description = "Python, Machine Learning, Cloud"
# matched_candidates = find_candidates(job_description)

# # Display matched candidates
# for candidate in matched_candidates:
#     print(f"Name: {candidate['Name']}")
#     print(f"Skills: {candidate['Job Skills']}")
#     print(f"Experience: {candidate['Experience']} years")
#     print(f"Projects: {candidate['Projects']}")
#     print(f"Comments: {candidate['Comments']}\n")