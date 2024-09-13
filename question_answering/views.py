from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from os import path  # Add this import
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from django.conf import settings

load_dotenv()
#########   LLM Chain     ###############
# Set your OpenAI API key here
api_key = os.getenv("OPENAI_API_KEY")
url = "https://oneapi.gptnb.me/v1"
model = ChatOpenAI(
    #model="claude-3-sonnet-20240229",
    model="gpt-4o",
    #model="gemini-1.5-pro-latest",
    openai_api_key=api_key,
    openai_api_base=url,
)

loader = PyPDFLoader(path.join(settings.BASE_DIR, 'question_answering', 'icluster_user_guide_v9_2_1.pdf'))
mypdf = loader.load()

document_splitter = RecursiveCharacterTextSplitter(
  chunk_size = 300,
  chunk_overlap = 70
)

docs = document_splitter.split_documents(mypdf)

embeddings = OpenAIEmbeddings(
  model="text-embedding-3-large",
  #model="gemini-1.5-pro-latest",
  openai_api_key=api_key,
  openai_api_base=url,
)

persist_directory = 'db'

my_database = Chroma.from_documents(
  documents=docs,
  embedding=embeddings,
  persist_directory=persist_directory
)

retaining_memory = ConversationBufferWindowMemory(
  memory_key='chat_history',
  k=5,
  return_messages=True
)

question_answering = ConversationalRetrievalChain.from_llm(
  llm = model,
  retriever=my_database.as_retriever(),
  memory=retaining_memory
)

# Create your views here.
@csrf_exempt
def answer_question(request):
    if request.method == 'GET':
        question = request.GET.get('question')
        if question:
            answer = question_answering.invoke({"question": question})
            return JsonResponse({'answer': answer['answer']})
        else:
            return JsonResponse({'error': 'No question provided'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

