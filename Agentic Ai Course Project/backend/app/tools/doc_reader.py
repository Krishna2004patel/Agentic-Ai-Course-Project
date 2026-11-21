import os
from typing import Dict, Any

class DocumentReaderTool:
    """Safe document extractor supporting PDF, DOCX, TXT, and Markdown files."""
    
    @staticmethod
    def read_document(file_path: str, max_chars: int = 15000) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"success": False, "error": f"File does not exist: {file_path}"}
        
        ext = os.path.splitext(file_path)[1].lower()
        extracted_text = ""
        
        try:
            if ext == ".txt" or ext == ".md":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()
                    
            elif ext == ".pdf":
                try:
                    import pypdf
                    reader = pypdf.PdfReader(file_path)
                    pages_text = []
                    for i, page in enumerate(reader.pages):
                        t = page.extract_text()
                        if t:
                            pages_text.append(f"--- Page {i+1} ---\n{t}")
                    extracted_text = "\n".join(pages_text)
                except Exception as pe:
                    return {"success": False, "error": f"PDF extraction error: {pe}"}
                    
            elif ext in (".docx", ".doc"):
                try:
                    import docx
                    doc = docx.Document(file_path)
                    extracted_text = "\n".join([p.text for p in doc.paragraphs if p.text])
                except Exception as de:
                    # Fallback to zipfile XML parsing
                    import zipfile, xml.etree.ElementTree as ET
                    with zipfile.ZipFile(file_path) as z:
                        xml_content = z.read('word/document.xml')
                        tree = ET.fromstring(xml_content)
                        paragraphs = []
                        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
                            texts = [node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text]
                            if texts:
                                paragraphs.append(''.join(texts))
                        extracted_text = '\n'.join(paragraphs)
            else:
                # Attempt plain text read
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    extracted_text = f.read()

            truncated = len(extracted_text) > max_chars
            final_text = extracted_text[:max_chars]

            return {
                "success": True,
                "file_path": file_path,
                "file_type": ext,
                "character_count": len(extracted_text),
                "is_truncated": truncated,
                "text": final_text
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
