from langchain_core.prompts import PromptTemplate
from .prompt import AUTISM_PROMPT_CHATBOT, SUICIDE_CHECK_PROMPT
from langchain_core.output_parsers import StrOutputParser
from .llm import gemini_llm
from .tools import send_alert_email
from .database import store_chat_history, get_chat_history

def conversation_chain(llm):
    """To get the Conversation Stage"""
    prompt = PromptTemplate(
        template= AUTISM_PROMPT_CHATBOT,
        input_variables= [
                "name",
                "age",
                "conversation_history",
                "hobbies",
                "gender",
                "user_input",
                "level"
        ]
    )

    chain = prompt | llm | StrOutputParser()

    return chain


def conversation_chain_mail(llm):
    """To get the Conversation Stage"""
    prompt = PromptTemplate(
        template= SUICIDE_CHECK_PROMPT,
        input_variables= [
                "user_input",
                "conversation_history"
             
        ]
    )

    chain = prompt | llm | StrOutputParser()

    return chain



def get_response(name = "", age = "", hobbies = "", level = "", gender = "", user_input = "", conversation_history=""):

    chain = conversation_chain(gemini_llm())
    try:
        response = chain.invoke({
                "name" : name,
                "age" : age,
                "hobbies" : hobbies,
                "level" : level,
                "gender"  : gender,
                "user_input" : user_input,
                "conversation_history" : conversation_history
                })

        return response
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_response_mail(user_input = "", conversation_history=""):

    chain = conversation_chain_mail(gemini_llm())
    try:
        response = chain.invoke({
                "user_input" : user_input,
                "conversation_history" : conversation_history
                })

        return response
    except Exception as e:
        return f"Error: {str(e)}"



user_input = "" 

if __name__ == "__main__":
    while True:
        conversation_history = get_chat_history("ram@gmail.com")
        print(conversation_history)
        response_mail = get_response_mail(conversation_history)
        print(f"Response Mail : {response_mail}")
        if(response_mail == "yes"):
            print(send_alert_email("bignya18@gmail.com","ram", conversation_history))
          
    
        response = get_response("ram", "34" , "cubing", "3", "MALE", conversation_history)
        print(f"Autism Chatbot: {response}")
        

        user_input = input("User : ")

        store_chat_history("ram@gmail.com", user_input, response)


     
