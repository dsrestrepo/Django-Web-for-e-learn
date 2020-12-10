from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, Course, Test, TestData, Comment, Message, Movies
from django.core.paginator import Paginator


import pandas as pd
import os
from gensim.test.utils import common_texts
from gensim.models.word2vec import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
import string


def index(request):
    return render(request,'finalProject/index.html',{
    })

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "finalProject/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "finalProject/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "finalProject/register.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "finalProject/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "finalProject/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

#Couses description
course_description={
        'Statistics': 'The statistics course is an interactive course where you will learn obout topics like:  <ul><li>statistical inference</li><li>Probability</li><li>Linear Algebra</li><li>Regressions </ul>',
        'Computer Science': 'Computer Science course is an interactive course where you will learn obout topics like:<ul><li>Intro to CS</li><li>Programming Basics theory</li><li>Programming Basics python</li><li>UML diagrams</li></ul>',
        'Data Science': 'Data Science course is an interactive course where you will learn obout topics like: <ul><li>R Programming</li><li>Python Programming</li><li>Artificial Inteligence</li><li>Machine Learning</li></ul>',
        'Communications': 'Communications course is an interactive course where you will learn obout topics like:<ul><li>Telecomunicatios Theory</li><li>Information Theory</li><li>Digital Communications</li><li>Analogic Communications</li></ul>',
        'Social': 'A Movie Recommender System that uses: <ul> <li>Colaborative filtering</li>    <li>Content Based</li>    <li>Movie Leans</li>    <li>Buil in python</li></ul>'
}
#course answers
answers_final={
    'Statistics': ['1','2','3','4','5'],
    'Computer Science': ['1','2','3','4','5'],
    'Data Science': ['1','2','3','4','5'],
    'Communications': ['1','2','3','4','5']
}

def course(request, cname):    
    #see if course exist
    try:
        course = Course.objects.get(course_name=cname)
    except Course.DoesNotExist:
        course = False
    #if course exist
    if course:
        #see if user is logged
        if request.user.is_authenticated:
            user = request.user
            #user is logged see if user is in course
            try:
                in_course = course.users.get(username=user)
            except User.DoesNotExist:
                in_course = False
            final_test = False
            #if user is in course see if user has done the final test
            if in_course:
                try:
                    final_test = Test.objects.get(user=user, test_version='3',course=course)
                except Test.DoesNotExist:
                    final_test = False
        #if user is not logged just show the course information
        else:
            in_course = True
            final_test = False
    #course doesn't exist, create the course
    else:
        course = course = Course.objects.create(course_name = cname, description=course_description[cname])
        final_test = False

        #if user is not logged just show the course information
        if request.user.is_authenticated:
            in_course = False
        else:
            in_course = True
    print(in_course)
    print(final_test)

    #pagination:
    #take the comments
    posts = course.comments.all()
    total_posts = posts.order_by("-timestamp").all()
    paginator = Paginator(total_posts, 10) # Show 10 post per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'finalProject/course.html',{
        "cname":cname,
        "in_course":in_course,
        "final_test":final_test,
        "page_obj":page_obj,
        "total_posts": total_posts
    })


@login_required
def make_test(request):
    if request.method == "POST":
        # Attempt to upload test
        user = request.user
        course_name = request.POST["course"]
        version = request.POST["version"]
        question1 = request.POST["question1"]
        question2 = request.POST["question2"]
        question3 = request.POST["question3"]
        question4 = request.POST["question4"]
        question5 = request.POST["question5"]
        question6 = request.POST["question6"]
        #takes the course instance in the model Course
        try:
            course = Course.objects.get(course_name = course_name)
        except Course.DoesNotExist:
            course = Course.objects.create(course_name = course_name, description=course_description[course_name])
        #see if is the register test
        if version == '1':
            #add the user to course
            course.users.add(user)
        #Register the test
        test = Test.objects.create(test_version = version, user = user, course = course,result=5)
        #Register the results of the test
        TestData.objects.create(test = test, question1= question1,question2= question2,question3= question3,question4= question4,question5= question5,question6=question6)
        return HttpResponseRedirect(reverse('course', args = (course_name,)))


