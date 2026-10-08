from langchain_core.runnables import  RunnableLambda
import os 
import mlflow
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage, HumanMessage
import re



load_dotenv()

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Agent Notetaker MOM")
mlflow.autolog()

system_prompt = SystemMessage(
    content="""
        You are an expert in generating professional Minutes of Meeting (MOM) documents. 
        Your goal is to transform raw meeting notes into a structured, clear, and official MOM document.
        You can achieve this goal by:
        1. **Analyzing the input notes** to identify key discussions, decisions, and action items.
        2. **Organizing the information** into standard MOM sections, such as:
            - Meeting Details (Date, Time, Attendees)
            - Discussion Points
            - Decisions Made
            - Action Items (with assigned owners and deadlines)
            - Next Steps
        3. **Ensuring clarity and professionalism** by using clear language, proper formatting, and a formal tone.
        4. use indonesian language for response
    """
)



def filter_text(output):
    text = output["messages"][-1].content
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return text.strip()


llm  = ChatGroq( 
                    model_name="openai/gpt-oss-20b",
                    temperature=0.5,
                    api_key=os.getenv("GROQ_API_KEY"),
                )

agent_MOM = create_agent(
    model= llm,
    name="agent_MOM",
    system_prompt = system_prompt,
    debug=True,
    
    )


agent_MOM = agent_MOM | RunnableLambda(filter_text)

if __name__ == "__main__":
    
    with open("mom_test.txt", "r") as f:
        trascript_mom = f.read()


    with mlflow.start_run(run_name = "test_mom_agent"):
        result = agent_MOM.invoke({
            'messages': [{'role':'user', 'content':trascript_mom}]
        })
        
        print(result)
        
    if not os.path.exists("result"):
        os.makedirs("result")
        
    with open("result/MOM_result.txt", "w", encoding="utf-8") as file:
        file.write(result)
    
    
    


    


