prompt1 = \
'''
User:

You are an assistant for question-answering tasks related to a set of religious scripture text.
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three or four sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
'''

# Prompt from hub looks like this: hub.pull("rlm/rag-prompt")

prompt_from_hub = \
'''
human

You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
'''