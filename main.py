from langchain_community.document_loaders.csv_loader import CSVLoader
from csv_constants import csv_columns, csv_simplified_columns
from create_vector_store import VectorStore
from GradioGUI import GradioGUI
from flow import Flow
import os


vs = None
while True:
    if os.path.exists("vec_store"):
        user = input("There's a Vector Store saved, do you want to load it?\n \
            Yes (load vec_store file)\n \
            No (re-create vec_store):\n --> ")
        if user not in ["Yes","No"]:
            print("Please enter Yes/No")
            continue
    else:
        user = "No"
    break
    
if user == "Yes":
    print("fetching saved vector store...")
    vs = VectorStore().vector_store
    print("done...")
elif user == "No":
    file_path = "./data/lds-scriptures.csv"

    loader = CSVLoader(file_path=file_path,
                    content_columns=["scripture_text"],
                    metadata_columns=csv_simplified_columns
                    )
    data = loader.load()
    print(len(data), "rows in CSV")
    docs = []
    print("creating Document collection...")
    # FOR SOME REASON ONLY BATCHED ADDING WORKS
    # otherwise Segmentation fault (core dumped) ERROR
    # TODO: Fix hardcoded values
    for fold in [(0,10000),(10000,20000),(20000,30000),(30000,40000),(40000,41996)]:
        sub_doc = []
        for record in data[fold[0]:fold[1]]:
            record.page_content = record.page_content.strip("scripture_text: ")
            sub_doc.append(record)
        docs.append(sub_doc)
        
    print(len(docs),"docs in collection ready to add to vecstore.") 
    #print("docs",docs)
    print("done...")
    print("creating new vector store...")
    vs = VectorStore(create=True).vector_store
    print("adding vectorized documents to Vector Store")
    for d in docs:
        print("adding fold")
        vs.add_documents(documents = d)
    print("saving for future use as vec_store")
    vs.dump("./vec_store")
    print("done...")

# Test similarity search
#sim = vs.similarity_search_with_score("Faith is like a seed", k=10)
#for doc in sim:
#    print(sim.page_content, sim.metadata.get(verse_title))

flow = Flow(vs)
graph = flow.build_graph()
gui = GradioGUI(graph)
gui.launch_gui()

#response = graph.invoke({"question": "What do I need to do to attain Salvation?"})
#print(response["answer"])