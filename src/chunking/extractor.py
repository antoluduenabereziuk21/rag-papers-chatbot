import fitz
import pymupdf

MIN_BLOCK_LENGTH = 100  # filtra bloques cortos tipo watermarks/headers

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = pymupdf.open(pdf_path)
    paragraphs = []

    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            # acá va el filtro: ¿qué condición decide si "text" se agrega a paragraphs?
            if len(text) >= MIN_BLOCK_LENGTH:
                paragraphs.append(text)
    doc.close()
    return "\n\n".join(paragraphs)


if __name__ == "__main__":
    texto = extract_text_from_pdf("data/raw_papers/2506.06962v3.pdf")  # o el id de PDF que tengas
    print(texto[:1000])  # primeros 1000 caracteres, para no inundar la terminal
    print(f"\n\nTotal de caracteres extraídos: {len(texto)}")