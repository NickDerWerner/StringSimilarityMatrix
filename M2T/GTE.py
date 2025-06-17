import torch
import torch.nn.functional as F
from transformers import AutoModel, AutoTokenizer
from sentence_transformers.util import cos_sim # Or implement your own cosine similarity


model_path = 'Alibaba-NLP/gte-large-en-v1.5' # English model


print(f"Loading tokenizer from: {model_path}")
tokenizer = AutoTokenizer.from_pretrained(model_path)

print(f"Loading model from: {model_path} (this may take a moment if downloading for the first time)")
model = AutoModel.from_pretrained(model_path, trust_remote_code=True)
model.eval() # Set the model to evaluation mode (good practice)


# 1. Define your two strings
sentences = [
    "You want to build a tree house.",
    "First you collect your requirements,",
    "and send them to a tree house architect.",
    "The architect sends you back a draft,",
    "which you refine multiple times with additional requirements.",
    "You then create the list of needed materials from the plan.",
    "These materials fall into several categories,",
    "you order them from several online stores.",
    "While the order is processed,",
    "you send messages to several of your friends to build the house.",
    "After the house is built,",
    "you send invitations for a tree house party to your friends.",
    "In order to buy the snacks for the party, a list of people that attend the party is created."
]

tasks = [
    "Collect Requirements",
    "Send Requirements to Architect",
    "Architect Sends Draft",
    "Review and Refine Draft",
    "Send Refinements to Architect",
    "Create List of Needed Materials",
    "Order Materials",
    "Await Material Delivery",
    "Contact Friends for Building",
    "Send Party Invitations",
    "Create List of Party Attendees"
]
num_sentences = len(sentences)
num_tasks = len(tasks)


matrix = [[0 for _ in range(num_tasks)] for _ in range(num_sentences)]

def semanticSimilariy(str1,str2):
    # 4. Tokenize the input texts
    # GTE v1.5 supports up to 8192 tokens
    print("Tokenizing texts...")
    input_texts = [str1, str2]  # Prepare the input texts as a list
    batch_dict = tokenizer(input_texts, max_length=8192, padding=True, truncation=True, return_tensors='pt')

    # Optional: Move tokenized inputs to GPU if model is on GPU
    # if torch.cuda.is_available():
    #    batch_dict = {k: v.to('cuda') for k, v in batch_dict.items()}

    # 5. Get the embeddings
    print("Generating embeddings...")
    with torch.no_grad(): # Disable gradient calculations for inference
        outputs = model(**batch_dict)
        # Use the embedding of the [CLS] token (first token)
        embeddings = outputs.last_hidden_state[:, 0]

    # 6. Normalize embeddings for cosine similarity
    # This is important for getting meaningful cosine similarity scores
    embeddings = F.normalize(embeddings, p=2, dim=1)
    print("Embeddings generated and normalized.")

    # 7. Calculate cosine similarity
    # embeddings[0] is the embedding for string1
    # embeddings[1] is the embedding for string2
    similarity_score = cos_sim(embeddings[0].unsqueeze(0), embeddings[1].unsqueeze(0)) # cos_sim expects 2D tensors

    # If you prefer to calculate manually (and have normalized embeddings):
    # similarity_score_manual = torch.matmul(embeddings[0], embeddings[1].T)
    print(f"Cosine Similarity: {similarity_score.item():.4f}")
    return similarity_score.item()  # Return the similarity score as a float


for s in range(num_sentences):
    for t in range(num_tasks):
        x = semanticSimilariy(sentences[s], tasks[t]) 
        matrix[s][t] = x  # Store the similarity score in the matrix
