# # In utils.py

# from transformers import BertModel, BertTokenizer
# import torch
# from sklearn.metrics.pairwise import cosine_similarity

# tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
# model = BertModel.from_pretrained('bert-base-multilingual-cased')

# def encode(text):
#     encoded_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128)
#     with torch.no_grad():
#         model_output = model(**encoded_input)
#     return model_output.pooler_output.numpy()  # Convert to numpy array

# import numpy as np

# # def calculate_similarity(text1, text2):
# def calculate_semantic_similarity(text1, text2):
#     embedding1 = encode(text1)
#     embedding2 = encode(text2)

#     # Compute cosine similarity manually
#     similarity_score = np.dot(embedding1.flatten(), embedding2.flatten()) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
    
#     return similarity_score


# text1 = "Hello, how are you?"
# text2 = "Hi there! I'm doing well, thank you."

# # Calculate similarity between text1 and text2
# similarity_score = calculate_semantic_similarity(text1, text2)
# print("Similarity Score:", similarity_score)





# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# def calculate_similarity(text1, text2):
#     # Tokenize the input texts
#     vectorizer = CountVectorizer().fit_transform([text1, text2])
#     vectors = vectorizer.toarray()

#     # Calculate the cosine similarity between the vectors
#     similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    
#     return similarity
# text1 = "This is a sample annotation"
# text2 = "This is another sample annotation"

# similarity_score = calculate_similarity(text1, text2)
# print("Similarity Score:", similarity_score)
