from django.shortcuts import render
from django.views import View
from .models import CourseOrg, CityDict, Teacher
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from django.http import HttpResponse, JsonResponse
from operation.models import UserFavorite
from courses.models import Course


# Create your views here.
class OrganizationView(View):
    def get(self, request):
        org_list = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        category = CourseOrg.objects.values('category').distinct()
        hot_org = CourseOrg.objects.order_by("-click_nums")[0:3]
        current_page = 'org_list'

        ct = request.GET.get('ct', '')
        city_id = request.GET.get('city', '')
        sort = request.GET.get('sort', '')
        if ct:
            org_list = org_list.filter(category=ct)
        if city_id:
            org_list = org_list.filter(address=city_id)
        if sort:
            if sort == 'students':
                org_list = org_list.order_by('-students')
            elif sort == 'courses':
                org_list = org_list.order_by('-course_nums')

        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(org_list, 3, request=request)
        org_page = p.page(page)
        return render(request, 'organizations/org-list.html',
                      {'org_list': org_page, 'all_citys': all_citys, 'categorys': category, 'ct': ct,
                       'city_id': city_id, 'sort': sort, 'page': page, 'hot_org': hot_org,
                       'current_page': current_page})


class UserAskView(View):
    def post(self, request):
        user_askform = UserAskForm(request.POST)
        if user_askform.is_valid():
            user_ask = user_askform.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '添加出错'})


class OrgDetailHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        org = CourseOrg.objects.get(id=org_id)
        org.click_nums += 1
        org.save()
        all_course = org.course_set.all()[:3]
        all_teacher = org.teacher_set.all()[:3]

        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                is_fav = True
        return render(request, 'organizations/org-detail-homepage.html',
                      {'org': org, 'current_page': current_page, 'all_course': all_course, 'all_teacher': all_teacher,
                       'is_fav': is_fav})


class OrgDetailCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        org = CourseOrg.objects.get(id=org_id)
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                is_fav = True
        return render(request, 'organizations/org-detail-course.html',
                      {'current_page': current_page, 'org': org, 'is_fav': is_fav})


class OrgDetailTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        org = CourseOrg.objects.get(id=org_id)
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                is_fav = True
        return render(request, 'organizations/org-detail-teachers.html',
                      {'current_page': current_page, 'org': org, 'is_fav': is_fav})


class OrgDetailDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        org = CourseOrg.objects.get(id=org_id)
        is_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org.id, fav_type=2):
                is_fav = True
        return render(request, 'organizations/org-detail-desc.html',
                      {'current_page': current_page, 'org': org, 'is_fav': is_fav})


class AddFavView(View):
    def post(self, request):
        fav_id = int(request.POST.get('fav_id', 0))
        fav_type = int(request.POST.get('fav_type', 0))
        if not request.user.is_authenticated():
            return JsonResponse({'status': 'fail', 'msg': '用户未登陆'})
        exist_records = UserFavorite.objects.filter(fav_id=fav_id, fav_type=fav_type)
        if exist_records:
            exist_records.delete()
            # 课程
            if fav_type == 1:
                course = Course.objects.get(id=fav_id)
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            # 机构
            if fav_type == 2:
                course_org = CourseOrg.objects.get(id=fav_id)
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0:
                    course_org.fav_nums = 0
                course_org.save()
            # 教师
            if fav_type == 3:
                teacher = Teacher.objects.get(id=fav_id)
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return JsonResponse({'status': 'success', 'msg': '收藏'})
        else:
            user_fav = UserFavorite()
            if fav_id > 0 and fav_type > 0:
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                # 课程
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums += 1
                    course.save()
                # 机构
                if fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums += 1
                    course_org.save()
                # 教师
                if fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums += 1
                    teacher.save()
                return JsonResponse({'status': 'success', 'msg': '已收藏'})
            else:
                return JsonResponse({'status': 'fail', 'msg': '收藏出错'})