@login_required
def profile(request,username):
    #get the user og the profile to show
    user=User.objects.get(username=username)
    #get the courses of this user
    try:
        courses = Course.objects.filter(users=user)
    except Course.DoesNotExist:
        courses = None
    #get the tests of this user
    try:
        test = Test.objects.filter(user=user)
    except Test.DoesNotExist:
        test= None
    #if we have test order in inverse order of how were done
    if test:
        test = test.order_by("-id").all()
    #take the posts of the user
    posts = user.posts.all()
    total_posts = posts.order_by("-timestamp").all()
    paginator = Paginator(total_posts, 10) # Show 10 post per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    #Take the messages for the user
    messages = user.messages.all()
    messages = messages.order_by("-timestamp").all()
    return render(request,'finalProject/profile.html',{
        'courses':courses,
        'user':user,
        'page_obj': page_obj,
        'tests':test,
        'messages': messages
    })


@csrf_exempt
@login_required
def test(request):
    # get the post data
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        user = request.user
        course_name = data.get("course", "")
        version = data.get("version", "")
        question1 = data.get("question1", "")
        question2 = data.get("question2", "")
        question3 = data.get("question3", "")
        question4 = data.get("question4", "")
        question5 = data.get("question5", "")
        question6 = data.get("question6", "")
        #get the course
        try:
            course = Course.objects.get(course_name = course_name)
        except Course.DoesNotExist:
            course = Course.objects.create(course_name = course_name, description=course_description[course_name])
        #see if is the register test
        if version == '1':
            #add the user to course
            course.users.add(user)
        #calcule the result from 0 to 5:
        questions=[question1,question2,question3,question4,question5,question6]
        result=0
        if version == '1':
            result=5
        elif version == '3':
            for i in range(0,5):
                print(answers_final[course_name][i])
                print(questions[i])
                if answers_final[course_name][i] == questions[i]:
                    result=result+1
        #Register the test
        test = Test.objects.create(test_version = version, user = user, course = course,result=result)
        #Register the results of the test
        TestData.objects.create(test = test, question1= question1,question2= question2,question3= question3,question4= question4,question5= question5,question6=question6)
        return JsonResponse({"message": "The final test has been upload","result":result}, status=201)    
        #return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

@csrf_exempt
@login_required
def newPost(request):
    # Composing new post, methond == POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    #takes the data
    data = json.loads(request.body)
    content = data.get("content", "")
    course_name = data.get("course_name","")
    #takes the course
    course = Course.objects.get(course_name=course_name)
    #create the comment
    newpost= Comment(user=request.user, content=content,course=course)
    newpost.save()
    return JsonResponse({"message": "Post successfully."}, status=201)


@csrf_exempt
@login_required
def newMessage(request):
    # Composing new post, methond == POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    message = data.get("message", "")
    user = data.get("user","")
    #Verify if user to send message exist
    try:
        user = User.objects.get(username=user)
    except User.DoesNotExist:
        #if user doesn't exist returns error
        return JsonResponse({
                "error": f"User with username {user} does not exist."
            }, status=400)
    #takes the uer sender
    sender = request.user
    #Create the message
    newMessage= Message(user=user, content=message, sender=sender, read = user == request.user)
    newMessage.save()
    return JsonResponse({"message": "Post successfully."}, status=201)

