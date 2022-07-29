from django import forms
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.shortcuts import render
from django.utils import timezone

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from taggit.models import TaggedItemBase

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet


class SignUp(models.Model):
    objects = models.Manager()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    person_email = models.CharField(max_length=50)
    person_email_verify = models.CharField(max_length=50)
    shop_name = models.CharField(max_length=50)
    shop_website = models.CharField(max_length=60)
    shop_details = models.CharField(max_length=500)
    industry_type = models.CharField(max_length=30)
    product_type = models.CharField(max_length=30)
    employee_count = models.CharField(max_length=30)
    sales_interest = models.BooleanField(default=False)
    finance_interest = models.BooleanField(default=False)
    marketing_interest = models.BooleanField(default=False)
    social_interest = models.BooleanField(default=False)
    other_interest = models.BooleanField(default=False)
    other_description = models.CharField(max_length=50)


class BlogSubscribe(models.Model):
    email = models.EmailField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email_id


class BlogIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    def get_context(self, request, cat_id=None):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        if cat_id:
            '''
                - the category_id needs to be passed in from the frontend in the URL to filter
                - I have set up a route below to grab the id though the url
                - if cat_id, grab all the blogs with the blogcategory_id of cat_id ONLY
                manyTomany table <layout_blogpage_categories> relates
                <layout_blogcategory> and <layout_blogpage>
            '''
            pass
        blogpages = self.get_children().live().order_by('-first_published_at')
        # Paginate all posts by 9 per page
        categories=BlogCategory.objects.all()
        context['categories']=[]
        for cat in categories:
            context['categories'].append(cat.name)
        paginator = Paginator(blogpages, 9)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context['blogpages'] = posts
        return context



    @route(r'^(\d+)/', name="pk")
    def filter_newsletter(self, request,pk):
        context = self.get_context(request, cat_id=pk)
        return render(request,"layout/blog_index_page.html",context)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context


class BlogPage(Page):

    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    preview = models.CharField(blank=True, max_length=250)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.FilterField('categories'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro', heading="Subtitle in post"),
        FieldPanel('preview', heading="Preview shown on Blog Index"),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'
