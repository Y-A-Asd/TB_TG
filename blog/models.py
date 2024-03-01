from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel
from shop.models import Customer


class Blog(TranslatableModel, BaseModel):
    """
    Model representing a blog post.

    Attributes:
        title (CharField): The title of the blog post.
        body (TextField, optional): The body/content of the blog post.
        thumbnail (ImageField): The thumbnail image associated with the blog post.
        views (IntegerField): The number of views the blog post has received.
        author (ForeignKey): The author of the blog post.
    """
    translations = TranslatedFields(
        title=models.CharField(_("Title"), max_length=255, unique=True),
        body=models.TextField(_("Body"), null=True, blank=True)
    )
    thumbnail = models.ImageField(_('Thumbnail'), upload_to='blogs/thumbnail/')
    views = models.IntegerField(_('Views'), default=0)
    author = models.ForeignKey(Customer, on_delete=models.PROTECT, verbose_name=_('Author'))

    def __str__(self):
        return f"{self.title} - {self.author}"

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")


class BlogComment(BaseModel):
     """
    Model representing a comment on a blog post.

    Attributes:
        customer (ForeignKey): The customer who left the comment.
        blog (ForeignKey): The blog post on which the comment is made.
        subject (CharField): The subject/title of the comment.
        message (TextField): The content/message of the comment.
        active (BooleanField): Indicates whether the comment is active.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name=_("Customer"))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_("Blog"), related_name='comments')
    subject = models.CharField(_("Subject"), max_length=255)
    message = models.TextField(_("Message"))
    active = models.BooleanField(_("Active"), default=False)

    def __str__(self):
        return f"{self.customer} - {self.subject}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