@csrf_exempt
@login_required
def editUser(request):
    #take the PUT request
    if request.method == "PUT":
        data = json.loads(request.body)
        #takes the information
        username = data["username"]
        first_name = data["first_name"]
        last_name = data["last_name"]
        country = data["country"]
        career = data["career"]
        profession = data["profession"]
        email=data["email"]
        #just edit if the profile of the user that've send the request
        if username == request.user.username:
            user = User.objects.get(username= username)
            user.profession = profession
            user.first_name = first_name
            user.last_name = last_name
            user.country = country
            user.career = career
            user.email = email
            user.save() 
        return JsonResponse({"message": "User Edited"}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def read(request):
    #method put
    if request.method == "PUT":
        data = json.loads(request.body)
        ID = data["id"]
        #mark message as read
        try:
            message = Message.objects.get(id = ID)
        except Message.DoesNotExist:
            #if the message doesn't exist returns error
            return JsonResponse({
                "error": f"The message with id: {ID} does not exist."
            }, status=400)
        message.read = True
        message.save() 
        return JsonResponse({"message": "message mark as read"}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)




#social web:
def social_web(request):
    cname = 'Social'
    #see if course exist
    try:
        course = Course.objects.get(course_name=cname)
    except Course.DoesNotExist:
        course = False
    #if course exist
    if course == False:
        course = Course.objects.create(course_name = cname, description=course_description[cname])

    #pagination:
    #take the comments
    posts = course.comments.all()
    total_posts = posts.order_by("-timestamp").all()
    paginator = Paginator(total_posts, 10) # Show 10 post per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request,'finalProject/social_web.html',{
        "cname":'Social Web',
        "page_obj":page_obj,
        "total_posts": total_posts
    })


csv_path = os.path.join(os.path.dirname(__file__), 'metadata_df_csv.csv')
csv_path3 = os.path.join(os.path.dirname(__file__), 'ratings_df_clean_3stars.csv')
csv_path2 = os.path.join(os.path.dirname(__file__), 'ratings_df_clean.csv')
model_path = os.path.join(os.path.dirname(__file__), 'word2vec.model')

