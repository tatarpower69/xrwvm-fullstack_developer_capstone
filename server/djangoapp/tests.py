from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel

class PortalTests(TestCase):
    def test_registration_login_and_logout(self):
        response = self.client.post('/djangoapp/register', data={'userName':'driver','password':'MotorRoad!2026','firstName':'Demo'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.get(username='driver').check_password('MotorRoad!2026'))
        self.assertEqual(self.client.post('/djangoapp/logout').status_code,200)
        self.assertEqual(self.client.post('/djangoapp/login',data={'userName':'driver','password':'wrong'},content_type='application/json').status_code,401)
        self.assertEqual(self.client.post('/djangoapp/login',data={'userName':'driver','password':'MotorRoad!2026'},content_type='application/json').status_code,200)
    def test_review_requires_login_and_csrf(self):
        self.assertEqual(self.client.post('/djangoapp/add_review', data={},content_type='application/json').status_code,401)
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/djangoapp/login',data={},content_type='application/json').status_code,403)
    @patch('djangoapp.views.post_review',return_value={'id':10})
    def test_review_uses_authenticated_author(self, service):
        user=User.objects.create_user('driver',password='MotorRoad!2026')
        self.client.force_login(user)
        response=self.client.post('/djangoapp/add_review',data={'name':'Forged','dealership':1,'review':'Great service','car_year':2023},content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(service.call_args.args[0]['name'],'driver')
    @patch('djangoapp.views.get_request',return_value=[{'id':1,'state':'Kansas'}])
    def test_state_filter(self,service):
        response=self.client.get('/djangoapp/get_dealers/Kansas')
        self.assertEqual(response.json()['dealers'][0]['state'],'Kansas')
        service.assert_called_once_with('fetchDealers/Kansas')
    def test_car_catalog(self):
        make=CarMake.objects.create(name='Toyota')
        CarModel.objects.create(car_make=make,name='Camry',type='SEDAN',year=2023)
        self.assertEqual(self.client.get('/djangoapp/get_cars').json()['CarModels'][0]['CarMake'],'Toyota')
