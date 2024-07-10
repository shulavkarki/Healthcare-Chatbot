import os
import json
# import pinecone
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# from sample_scrape import clean_text

DATASET_DIR = "dataset:v1"
#pinecone
API_KEY = "682f1c01-2320-4587-8355-c634f690d723"
pc = Pinecone(api_key=API_KEY)
index = pc.Index("healthcare-chatbot")

#sentence transformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    replacements = {
        "\n": " ",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2014": "--",
        "\"": "'",
        "ç": "c",
        "è": "e",
        "ü": "u",
        "é": "e",
        "ö": "o",
        
    }
    
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text

def main():
    for filename in os.listdir(DATASET_DIR):
        if filename.endswith('.json'):
            file_path = os.path.join(DATASET_DIR, filename)
            
            #read dataset
            with open(file_path, 'r') as json_file:
                dataset = json.load(json_file)
                # Do something with the dataset
            
            print(f"{filename} reading...")
            
            for disease_name in dataset:
                print(f"{disease_name} indexing...", end='\r')  # Print indexing message and overwrite on the same line
                for j in dataset[disease_name]:
                    for idx, question in enumerate(dataset[disease_name][j]):
                        if question == "source":
                            continue
                        data = {}
                        data["id"] = f"{clean_text(disease_name)}_{j}{idx}"
                        data["values"] = model.encode(dataset[disease_name][j][question]).tolist()
                        data["metadata"] = {}
                        data["metadata"]["title"] = clean_text(question)
                        data["metadata"]["content"] = dataset[disease_name][j][question]
                        data["metadata"]["source"] = dataset[disease_name][j]["source"]
                        
                        #index pinecone
                        try:
                            index.upsert(
                                [data]
                            )
                        except Exception as e:
                            print(f"Error while indexing {disease_name}")
                    
                print(f"{disease_name} indexed!")
            print("___")    
if __name__ == "__main__":
    main()