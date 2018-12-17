from django.shortcuts import render
from django.views import View
from .models import CourseOrg, CityDict


# Create your views here.
class OrganizationView(View):
    def get(self, request):
        org_list = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        category = CourseOrg.objects.values('category').distinct()

        ct = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        if ct:
            org_list = org_list.filter(category=ct)
        if city_id:
            org_list = org_list.filter(address=city_id)
        return render(request, 'organizations/org-list.html',
                      {'org_list': org_list, 'all_citys': all_citys, 'categorys': category, 'ct': ct,
                       'city_id': city_id})

        def post(self, request):
            pass
