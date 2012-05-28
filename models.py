# coding=utf-8

# Add site field to user and also checks that username and site are unique

from django.contrib.auth.models import User, UserManager

class SiteUser(User):
    site = models.ForeignKey('sites.Site',
                            verbose_name=_(u'Site al que pertenece'),
                            related_name='+',
                            null=True)

    objects = UserManager()

    def save(self, force_insert=False, force_update=False, using=None):
        self.username = self.username.lower()
        if not self.site:
            self.site_id = get_current_site().pk
        super(SiteUser, self).save(force_insert, force_update, using)

    def validate_unique(self, exclude=None):
        from django.core.exceptions import ValidationError
        if SiteUser.objects.exclude(pk=self.pk).filter(username=self.username.lower(), site_id=get_current_site().pk).exists():
            raise ValidationError({'username': ['Nombre de usuario ya en uso']})

    class Meta:
        verbose_name = _(u'Perfil')
        verbose_name_plural = _(u'Perfiles')