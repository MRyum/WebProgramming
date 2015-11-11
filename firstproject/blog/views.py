from django.shortcuts import render
from django.utils import timezone
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

def post_list(request):
	posts= Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,post_id):
	post = get_object_or_404(Post,pk=post_id)
	return render(request,'blog/post_detail.html',{'post':post})

@login_required
def post_new(request):
	if request.method =="POST":
		 form = PostForm(request.POST)
		 if form.is_valid():
			 post = form.save(commit=False)
			 post.author = request.user
			 post.published_date = timezone.now()
			 post.save()
			 return redirect('blog.views.post_detail',post_id=post.pk)
	else:
		form = PostForm()
	return render(request,'blog/post_edit.html',{'form':form})

@login_required
def post_edit(request,post_id):
	post = get_object_or_404(Post,pk=post_id)
	if request.method =="POST":
		 form = PostForm(request.POST)
		 if form.is_valid():
			 post = form.save(commit=False)
			 post.pk = post_id
			 post.author = request.user
			 post.published_date = timezone.now()
			 post.save()
			 return redirect('blog.views.post_detail',post_id=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request,'blog/post_edit.html',{'form':form})

def post_draft_list(request) :
	posts=Post.objects.filter(published_date__isnull=True).order_by('created_date')

	return render(request, 'blog/post_draft_list.html', {'posts':posts })

@login_required
def post_publish(request, post_id) :
	post = get_object_or_404(Post, pk=post_id)
	post.publish()
	return redirect('blog.views.post_detail', post_id=post_id)

@login_required
def post_remove(request, post_id) :
	post = get_object_or_404(Post, pk=post_id)
	post.delete()

	return redirect('blog.views.post_list')


def add_comment_to_post(request, post_id) :
	post = get_object_or_404(Post, pk=post_id)
	if request.method == "POST" :
		form = CommentForm(request.POST)
		if form.is_valid() :
			comment = form.save(commit = False)
			comment.post = post
			comment.save()
			return redirect('blog.views.post_detail', post_id=post.pk)
	else:
		form = CommentForm()
		return render(request, 'blog/add_comment_to_post.html', { 'form' : form})

@login_required
def comment_approve(request, post_id) :
	comment=get_object_or_404(Comment, pk=post_id)
	comment.approve()
	return redirect('blog.views.post_detail', post_id=comment.post.pk)

@login_required
def comment_remove(request, post_id) :
	comment=get_object_or_404(Comment, pk=post_id)
	post_pk=comment.post.pk
	comment.delete()

	return redirect('blog.views.post_detail', post_id=post_pk)

def real_first(request) :
	return render(request,'blog/real_first.html')
