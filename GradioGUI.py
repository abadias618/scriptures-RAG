import gradio as gr
import datetime

class GradioGUI:
    def __init__(self, graph):
        self.graph = graph
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"./saved_chats/chat_history_{timestamp}.txt"
        
    def format_logs(self, log: list):
        result = ("-" * 20) + "\n"
        result += log[0].get("role") + " : " + log[0].get("content") + "\n\n"
        result += log[1].get("role") + " : " + log[1].get("content") + "\n" 
        return result
    
    def question(self, message, history):
        if len(history) > 0:
            log = self.format_logs([history[len(history)-2],
                                    history[len(history)-1]])
            
            with open(self.filename, "a") as file:
                file.write(log)
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