import requests
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings

from api.models.tvshow import TvShow, UserTvShow, ViewHistory
from bingeauth.models.user import User
from bingebase.settings import API_KEY

TEST_DATA = {
    "page": 1,
    "results": [
        {
            "backdrop_path": "/oKt4J3TFjWirVwBqoHyIvv5IImd.jpg",
            "first_air_date": "2019-06-16",
            "genre_ids": [18],
            "id": 85552,
            "name": "Euphoria",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Euphoria",
            "overview": "A group of high school students navigate love and friendships in a world of drugs, sex, trauma, and social media.",
            "popularity": 4799.821,
            "poster_path": "/jtnfNzqZwN4E32FGGxx1YZaBWWf.jpg",
            "vote_average": 8.4,
            "vote_count": 5513,
        },
        {
            "backdrop_path": "/sjx6zjQI2dLGtEL0HGWsnq6UyLU.jpg",
            "first_air_date": "2021-12-29",
            "genre_ids": [10765, 10759],
            "id": 115036,
            "name": "The Book of Boba Fett",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "The Book of Boba Fett",
            "overview": "Legendary bounty hunter Boba Fett and mercenary Fennec Shand must navigate the galaxy’s underworld when they return to the sands of Tatooine to stake their claim on the territory once ruled by Jabba the Hutt and his crime syndicate.",
            "popularity": 2563.477,
            "poster_path": "/gNbdjDi1HamTCrfvM9JeA94bNi2.jpg",
            "vote_average": 8.2,
            "vote_count": 418,
        },
        {
            "backdrop_path": "/35SS0nlBhu28cSe7TiO3ZiywZhl.jpg",
            "first_air_date": "2018-05-02",
            "genre_ids": [10759, 18],
            "id": 77169,
            "name": "Cobra Kai",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Cobra Kai",
            "overview": "This Karate Kid sequel series picks up 30 years after the events of the 1984 All Valley Karate Tournament and finds Johnny Lawrence on the hunt for redemption by reopening the infamous Cobra Kai karate dojo. This reignites his old rivalry with the successful Daniel LaRusso, who has been working to maintain the balance in his life without mentor Mr. Miyagi.",
            "popularity": 1912.292,
            "poster_path": "/6POBWybSBDBKjSs1VAQcnQC1qyt.jpg",
            "vote_average": 8.1,
            "vote_count": 4105,
        },
        {
            "backdrop_path": "/yfXSvNfF43S0cxpxCEKaU17yZ64.jpg",
            "first_air_date": "1983-09-19",
            "genre_ids": [10751],
            "id": 2778,
            "name": "Wheel of Fortune",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Wheel of Fortune",
            "overview": "This game show sees contestants solve word puzzles, similar to those used in Hangman, to win cash and prizes determined by spinning a giant carnival wheel.",
            "popularity": 1709.561,
            "poster_path": "/2fvAIyVfFHQdhJ7OsJWuMlF7836.jpg",
            "vote_average": 6.8,
            "vote_count": 40,
        },
        {
            "backdrop_path": "/vjcuLy14kxgxCaBToAudZWrGQQh.jpg",
            "first_air_date": "2021-01-18",
            "genre_ids": [],
            "id": 117031,
            "name": "People Puzzler",
            "origin_country": [],
            "original_language": "en",
            "original_name": "People Puzzler",
            "overview": 'Three lucky contestants put their pop culture knowledge to the test to complete iconic, People Puzzler crosswords. The player with the most points at the end of three rounds wins the game and goes on to play the "Fast Puzzle Round" for an enormous cash prize.',
            "popularity": 1446.612,
            "poster_path": "/gELQSCY5KKIGQAmOHbcgcRGNlp5.jpg",
            "vote_average": 6,
            "vote_count": 10,
        },
        {
            "backdrop_path": "/l6zdjUDOaklBWfxqa7AtbLr2EnA.jpg",
            "first_air_date": "2021-12-13",
            "genre_ids": [10751, 35, 18],
            "id": 135753,
            "name": "Love Twist",
            "origin_country": ["KR"],
            "original_language": "ko",
            "original_name": "사랑의 꽈배기",
            "overview": "A drama depicting a sweet twist in love between the parents and children of three families around the love of two main characters.",
            "popularity": 1279.173,
            "poster_path": "/5bTF522eYn6g6r7aYqFpTZzmQq6.jpg",
            "vote_average": 2,
            "vote_count": 1,
        },
        {
            "backdrop_path": "/13Zr7Nl9ivlvAhuDTHKLoO7HFKL.jpg",
            "first_air_date": "2002-09-08",
            "genre_ids": [10764, 10767],
            "id": 153748,
            "name": "Big Brother Famosos",
            "origin_country": ["PT"],
            "original_language": "pt",
            "original_name": "Big Brother Famosos",
            "overview": "Big Brother Famosos is the celebrity version of Big Brother Portugal.",
            "popularity": 1109.874,
            "poster_path": "/ra056721T5KEAsUnqQ2gulHJnQX.jpg",
            "vote_average": 2,
            "vote_count": 1,
        },
        {
            "backdrop_path": "/gIApbx2ffXVhJb2D4tiEx2b06nl.jpg",
            "first_air_date": "2005-03-27",
            "genre_ids": [18],
            "id": 1416,
            "name": "Grey's Anatomy",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Grey's Anatomy",
            "overview": "Follows the personal and professional lives of a group of doctors at Seattle’s Grey Sloan Memorial Hospital.",
            "popularity": 1067.662,
            "poster_path": "/zPIug5giU8oug6Xes5K1sTfQJxY.jpg",
            "vote_average": 8.2,
            "vote_count": 7445,
        },
        {
            "backdrop_path": "/ktDJ21QQscbMNQfPpZBsNORxdDx.jpg",
            "first_air_date": "2016-01-25",
            "genre_ids": [80, 10765],
            "id": 63174,
            "name": "Lucifer",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Lucifer",
            "overview": "Bored and unhappy as the Lord of Hell, Lucifer Morningstar abandoned his throne and retired to Los Angeles, where he has teamed up with LAPD detective Chloe Decker to take down criminals.\xa0But the longer he's away from the underworld, the greater the threat that the worst of humanity could escape.",
            "popularity": 1033.231,
            "poster_path": "/ekZobS8isE6mA53RAiGDG93hBxL.jpg",
            "vote_average": 8.5,
            "vote_count": 11323,
        },
        {
            "backdrop_path": "/1P3QtW1IkivqDrKbbwuR0zCYIf8.jpg",
            "first_air_date": "2021-11-18",
            "genre_ids": [10765, 18],
            "id": 71914,
            "name": "The Wheel of Time",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "The Wheel of Time",
            "overview": "Follow Moiraine, a member of the shadowy and influential all-female organization called the “Aes Sedai” as she embarks on a dangerous, world-spanning journey with five young men and women. Moiraine believes one of them might be the reincarnation of an incredibly powerful individual, whom prophecies say will either save humanity or destroy it.",
            "popularity": 1031.622,
            "poster_path": "/mpgDeLhl8HbhI03XLB7iKO6M6JE.jpg",
            "vote_average": 7.9,
            "vote_count": 1043,
        },
        {
            "backdrop_path": "/wiE9doxiLwq3WCGamDIOb2PqBqc.jpg",
            "first_air_date": "2013-09-12",
            "genre_ids": [18, 80],
            "id": 60574,
            "name": "Peaky Blinders",
            "origin_country": ["GB"],
            "original_language": "en",
            "original_name": "Peaky Blinders",
            "overview": "A gangster family epic set in 1919 Birmingham, England and centered on a gang who sew razor blades in the peaks of their caps, and their fierce boss Tommy Shelby, who means to move up in the world.",
            "popularity": 1001.586,
            "poster_path": "/pE8CScObQURsFZ723PSW1K9EGYp.jpg",
            "vote_average": 8.6,
            "vote_count": 4877,
        },
        {
            "backdrop_path": "/41yaWnIT8AjIHiULHtTbKNzZTjc.jpg",
            "first_air_date": "2014-10-07",
            "genre_ids": [18, 10765],
            "id": 60735,
            "name": "The Flash",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "The Flash",
            "overview": 'After a particle accelerator causes a freak storm, CSI Investigator Barry Allen is struck by lightning and falls into a coma. Months later he awakens with the power of super speed, granting him the ability to move through Central City like an unseen guardian angel. Though initially excited by his newfound powers, Barry is shocked to discover he is not the only "meta-human" who was created in the wake of the accelerator explosion -- and not everyone is using their new powers for good. Barry partners with S.T.A.R. Labs and dedicates his life to protect the innocent. For now, only a few close friends and associates know that Barry is literally the fastest man alive, but it won\'t be long before the world learns what Barry Allen has become...The Flash.',
            "popularity": 980.885,
            "poster_path": "/lJA2RCMfsWoskqlQhXPSLFQGXEJ.jpg",
            "vote_average": 7.8,
            "vote_count": 9116,
        },
        {
            "backdrop_path": "/9hNJ3fvIVd4WE3rU1Us2awoTpgM.jpg",
            "first_air_date": "2021-12-24",
            "genre_ids": [18, 10765],
            "id": 96777,
            "name": "The Silent Sea",
            "origin_country": ["KR"],
            "original_language": "ko",
            "original_name": "고요의 바다",
            "overview": "During a perilous 24-hour mission on the moon, space explorers try to retrieve samples from an abandoned research facility steeped in classified secrets.",
            "popularity": 964.549,
            "poster_path": "/fFT0IgqtCOks4munDTxQwkvNJkd.jpg",
            "vote_average": 8.1,
            "vote_count": 214,
        },
        {
            "backdrop_path": "/8lBlBItnehgOAwFt0ezxlXuWeIO.jpg",
            "first_air_date": "2021-11-08",
            "genre_ids": [10766, 18],
            "id": 132375,
            "name": "Um Lugar ao Sol",
            "origin_country": ["BR"],
            "original_language": "pt",
            "original_name": "Um Lugar ao Sol",
            "overview": "",
            "popularity": 957.339,
            "poster_path": "/63qlVcvlVzOvMaFO8tFA2VG64Yc.jpg",
            "vote_average": 5,
            "vote_count": 5,
        },
        {
            "backdrop_path": "/eD2U2RwxQosUDwvu19n46KvJEf9.jpg",
            "first_air_date": "2021-09-13",
            "genre_ids": [18, 35],
            "id": 124549,
            "name": "Marry Me, Marry You",
            "origin_country": ["PH"],
            "original_language": "tl",
            "original_name": "Marry Me, Marry You",
            "overview": "A couple navigates the traditional expectations attached to marriage — that it extends beyond one’s partner, and includes their friends and family, too.",
            "popularity": 954.191,
            "poster_path": "/7qZUC0AQmSi7pxNP6cH3swkb8Is.jpg",
            "vote_average": 3.5,
            "vote_count": 6,
        },
        {
            "backdrop_path": "/t9gfV0eM9nWqJ4vMey4CSYFiqmZ.jpg",
            "first_air_date": "2021-11-14",
            "genre_ids": [18, 9648],
            "id": 117488,
            "name": "Yellowjackets",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Yellowjackets",
            "overview": "This equal parts survival epic, psychological horror story and coming-of-age drama tells the saga of a team of wildly talented high school girls soccer players who become the (un)lucky survivors of a plane crash deep in the remote northern wilderness. The series chronicles their descent from a complicated but thriving team to savage clans, while also tracking the lives they’ve attempted to piece back together nearly 25 years later.",
            "popularity": 951.374,
            "poster_path": "/XtnjzjjFAnmTEiDk4xu7diCvMF.jpg",
            "vote_average": 7.3,
            "vote_count": 83,
        },
        {
            "backdrop_path": "/1R68vl3d5s86JsS2NPjl8UoMqIS.jpg",
            "first_air_date": "2021-11-24",
            "genre_ids": [10759, 18],
            "id": 88329,
            "name": "Hawkeye",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Hawkeye",
            "overview": "Former Avenger Clint Barton has a seemingly simple mission: get back to his family for Christmas. Possible? Maybe with the help of Kate Bishop, a 22-year-old archer with dreams of becoming a superhero. The two are forced to work together when a presence from Barton’s past threatens to derail far more than the festive spirit.",
            "popularity": 934.608,
            "poster_path": "/pqzjCxPVc9TkVgGRWeAoMmyqkZV.jpg",
            "vote_average": 8.4,
            "vote_count": 1507,
        },
        {
            "backdrop_path": None,
            "first_air_date": "2021-11-15",
            "genre_ids": [18],
            "id": 122551,
            "name": "Viral Scandal",
            "origin_country": ["PH"],
            "original_language": "tl",
            "original_name": "Viral Scandal",
            "overview": "The lives of a simple family becomes disrupted when a scandalous video involving their eldest daughter goes viral.",
            "popularity": 931.446,
            "poster_path": "/zPsJG3DRDeZZCoja9nnU6p4d67V.jpg",
            "vote_average": 2,
            "vote_count": 1,
        },
        {
            "backdrop_path": "/xAKMj134XHQVNHLC6rWsccLMenG.jpg",
            "first_air_date": "2021-10-12",
            "genre_ids": [80, 10765],
            "id": 90462,
            "name": "Chucky",
            "origin_country": ["US"],
            "original_language": "en",
            "original_name": "Chucky",
            "overview": "After a vintage Chucky doll turns up at a suburban yard sale, an idyllic American town is thrown into chaos as a series of horrifying murders begin to expose the town’s hypocrisies and secrets. Meanwhile, the arrival of enemies — and allies — from Chucky’s past threatens to expose the truth behind the killings, as well as the demon doll’s untold origins.",
            "popularity": 921.991,
            "poster_path": "/iF8ai2QLNiHV4anwY1TuSGZXqfN.jpg",
            "vote_average": 7.9,
            "vote_count": 2898,
        },
        {
            "backdrop_path": "/5npLowyLY2fqUpyAOq2x0bXwwIv.jpg",
            "first_air_date": "2022-01-05",
            "genre_ids": [18],
            "id": 134949,
            "name": "Rebelde",
            "origin_country": ["MX"],
            "original_language": "es",
            "original_name": "Rebelde",
            "overview": "Head back to Elite Way School as a new generation of students hope to win the Battle of the Bands.",
            "popularity": 916.815,
            "poster_path": "/jRlI5euugVZR6a1Ptt0nSWeiWH.jpg",
            "vote_average": 7.3,
            "vote_count": 88,
        },
    ],
    "total_pages": 6162,
    "total_results": 123234,
}


