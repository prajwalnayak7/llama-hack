import mindsdb_sdk
import pandas as pd
import glob
import os
from typing import Optional, List, Dict
import logging
from pathlib import Path
import PyPDF2
import io
import sys

# Set up logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class KnowledgeBaseLoader:
    def __init__(self, host: str = 'http://127.0.0.1:47334'):
        """Initialize the Knowledge Base Loader."""
        try:
            self.server = mindsdb_sdk.connect(host)
            logger.info(f"Successfully connected to MindsDB at {host}")
        except Exception as e:
            logger.error(f"Failed to connect to MindsDB: {str(e)}")
            raise

    def extract_text_from_pdf(self, file_path: str) -> Optional[str]:
        """
        Extract text content from a PDF file with enhanced error handling.
        """
        try:
            with open(file_path, 'rb') as file:
                # Create PDF reader object
                pdf_reader = PyPDF2.PdfReader(file, strict=False)
                
                # Initialize text container
                text_content = []
                
                # Process each page
                for page_num in range(len(pdf_reader.pages)):
                    try:
                        page = pdf_reader.pages[page_num]
                        text = page.extract_text()
                        if text:
                            text_content.append(text)
                        else:
                            logger.warning(f"No text extracted from page {page_num + 1} in {file_path}")
                    except Exception as page_error:
                        logger.warning(f"Error extracting text from page {page_num + 1} in {file_path}: {str(page_error)}")
                        continue
                
                if not text_content:
                    logger.warning(f"No text content extracted from {file_path}")
                    return None
                
                return "\n".join(text_content)

        except Exception as e:
            logger.error(f"Failed to process PDF {file_path}: {str(e)}")
            return None

    def get_or_create_kb(self, kb_name: str) -> mindsdb_sdk.knowledge_bases.KnowledgeBase:
        """Get existing knowledge base or create a new one."""
        try:
            kb = self.server.knowledge_bases.get(kb_name)
            logger.info(f"Found existing knowledge base: {kb_name}")
            return kb
        except Exception:
            logger.info(f"Creating new knowledge base: {kb_name}")
            return self.server.knowledge_bases.create(kb_name)

    def prepare_data_for_insertion(self, text: str, file_path: str) -> Dict:
        """Prepare data in the format expected by MindsDB."""
        return {
            'text': text,
            'metadata': {
                'source': os.path.basename(file_path),
                'type': 'pdf'
            }
        }

    def load_pdfs_to_kb(self, kb_name: str, data_path: str) -> None:
        """Load PDF files into the knowledge base."""
        kb = self.get_or_create_kb(kb_name)
        pdf_files = glob.glob(os.path.join(data_path, '*.pdf'))
        
        if not pdf_files:
            logger.warning(f"No PDF files found in {data_path}")
            return

        total_files = len(pdf_files)
        successful_imports = 0

        for idx, file_path in enumerate(pdf_files, 1):
            try:
                logger.info(f"Processing file {idx}/{total_files}: {file_path}")
                
                # Extract text content
                text_content = self.extract_text_from_pdf(file_path)
                
                if text_content:
                    # Prepare data for insertion
                    data = self.prepare_data_for_insertion(text_content, file_path)
                    
                    # Insert into knowledge base
                    try:
                        kb.insert_files([file_path])
                        # kb.insert(data)
                        successful_imports += 1
                        logger.info(f"Successfully imported content from {file_path}")
                    except Exception as insert_error:
                        logger.error(f"Failed to insert content from {file_path}: {str(insert_error)}")
                else:
                    logger.error(f"No valid text content extracted from {file_path}")
            
            except Exception as e:
                logger.error(f"Failed to process {file_path}: {str(e)}", exc_info=True)
                continue

        logger.info(f"Import complete. Successfully processed {successful_imports}/{total_files} files.")

    def list_knowledge_bases(self) -> List[str]:
        """List all available knowledge bases."""
        try:
            kb_list = self.server.knowledge_bases.list()
            return [kb.name for kb in kb_list]
        except Exception as e:
            logger.error(f"Failed to list knowledge bases: {str(e)}")
            return []

    def drop_knowledge_base(self, kb_name: str) -> bool:
        """Drop a knowledge base."""
        try:
            self.server.knowledge_bases.drop(kb_name)
            logger.info(f"Successfully dropped knowledge base: {kb_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to drop knowledge base {kb_name}: {str(e)}")
            return False

# Example usage
try:
    loader = KnowledgeBaseLoader()
    
    # Load PDFs into knowledge base
    loader.load_pdfs_to_kb('my_kb', './data/')
    
    # List all knowledge bases
    kb_list = loader.list_knowledge_bases()
    logger.info(f"Available knowledge bases: {kb_list}")

except Exception as e:
    logger.error(f"Main execution failed: {str(e)}", exc_info=True)
    sys.exit(1)

