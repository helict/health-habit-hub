from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

sentences = [
    "ich müde bin",
    "müde bin",
    "wenn ich müde bin",
    "mache ich Atemübungen",
    "Immer wenn",
    "Immer wenn ich müde bin"
]

embeddings = model.encode(sentences, convert_to_tensor=True)

similarity_matrix = util.cos_sim(embeddings, embeddings)

print("Cosine Similarity Matrix:")
for i in range(len(sentences)):
    for j in range(len(sentences)):
        print(f"Sim({sentences[i]} , {sentences[j]}) = {similarity_matrix[i][j]:.4f}")
