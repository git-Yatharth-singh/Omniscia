import os
from ingestion.pdf_loader import extract_images,load_pdf
import pytest
import pymupdf


def test_image_extraction():
    images = extract_images(
        "data/documents/omniscIa_chart_test.pdf"
    )

    assert len(images) > 0, "No images were extracted from the test PDF."

    for image in images:
        assert os.path.exists(image["path"]), (
            f"Extracted image file does not exist: {image['path']}"
        )


def test_invalid_pdf():
    with pytest.raises(ValueError, match="Could not process PDF"):
        load_pdf("data/documents/this_file_does_not_exist.pdf")




def test_empty_pdf(tmp_path):
    empty_pdf = tmp_path / "empty.pdf"

    with pymupdf.open() as document:
        document.new_page()
        document.save(str(empty_pdf))

    # Create a valid PDF containing a blank page.
    with pytest.raises(ValueError, match="no extractable text"):
        load_pdf(str(empty_pdf))

