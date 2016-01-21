from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, DeleteView, ListView, CreateView, DetailView

from .models import Profile, Image
from .forms import ImageForm, ImageReportForm


# Create your views here.

def index(request):
    images = Image.objects.order_by('-created_at')
    return render(request, 'telentapp/index.html', {'images': images})


class IndexView(ListView):
    queryset = Image.objects.order_by('-created_at')
    template_name = 'telentapp/index.html'
    context_object_name = 'images'
    paginate_by = 10


def user_profile(request, username):
    object = User.objects.filter(username=username).first()

    if object == None:
        raise Http404
    profile, created = Profile.objects.get_or_create(user=object)

    return render(request, 'telentapp/profile.html', {'object': object, 'profile': profile})


class UserProfile(DetailView):
    queryset = User.objects.all()
    template_name = 'telentapp/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get_or_create(user=self.get_object())[0]

        return context


def latest_images(request):
    images = Image.objects.order_by('created_at')

    return render(request, 'telentapp/images/latest.html', {'images': images})


class LatestImagesView(ListView):
    queryset = Image.objects.order_by('created_at')
    template_name = 'telentapp/images/latest.html'
    context_object_name = 'images'


def image(request, slug):
    import datetime
    from django.utils.timezone import utc
    from django.db.models import F

    image = get_object_or_404(Image, slug=slug)
    timedelta = datetime.datetime.utcnow().replace(tzinfo=utc) - image.created_at
    Image.objects.filter(slug=slug).update(views=F('views') + 1)

    return render(request, 'telentapp/images/image.html', {'image': image, 'timedelta': timedelta})


class ImageView(DetailView):
    queryset = Image.objects.all()
    template_name = 'telentapp/images/image.html'

    def get(self, request, *args, **kwargs):
        from django.db.models import F
        Image.objects.filter(slug=kwargs.get('slug')).update(views=F('views') + 1)

        return super(ImageView, self).get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        object = super(ImageView, self).get_object()

        return object

    def get_context_data(self, **kwargs):
        import datetime
        from django.utils.timezone import utc

        context = super(ImageView, self).get_context_data(**kwargs)
        object = self.get_object()
        context['timedelta'] = datetime.datetime.utcnow().replace(tzinfo=utc) - object.created_at
        return context


@login_required
def upload_image(request):
    if request.method == "POST":
        form = ImageForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()

            return redirect(image)
    else:
        form = ImageForm()

    return render(request, 'telentapp/images/upload.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UploadImageView(CreateView):
    form_class = ImageForm
    template_name = 'telentapp/images/upload.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = request.user
            self.object.save()

            return redirect(self.object)
        else:
            return self.form_invalid(form)


class PopularView(ListView):
    queryset = Image.objects.order_by('-views')
    template_name = 'telentapp/images/popular.html'
    paginate_by = 10


def popular(request):
    images = Image.objects.order_by('-views')

    return render(request, 'telentapp/images/popular.html', {'images': images})


class ImageEditView(UpdateView):
    model = Image
    template_name = 'telentapp/images/update.html'
    fields = ['image', 'description', 'location']


class ImageReportCreationView(CreateView):
    form_class = ImageReportForm
    template_name = 'telentapp/images/report.html'

    def dispatch(self, request, *args, **kwargs):
        self.image_slug = kwargs['slug']
        return super(ImageReportCreationView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ImageReportCreationView, self).get_context_data(**kwargs)

        context['image'] = Image.objects.get(slug=self.image_slug)

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.image = Image.objects.get(slug=kwargs['slug'])
            self.object.user = request.user
            self.object.save()

            return redirect('home')

        else:
            return self.form_invalid(form)
