import pymupdf
import os
import fitz

def load_pdf(pdf_path):

    pages = []
    table_records = []

    try:
        with pymupdf.open(pdf_path) as document:
            if document.page_count == 0:
                raise ValueError("PDF contains no pages.")

            for page_number, page in enumerate(document):
                page_number = page_number+1
                text = page.get_text().strip()
                tables = page.find_tables().tables

                for table_index, table in enumerate(tables):
                    table_data = table.extract()

                    table_text = "\n".join(
                        " | ".join(str(cell or "") for cell in row)
                        for row in table_data
                    )

                    table_record = {
                        "document": pdf_path.split("/")[-1],
                        "page": page_number,
                        "table_id": f"page_{page_number}_table_{table_index + 1}",
                        "text": table_text
                    }

                    table_records.append(table_record)
                if not text:
                    print(f"Warning: Page {page_number} contains no extractable text. Skipping.")
                    continue
                page_data = {
                    "page": page_number,
                    "text": text
                }
                pages.append(page_data)

    except Exception as e:
        raise ValueError(f"Could not process PDF: {e}") from e

    if not pages:
        raise ValueError("PDF contains no extractable text.")

    return pages, table_records

def extract_images(pdf_path):
    output_dir = "data/extracted_images"
    os.makedirs(output_dir, exist_ok=True)

    extracted_images = []

    with fitz.open(pdf_path) as doc:
        for page_index, page in enumerate(doc):
            images = page.get_images(full=True)
            for image_index, image_info in enumerate(images):
                xref = image_info[0]
                image_data = doc.extract_image(xref)
                image_bytes = image_data["image"]
                image_ext = image_data["ext"]
                filename = (
                f"page_{page_index + 1}_"
                f"image_{image_index + 1}.{image_ext}"
                            )
                image_path = os.path.join(output_dir, filename)
                with open(image_path, "wb") as image_file:
                    image_file.write(image_bytes)

                    extracted_images.append({
                        "image_id": f"page_{page_index + 1}_image_{image_index + 1}",
                        "page": page_index + 1,
                        "path": image_path,
                        "extension": image_ext
                    })

    return extracted_images