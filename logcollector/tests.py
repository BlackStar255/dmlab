from django.test import TestCase
from django.core.urlresolvers import reverse
from logcollector.models import Log

# Create your tests here.
class TestPostRequest(TestCase):
    def test_created_valid_log_entry(self):
        request_body = {'timestamp': 1, 'dim1': 1, 'dim2': 1, 'value':3}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 201)
        
    def test_created_invalid_log_entry_with_missing_parameter(self):
        request_body = {'timestamp': 1, 'dim1': 1, 'value':3}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 400)
        
    def test_created_invalid_log_entry_with_wrong_timestamp_type(self):
        request_body = {'timestamp': 'a', 'dim1': 1, 'dim2': 1, 'value':3}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 400)    
    
    def test_created_invalid_log_entry_with_wrong_dim1_type(self):
        request_body = {'timestamp': 1, 'dim1': 'a', 'dim2': 1, 'value':3}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 400)    

    def test_created_invalid_log_entry_with_wrong_dim2_type(self):
        request_body = {'timestamp': 1, 'dim1': 1, 'dim2': 'a', 'value':3}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 400)    

    def test_created_invalid_log_entry_with_wrong_value_type(self):
        request_body = {'timestamp': 1, 'dim1': 1, 'dim2': 1, 'value': 'a'}
        response = self.client.post('/log/', request_body)
        self.assertEqual(response.status_code, 400)
        

class TestDatabase(TestCase):
    def setUp(self):
        Log(timestamp=1, dim1=1, dim2=1, value=1).save()
        Log(timestamp=2, dim1=1, dim2=2, value=2.5).save()
        Log(timestamp=3, dim1=2, dim2=1, value=3).save()
        Log(timestamp=4, dim1=2, dim2=2, value=4.5).save()
        

class TestGetRequestErrors(TestCase):

    def test_not_exisiting_timestamp_paramters(self):
        response = self.client.get('/log/')
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_t1_type(self):
        response = self.client.get('/log/?t1=alma&t2=3')
        self.assertEqual(response.status_code, 400)
    
    def test_invalid_t2_type(self):
        response = self.client.get('/log/?t1=1&t2=alma')
        self.assertEqual(response.status_code, 400)
 
    def test_exisiting_timestamp_paramteres_missing_method(self):
        response = self.client.get('/log/?t1=1&t2=3')
        self.assertEqual(response.status_code, 400)
    
    def test_exisiting_timestamp_paramteres_invalid_method(self):
        response = self.client.get('/log/?t1=1&t2=3&method=alma')
        self.assertEqual(response.status_code, 400)        


class TestMax(TestDatabase):    
         
    def test_result_is_float(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Max')
        self.assertEqual(float(response.content),4.5)
        self.assertEqual(response.status_code,200)

    def test_valid_max_request_without_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Max')
        self.assertEqual(response.content, "4.5")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_max_request_with_dim1_without_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Max&dim1=1')
        self.assertEqual(response.content, "2.5")
        self.assertEqual(response.status_code, 200)

    def test_valid_max_request_without_dim1_with_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Max&dim2=2')
        self.assertEqual(response.content, "4.5")
        self.assertEqual(response.status_code, 200)
        
    def test_valid_max_request_with_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Max&dim1=2&dim2=1')
        self.assertEqual(response.content, "3.0")
        self.assertEqual(response.status_code, 200)
        

class TestMin(TestDatabase):       

    def test_valid_min_request_without_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Min')
        self.assertEqual(response.content, "1.0")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_min_request_with_dim1_without_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Min&dim1=1')
        self.assertEqual(response.content, "1.0")
        self.assertEqual(response.status_code, 200)

    def test_valid_min_request_without_dim1_with_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Min&dim2=2')
        self.assertEqual(response.content, "2.5")
        self.assertEqual(response.status_code, 200)
        
    def test_valid_min_request_with_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Min&dim1=2&dim2=1')
        self.assertEqual(response.content, "3.0")
        self.assertEqual(response.status_code, 200)

class TestAvg(TestDatabase):       

    def test_valid_avg_request_without_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Avg')
        self.assertEqual(response.content, "2.75")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_avg_request_with_dim1_without_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Avg&dim1=1')
        self.assertEqual(response.content, "1.75")
        self.assertEqual(response.status_code, 200)

    def test_valid_avg_request_without_dim1_with_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Avg&dim2=2')
        self.assertEqual(response.content, "3.5")
        self.assertEqual(response.status_code, 200)
        
    def test_valid_avg_request_with_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=Avg&dim1=2&dim2=1')
        self.assertEqual(response.content, "3.0")
        self.assertEqual(response.status_code, 200)
        
class TestStdDev(TestDatabase):       

    def test_valid_stddev_request_without_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=StdDev')
        self.assertEqual(response.content, "1.25")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_stddev_request_with_dim1_without_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=StdDev&dim1=1')
        self.assertEqual(response.content, "0.75")
        self.assertEqual(response.status_code, 200)

    def test_valid_stddev_request_without_dim1_with_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=StdDev&dim2=2')
        self.assertEqual(response.content, "1.0")
        self.assertEqual(response.status_code, 200)
        
    def test_valid_stddev_request_with_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=StdDev&dim1=2&dim2=1')
        self.assertEqual(response.content, "0.0")
        self.assertEqual(response.status_code, 200)
        
class TestMvgAvg(TestDatabase):       

    def test_valid_mvgavg_request_without_n_parameter(self):
        response = self.client.get('/log/?t1=1&t2=4&method=MvgAvg')
        self.assertEqual(response.status_code, 400)

    def test_valid_mvgavg_request_without_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=MvgAvg&n=2')
        self.assertEqual(response.content, "3.33333333333333")
        self.assertEqual(response.status_code, 200)
    
    def test_valid_mvgavg_request_with_dim1_without_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=MvgAvg&dim1=1&n=2')
        self.assertEqual(response.content, "2.5")
        self.assertEqual(response.status_code, 200)

    def test_valid_mvgavg_request_without_dim1_with_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=MvgAvg&dim2=2&n=2')
        self.assertEqual(response.content, "3.5")
        self.assertEqual(response.status_code, 200)
        
    def test_valid_mvgavg_request_with_dim1_dim2(self):
        response = self.client.get('/log/?t1=1&t2=4&method=MvgAvg&dim1=2&dim2=1&n=2')
        self.assertEqual(response.content, "3.0")
        self.assertEqual(response.status_code, 200)
           
        
        
        
