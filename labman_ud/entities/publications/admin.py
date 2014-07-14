# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###########################################################################
# Class: VivaPanelInline
###########################################################################

class VivaPanelInline(admin.TabularInline):
    model = VivaPanel
    extra = 1


###########################################################################
# Class: PublicationSeeAlsoInline
###########################################################################

class PublicationSeeAlsoInline(admin.TabularInline):
    model = PublicationSeeAlso
    extra = 1


###########################################################################
# Class: PublicationSeeAlsoAdmin
###########################################################################

class PublicationSeeAlsoAdmin(admin.ModelAdmin):
    model = PublicationSeeAlso

    list_display = ['publication', 'see_also']
    search_fields = ['publication__title']


###########################################################################
# Class: ThesisSeeAlsoInline
###########################################################################

class ThesisSeeAlsoInline(admin.TabularInline):
    model = ThesisSeeAlso
    extra = 1


###########################################################################
# Class: ThesisSeeAlsoAdmin
###########################################################################

class ThesisSeeAlsoAdmin(admin.ModelAdmin):
    model = ThesisSeeAlso

    list_display = ['thesis', 'see_also']
    search_fields = ['thesis__title']


###########################################################################
# Class: PublicationTagAdmin
###########################################################################

class PublicationTagInline(admin.TabularInline):
    model = PublicationTag
    extra = 1


###########################################################################
# Class: PublicationAuthorInline
###########################################################################

class PublicationAuthorInline(admin.TabularInline):
    model = PublicationAuthor
    extra = 1


###########################################################################
# Class: PublicationEditorInline
###########################################################################

class PublicationEditorInline(admin.TabularInline):
    model = PublicationEditor
    extra = 1


###########################################################################
# Class: ThesisAbstractInline
###########################################################################

class ThesisAbstractInline(admin.TabularInline):
    model = ThesisAbstract
    extra = 1


###########################################################################
# Class: CoAdvisorInline
###########################################################################

class CoAdvisorInline(admin.TabularInline):
    model = CoAdvisor
    extra = 1


###########################################################################
# Class: PublicationAdmin
###########################################################################

class PublicationAdmin(admin.ModelAdmin):
    model = Publication

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: ThesisAdmin
###########################################################################

class ThesisAdmin(admin.ModelAdmin):
    model = Thesis

    search_fields = ['title', 'author__full_name']
    list_display = ['title', 'author', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        VivaPanelInline,
        CoAdvisorInline,
        ThesisSeeAlsoInline,
        ThesisAbstractInline,
    ]


###########################################################################
# Class: VivaPanelAdmin
###########################################################################

class VivaPanelAdmin(admin.ModelAdmin):
    model = VivaPanel


###########################################################################
# Class: PublicationAuthorAdmin
###########################################################################

class PublicationAuthorAdmin(admin.ModelAdmin):
    model = PublicationAuthor

    search_fields = ['publication__slug', 'author__slug']
    list_display = ['publication', 'author']
    list_filter = ['author__full_name']


###########################################################################
# Class: PublicationEditorAdmin
###########################################################################

class PublicationEditorAdmin(admin.ModelAdmin):
    model = PublicationEditor

    search_fields = ['publication__slug', 'editor__slug']
    list_display = ['publication', 'editor']
    list_filter = ['editor__full_name']


###########################################################################
# Class: PublicationTagAdmin
###########################################################################

class PublicationTagAdmin(admin.ModelAdmin):
    model = PublicationTag

    search_fields = ['publication__slug', 'tag__slug']
    list_display = ['publication', 'tag']
    list_filter = ['tag__name']


###########################################################################
# Class: BookAdmin
###########################################################################

class BookAdmin(admin.ModelAdmin):
    model = Book

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: BookSectionAdmin
###########################################################################

class BookSectionAdmin(admin.ModelAdmin):
    model = BookSection

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: ProceedingsAdmin
###########################################################################

class ProceedingsAdmin(admin.ModelAdmin):
    model = Proceedings

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: ConferencePaperAdmin
###########################################################################

class ConferencePaperAdmin(admin.ModelAdmin):
    model = ConferencePaper

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: JournalAdmin
###########################################################################

class JournalAdmin(admin.ModelAdmin):
    model = Journal

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: JournalArticleAdmin
###########################################################################

class JournalArticleAdmin(admin.ModelAdmin):
    model = JournalArticle

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: MagazineAdmin
###########################################################################

class MagazineAdmin(admin.ModelAdmin):
    model = Magazine

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: MagazineArticleAdmin
###########################################################################

class MagazineArticleAdmin(admin.ModelAdmin):
    model = MagazineArticle

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]


###########################################################################
# Class: ThesisAbstractAdmin
###########################################################################

class ThesisAbstractAdmin(admin.ModelAdmin):
    model = ThesisAbstract


###########################################################################
# Class: CoAdvisorAdmin
###########################################################################

class CoAdvisorAdmin(admin.ModelAdmin):
    model = CoAdvisor


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(PublicationSeeAlso, PublicationSeeAlsoAdmin)
admin.site.register(ThesisSeeAlso, ThesisSeeAlsoAdmin)

admin.site.register(Book, BookAdmin)
admin.site.register(BookSection, BookSectionAdmin)
admin.site.register(Proceedings, ProceedingsAdmin)
admin.site.register(ConferencePaper, ConferencePaperAdmin)
admin.site.register(Journal, JournalAdmin)
admin.site.register(JournalArticle, JournalArticleAdmin)
admin.site.register(Magazine, MagazineAdmin)
admin.site.register(MagazineArticle, MagazineArticleAdmin)

admin.site.register(Thesis, ThesisAdmin)
admin.site.register(ThesisAbstract, ThesisAbstractAdmin)
admin.site.register(CoAdvisor, CoAdvisorAdmin)
admin.site.register(VivaPanel, VivaPanelAdmin)

admin.site.register(PublicationAuthor, PublicationAuthorAdmin)
admin.site.register(PublicationEditor, PublicationEditorAdmin)
admin.site.register(PublicationTag, PublicationTagAdmin)