class Command(BaseCommand):
    help = "create data for developing purposes"

    def add_arguments(self, parser):
        parser.add_argument(
            "--use_api",
            action="store_true",
            help="uses api call to get 10 most popular shows",
        )

    def handle(self, *args, **options):
        # Only possible in dev mode
        if settings.DEBUG:
            print("clearing database")
            # Truncate all previous data

            with connection.cursor() as cursor:
                cursor.execute("delete from api_viewhistory", [])
                cursor.execute("delete from api_usertvshow", [])
                cursor.execute("delete from api_tvshow", [])

            if options["use_api"]:
                # use api call
                url = "https://api.themoviedb.org/3/tv/popular?api_key={}&language=en-US&page=1".format(
                    API_KEY
                )
                response = requests.get(url)
                response_data = response.json()

            else:
                # use TEST_DATA dict
                response_data = TEST_DATA

            # create show data
            for show_data in response_data.get("results"):
                # create show
                tvshow = TvShow.objects.create(
                    show_title=show_data.get("name"),
                    api_id=show_data.get("id"),
                    is_detailed=False,
                    first_air_date=show_data.get("first_air_date"),
                    vote_average=show_data.get("vote_average"),
                    vote_count=show_data.get("vote_count"),
                    overview=show_data.get("overview"),
                    poster_path=show_data.get("poster_path"),
                )

            # get testuser or create
            try:
                test_user = User.objects.get(email="testuser@test.com")
            except User.DoesNotExist:
                test_user = User.objects.create(
                    email="testuser@test.com",
                    password="TestUser12345!",
                )

            show1 = TvShow.objects.first()
            show2 = TvShow.objects.last()

            user_tv_show = UserTvShow.objects.create(
                userprofile=test_user.userprofile, show=show1
            )
            UserTvShow.objects.create(userprofile=test_user.userprofile, show=show2)
            ViewHistory.objects.create(
                user_tvshow=user_tv_show,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=1),
            )
