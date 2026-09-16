import asyncio
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "Sos un asistente útil."),
    ("human", "{pregunta}"),
])

modelo = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0,
)

parser = StrOutputParser()

chain= prompt | modelo | parser

async def main() -> None:
    respuesta = await chain.ainvoke({
        "pregunta": "¿Qué es Python?"
    })

    print(respuesta)


if __name__ == "__main__":
    asyncio.run(main())