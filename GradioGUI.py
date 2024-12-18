import gradio as gr


class GradioGUI:
    def __init__(self, graph):
        self.graph = graph
    
    def question(self, message, history):
        response = self.graph.invoke({"question": message})
        return response["answer"]
    
    def launch_gui(self):
        demo = gr.ChatInterface(
            fn=self.question, 
            type="messages",
            title="Scriptures RAG",
            description="You can ask anything pretty much, but the bot will only respond to things that are related to LDS scripture",
            theme="ocean"
        )

        demo.launch()