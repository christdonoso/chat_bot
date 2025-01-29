
from pydantic_ai.models.openai import OpenAIModel
from docx import Document
from pydantic_ai import Agent, RunContext
import nest_asyncio


nest_asyncio.apply()

API_KEY = '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'


model = OpenAIModel('gpt-4o', api_key=API_KEY)


agent = Agent(
    model=model,
    system_prompt=(
        'Eres un asistente de un curso, cuya informacion se encuentra en el sylabus del curso'
        'para responder solo puedes utilizar la informacion que te proporciona la funcion get_info'
        'en caso de que te pregunten informacion que no se encuentra en el documento, responde utilizando la funcion skip_message'
    ),
)

@agent.tool
def get_info(ctx: RunContext[str]):
    """
    Lee el contenido de un archivo .docx, incluyendo párrafos y tablas.

    :param ruta_archivo: Ruta al archivo de Word (.docx).
    :return: Contenido completo del archivo como una cadena de texto.
    """
    try:
        # Cargar el documento
        documento = Document('syllabus.docx')

        contenido = []

        # Leer los párrafos
        for parrafo in documento.paragraphs:
            if parrafo.text.strip():  # Evitar líneas vacías
                contenido.append(parrafo.text)

        # Leer las tablas
        for tabla in documento.tables:
            for fila in tabla.rows:
                fila_texto = [celda.text.strip() for celda in fila.cells]
                contenido.append("\t".join(fila_texto))  # Separar celdas con tabulación

        # Unir todo el contenido en un solo texto
        return "\n".join(contenido)

    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return ""


def run_agent(promt:str):
    result_sync = agent.run_sync(
        promt, model_settings={'temperature': 0.0}
        )
    print('respuesta:', result_sync.data)
    print('-'*50)
    return result_sync.data


if __name__ == '__main__':
    while True:
        promt = input('Escribe tu pregunta: ')
        result_sync = agent.run_sync(
            promt, model_settings={'temperature': 0.0}
        )
        print('respuesta:', result_sync.data)
        print('-'*50)