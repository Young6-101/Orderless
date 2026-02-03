from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text(text: str, chunk_size=500, chunk_overlap=50):
    """
    将长文本切成小块。
    chunk_size: 每一块的大小（500字左右适合找逻辑）
    chunk_overlap: 每一块之间重复一部分，防止逻辑被切断
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    return splitter.split_text(text)