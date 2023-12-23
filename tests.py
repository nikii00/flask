import unittest
import warnings
from customer import app as customer_app
from invoice import app as invoice_app
from items import app as item_app
from job import app as job_app
from order import app as order_app
from task import app as task_app



class CustomerAppTests(unittest.TestCase):
    def setUp(self):
        customer_app.config["TESTING"] = True
        self.app = customer_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getcustomers(self):
        response = self.app.get("/customers")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Powell" in response.data.decode())

    def test_getcustomers_by_id(self):
        response = self.app.get("/customers/2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Chapell" in response.data.decode())

class InvoiceAppTests(unittest.TestCase):
    def setUp(self):
        invoice_app.config["TESTING"] = True
        self.app = invoice_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getinvoice(self):
        response = self.app.get("/invoice")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invoice for plumbing repairs in the kitchen" in response.data.decode())

    def test_getinvoice_by_id(self):
        response = self.app.get("/invoice/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Invoice for plumbing repairs in the kitchen" in response.data.decode())
        
class ItemAppTests(unittest.TestCase):
    def setUp(self):
        item_app.config["TESTING"] = True
        self.app = item_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getitems(self):
        response = self.app.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Electrical rewiring" in response.data.decode())

    def test_getitems_by_id(self):
        response = self.app.get("/items/2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Electrical rewiring" in response.data.decode())
        
        
class JobAppTests(unittest.TestCase):
    def setUp(self):
        job_app.config["TESTING"] = True
        self.app = job_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getjob(self):
        response = self.app.get("/job")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Fence repair and painting" in response.data.decode())

    def test_getjob_by_id(self):
        response = self.app.get("/job/7")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Fence repair and painting" in response.data.decode())
        
        
class OrderAppTests(unittest.TestCase):
    def setUp(self):
        order_app.config["TESTING"] = True
        self.app = order_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_getorder(self):
        response = self.app.get("/order")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cost for patio extension materials" in response.data.decode())

    def test_getorder_by_id(self):
        response = self.app.get("/order/5")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Cost for patio extension materials" in response.data.decode())
        
        
class TaskAppTests(unittest.TestCase):
    def setUp(self):
        task_app.config["TESTING"] = True
        self.app = task_app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_gettask(self):
        response = self.app.get("/task")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Organic optimal attitude" in response.data.decode())

    def test_gettask_by_id(self):
        response = self.app.get("/task/12")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Organic optimal attitude" in response.data.decode())

if __name__ == "__main__":
    unittest.main()
