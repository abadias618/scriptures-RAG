from langchain import hub
from typing_extensions import List, TypedDict
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings


# Define state for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
# prompt from hub looks like this:
'''
human

You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
'''
class Flow:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        # TODO: build better prompt focused on scriptures
        self.prompt = hub.pull("rlm/rag-prompt")

    # Define application steps
    def retrieve(self, state: State):
        retrieved_docs = self.vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}
    
    def generate(self, state: State):
        # TODO: include sources of where we got the answer from
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = self.prompt.invoke({"question": state["question"], "context": docs_content})
        response = self.llm.invoke(messages)
        return {"answer": response.content}
    
    def build_graph(self):
        graph_builder = StateGraph(State).add_sequence([self.retrieve, self.generate])
        graph_builder.add_edge(START, "retrieve")
        graph = graph_builder.compile()
        return graph