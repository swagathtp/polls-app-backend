from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question,Tags
from django.shortcuts import get_object_or_404, render,get_list_or_404
from django.db.models import F
from django.urls import reverse
from django.views import generic
import json
from django.http import JsonResponse
from django.core import serializers
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

# class DetailView(generic.DetailView):
#     model = Question
#     template_name = "polls/detail.html"

def increment_poll(request,pk):
    body=json.loads(request.body)
    inc_option=body['incrementOption']
    choice=Choice.objects.get(question_id=pk,choice_text=inc_option)
    print(choice)
    choice.votes +=1
    choice.save()
    response={"msg": "Poll Updated Successfuly","success":True}
    return response

def poll_detail(request,pk):
            print(pk)
            data={}
            polls=Question.objects.filter(id=pk)
            for poll in polls:
                 total_vote=0
                 poll_id=poll.id
                 poll_ques=poll.question_text
                 poll_choice=Choice.objects.filter(question_id=poll_id)
                 tag_choice=Tags.objects.filter(question_id=poll_id)
                 tags=[]
                 for filter_tag in tag_choice:
                      tags.append(filter_tag.tag)
                      print(tags)
                 option_votes={}
                 option_votes={}
                 for choice in poll_choice:
                    choice_text=choice.choice_text
                    choice_vote=choice.votes
                    option_votes[choice_text] = choice_vote
                    total_vote=total_vote+choice_vote
                 data={"Question":poll_ques,"Questionid":poll_id,"Tags":tags,"OptionVote":option_votes,"Totalvote":total_vote}
                 dict={"msg":'Fetched polls Successfully',"data":data,"success":'true'}
            return dict

def polls_manager(request,pk):
     if request.method=='PUT':
          return JsonResponse(increment_poll(request,pk),safe=False)
     elif request.method=='GET':
        return JsonResponse(poll_detail(request,pk),safe=False)



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
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

def get_all_polls(request):
            polls=Question.objects.filter()
            data = serializers.serialize('json',polls)
            question = get_list_or_404(Question)
            data=[]
            for poll in question:
                total_vote=0
                poll_id=poll.id
                poll_ques=poll.question_text
                poll_choice=Choice.objects.filter(question_id=poll_id)
                tag_choice=Tags.objects.filter(question_id=poll_id)
                print(tag_choice)
                tags=[]
                for new_tags in tag_choice:
                    # print(new_tags)
                    tags.append(new_tags.tag)
                    # print(tags)
                option_votes={}
                for choice in poll_choice:
                    choice_text=choice.choice_text
                    choice_vote=choice.votes
                    option_votes[choice_text] = choice_vote
                    total_vote=total_vote+choice_vote
                poll_dict={"Question":poll_ques,"Questionid":poll_id,"OptionVote":option_votes,"Tags":tags,"Totalvote":total_vote}
                data.append(poll_dict)
                dict={"msg":'Fetched polls Successfully',"data":data,"success":'true'}
            return dict

def filter_poll(request):
        filtered_tag=request.GET.get('tags','')
        tag_list=filtered_tag.split(',')
        polls=Question.objects.filter(tags__tag__in=tag_list).distinct()
        data=[]
        for poll in polls:
               total_vote=0
               poll_id=poll.id
               poll_ques=poll.question_text
               poll_choice=Choice.objects.filter(question_id=poll_id)
               tag_choice=Tags.objects.filter(question_id=poll_id)
               tags=[]
               for new_tags in tag_choice:
                   tags.append(new_tags.tag)
               option_votes={}
               for choice in poll_choice:
                   choice_text=choice.choice_text
                   choice_vote=choice.votes
                   option_votes[choice_text] = choice_vote
                   total_vote=total_vote+choice_vote
               poll_dict={"Question":poll_ques,"Questionid":poll_id,"Option Vote":option_votes,"Tags":tags,"Totalvote":total_vote}
               data.append(poll_dict)
               response_dict={"msg":'Fetched polls Successfully',"data":data,"success":'true'}
        return response_dict

def post_polls(request):
            body=json.loads(request.body)
            poll_ques=body.get('Question')
            new_question=Question(question_text=poll_ques)
            new_question.save()
            print(new_question)
            option_votes=body.get('OptionVote')
            for choice_text in option_votes:
                new_choice=Choice(choice_text=choice_text,question=new_question)
                new_choice.save()
            tags=body.get('Tags')
            print(tags)
            for new_tags in tags:
                print(new_tags)
                new_tags=Tags(tag=new_tags,question=new_question)
                new_tags.save()
            response={'msg':"Poll created Successfully","success":True}
            return response


def polls_controller(request):
    if request.method =='POST':
        return JsonResponse(post_polls(request),safe=False,)
    
    elif "tags" in request.GET:
        result=filter_poll(request)
        return JsonResponse(result,safe=False)
    else:
        return JsonResponse(get_all_polls(request),safe=False)

def get_tags_list(request):
     print("HI")
     filter_tag=Tags.objects.all()
     data = serializers.serialize('json',filter_tag)
     load_data=json.loads(data)
     filtered_tag=[]
     for tags in load_data:
      tag_value=tags['fields']['tag']
      if tag_value not in filtered_tag:
           filtered_tag.append(tag_value)
     print(tag_value)
     return filtered_tag


def tags_manager(request):
     tag_list=[]
     tag_list=get_tags_list(request)
     return JsonResponse(tag_list,safe=False)