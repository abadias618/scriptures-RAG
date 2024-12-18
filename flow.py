from langchain import hub
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from prompts import prompt1


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


class Flow:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.prompt = PromptTemplate.from_template(prompt1)

    # Define application steps
    def retrieve(self, state: State):
        # kinda have to tune 'k', defaults to 4 but I think 10 is better
        retrieved_docs = self.vector_store.similarity_search(state["question"],k=10)
        return {"context": retrieved_docs}
    
    def generate(self, state: State):
        # TODO: include sources of where we got the answer from
        docs_content = "\n\n---\n\n".join(doc.page_content + 
                                          "\n\nThis verse is in " + 
                                          doc.metadata.get("volume_title") + 
                                          ", specifically in " + 
                                          doc.metadata.get("verse_title") 
                                          for doc in state["context"])
        # DEBUG to print the context
        #print("CONTEXT\n",docs_content)
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        sources = [doc.metadata.get("verse_title") for doc in state["context"]]
        return {"answer": response.content + "\nSOURCES:\n" + "\n".join(sources)}
    
    def build_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        return graph