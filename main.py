from langchain_community.document_loaders.csv_loader import CSVLoader
from create_vector_store import VectorStore
import os

vs = None
if os.path.exists("vec_store"):
    user = input("There's a Vector Store saved, do you want to load it? (Yes/No): ")
else:
    user = "No"
    
if user == "Yes":
    print("fetching saved vector store...")
    vs = VectorStore().vector_store
    print("done...")
elif user == "No":
    file_path = "./data/lds-scriptures.csv"
    cols = ["volume_id",
            "book_id",
            "chapter_id",
            "verse_id",
            "volume_title",
            "book_title",
            "volume_long_title",
            "book_long_title",
            "volume_subtitle",
            "book_subtitle",
            "volume_short_title",
            "book_short_title",
            "volume_lds_url",
            "book_lds_url",
            "chapter_number",
            "verse_number",
            "verse_title",
            "verse_short_title"]

    loader = CSVLoader(file_path=file_path,
                    content_columns=["scripture_text"],
                    metadata_columns=cols
                    )
    data = loader.load()
    print(len(data), "rows in CSV")
    docs = []
    print("creating Document collection...")
    for record in data[0:3]:
        #print(type(record))
        #print(record,"\n")
        record.page_content = record.page_content.strip("scripture_text: ")
        docs.append(record)
        
    #print("docs",docs)
    print("done...")
    print("creating new vector store...")
    vs = VectorStore(create=True).vector_store
    print("adding vectorized documents to Vector Store")
    vs.add_documents(documents = docs)
    print("saving for future use as vec_store")
    vs.dump("./vec_store")
    print("done...")

print("vec store obj",vs)
r = vs.as_retriever()
print("retriever obj",r)
results = r.invoke("In the beginning God created the heaven and the earth.")
for doc in results:
    print(doc.page_content)

sim = vs.similarity_search_with_score("light", k=3)
print(sim)