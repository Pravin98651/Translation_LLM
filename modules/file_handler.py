from typing import Optional
import docx
import PyPDF2
import io

class FileHandler:
    @staticmethod
    def extract_text_from_file(file, file_type: str) -> Optional[str]:
        """
        Extract text from uploaded file based on its type.
        
        Args:
            file: The uploaded file object
            file_type: The type of file (txt, docx, pdf)
            
        Returns:
            Extracted text or None if extraction fails
        """
        try:
            if file_type == 'txt':
                return file.getvalue().decode('utf-8')
                
            elif file_type == 'docx':
                doc = docx.Document(io.BytesIO(file.getvalue()))
                return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
                
            elif file_type == 'pdf':
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
                text = []
                for page in pdf_reader.pages:
                    text.append(page.extract_text())
                return '\n'.join(text)
                
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            print(f"Error extracting text from file: {str(e)}")
            return None 