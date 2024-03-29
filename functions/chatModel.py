import os, logging, sys
from llama_index.core import (
    VectorStoreIndex,
    ServiceContext,
)
from llama_index.core.indices.query.query_transform.base import (
    StepDecomposeQueryTransform,
)
from llama_index.core.query_engine.multistep_query_engine import (
    MultiStepQueryEngine,
)
from llama_index.llms.openai import OpenAI
from llama_index.readers.file import PyMuPDFReader
from dotenv import load_dotenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()
OpenAI.api_key = os.environ['OPENAI_API_KEY']
gpt4 = OpenAI(temperature=0.9, model='gpt-4')
gpt3 = OpenAI(temperature=0.9, model='gpt-3.5-turbo-0125')

class Model():
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_index(self):
        loader = PyMuPDFReader()
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f'The file \'{self.file_path}\' does not exist.')
        documents = loader.load(file_path=self.file_path)

        service_context = ServiceContext.from_defaults(chunk_size=1024, chunk_overlap=0, llm=gpt3)

        index = VectorStoreIndex.from_documents(
            documents, service_context=service_context
        )
        return index

    def query(self, index, prompt: str, summary_of_data: str):
        step_decompose_transform = StepDecomposeQueryTransform(llm=gpt3, verbose=True)

        service_context = ServiceContext.from_defaults(llm=gpt3)
        query_engine = index.as_query_engine(service_context=service_context)

        query_engine = MultiStepQueryEngine(
            query_engine=query_engine,
            query_transform=step_decompose_transform,
            index_summary=summary_of_data,
        )

        query_response = query_engine.query(prompt)

        return query_response.response

