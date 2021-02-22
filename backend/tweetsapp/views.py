from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

###############################
# Django Rest Framework views
###############################

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.Post)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.object.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({'message': 'Tweet Removed!'}, status = 200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, tweet_id, *args, **kwargs):
    '''
    id is required
    action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists():
            return Response({}, status=400)
        obj = qs.first()
        if action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            obj.likes.remove(request.user)
        elif action == 'retweet':
            parent_obj = obj
            new_tweet = Tweet.objects.create(user = request.user, parent = parent_obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=200)
        return Response({}, status=200)
    
################################
# Pure Django views 
################################

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        if next_url != None:
            return redirect(next_url)
        form = TweetForm
    return render(request, 'components/form.html', context={"form": form})

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)
    
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    
    data = {
        "id": tweet_id
    }
    status = 200
    
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not Found!"
        status = 404
    
    return JsonResponse(data, status=status)

def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{"id": x.id, "content": x.content} for x in qs]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)
