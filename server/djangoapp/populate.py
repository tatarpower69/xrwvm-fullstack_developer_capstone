from .models import CarMake, CarModel

def initiate():
    for make, model, kind in [('Toyota', 'Camry', 'SEDAN'), ('Honda', 'CR-V', 'SUV'), ('Ford', 'Explorer', 'SUV')]:
        car_make, _ = CarMake.objects.get_or_create(name=make, defaults={'description': f'{make} vehicles'})
        CarModel.objects.get_or_create(car_make=car_make, name=model, year=2023, defaults={'type': kind})
