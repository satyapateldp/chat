import unittest
from io import BytesIO
import json
from app import app


class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        """Create a test client and setup for tests."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        """Test the index page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'PDF QA Chatbot', response.data)

    def test_ask_question(self):
        """Test the /ask endpoint with a sample question and PDF."""
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Title (Sample PDF)\n>>\nendobj\n2 0 obj\n<<\n/Type /Catalog\n/Pages 3 0 R\n>>\nendobj\n3 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [4 0 R]\n>>\nendobj\n4 0 obj\n<<\n/Type /Page\n/Parent 3 0 R\n/MediaBox [0 0 612 792]\n/Contents 5 0 R\n>>\nendobj\n5 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 24 Tf\n100 700 Td\n(Hello, World!) Tj\nET\nendstream\nendobj\nxref\n0 6\n0000000000 65535 f \n0000000015 00000 n \n0000000061 00000 n \n0000000104 00000 n \n0000000154 00000 n \n0000000219 00000 n \ntrailer\n<<\n/Size 6\n/Root 2 0 R\n>>\nstartxref\n287\n%%EOF\n'

        data = {
            'question': 'What is your education ?',
            'pdf_file': (BytesIO(pdf_content), 'SatyawanPatelPython2years.pdf')
        }

        response = self.app.post('/ask', data=data, content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('answer', response_data)
        self.assertEqual(response_data['answer'], 'Sample PDF')

    def test_no_pdf_file(self):
        """Test the /ask endpoint with no PDF file uploaded."""
        data = {'question': 'What is the title of the PDF?'}
        response = self.app.post('/ask', data=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'No PDF file uploaded')

    def test_no_question(self):
        """Test the /ask endpoint with no question provided."""
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Title (Sample PDF)\n>>\nendobj\n'
        data = {
            'pdf_file': (BytesIO(pdf_content), 'SatyawanPatelPython2years.pdf')
        }
        response = self.app.post('/ask', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'No question provided')

if __name__ == '__main__':
    unittest.main()
