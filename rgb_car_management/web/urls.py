from django.urls import path

from rgb_car_management.web.views import CreateCar, EditCar, \
    DeleteCar, CreateCustomer, EditCustomer, DeleteCustomer, AcceptedCars, IssuedCars, Customers, CreateAcceptedCar, \
    EditAcceptedCar, DeleteAcceptedCar, CreateIssuedCar, EditIssuedCar, DeleteIssuedCar, Cars, Register, Login, Logout, \
    HomeRedirect, AcceptedCarPdf, IssuedCarPdf, ProblemsJsonView, AcceptedIssuesJsonView, AcceptedCarDetails, \
    IssuedCarDetails

urlpatterns = [
    path('', HomeRedirect.as_view(), name='home redirect'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('accepted-cars/', AcceptedCars.as_view(), name='accepted cars'),
    path('issued-cars/', IssuedCars.as_view(), name='issued cars'),
    path('cars/', Cars.as_view(), name='cars'),
    path('customers/', Customers.as_view(), name='customers'),
    path('create/accepted-car/', CreateAcceptedCar.as_view(), name='create accepted car'),
    path('accepted-car-details/<int:pk>/', AcceptedCarDetails.as_view(), name='accepted car details'),
    path('edit/accepted-car/<int:pk>/', EditAcceptedCar.as_view(), name='edit accepted car'),
    path('delete/accepted-car/<int:pk>/', DeleteAcceptedCar.as_view(), name='delete accepted car'),
    path('create/issued-car/', CreateIssuedCar.as_view(), name='create issued car'),
    path('issued-car-details/<int:pk>/', IssuedCarDetails.as_view(), name='issued car details'),
    path('edit/issued-car/<int:pk>/', EditIssuedCar.as_view(), name='edit issued car'),
    path('delete/issued-car/<int:pk>/', DeleteIssuedCar.as_view(), name='delete issued car'),
    path('create/car/', CreateCar.as_view(), name='create car'),
    path('edit/car/<int:pk>/', EditCar.as_view(), name='edit car'),
    path('delete/car/<int:pk>/', DeleteCar.as_view(), name='delete car'),
    path('create/customer/', CreateCustomer.as_view(), name='create customer'),
    path('edit/customer/<int:pk>/', EditCustomer.as_view(), name='edit customer'),
    path('delete/customer/<int:pk>/', DeleteCustomer.as_view(), name='delete customer'),
    path('priem/<int:pk>/pdf/', AcceptedCarPdf.as_view(), name='accepted car pdf'),
    path('izdavane/<int:pk>/pdf/', IssuedCarPdf.as_view(), name='issued car pdf'),
    path('api/problems/', ProblemsJsonView.as_view(), name='problems json'),
    path('api/accepted-issues/', AcceptedIssuesJsonView.as_view(), name='accepted issues json'),
]
