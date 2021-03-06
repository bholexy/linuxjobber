import subprocess, json, os
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django import template as temp#, forms
from django.views import generic
from django.conf import settings

#################################################
#    IMPORTS FROM WITHIN Linuxjobber APPLICATION  #
from .models import GradesReport, Course, CourseTopic
from .forms import *
from .utils.djangolabsutils import grade_django_lab

register = temp.Library()


""" Dummy method for listing courses """
def courses(request):
    if not request.user.is_authenticated:
        return redirect("home:login")
    courses = Course.objects.all()
    context ={
            'courses': courses     
            }
    return render(request, 'courses/courses.html', context)


"""
     View for listing all topics on a particular course 
    Here we use the course name as passed in the url to obtain the course topics, by applying the Django models relationship manager
"""
class CourseTopicsView(generic.ListView):
    template_name = 'courses/topics.html'
 
    def get_queryset(self):
        return CourseTopic.objects.filter(course__course_title = self.kwargs.get('course_name').replace("_", " "))
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(course_title = self.kwargs.get('course_name').replace("_", " "))
        return context


"""
    View for presenting topic detail (Video), with a link to the lab (where the tasks are listed)
    As in the topics listing view, we also use the manager here to obtain the specific topic,
        using the topic number provided and the course name
"""
def topicdetails(request, course_name, lab_no):
    context ={
            'topic': CourseTopic.objects.get(course__course_title = course_name.replace("_"," "),topic_number = lab_no)
            }
    return render(request, 'courses/topic_detail.html', context)


"""
    internal method for obtaining the list of accessible instances. Returns a list of all available instances, or an emtpy list if none
"""
def get_active_instances():
    return ['34.145.168.21','34.145.128.1']


"""
    internal method for instantiating the submission form for each lab.
    Uses the course topic and user information provided, to Instantiate the form
"""
def get_gradingform(course_topic, user_obj):
    submit_typ = course_topic.course.lab_submission_type
    form = None
    if submit_typ == 1:
        form = DocumentGradingForm()
    elif submit_typ == 2:
        # For this submission type, we need to obtain a list of instances, set the field widget type to select, set the select's options to the ip addresses returned.
        # If no instance was found to be available, display message "No instances found! Enter IP address"
        form = MachineGradingForm({'machine': '',
                                   'user_id': user_obj.id})
#         form.fields['machine'].widget = forms.Select(choices=(
#         (1, 'submit by uploading document'),
#         (2, 'submit by machine ID'),
#         (3, 'submit from repo')
#     ))
    else:
        form = MachineGradingForm({'machine': user_obj.email,
                                   'user_id': user_obj.id})
        form.fields['machine'].widget = HiddenInput()
        form.fields['machine'].label = "User_email"
    return form


"""
    View for presenting the labtasks, with a provision for submiting the labs.
    Accepts the course name and lab_number, and uses these two parameters to obtain the labID. Using the labID obtained, it queries the list of tasks.
"""
class LabDetailsView(generic.DetailView):
    template_name = 'courses/tasks.html'
    
    def get_object(self):
        return get_object_or_404(CourseTopic, course__course_title = self.kwargs.get('course_name').replace("_", " "),topic_number = self.kwargs.get('lab_no'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = get_gradingform(context['coursetopic'], self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Here we process the user's information, by calling application to do actual grading. Then we render the results gotten from the database
        data = request.POST
        topic = self.get_object()
        course = topic.course.course_title.split()[0].upper()
        topic_id = str(topic.id)
        topic_slug = topic.lab_name
        user_ID = request.POST.get('user_id')#dict.get(user_id, False)#str(data['user_id'])
        user_Add = request.POST.get('machine')#data['machine']
        sub_type = topic.course.lab_submission_type
        if sub_type == 1:
            form = DocumentGradingForm(request.POST, request.FILES)
            if not form.is_valid():
                return HttpResponseBadRequest("Invalid Request")
            new_upload = form.save(commit = False)
            new_upload.user = request.user
            new_upload.course_topic = topic
            form.save()
            output = grade_django_lab(request.FILES['document'], topic.topic_number, request.user)                
            if output == 'Failed':
                return HttpResponse("Result: " + output +" \n <a href='/courses/Django/labs/"+str(topic.topic_number)+"/'>Click here to try again</a>")
            else:
                return HttpResponse(output)
        elif sub_type == 2:
            # GraderServer "machine" data['machine'] "sysadmin" topic_id course data['user_id']
            command = [ settings.BASE_DIR+"/Courses/utils/GraderServer.py","machine",user_Add, "sysadmin", topic_id, course, user_ID ]
            subprocess.check_call(command, stderr=subprocess.STDOUT, bufsize=-1)
            handle_rslts(settings.BASE_DIR+"/Courses/utils/"+user_Add,request.user,topic)
        else:
            # /path/to/where/GraderServer.py "repo" course topic_id topic_slug data['user_id'] user_IP 
            command = [ settings.BASE_DIR+"/Courses/utils/GraderServer.py","repo", course, topic_id, topic_slug, user_ID, user_Add ]
            subprocess.check_call(command, stderr=subprocess.STDOUT, bufsize=-1)
            handle_rslts(settings.BASE_DIR+"/Courses/utils/"+user_Add,request.user,topic)
        result = GradesReport.objects.filter(user = data['user_id'], course_topic = topic_id,)
        course_top = get_object_or_404(CourseTopic, pk=int(topic_id))
        return render(request, 'courses/result.html',{'result':result,'coursetopic':course_top})


"""
    Internal method for handling result.
"""
def handle_rslts(obj,userr,topic):
    with open(obj,"r") as f:
        data = json.load(f)
    user_id = data.pop('userID') # will use this for logging
    lab_id = data.pop('lab_id') # will use this for logging
    for elem in data:
        try:
            record = GradesReport.objects.get(task_no = elem, course_topic = topic)
            record.grade = data[elem]
            record.save()
        except GradesReport.DoesNotExist:
            GradesReport(user=userr, course_topic = topic,score = 0, task_no = elem,grade= data[elem]).save()
    os.remove(obj)

