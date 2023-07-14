from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
import requests
import json
def form_req(request):
    template='polls/forms.html'
    content={'val':'he','questions':None}
    if request.method=='GET':
        print("in get :")
        return render(request,template,content)
    print(request.method)
    if request.method == 'POST':
        print("in post :")
        content['val']=request.POST['the choice']
        content['questions']=Question.objects.filter(choice__choice_text=content['val'])
        print(content["questions"])
        res=requests.get('https://api.geoapify.com/v1/geocode/search?city={}&format=json&apiKey=d0f637b5187e487196dd3d9504742ecf'.format(content['val']))
        dict_res=res.json()
        '''print(dict_res.keys(),dict_res)
        for key in dict_res.keys():
            print(type(dict_res[key]))
        for data in dict_res['results'][0]:
            print(data,'\n',type(data))'''
        lat=dict_res['results'][0]['lat']
        lon=dict_res['results'][0]['lon']
        print(lat,lon)
        return render(request,template,content)
        '''print(type(request.POST),'req')
        res=request.POST
        key=res.keys()
        value=res.values()
        res=dict(zip(list(res.keys())[1:],list(res.values())[1:]))
        return JsonResponse(res)
        print(json.dumps(request))
        print(request.POST)
        return HttpResponse(f"jghyu{json.dumps(request.POST)}")'''
        
    #return render(request,'polls/forms.html')
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        '''"""Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]
        '''
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    """
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from .models import Choice, Question
from django.urls import reverse
# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
'''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
    

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

    """