import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
# from langchain.retrievers import DenseRetriever
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process

# Step 1: Load and embed PDF data from the "data" directory


def load_pdf_data(directory="data"):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory, filename)
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
    return documents


pdf_documents = load_pdf_data()

# Step 2: Create vector store for retrieval
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
vectorstore = FAISS.from_documents(pdf_documents, embeddings)

# Create a retriever to use RAG
retriever = DenseRetriever(vectorstore=vectorstore)

# Step 3: Initialize Google Gemini LLM (AI Tutor)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    verbose=True,
    temperature=0.6,
    google_api_key="AIzaSyDbtri1zpDI6a_oruxxaWtxjIL8s-Ua2c4",  # Add your API key here
    request_timeout=30
)

# Step 4: Define the agents

# Tutor Agent for explaining concepts
tutor_agent = Agent(
    role='AI Tutor for explaining concepts and clearing doubts',
    goal="""You are an AI tutor responsible for teaching concepts and helping students understand difficult topics. 
            Use the provided PDF documents to answer questions and provide explanations based on the context of the material.""",
    backstory="""You have helped students understand complex topics by using available study materials.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[retriever]  # Use retriever to fetch context from PDF
)

# Quiz Generator Agent for creating quizzes
quiz_generator_agent = Agent(
    role='AI Quiz Generator',
    goal="""You generate quizzes for students based on the topics covered in the provided PDF documents. The quiz should test 
            students' understanding of the material.""",
    backstory="""You generate quizzes that test students' understanding and are aligned with the context of the study materials.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[retriever]  # Use retriever to fetch context for quiz creation
)

# Quiz Evaluator & Report Generator Agent
quiz_evaluator_agent = Agent(
    role='AI Quiz Evaluator and Report Generator',
    goal="""You evaluate the student's quiz responses based on the material in the PDF documents, providing grades, feedback, 
            and a report card with suggestions for improvement.""",
    backstory="""You help assess student performance and generate detailed feedback based on quiz results.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    tools=[retriever]  # Use retriever to fetch context for evaluation
)

# Function to simulate chat interaction with the agents


def chat_with_agent(agent, prompt):
    task = Task(description=prompt, agent=agent,
                expected_output="Response to user's input.")
    crew = Crew(agents=[agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return result

# Interactive Chat Loop with Seamless Flow


def interactive_chat():
    print("Welcome to the AI Tutor. Let's begin with your learning journey.\n")

    # Starting a chat flow
    while True:
        # Convert input to lowercase for easier matching
        user_input = input("\nYou: ").lower()

        # Tutor helps to explain the concept
        if "explain" in user_input or "help" in user_input or "concept" in user_input:
            response = chat_with_agent(tutor_agent, user_input)
            print(f"AI Tutor: {response}")

            # AI Tutor offers a quiz
            follow_up = input(
                "Would you like to test your understanding with a quiz? (yes/no)\n").lower()
            if "yes" in follow_up:
                response = chat_with_agent(
                    quiz_generator_agent, f"Generate a quiz based on {user_input}")
                print(f"Quiz: {response}")

        # After quiz, evaluating answers and generating a report
        elif "quiz" in user_input:
            answers = input("\nSubmit your quiz answers: ")
            response = chat_with_agent(
                quiz_evaluator_agent, f"Evaluate these answers: {answers}")
            print(f"Evaluation: {response}")

            # After evaluation, offer homework
            follow_up = input(
                "Would you like additional assignments or activities? (yes/no)\n").lower()
            if "yes" in follow_up:
                response = chat_with_agent(
                    tutor_agent, "Generate homework for the student.")
                print(f"Homework: {response}")

        # Gracefully exit conversation
        elif "exit" in user_input or "bye" in user_input:
            print("Exiting... Goodbye!")
            break

        else:
            print("I'm here to help! You can ask for explanations, quizzes, or grades.")


# Run the chat interface
interactive_chat()
