import ollama
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from prompt_template import PromptTemplate
#setup
API_KEY = ""
INDEX_NAME = "healthcare-chatbot"


pc = Pinecone(api_key=API_KEY)
index = pc.Index(INDEX_NAME)

sent_model = SentenceTransformer('all-MiniLM-L6-v2')

    # You are an expert Doctor/Physician chatbot. You'll be asked question regarding different diseases and health related issues. 
    # Consider the given information/context below to answer the user question. Also if the question is not health related then reply with "Cannot process the query.".

def get_prompt(contexts, question):    
    template = f"""
    {PromptTemplate.template_v3}
    Context:{contexts}
    Question:{question}
    Answer: 
    """
    return template

def get_relevant_results(query):
    query_vector = sent_model.encode(query).tolist()

    rel_content = index.query(
        # namespace="example-namespace",
        vector=query_vector,
        top_k=3,
        include_metadata=True
    )
    contexts = [item['metadata']['content'] for item in rel_content['matches']]
    sources = [item['metadata']['source'] for item in rel_content['matches']]
    # print(" ".join(contexts))
    return " ".join(contexts), sources

def generate_response(query):
    contexts, source = get_relevant_results(query)
    prompt = get_prompt(contexts, query)
    # print(source)
    res = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return res["message"]["content"], source

