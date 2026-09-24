def chunk_text(
    text: str,
    tokenizer,
    chunk_size: int = 350,
    overlap: int = 50
) -> list[dict]:
    
    tokens = tokenizer.encode(text)
    step = chunk_size - overlap  # el "salto" que calculamos recién
    
    chunks = []
    start = 0
    chunk_index = 0  # ← nuevo contador, arranca en 0

    while start < len(tokens):
        chunk_tokens = tokens[start:start + chunk_size]
        chunk_str = tokenizer.decode(chunk_tokens)
        chunks.append({
            "text": chunk_str,
            "chunk_index": chunk_index,
            "start": start,
            "end": start + len(chunk_tokens),
            "length": len(chunk_tokens),
        })
        start += step
        chunk_index += 1  # ← incrementar el contador acá

    return chunks


if __name__ == "__main__":
    from sentence_transformers import SentenceTransformer
    import sys
    import os

    sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
    from src.chunking.extractor import extract_text_from_pdf

    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    texto = extract_text_from_pdf("data/raw_papers/2506.06962v3.pdf")

    resultado = chunk_text(texto, model.tokenizer, chunk_size=350, overlap=50)

    print(f"Total de chunks generados: {len(resultado)}")
    print(f"\nPrimer chunk:\n{resultado[0]}")
    print(f"\nÚltimo chunk:\n{resultado[-1]}")