from django.shortcuts import render, redirect
from apps.products.models import Category
from django.core.exceptions import PermissionDenied
from .forms import UserCommentsForm
from .models import Comments

# Create your views here.
def Home_page(request):
    context = {'show_extra': True}
    return render(request, 'pages/home.html', context)

def comment_page(request):
    form = UserCommentsForm()
    comments = Comments.objects.filter(parent=None)
    total_comments = Comments.objects.all().count()

    user = request.user

    if request.method == 'POST':
        form = UserCommentsForm(request.POST)

        if user.is_authenticated:

            if form.is_valid():
                form.save()
        else:
            return redirect('login')
    else:
        form = UserCommentsForm()

    context = {'form': form, 'comments': comments, 'total_comments': total_comments}
    return render(request, 'public/comments.html', context)

def delete_comment_view(request, comment_id):
    comment = Comments.objects.get(id=comment_id)
    comment.delete()
    return redirect('comments')

# renders 404 page
def page_not_found(request, exceptions):
    return render(request, '404.html', status=404)