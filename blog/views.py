from django.shortcuts import HttpResponse, HttpResponseRedirect, get_object_or_404, reverse, Http404, render

from .models import Blog
from .forms import BlogForm,CommentForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponseBadRequest,HttpResponseForbidden
from django.contrib.auth.decorators import login_required


@login_required
def post_list(request):

    posts=Blog.objects.all()
    page=request.GET.get('page',1)
    paginator=Paginator(posts,3)
    try:
        posts=paginator.page(page)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts=paginator.page(1)
    context = {'posts': posts}
    return render(request,'blog/post-list.html',context)




@login_required
def post_create(request):
    form=BlogForm()
    context = {'form': form}
    if request.method == "POST":
        print(request.POST)
        form = BlogForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.user=request.user
            blog.save()
            return HttpResponseRedirect(reverse('post_details',kwargs={'id':blog.id}))
    return render(request,'blog/post-create.html',context)

@login_required
def post_details(request, id):
    form=CommentForm()
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog/post-details.html', {
        "blog": blog,
        'form': form,
    })
@login_required
def post_uptade(request, id):
    blog=get_object_or_404(Blog,id=id)
    if request.user != blog.user:
        return HttpResponseForbidden()
    form=BlogForm(instance=blog,data=request.POST or None,files=request.FILES or None)
    if form.is_valid():
        blog = form.save()
        return HttpResponseRedirect(reverse('post_details', kwargs={'id': blog.id}))
    context = {'form': form, 'blog': blog}
    return render(request,'blog/post-uptade.html',context)

@login_required
def post_delete(request,id):
    blog=get_object_or_404(Blog,id=id)
    if request.user != blog.user:
        return HttpResponseForbidden()
    blog.delete()
    return HttpResponseRedirect(reverse('post_list'))

@login_required
def add_comment(request,id):
    if request.method=='GET':
        return HttpResponseBadRequest()
    blog=get_object_or_404(Blog,id=id)
    form=CommentForm(data=request.POST)
    if form.is_valid():
        new_comment=form.save(commit=False)
        new_comment.blog=blog
        new_comment.user=request.user
        new_comment.save()
        return HttpResponseRedirect((reverse('post_details',kwargs={'id':blog.id})))



