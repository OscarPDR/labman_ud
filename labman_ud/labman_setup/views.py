
from django.core.files import File
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.models import User

from entities.news.models import *
from entities.organizations.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *
from entities.utils.models import *
from labman_setup.models import *

import urllib
import datetime


# Create your views here.


####################################################################################################
###     View: populate_database()
####################################################################################################

def populate_database(request):
    if RequestContext(request).get('INITIAL_SETUP'):

        User.objects.create_superuser(
            username=u"admin",
            password=u"admin",
            email=u"superuser@admin.org",
        )

        general_settings = LabmanDeployGeneralSettings(
            research_group_full_name=u"The Simpsons universe",
            research_group_description=u"<p><i><b>The Simpsons </b></i>is an American family animated television sitcom, created by <a href='/wiki/Matt_Groening' title='Matt Groening'>Matt Groening</a> and produced by the <a href='/wiki/Fox_Broadcasting_Company' title='Fox Broadcasting Company' class='mw-redirect'>Fox Broadcasting Company</a>. The main characters are a satire of a working-class family, consisting of Homer, Marge, Bart, Lisa and Maggie. The series lampoons many aspects of American culture, society, politics and history.</p>",
            address=u"Springfield<br>USA",
            contact_person=u"Matt Groening",
        )

        general_settings.save()

        general_settings_logo_url = u"http://simpsonswiki.com/w/images/thumb/6/69/Cooling_Towers_Tapped_Out.png/150px-Cooling_Towers_Tapped_Out.png"
        general_settings_team_image_url = u"http://www.asset1.net/tv/pictures/show/the-simpsons/The-Simpsons-KeyArt-03-16x9-1.jpg"

        _save_general_settings_images(general_settings, general_settings_logo_url, general_settings_team_image_url)

        nuclear_power_plant = Organization(
            organization_type=u"Enterprise",
            full_name=u"Springfield Nuclear Power Plant",
        )

        elementary_school = Organization(
            organization_type=u"Educational organization",
            full_name=u"Springfield Elementary School",
        )

        nuclear_power_plant.save()
        elementary_school.save()

        seymour_skinner = Person(
            first_name=u"Seymour",
            first_surname=u"Skinner",
            biography=u"<p>Seymour is ethnically Armenian, the name 'Armin Tamzarian' would suggest he is from Eastern Armenian heritage.</p>",
            gender=u"Male",
            personal_website=u"http://simpsons.wikia.com/wiki/Seymour_Skinner",
            is_active=True,
        )

        bart_simpson = Person(
            first_name=u"Bart",
            first_surname=u"Simpson",
            biography=u"<p>Bart is a self-proclaimed underachiever who is constantly in detention. He is easily distracted. His penchant for shocking people began before he was born: Bart 'mooned' <a href='/wiki/Julius_Hibbert' title='Julius Hibbert'>Dr. Hibbert</a> while he performed a sonogram on Marge, and moments after being born he set fire to Homer's tie (Marge saying that he could not have done it on purpose because he was only ten minutes old). Bart's first words were 'Ay Caramba'.</p>",
            gender=u"Male",
            personal_website=u"http://simpsons.wikia.com/wiki/Bart_Simpson",
            is_active=True,
            konami_code_position=u"El Barto",
        )

        lisa_simpson = Person(
            first_name=u"Lisa",
            first_surname=u"Simpson",
            biography=u"<p>Lisa is quite eclectic in her knowledge and is notably more concerned with world affairs and problems than her cohorts, which has led her to alienate herself from her peers.</p>",
            gender=u"Female",
            personal_website=u"http://simpsons.wikia.com/wiki/Lisa_Simpson",
            is_active=True,
        )

        edna_krabappel = Person(
            first_name=u"Edna",
            first_surname=u"Krabappel",
            biography=u"<p>Edna was an A-grade student back in school and held a Master's in Education from Bryn Mawr College. Her life dream once was to teach to young students; however, after years of teaching jaded her positive image, and after her husband left for another woman, their marriage counselor, Edna started drinking her days away, got fired from teaching in a prestigious private school, and eventually made her way into Springfield Elementary.</p>",
            gender=u"Female",
            personal_website=u"http://simpsons.wikia.com/wiki/Edna_Krabappel",
            is_active=False,
        )

        professor_frink = Person(
            first_name=u"Jonathan",
            first_surname=u"Frink",
            biography=u"<p>Born in the 1950s, Frink is Springfield's local mad scientist.</p>",
            title=u"Dr.",
            gender=u"Male",
            personal_website=u"http://simpsons.wikia.com/wiki/Jonathan_Frink",
            is_active=False,
        )

        seymour_skinner.save()
        bart_simpson.save()
        lisa_simpson.save()
        edna_krabappel.save()
        professor_frink.save()

        seymour_skinner_image_url = u"http://ts4.mm.bing.net/th?q=Principal+Skinner"
        bart_simpson_image_url = u"https://tappedoutdaily.files.wordpress.com/2013/08/bart-simpson-looking-cut-out.png"
        bart_simpson_konami_image_url = u"http://img4.wikia.nocookie.net/__cb20130525075502/simpsons/images/d/d0/Sdfgvfv.jpg"
        lisa_simpson_image_url = u"https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcSj7utXxco0w9Fp0nFjIyZIqC-BoNRZ7BDrJQmH_9qpyf4zFvA7Ug"
        edna_krabappel_image_url = "http://gopractice.biz/wp-content/uploads/2013/11/394455-edna_krabappel_large.png"
        professor_frink_image_url = u"https://a4-images.myspacecdn.com/images03/22/466499ff26d244bf8a3dd462376980d9/300x300.jpg"

        _save_profile_picture(seymour_skinner, seymour_skinner_image_url, None)
        _save_profile_picture(bart_simpson, bart_simpson_image_url, bart_simpson_konami_image_url)
        _save_profile_picture(lisa_simpson, lisa_simpson_image_url, None)
        _save_profile_picture(edna_krabappel, edna_krabappel_image_url, None)
        _save_profile_picture(professor_frink, professor_frink_image_url, None)

        seymour_skinner_job_1 = Job(
            person=seymour_skinner,
            organization=elementary_school,
            position=u"Teacher",
            start_date=datetime.date(2000, 1, 1),
            end_date=datetime.date(2009, 12, 31),
        )

        seymour_skinner_job_2 = Job(
            person=seymour_skinner,
            organization=elementary_school,
            position=u"Principal",
            start_date=datetime.date(2010, 1, 1),
        )

        bart_simpson_job = Job(
            person=bart_simpson,
            organization=elementary_school,
            position=u"Student",
            start_date=datetime.date(2008, 1, 1),
        )

        lisa_simpson_job = Job(
            person=lisa_simpson,
            organization=elementary_school,
            position=u"Student",
            start_date=datetime.date(2010, 1, 1),
        )

        edna_krabappel_job = Job(
            person=edna_krabappel,
            organization=elementary_school,
            position=u"Teacher",
            start_date=datetime.date(2005, 1, 1),
            end_date=datetime.date(2011, 12, 31),
        )

        professor_frink_job = Job(
            person=professor_frink,
            organization=elementary_school,
            position=u"Science teacher",
            start_date=datetime.date(2006, 1, 1),
            end_date=datetime.date(2007, 12, 31),
        )

        seymour_skinner_job_1.save()
        seymour_skinner_job_2.save()
        bart_simpson_job.save()
        lisa_simpson_job.save()
        edna_krabappel_job.save()
        professor_frink_job.save()

        school_as_unit = Unit(
            organization=elementary_school,
            head=seymour_skinner,
            order=1,
        )

        school_as_unit.save()

        role_principal_researcher = Role(
            name=u"Principal researcher",
        )

        role_principal_researcher.save()

        role_project_manager = Role(
            name=u"Project manager",
        )

        role_project_manager.save()

        role_researcher = Role(
            name=u"Researcher",
        )

        role_researcher.save()

        project_hamster = Project(
            project_leader=elementary_school,
            project_type=u"Research project",
            full_name=u"Is my brother dumber than a hamster?",
            description=u"Lisa connects an electrical current to a cupcake, and sets up a sign saying: 'Do not touch.' Bart sees the sign, but try to eat the cupcake anyway. He gets shocked over and over again. In a later scene, Marge tells Bart to get the cupcakes in the kitchen, but when he's going to take them down, he falls down on the floor shivering. The entire scene is very similar to the conference scene in A Clockwork Orange.",
            start_year=1993,
            end_year=1994,
            status=u"Finished",
        )

        project_hamster.save()

        project_itchy_scratchy = Project(
            project_leader=elementary_school,
            project_type=u"Development project",
            full_name=u"The Itchy & Scratchy Show",
            description=u"After being disappointed by a new episode of Itchy & Scratchy, Bart and Lisa decide that they can write a better one themselves.",
            start_year=1993,
            end_year=1996,
            status=u"Ongoing",
        )

        project_itchy_scratchy.save()

        project_badass = Project(
            project_leader=elementary_school,
            project_type=u"Project",
            full_name=u"Sweet Seymour Skinner's Baadasssss Song",
            description=u"Bart Simpson, feeling partially responsible for Skinner's firing, tries to help his old principal get his job back.",
            start_year=2018,
            end_year=2020,
            status=u"Not started",
        )

        project_badass.save()

        frink_at_project_hamster = AssignedPerson(
            project=project_hamster,
            person=professor_frink,
            role=role_principal_researcher,
        )

        lisa_at_project_hamster = AssignedPerson(
            project=project_hamster,
            person=lisa_simpson,
            role=role_researcher,
        )

        seymour_at_project_itchy_scratchy = AssignedPerson(
            project=project_itchy_scratchy,
            person=seymour_skinner,
            role=role_principal_researcher,
        )

        edna_at_project_itchy_scratchy = AssignedPerson(
            project=project_itchy_scratchy,
            person=edna_krabappel,
            role=role_project_manager,
        )

        lisa_at_project_itchy_scratchy = AssignedPerson(
            project=project_itchy_scratchy,
            person=lisa_simpson,
            role=role_researcher,
        )

        bart_at_project_itchy_scratchy = AssignedPerson(
            project=project_itchy_scratchy,
            person=bart_simpson,
            role=role_researcher,
        )

        skinner_at_project_badass = AssignedPerson(
            project=project_badass,
            person=seymour_skinner,
            role=role_principal_researcher,
        )

        skinner_at_project_badass_manager = AssignedPerson(
            project=project_badass,
            person=seymour_skinner,
            role=role_project_manager,
        )

        bart_at_project_badass = AssignedPerson(
            project=project_badass,
            person=bart_simpson,
            role=role_researcher,
        )

        frink_at_project_hamster.save()
        lisa_at_project_hamster.save()
        seymour_at_project_itchy_scratchy.save()
        edna_at_project_itchy_scratchy.save()
        lisa_at_project_itchy_scratchy.save()
        bart_at_project_itchy_scratchy.save()
        skinner_at_project_badass.save()
        skinner_at_project_badass_manager.save()
        bart_at_project_badass.save()

        humour_tag = Tag(
            name='Humour',
        )

        humour_tag.save()

        fiction_tag = Tag(
            name='Fiction',
        )

        fiction_tag.save()

        springfield_tag = Tag(
            name='Springfield',
        )

        springfield_tag.save()

        itchy_scratchy_tag = Tag(
            name='Itchy and Scratchy',
        )

        itchy_scratchy_tag.save()

        science_tag = Tag(
            name='Science',
        )

        science_tag.save()

        ProjectTag.objects.create(
            project=project_hamster,
            tag=science_tag,
        )

        ProjectTag.objects.create(
            project=project_hamster,
            tag=humour_tag,
        )

        ProjectTag.objects.create(
            project=project_hamster,
            tag=springfield_tag,
        )

        ProjectTag.objects.create(
            project=project_itchy_scratchy,
            tag=itchy_scratchy_tag,
        )

        ProjectTag.objects.create(
            project=project_itchy_scratchy,
            tag=humour_tag,
        )

        harpooned_heart_book = Book(
            title=u"The Harpooned Heart Series",
            year=2004,
        )

        harpooned_heart_book.save()

        harpooned_heart_book_section = BookSection(
            title=u"The Harpooned Heart",
            abstract=u"Temperance Barrows lives on Nantucket with her two children and husband Captain Mordecai Barrows who is a crude, rude, perverted druken brute. When he returns from his month whaling trip he only catches a seagull and leaves to go to a bar. While Temperance does the laundry she meets Cyrus Manley who is new to the island. The two become very good friends and eventually, lovers. When Mordecai finds out he corners Cyrus on top of a cliff with a harpoon. When Cyrus says that Temperance is pregnant with his child, Mordecai throws his harpoon, impaling Cyrus on a whale that Temperance had admired from a distance. However, the harpoon's rope becomes wrapped around Mordecai's leg, dragging him under the sea to die with his enemy. Temperance then realizes its the end.",
            year=2004,
            pages=u"1-286",
            bibtex=u"@book_section { 'title': 'The Harpooned Heart' }",
            parent_book=harpooned_heart_book,
        )

        harpooned_heart_book_section.save()

        lisa_harpooned_heart = PublicationAuthor(
            author=lisa_simpson,
            publication=harpooned_heart_book_section,
            position=1,
        )

        lisa_harpooned_heart.save()

        itchy_scratchy_scripts = Journal(
            title=u"Scripts for the Itchy & Scratchy Show",
            year=1993,
        )

        itchy_scratchy_scripts.save()

        barbershop_journal_article = JournalArticle(
            title=u"Little Barbershop of Horrors",
            abstract=u"Scratchy goes to Itchy's barber shop for a haircut. Itchy seats Scratchy in the chair, then pours barbecue sauce and flesh-eating ants onto Scratchy's head. The ants devour the fur and flesh from Scratchy's head, leaving only his skull. Itchy then uses the chair lift to propel Scratchy into the air, through the ceiling, and into Elvis Presley's television set in the room upstairs, where Elvis is watching TV. Elvis comments that 'This show ain't no good,'' and shoots the TV.",
            year=1993,
            parent_journal=itchy_scratchy_scripts,
        )

        barbershop_journal_article.save()

        lisa_barbershop = PublicationAuthor(
            author=lisa_simpson,
            publication=barbershop_journal_article,
            position=1,
        )

        bart_barbershop = PublicationAuthor(
            author=bart_simpson,
            publication=barbershop_journal_article,
            position=2,
        )

        lisa_barbershop.save()
        bart_barbershop.save()

        screams_mall_journal_article = JournalArticle(
            title=u"Screams From a Mall",
            abstract=u"Scratchy is at the mall. His shop is on the top floor, so he uses an escalator. Itchy nails his feet, causing it to be stuck, just as Scratchy was finally at the top floor. He tries to get them out, but he is too late and his fur is ripped. Itchy puts Scratchy's fur in sale, in a fur shop, and a rich couple buys it, and gives Itchy money. However, Scratchy (with flesh replacing the fur) informs them to give it to him. He goes out of the mall, but women are preventing animals being hurt for fur, so they attack Scratchy.",
            year=1993,
            parent_journal=itchy_scratchy_scripts,
        )

        screams_mall_journal_article.save()

        lisa_screams_mall = PublicationAuthor(
            author=lisa_simpson,
            publication=screams_mall_journal_article,
            position=2,
        )

        bart_screams_mall = PublicationAuthor(
            author=bart_simpson,
            publication=screams_mall_journal_article,
            position=1,
        )

        lisa_screams_mall.save()
        bart_screams_mall.save()

        PublicationTag.objects.create(
            publication=harpooned_heart_book_section,
            tag=springfield_tag,
        )

        PublicationTag.objects.create(
            publication=harpooned_heart_book_section,
            tag=fiction_tag,
        )

        PublicationTag.objects.create(
            publication=barbershop_journal_article,
            tag=itchy_scratchy_tag,
        )

        PublicationTag.objects.create(
            publication=barbershop_journal_article,
            tag=humour_tag,
        )

        PublicationTag.objects.create(
            publication=screams_mall_journal_article,
            tag=itchy_scratchy_tag,
        )

        PublicationTag.objects.create(
            publication=screams_mall_journal_article,
            tag=springfield_tag,
        )

        RelatedPublication.objects.create(
            project=project_itchy_scratchy,
            publication=barbershop_journal_article,
        )

        RelatedPublication.objects.create(
            project=project_itchy_scratchy,
            publication=screams_mall_journal_article,
        )

        news_1 = News(
            title=u"Bart to Martin: 'Eat my shorts'",
            content=u"<img src='http://www.simpsoncrazy.com/content/lists/newspaper/news_027.jpg' />",
        )

        news_1.save()

        news_2 = News(
            title=u"Extra!!! Prince beats Simpson",
            content=u"<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec at dapibus neque. Etiam quis pulvinar ante. Sed ut nulla eu purus mattis elementum.</p><br><img src='http://www.simpsoncrazy.com/content/lists/newspaper/news_028.jpg' />",
        )

        news_2.save()

        news_3 = News(
            title=u"First day of spring",
            content=u"<p>Ants, Picnickers Reach Last-Minute Accord</p><br><img src='http://www.simpsoncrazy.com/content/lists/newspaper/news_145.jpg' />",
        )

        news_3.save()

        PersonRelatedToNews.objects.create(
            person=bart_simpson,
            news=news_1,
        )

        PersonRelatedToNews.objects.create(
            person=lisa_simpson,
            news=news_1,
        )

        PersonRelatedToNews.objects.create(
            person=bart_simpson,
            news=news_2,
        )

        PersonRelatedToNews.objects.create(
            person=seymour_skinner,
            news=news_3,
        )

        ProjectRelatedToNews.objects.create(
            project=project_itchy_scratchy,
            news=news_3,
        )

        PublicationRelatedToNews.objects.create(
            publication=barbershop_journal_article,
            news=news_3,
        )

    else:
        # Database already initialised
        pass

    return HttpResponseRedirect(reverse('home'))


def _save_profile_picture(person_instance, image_url, konami_url):
    result = urllib.urlretrieve(image_url)

    person_instance.profile_picture.save(
        os.path.basename(image_url),
        File(open(result[0]))
    )

    if konami_url:
        result_konami = urllib.urlretrieve(konami_url)

        person_instance.profile_konami_code_picture.save(
            os.path.basename(konami_url),
            File(open(result_konami[0]))
        )

    person_instance.save()


def _save_general_settings_images(settings_instance, logo_url, team_image_url):
    result_logo = urllib.urlretrieve(logo_url)

    settings_instance.research_group_official_logo.save(
        os.path.basename(logo_url),
        File(open(result_logo[0]))
    )

    result_team_image = urllib.urlretrieve(team_image_url)

    settings_instance.research_group_team_image.save(
        os.path.basename(team_image_url),
        File(open(result_team_image[0]))
    )

    settings_instance.save()
