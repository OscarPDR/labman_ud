# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *

###		PublicationRankInline
####################################################################################################

class PublicationRankInline(admin.TabularInline):
    model = PublicationRank
    extra = 1

###		VivaPanelInline
####################################################################################################

class VivaPanelInline(admin.TabularInline):
    model = VivaPanel
    extra = 1

###		PublicationSeeAlsoInline
####################################################################################################

class PublicationSeeAlsoInline(admin.TabularInline):
    model = PublicationSeeAlso
    extra = 1

###		PublicationSeeAlsoAdmin
####################################################################################################

class PublicationSeeAlsoAdmin(admin.ModelAdmin):
    model = PublicationSeeAlso

    list_display = ['publication', 'see_also']
    search_fields = ['publication__title']

###		ThesisSeeAlsoInline
####################################################################################################

class ThesisSeeAlsoInline(admin.TabularInline):
    model = ThesisSeeAlso
    extra = 1

###		ThesisSeeAlsoAdmin
####################################################################################################

class ThesisSeeAlsoAdmin(admin.ModelAdmin):
    model = ThesisSeeAlso

    list_display = ['thesis', 'see_also']
    search_fields = ['thesis__title']

###		PublicationTagAdmin
####################################################################################################

class PublicationTagInline(admin.TabularInline):
    model = PublicationTag
    extra = 1

###		PublicationAuthorInline
####################################################################################################

class PublicationAuthorInline(admin.TabularInline):
    model = PublicationAuthor
    extra = 1

###		PublicationEditorInline
####################################################################################################

class PublicationEditorInline(admin.TabularInline):
    model = PublicationEditor
    extra = 1

###		ThesisAbstractInline
####################################################################################################

class ThesisAbstractInline(admin.TabularInline):
    model = ThesisAbstract
    extra = 1

###		CoAdvisorInline
####################################################################################################

class CoAdvisorInline(admin.TabularInline):
    model = CoAdvisor
    extra = 1

###		PublicationAdmin
####################################################################################################

class PublicationAdmin(admin.ModelAdmin):
    model = Publication

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]

###		ThesisAdmin
####################################################################################################

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

###		VivaPanelAdmin
####################################################################################################

class VivaPanelAdmin(admin.ModelAdmin):
    model = VivaPanel

    search_fields = ['person__full_name']
    list_display = ['thesis', 'person', 'role']
    list_filter = ['thesis', 'role']

###		PublicationAuthorAdmin
####################################################################################################

class PublicationAuthorAdmin(admin.ModelAdmin):
    model = PublicationAuthor

    search_fields = ['publication__slug', 'author__slug']
    list_display = ['publication', 'author']
    list_filter = ['author__full_name']

###		PublicationEditorAdmin
####################################################################################################

class PublicationEditorAdmin(admin.ModelAdmin):
    model = PublicationEditor

    search_fields = ['publication__slug', 'editor__slug']
    list_display = ['publication', 'editor']
    list_filter = ['editor__full_name']

###		PublicationTagAdmin
####################################################################################################

class PublicationTagAdmin(admin.ModelAdmin):
    model = PublicationTag

    search_fields = ['publication__slug', 'tag__slug']
    list_display = ['publication', 'tag']
    list_filter = ['tag__name']

###		BookAdmin
####################################################################################################

class BookAdmin(admin.ModelAdmin):
    model = Book

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]

###		BookSectionAdmin
####################################################################################################

class BookSectionAdmin(admin.ModelAdmin):
    model = BookSection

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]

###		ProceedingsAdmin
####################################################################################################

class ProceedingsAdmin(admin.ModelAdmin):
    model = Proceedings

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationEditorInline,
        PublicationTagInline,
    ]

###		ConferencePaperAdmin
####################################################################################################

class ConferencePaperAdmin(admin.ModelAdmin):
    model = ConferencePaper

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]

###		JournalAdmin
####################################################################################################

class JournalAdmin(admin.ModelAdmin):
    model = Journal

    search_fields = ['title', 'slug']
    list_display = ['title', 'year', 'slug']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]

###		JournalArticleAdmin
####################################################################################################

class JournalArticleAdmin(admin.ModelAdmin):
    model = JournalArticle

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]

###		MagazineAdmin
####################################################################################################

class MagazineAdmin(admin.ModelAdmin):
    model = Magazine

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]

###		MagazineArticleAdmin
####################################################################################################

class MagazineArticleAdmin(admin.ModelAdmin):
    model = MagazineArticle

    search_fields = ['title', 'slug']
    list_display = ['title', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        PublicationRankInline,
        PublicationSeeAlsoInline,
        PublicationAuthorInline,
        PublicationTagInline,
    ]

###		ThesisAbstractAdmin
####################################################################################################

class ThesisAbstractAdmin(admin.ModelAdmin):
    model = ThesisAbstract

###		CoAdvisorAdmin
####################################################################################################

class CoAdvisorAdmin(admin.ModelAdmin):
    model = CoAdvisor

###		PublicationRankAdmin
####################################################################################################

class PublicationRankAdmin(admin.ModelAdmin):
    model = PublicationRank

    search_fields = ['publication__slug']
    list_display = ['publication', '_child_type', 'ranking']
    list_filter = ['ranking']

###		RankingAdmin
####################################################################################################

class RankingAdmin(admin.ModelAdmin):
    model = Ranking

    exclude = ['slug']


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

admin.site.register(Ranking, RankingAdmin)

admin.site.register(PublicationAuthor, PublicationAuthorAdmin)
admin.site.register(PublicationEditor, PublicationEditorAdmin)
admin.site.register(PublicationTag, PublicationTagAdmin)
admin.site.register(PublicationRank, PublicationRankAdmin)
