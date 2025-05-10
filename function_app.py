import logging
import azure.functions as func
import base64
import fitz  # PyMuPDF
import json

def extract_links_from_pdf(pdf_bytes):
    urls = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            links = page.get_links()
            for link in links:
                if 'uri' in link:
                    urls.append(link['uri'])
    return urls

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing request to extract URLs from PDF.')

    try:
        body = req.get_json()
        base64_pdf = body.get('pdf_base64')

        if not base64_pdf:
            return func.HttpResponse(
                "Missing 'pdf_base64' in request body.",
                status_code=400
            )

        pdf_bytes = base64.b64decode(base64_pdf)
        urls = extract_links_from_pdf(pdf_bytes)

        return func.HttpResponse(
            json.dumps({"urls": urls}),
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error processing PDF: {e}")
        return func.HttpResponse(
            f"Internal server error: {str(e)}",
            status_code=500
        )
