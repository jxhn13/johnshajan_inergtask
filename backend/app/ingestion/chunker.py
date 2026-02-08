from llama_index.core.node_parser import SentenceSplitter

def chunk_text(text: str):
    return SentenceSplitter(chunk_size=512, chunk_overlap=50).split_text(text)
