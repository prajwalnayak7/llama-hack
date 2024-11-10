from dotenv import load_dotenv
load_dotenv("../.env")
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader


def parse_file(file_path):
    """
    Parse a given file into a list of LlamaDocument
    """
    # set up parser
    parser = LlamaParse(
        result_type="text"  # "markdown" and "text" are available
    )

    # use SimpleDirectoryReader to parse our file
    file_extractor = {".pdf": parser}
    documents = SimpleDirectoryReader(input_files=[file_path], file_extractor=file_extractor).load_data()
    return documents

def query_document(file_path, query):
    """
    Parse a given file into a list of LlamaDocument, create an index,
    and query it with the given query
    """
    # one extra dep
    from llama_index.core import VectorStoreIndex

    # get the document
    document = parse_file(file_path)

    # create an index from the parsed markdown
    index = VectorStoreIndex.from_documents(document)

    # create a query engine for the index
    query_engine = index.as_query_engine()

    # query the engine
    response = query_engine.query(query)
    return response

query = "What can you do in the Bay of Fundy?"
response = query_document('data/scenario1.pdf', query)
print(response)