#API
####################
"""Search movies"""
####################
@csrf_exempt
def load_csv_file(request):
    #method put
    if request.method == "PUT":
        
        data = json.loads(request.body)
        movie = data["movie"]
        movie = movie.lower()
        movie = string.capwords(movie)
        
        ratings_df = pd.read_csv(csv_path3)
        metadata_df = pd.read_csv(csv_path)
        movies_df = pd.read_csv(csv_path2)
        
        movies = movies_df['tmdbId'].unique().tolist()

        metadata_df = metadata_df[metadata_df['tmdbId'].isin(movies)]

        metadata_df = metadata_df[metadata_df['title'].str.contains(movie)]
        
        movies = metadata_df['title'].tolist()
        posters = metadata_df['poster_path'].tolist()
        ids = metadata_df['tmdbId'].tolist()
        #print(posters)
        return JsonResponse({"movies": movies, 'posters':posters, 'ids':ids}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


####################
"""Content Based"""
####################

#API
@csrf_exempt
def get_recommendation(request):
    #method put
    if request.method == "PUT":

        data = json.loads(request.body)
        id_movie = data["id"]
        #id_movie = abs(id_movie)
        ##content based:
        model = Word2Vec.load(model_path)#load model
        #load csv
        ratings_df = pd.read_csv(csv_path3)
        print(ratings_df)
        movies_df = pd.read_csv(csv_path2)
        metadata_df = pd.read_csv(csv_path)
        #function that returns similar movies
        #function that returns similar movies
        def most_similar_movie(movieId):
            print("Similar of "+ratings_df[ratings_df['tmdbId'] == int(movieId)].iloc[0]['title'])
            #return [(int(x[0]), ratings_df[ratings_df['tmdbId'] == int(x[0])].iloc[0]['title']) for x in model.wv.most_similar(movieId)]
            return [(int(x[0]), ratings_df[ratings_df['tmdbId'] == int(x[0])].iloc[0]['title']) for x in model.wv.most_similar(movieId)]

        def most_similar_gener(genres):
            count = 0
            for genre in genres:
                if count == 0:
                    vector = model[genre]
                    count = count + 1
                else:
                    vector = model[genre] + vector
            print("Similar of ",list(genres))
            #print(model.wv.most_similar([vector]))
            resp = []
            for x in model.wv.most_similar([vector]):
                try:
                    int(x[0])
                    resp.append((int(x[0]), ratings_df[ratings_df['tmdbId'] == int(x[0])].iloc[0]['title']))
                except:
                    print(x)
            return resp
        
        #cosine
        description_df = metadata_df[['tmdbId', 'overview','title']]
        tfidf = TfidfVectorizer(stop_words='english')#tfidf instance
        #Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
        overview_matrix = tfidf.fit_transform(description_df['overview'])
        similarity_matrix = linear_kernel(overview_matrix,overview_matrix)
        #movies index mapping
        mapping = pd.Series(description_df.index,index = description_df['tmdbId'])
                
        def most_similar_description(movie_input):
            movie_input = int(movie_input)
            movie_index = mapping[movie_input]
            #get similarity values with other movies
            #similarity_score is the list of index and similarity matrix
            similarity_score = list(enumerate(similarity_matrix[movie_index]))
            #sort in descending order the similarity score of movie inputted with all the other movies
            similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
            # Get the scores of the 15 most similar movies. Ignore the first movie.
            similarity_score = similarity_score[1:15]
            #return movie names using the mapping series
            movie_indices = [i[0] for i in similarity_score]
            movie_ids = description_df['tmdbId'].iloc[movie_indices].tolist()
            #return ([(int(movie),description_df[description_df['tmdbId'] == movie]['title'].to_string(index=False).strip()) for movie in movie_ids])
            return ([(int(movie),description_df[description_df['tmdbId'] == movie]['title'].to_string(index=False).strip()) for movie in movie_ids])
                

        def get_genres(movie_id):
            return metadata_df[metadata_df['tmdbId'] == movie_id].genres.to_string(index=False).strip()

        def content_based(movie_id):
            #search by simmilar description
            description_sim = most_similar_description(movie_id)
            #search by simmilar movie name
            try:
                movie_sim = most_similar_movie(movie_id)
            except:
                movie_sim = []
            set_1 = set(description_sim)
            set_2 = set(movie_sim)
            moviesSet2_notin_Set1 = list(set_2 - set_1)
            combined_sim = description_sim + moviesSet2_notin_Set1
            #search by simmilar genres
            genres_string = get_genres(int(movie_id)) #take the genres of the movie
            genres = genres_string.split()
            #print(genres)
            #use the function
            try:
                genres_sim = most_similar_gener(genres)
            except:
                genres_sim = []
            set_1 = set(combined_sim)
            set_2 = set(genres_sim)
            moviesSet2_notin_Set1 = list(set_2 - set_1)
            combined_sim = combined_sim + moviesSet2_notin_Set1
            #don't repeat movies
            combined_similar_movies = list(set(combined_sim))
            return combined_similar_movies            
            
            ### Colaborative Filer
            
        prediction = content_based(id_movie)
        print(prediction)
        return JsonResponse({"recommendation": prediction}, status=201)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

#ratings
####################
"""Search movies"""
####################
@login_required
@csrf_exempt
def ratings(request,movie_id):
    user = request.user
    #method put
    if request.method == "POST":
        data = json.loads(request.body)
        rating = data["rating"]
        try:
            #if object exist edit:
            movie = Movies.objects.get(user=user, movie_id=movie_id)
            movie.rating = rating
            movie.save()
        except Movies.DoesNotExist:
            #if object doesn't exit create 
            movie = Movies.objects.create(movie_id = movie_id, user= user, rating=rating)
        return JsonResponse({"message": "Rate added"}, status=201)
    ##get movie rating:
    elif request.method == "GET":
        try:
            movie = Movies.objects.get(user=user, movie_id=movie_id)
            rating = movie.rating
        except Movies.DoesNotExist:
            rating = 0
        return JsonResponse({"rating": rating}, status=201)
    else:
        return JsonResponse({
            "error": "GET or POST request required."
        }, status=400)
