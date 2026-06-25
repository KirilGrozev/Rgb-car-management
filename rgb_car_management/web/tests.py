import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rgb_car_management.settings')
django.setup()

from rgb_car_management.web.models import CarIssueCategory, CarProblem

#CarIssueCategory(1, 'Спирачна система').save()
#CarIssueCategory(2, 'Окачване на колелата').save()
#CarIssueCategory(3, 'Стартова система').save()
#CarIssueCategory(4, 'Запалителна система').save()
#CarIssueCategory(5, 'Друго', True).save()

# CarProblem(1, 1, 'Накладки').save()
# CarProblem(2, 1, 'Спирачни дискове').save()
# CarProblem(3, 1, 'Спирачен апарат').save()
# CarProblem(4, 1, 'Спирачен барабан').save()
# CarProblem(5, 2, 'Амортисьори').save()
# CarProblem(6, 2, 'Пружини').save()
# CarProblem(7, 2, 'Въздушно окачване').save()
# CarProblem(8, 2, 'Сфера').save()
# CarProblem(9, 3, 'Алтернатор').save()
# CarProblem(10, 3, 'Стартер').save()
# CarProblem(11, 3, 'Бендикс').save()
# CarProblem(12, 4, 'Запалителна свещ').save()
# CarProblem(13, 4, 'Комутатор').save()
# CarProblem(14, 4, 'Подгревна свещ').save()
# CarProblem(15, 4, 'Запалителна бобина').save()

