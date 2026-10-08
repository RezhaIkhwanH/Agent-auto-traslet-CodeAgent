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
mlflow.set_experiment("Agent Voice Translation")
mlflow.autolog()

system_prompt = SystemMessage(
    content="""
        You are a professional translator for voice transcripts.
        Translate the user's transcript into natural, accurate Indonesian.
        Detect the source language automatically, preserve the original meaning and tone,
        and do not summarize, add details, or format the response as meeting minutes.
        Return only the translated text.
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

voice_translate_agent = create_agent(
    model= llm,
    name="voice_translate_agent",
    system_prompt = system_prompt,
    debug=True,
    
    )


voice_translate_agent = voice_translate_agent | RunnableLambda(filter_text)

if __name__ == "__main__":
    
    with open("voice_transcript.txt", "r", encoding="utf-8") as f:
        voice_transcript = f.read()


    with mlflow.start_run(run_name = "test_voice_translation"):
        result = voice_translate_agent.invoke({
            'messages': [{'role':'user', 'content':voice_transcript}]
        })
        
        print(result)
        
    if not os.path.exists("result"):
        os.makedirs("result")
        
    with open("result/voice_translation.txt", "w", encoding="utf-8") as file:
        file.write(result)
    
    
    


    


