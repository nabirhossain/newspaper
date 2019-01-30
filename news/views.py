from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404, HttpResponseRedirect
from .models import author, Category,  Post, Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateForm, CommentForm, registerUser, createAuthor
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, Count, Max
from taggit.models import Tag
from django.contrib.auth.decorators import login_required


## registration with email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import send_mail
# close registration import
# token import
from .token import activation_token
# close token


# Create your views here.

def index(request):
    kategorie = Category.objects.filter(parent=None).order_by('name')                       ## SHOW CATEGORY AND SUB-CATEGORY IN DROPDOWN LIST
    post = Post.published_objects.all().order_by('-posted')[0]                              ## SHOW POST FOR FIRST GRID
    post1 = Post.published_objects.all().order_by('-posted')[1:3]                           ## SHOW POST FOR SECOND GRID
    post2 = Post.published_objects.all().order_by('-posted')[3:8]                           ## SHOW POST FOR THIRD GRID
    breaking = Post.published_objects.all().order_by('-posted')[:6]                         ## SHOW BREAKING NEWS
    all_post = Post.published_objects.all().order_by('-posted')                             ## SHOW ALL POSTS
    most_popular = Post.published_objects.all().order_by('-views')[:4]                      ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:4]                       ## SHOW FOUR MOST RECENT NEWS
    search = request.GET.get('q')
    if search:
        all_post = all_post.filter(
            Q(title__icontains = search)|
            Q(body__icontains = search)
        )
    topic_cricket = get_object_or_404(Category, name='Cricket')                                          ## show some post for selected categories in home page
    cricket = Post.published_objects.all().filter(category=topic_cricket).order_by('-posted')[:4]
    topic_tech = get_object_or_404(Category, name='Tech')
    tech = Post.published_objects.all().filter(category=topic_tech).order_by('-posted')[0]
    topic_world = get_object_or_404(Category, name='Worlds')
    worlds = Post.published_objects.all().filter(category=topic_world).order_by('-posted')[:3]
    topic_opinion = get_object_or_404(Category, name='Opinion')
    opinion = Post.published_objects.all().filter(category=topic_opinion).order_by('-posted')[:3]
    topic_health = get_object_or_404(Category, name='Health')
    health = Post.published_objects.all().filter(category=topic_health).order_by('-posted')[0]
    topic_entertainment = get_object_or_404(Category, name='Entertainment')
    entertainment = Post.published_objects.all().filter(category=topic_entertainment).order_by('-posted')[:2]
    topic_business = get_object_or_404(Category, name='Business')
    business = Post.published_objects.all().filter(category=topic_business).order_by('-posted')[:3]
    topic_bd = get_object_or_404(Category, name='Bangladesh')
    bangladesh = Post.published_objects.all().filter(category=topic_bd).order_by('-posted')[:4]
    topic_finance = get_object_or_404(Category, name='Finance')
    finance = Post.published_objects.all().filter(category=topic_finance).order_by('-posted')[:4]
    context = {
        'post':post,
        'post1':post1,
        'post2':post2,
        'all_post' : all_post,
        'breaking' : breaking,
        'most_popular':most_popular,
        'tech':tech,
        'kategorie':kategorie,
        'recent':recent,
        'cricket': cricket,
        'worlds' : worlds,
        'opinion':opinion,
        'health' : health,
        'entertainment' : entertainment,
        'business' : business,
        'bangladesh' : bangladesh,
        'finance' : finance,

    }
    return render(request,'news/index.html', context)


@login_required
def post_create(request):
        form = CreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('news:index')
        return render(request, 'news/post_create.html', {"form": form})


def PostDetail(request, id, tag_slug=None):
    post = get_object_or_404(Post, pk=id)
    post2 = Post.published_objects.all().order_by('-posted')[:5]
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    kategorie = Category.objects.filter(parent=None).order_by('name')
    most_popular = Post.published_objects.all().order_by('-views')[:4]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    first = Post.published_objects.first()
    last = Post.published_objects.last()
    related = Post.published_objects.filter(category=post.category).exclude(id=id)[:2]
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post = post.filter(tags__in=[tag])
    if post.status == 'published':
        post.views += 1  # clock up the number of post views
        post.save()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post,  name=name, email=email, content=content, reply=comment_qs)
            comment.save()
    else:
        comment_form = CommentForm()

    context ={
        'post': post,
        'post2': post2,
        'breaking': breaking,
        'tag' : tag,
        'first':first,
        'last': last,
        'kategorie': kategorie,
        'related': related,
        'comments': comments,
        'most_popular': most_popular,
        'recent': recent,

    }
    return render(request,'news/post_detail.html', context)


