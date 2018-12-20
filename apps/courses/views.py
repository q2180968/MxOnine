from django.shortcuts import render
from django.views import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import *


# Create your views here.
class CourseListView(View):
    def get(self, request):
        current_page = 'courses'
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-students')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)
        courses = p.page(page)
        return render(request, 'course/course-list.html',
                      {'courses': courses, 'sort': sort, 'hot_courses': hot_courses, 'current_page': current_page})


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums += 1
        course.save()
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:1]
        else:
            relate_courses = []
        current_page = 'courses'
        return render(request, 'course/course-detail.html',
                      {'current_page': current_page, 'course': course, 'relate_courses': relate_courses})