def AllPost(request):
    post = Post.published_objects.all().order_by('-posted')
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    most_popular = Post.published_objects.all().order_by('-views')[:4]
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    kategorie = Category.objects.filter(parent=None).order_by('name')
    search = request.GET.get('q')
    if search:
        post = post.filter(
            Q(title__icontains = search)|
            Q(body__icontains = search)
        )
    paginator = Paginator(post, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 8 if index >= 8 else 0
    end_index = index + 8 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'post':post,
        'breaking':breaking,
        'kategorie':kategorie,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,
    }
    return render(request,'news/all_post.html', context)


def PostCategory(request, name):
    topic = get_object_or_404(Category, name=name)
    post = Post.published_objects.filter(category=topic.id)
    breaking = Post.published_objects.all().order_by('-posted')[:6]
    most_popular = Post.published_objects.all().order_by('-views')[:4]  ## SHOW MOST POULAR NEWS
    recent = Post.published_objects.filter().order_by('-posted')[0:4]
    kategorie = Category.objects.filter(parent=None).order_by('name')
    paginator = Paginator(post, 2)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'post': post,
        'topic': topic,
        'breaking': breaking,
        'kategorie': kategorie,
        'items': items,
        'page_range': page_range,
        'most_popular': most_popular,
        'recent': recent,
    }

    return render(request,'news/category.html', context)



def LogIn(request):
    if request.user.is_authenticated:
        return redirect('news:index')
    else:
        if request.method == "POST":
            user = request.POST.get('user')
            password = request.POST.get('pass')
            auth = authenticate(request, username=user, password=password)
            if auth is not None:
                login(request, auth)
                return redirect('news:index')
            else:
                messages.add_message(request, messages.ERROR, 'username or password not match')
                return render(request, 'registration/login.html')
    return render(request,'registration/login.html')

def LogOut(request):
    logout(request)
    return redirect('news:index')



def register(request):
    form =registerUser(request.POST or None)
    if form.is_valid():
        instance = form.save(commit = False)
        instance.is_active = False
        instance.save()
        site = get_current_site(request)
        mail_subject = "confirmation message for blog"
        message = render_to_string('confirmation_email.html',{
            'user': instance,
            'domain': site.domain,
            'uid' : instance.id,
            'token': activation_token.make_token(instance)
        })
        to_email = form.cleaned_data.get('email')
        to_list = [to_email]
        from_email = settings.EMAIL_HOST_USER
        send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
        return HttpResponse("<h1>Thanks for your registration. A confirmation link was sent to your mail</h1>")
        #messages.success(request, 'Registration has been successfully completed')
        #return redirect('blog:login')
    return render(request, 'registration/register.html', {"form":form})

def CreateProfile(request):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id= request.user.id)
        author_profile = author.objects.filter(auth_name = user.id)
        if author_profile:
            authorUser = get_object_or_404(author, auth_name = request.user.id)
            post = Post.published_objects.filter(author = authorUser.id)
            return render(request, 'news/author_profile.html', {"post":post}, {"user":authorUser})
        else:
            form = createAuthor(request.POST or None, request.FILES or None)
            if form.is_valid():
                instance = form.save(commit = False)
                instance.auth_name = user
                instance.save()
                return redirect('news:CreateProfile')
            return render(request, 'news/create_author_profile.html', {"form":form})
    else:
        return redirect('news:login')


def getAuthor(request, name):
    p_author = get_object_or_404(User, username=name)
    auth = get_object_or_404(author, auth_name=p_author.id)
    post = Post.published_objects.filter(author=auth.id)
    cat = Category.objects.all()
    paginator = Paginator(post, 3)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 4 if index >= 4 else 0
    end_index = index + 4 if index <= max_index else max_index
    page_range = paginator.page_range[start_index:end_index]
    context = {
        'auth':auth,
        'cat':cat,
        'post':post,
        'items': items,
        'page_range': page_range
    }
    return render(request,'news/author_profile.html', context)








'''
#from django.db.models import Count

#popular_events = Events.objects.annotate(attendee_count=Count('attendee')).filter(attendee_count__gt=50)
#https://stackoverflow.com/questions/11127448/get-most-popular-list-in-django
'''
