# -*- coding: utf-8 -*-
from typing import List, Dict, Any

PLACES = [

    # ══════════════════════════════════════════
    #  ԵՐԵՎԱՆ / Հայաստան
    # ══════════════════════════════════════════

    {
        "id": "kond-house",
        "category": "yerevan",
        "subcategory": "bars",
        "title_hy": "The Kond House",
        "title_en": "The Kond House",
        "location_hy": "Երևան, Լեո 46",
        "location_en": "46 Leo St, Yerevan",
        "maps_url": "https://maps.app.goo.gl/bzqxdPX6TcJt4qPA6",
        "rating": 4.7,
        "thumb": "/static/img/places/kond-house-bbq.jpg",
        "images": [
            "/static/img/places/kond-house-bbq.jpg",
            "/static/img/places/kond-house-dessert-or-cocktail.jpg",
            "/static/img/places/kond-house-terrace.jpg",
            "/static/img/places/kond-house-bar.jpg",
        ],
        "short_hy": "Տանիք, խորոված, գինի Կոնի սրտում",
        "short_en": "Rooftop BBQ and wine in Kond's heart",
        "description_hy": (
            "Թաքնած Քոնդ թաղամասի նեղ փողոցների մեջ՝ The Kond House‑ը ավելի շատ "
            "ընկերների բակ է հիշեցնում, քան պաշտոնական ռեստորան։ Քիչ աստիճաններ "
            "վերև, և դու արդեն տանիքիտ ես՝ ծուռ տանիքների, կախված լվացքի ու քաղաքի "
            "լույսերի տեսարանով՝ հին Երևանի տեքսուրայի և հարմարավետ ժամանակակից "
            "մթնոլորտի խառնուրդում։ "
            "Խոհանոցը ամբողջությամբ խորովածի և տնային հայկական ուտելիքի վրա է՝ "
            "խորոված խոզի միս, տնային լոր, ձուկ շամփուրի վրա, մեծ ափսեներ գյուղական "
            "կարտոֆիլով ու թարմ աղցաններով, որոնք դնում ես սեղանի կենտրոնում, որ բոլորը կիսեն։ "
            "Սա այն տեղն է, որտեղ պատվիրում ես խառը սեթ, շիշ հայկական կարմիր գինի "
            "կամ կոկտեյլների ցուցակից Negroni, և երեկոն ինքն իրեն երկարում է մինչև "
            "ուշ գիշեր։ "
            "Ներսում՝ փոքրիկ բար է՝ սուրճով, դասական կոկտեյլներով ու տնային խմիչքներով, "
            "իսկ երեկոյան երաժշտությունն ու մեղմ լույսերը տանիքը դարձնում են փոքր միջոցառում՝ "
            "թաքնված քաղաքի վրայի տանիքների միջև։"
        ),
        "description_en": (
            "Hidden in the narrow streets of Kond, one of the oldest neighborhoods "
            "of Yerevan, The Kond House feels more like visiting a friend's backyard "
            "than going to a formal restaurant. A few steps up and you are already "
            "on a rooftop terrace with views over crooked roofs, hanging laundry and "
            "the city lights in the distance a perfect mix of old Yerevan texture and "
            "modern comfort. "
            "The kitchen is all about hearty grill and home-style Armenian food: pork "
            "khorovats with a proper smoky crust, homemade sausages, trout or sterlet "
            "on skewers, big plates of village potatoes with herbs, and fresh salads "
            "like Greek or Caesar to share in the middle of the table. This is the kind "
            "of place where you order a set of mixed meats, a bottle of Armenian red "
            "wine or a Negroni from the cocktail list, and the evening naturally turns "
            "into a long, loud dinner with friends. "
            "Inside, a cozy bar serves coffee, classic cocktails and house drinks, while "
            "in the evenings the music and soft lights make the terrace feel almost like "
            "a small party hidden above the streets. It is easy to imagine starting with "
            "sunset photos over Kond, then slowly moving into grilled ribs, wine, a "
            "dessert and a strong nightcap and leaving with the feeling that you have "
            "discovered one of Yerevan's most atmospheric corners rather than just another "
            "restaurant."
        ),
    },                              # ← }, կոմայով
    {
        "id": "ulikhanyan-club",
        "category": "yerevan",
        "subcategory": "clubs",
        "title_hy": "Ulikhanyan Club",
        "title_en": "Ulikhanyan Club",
        "location_hy": "Երևան, Սայաթ-Նովա պողոտա 7",
        "location_en": "7 Sayat-Nova Ave, Yerevan",
        "maps_url": "https://maps.app.goo.gl/KRvsZWdKTFRCGB7M9",
        "rating": 4.8,
        "thumb": "/static/img/places/ulikhanyan-stage.jpg",
        "images": [
            "/static/img/places/ulikhanyan-stage.jpg",
            "/static/img/places/ulikhanyan-bar.jpeg",
            "/static/img/places/ulikhanyan-audience.jpeg",
        ],
        "short_hy": "Ջազ, գինի ու live սեթեր Սայաթ‑Նովայի վրա",
        "short_en": "Jazz, wine and late-night sets on Sayat-Nova Avenue",
        "description_hy": (
            "Սայաթ‑Նովա պողոտայի 7 համարի նկուղում գտնվող Ulikhanyan Club‑ը այն "
            "տեղն է, որտեղ «մի բաժակ գինի կնստենք ու կգնանք» արտահայտությունը շատ "
            "արագ վերածվում է մինչև վերջին բիս մնալու երեկոյի։ Փոքր, աղյուսապատ "
            "սրահ, բեմը գրեթե ձեռքիդ տակ, սեղաններ ու բարի զուգակցություն՝ "
            "մթնոլորտը ավելի շատ հիշեցնում է private jam‑session, քան մեծ концерт։ "
            "Երբ խմբի ջազը, fusion‑ը կամ էթնո‑ջազը սկսում է, քեզ թվում է, թե նստած "
            "ես փորձի վրա, ոչ թե պաշտոնական համերգում։ "
            "Բարը լուրջ է վերաբերվում խմիչքներին․ այստեղ կգտնես հայկական կարմիր "
            "և սպիտակ գինիներ, դասական կոկտեյլներ՝ Old Fashioned, Negroni, Dry "
            "Martini և խնամքով ընտրված բրենդի՝ դանդաղ երեկոյան համար։ Պարզ, "
            "բարային ուտեստներն ուղեկցում են խմիչքներին, ոչ թե ծանրացնում "
            "երեկոն։ "
            "Գրեթե ամեն երեկո կա live ծրագիր՝ jam‑session‑ներ, տոմսով համերգներ "
            "ու փոքրիկ փառատոնային line‑up‑ներ, իսկ հանդիսատեսը խառն է՝ "
            "երաժիշտներ, երևանցիներ ու հյուրեր, որոնք հաճախ ակումբն գտնում են "
            "բերանացի պատմություններից։ Եթե ուզում ես զգալ Երևանի գիշերային "
            "կողմը առանց մեծ, աղմկոտ ակումբների, ապա Ulikhanyan‑ը հենց այդ "
            "հարմարավետ, ջազային sweet spot‑ն է։"
        ),
        "description_en": (
            "Tucked in the basement at 7 Sayat-Nova Avenue, Ulikhanyan Club is one "
            "of those places where you go just for one drink and end up staying until "
            "the last encore. The room is small, brick-walled and intimate, with the "
            "stage almost within arm's reach, so when the band starts playing jazz, "
            "fusion or ethno-jazz, you feel more like part of a private jam session "
            "than a big concert. "
            "The bar takes its drinks seriously: a solid wine list with Armenian reds "
            "and whites, classic cocktails from Old Fashioned and Negroni to dry "
            "Martinis, and a good selection of Armenian brandy for a slow late-night "
            "sip. Simple bar snacks complete the picture without stealing the focus "
            "from the music. "
            "Live music is on almost every evening, from jam sessions on Mondays to "
            "ticketed concerts and festival-style lineups, and the crowd is a mix of "
            "musicians, locals and curious visitors who found the club by word of "
            "mouth. If you want to feel Yerevan's night side without going to a noisy "
            "club, Ulikhanyan is exactly that sweet spot – dim lights, great sound, "
            "strong drinks and the sense that you have discovered a small underground "
            "heart of the city's music scene."
        ),
    },                              # ← }, կոմայով
    {
            "id": "corpous-gastrobar",
            "category": "yerevan",
            "subcategory": "restaurants",
            "title_hy": "Corpous Gastrobar",
            "title_en": "Corpous Gastrobar",
            "location_hy": "Երևան, Հյուսիսային պողոտա 5",
            "location_en": "5 Northern Ave, Yerevan",
    "maps_url": "https://maps.app.goo.gl/chk3jk6zxJAZqBM36",
    "rating": 4.6,
    "thumb": "/static/img/places/corpous-interior.jpg",
    "images": [
        "/static/img/places/corpous-interior.jpg",
        "/static/img/places/corpous-food.jpg",
        "/static/img/places/corpous-cocktail.jpg",
    ],
    "short_hy": "Նախաճաշից մինչև կոկտեյլ՝ Հյուսիսային պողոտայում",
    "short_en": "From premium breakfast to late-night cocktails",
    "description_hy": (
        "Հյուսիսային պողոտայի վրա նստած Corpous Gastrobar‑ը այն վայրերից է, "
        "որտեղ կարող ես գալ և՛ վաղ առավոտյան սուրճի ու նախաճաշի, և՛ ուշ "
        "երեկոյան՝ կոկտեյլների և երաժշտության համար։ Ներսում լուսավոր է և "
        "ժամանակակից՝ մեծ պատուհաններ, փափուկ բազկաթոռներ ու բաց բար, այնպես որ "
        "մթնոլորտը միաժամանակ քաղաքային և ջերմ է՝ հարմար թե՛ ընկերների խմբի, թե՛ "
        "ավելի ինտիմ հանդիպման համար։ "
        "Մենյուն սահուն անցնում է նախաճաշից դեպի ընթրիք․ առավոտյան կարող ես ընտրել "
        "Eggs Benedict սաղմոնով կամ հայկական breakfast՝ թարմ հացով, պանրով ու "
        "կանաչիներով, իսկ օրվա երկրորդ կեսին անցնել միջերկրածովյան ուտեստների՝ "
        "խրթխրթան calamari, թունա տարտար, տրյուֆելային պաստա կամ լավ պատրաստված "
        "բեֆ կարպաչո։ Անուշեղենին էլ այստեղ լուրջ են վերաբերվում․ syrniki մանգոյի "
        "սոուսով, ճիշտ պատրաստված cheesecake և այլ քաղցրավենիքներ, որոնք իդեալական "
        "են թե՛ կաթնային սուրճի, թե՛ դեսերտային գինու հետ։ "
        "Բարը ունի ամբողջական wine list և իր փոքր կոկտեյլային մշակույթը․ prosecco, "
        "խնամքով ընտրված կարմիր և սպիտակ գինիներ, ինչպես նաև signature կոկտեյլներ, "
        "որոնց լուսանկարներն հաճախ հայտնվում են սոցցանցերում որպես «նոր մենյուի թարմ "
        "դրոփ»։ Երեկոյան, երբ Հյուսիսային պողոտայի լույսերը միանում են, մեղմ "
        "երաժշտությունը և բաժակների զնգոցը տեղը վերածում են հարմարավետ քաղաքային "
        "լաունջի՝ այնպիսի երեկոյի, երբ վերջում հասկանում ես, որ սա ուղղակի պատահական "
        "կանգառ չէր, այլ վայր, ուր ուզում ես հետ գալ։"
    ),
    "description_en": (
        "Sitting right on Northern Avenue, Corpous Gastrobar is the kind of place "
        "you can visit both for a slow morning coffee and breakfast, and for "
        "cocktails and music late at night. Inside, it feels bright and modern, "
        "with large windows, soft armchairs and an open bar, so the atmosphere is "
        "both urban and warm – equally good for a group of friends or a more "
        "intimate date. "
        "The menu slides smoothly from breakfast to dinner: in the morning you can "
        "go for Eggs Benedict with salmon or an Armenian Breakfast with fresh "
        "bread, cheese and herbs, then switch to Mediterranean-style plates like "
        "crispy calamari, fresh tuna tartare, truffle pasta or a nicely prepared "
        "beef carpaccio. Dessert is taken seriously too – syrniki with mango sauce, "
        "a proper cheesecake and other sweet plates that pair perfectly with a "
        "cappuccino or a glass of dessert wine. "
        "The bar has a full wine list and its own cocktail culture: elegant "
        "prosecco, carefully chosen reds and whites, plus signature cocktails that "
        "often appear on social media as fresh drops from the new menu. In the "
        "evening, when the lights of Northern Avenue come on, the soft music and "
        "clinking glasses turn the space into a cozy city lounge – the kind of "
        "night where you suddenly realize this was not just a random stop, but a "
        "place you will want to come back to."
    ),
},
{
    "id": "tsaghkadzor-ski-resort",
    "category": "armenia",
    "subcategory": "other",
    "title_hy": "Ծաղկաձոր լեռնադահուկային հանգույց և ճոպանուղի",
    "title_en": "Tsaghkadzor Ski Resort Ropeway",
    "location_hy": "Հայաստան, Ծաղկաձոր, Տանձաղբյուր փողոց",
    "location_en": "Tandzaghbyur St, Tsaghkadzor",
    "maps_url": "https://maps.app.goo.gl/MJ9o9aAWFEVp82t8A",
    "rating": 4.5,
    "thumb": "/static/img/places/tsaghkadzor-summit-view.webp",
    "images": [
        "/static/img/places/tsaghkadzor-summit-view.webp",
        "/static/img/places/tsaghkadzor-ski-snowboard.webp",
        "/static/img/places/tsaghkadzor-ropeway-winter.jpg",
    ],
    "short_hy": "Ճոպանուղի, ձյուն ու լեռների տեսարան Ծաղկաձորում",
    "short_en": "Winter sports, summer views and a long mountain day",
    "description_hy": (
        "Ծաղկաձորը այն տեղն է, որտեղ «մի անգամ ճոպանուղիով կբարձրանանք ու "
        "կվերադառնանք» արտահայտությունը գրեթե երբեք չի աշխատում։ Ձմռանը քաղաքը "
        "վերածվում է կոմպակտ լեռնադահուկային հանգստավայրի՝ փափուկ ձյուն, երկար "
        "վազորդեր և ճոպանուղի, որը քեզ բարձրացնում է հարթակից վեր, բացելով լայն "
        "պանորամասներ շրջակա լեռների վրա։ Նույնիսկ եթե երբեք չես սահել, պարզապես "
        "նստել ճոպանուղու նստարանին և դիտել, թե ինչպես է քաղաքը կամաց վերածվում փոքր "
        "կետերի, արդեն բավական է, որ զգաս․ սա սովորական օր չէ, այլ փոքր լեռնային "
        "արկած։ "
        "Ովքեր դահուկ կամ սնայբորդ են սիրում, Ծաղկաձորը դառնում է խաղադաշտ․ տեղում "
        "կարող ես վարձել սարքավորումները, բարձրանալ վերև և հետո այլևս ժամերին "
        "չնայել։ Կան և՛ մեղմ վազորդեր երեխաների ու սկսնակների համար, և՛ ավելի "
        "սուր թեքություններ փորձառուների համար։ Վազքի միջև մտնում ես փոքրիկ "
        "սրճարան՝ տաք շոկոլադի կամ mulled wine‑ի համար, տաքացնում ձեռքերդ ու "
        "կրկին դուրս գալիս ձյան վրա․ «մի անգամ կսահենք»‑ը շատ արագ վերածվում է "
        "ամբողջ օր տևող ձմեռային ծրագրի։ "
        "Ամռանը նույն ճոպանուղին քեզ տանում է կանաչ բլուրների ու անտառների վրայով․ "
        "մաքուր լեռնային օդ, լռություն և հեռվում բացվող լեռնաշղթա։ Վերին կայանում "
        "կարող ես քայլել գագաթի եզրով, լուսանկարել տեսարանները, անել փոքրիկ "
        "պիկնիկ կամ պարզապես նստել և հետևել, թե ինչպես է լույսը փոխվում լանջերի վրա։ "
        "Երբ երեկոյան վերադարձող ճոպանուղու վագոնում նստած ես, զգում ես, որ "
        "հասցրել ես և՛ սահել, և՛ քայլել, և՛ պարզապես հանգստանալ՝ առանց Երևանից "
        "շատ հեռանալու։"
    ),
    "description_en": (
        "Tsaghkadzor is the kind of place where the sentence “we’ll just take the "
        "ropeway once and head back” almost never happens. In winter the town turns "
        "into a compact ski resort – soft snow, long runs and a ropeway that lifts "
        "you high above the valley, opening up wide panoramas of the surrounding "
        "mountains. Even if you have never skied before, simply sitting on the "
        "chairlift and watching the town slowly disappear below is enough to feel "
        "that this is not a regular day trip, but a small mountain adventure. "
        "If you do ski or snowboard, Tsaghkadzor becomes your playground. You rent "
        "the gear on the spot, ride up, and after the first descent you stop counting "
        "hours. There are sleds and tubing, gentle slopes for kids and beginners, and "
        "steeper lines for those who want speed. After each run you can hide inside a "
        "small café for a hot chocolate or mulled wine, warm your hands and go back "
        "out again – what starts as “let’s just try one slope” usually turns into a "
        "full-on winter day. "
        "In summer Tsaghkadzor looks completely different. The same ropeway takes "
        "you over green hills and forests, into clear, cool mountain air where "
        "silence replaces the winter noise. At the top you can walk along the ridges, "
        "take photos of the mountain chain, have a small picnic or simply sit and "
        "watch the light move across the slopes. By the time you come back down in "
        "the evening, you feel like you have managed to ski, hike and recharge all "
        "in one day, without ever being too far from Yerevan."
    ),
},
{
    "id": "lake-sevan",
    "category": "armenia",
    "subcategory": "cafes",
    "title_hy": "Սևանա լիճ",
    "title_en": "Lake Sevan",
    "location_hy": "Հայաստան, Սևան",
    "location_en": "Sevan, Armenia",
    "maps_url": "https://maps.app.goo.gl/ySyoBNGzfBtdFSdM9",
    "rating": 4.9,
    "thumb": "/static/img/places/sevan-sunset-lakeview.jpg",
    "images": [
        "/static/img/places/sevan-sunset-lakeview.jpg",
        "/static/img/places/sevan-beach-club-overview.jpg",
        "/static/img/places/sevan-lakeside-drink-food.jpg",
    ],
    "short_hy": "Լողափ, մայրամուտ ու chill երաժշտություն Սևանի ափին",
    "short_en": "Beach, golden sunsets and chill music by the lake",
    "description_hy": (
        "Սևանա լիճը Հայաստանի այն վայրերից է, որտեղ ժամանակը սկսում է ուրիշ կերպ "
        "անցնել։ Ափ հասնելուն պես օդն արդեն այլ է՝ ավելի թեթև, ավելի մաքուր, "
        "ձայնը ջրի ալիքների, իսկ հեռվում՝ Սևանավանքը, որ կանգնած է թերակղզու "
        "վրա կարծես ամբողջ լճի վրա հսկի։ "
        "Ամռանը Սևանի ափը կյանքով է լցվում. մարդիկ լողում են, պառկում ժայռերին ու "
        "ավազի վրա, ֆրիսբի են խաղում կամ պարզապես նստած ջրին նայում՝ առանց "
        "ոչ մի ծրագրի։ Ափամերձ սրճարաններն ու բարերն աշխատում են ամբողջ ձմռան "
        "ու ամռան ընթացքում, ջրի եզրին քեզ առաջարկելով սառը գարեջուր, թան, "
        "թարմ ձուկ՝ ուղղակի բացօթյա կրակի վրա, կամ պարզ chill playlist, որ "
        "հնչում է lazy afternoon‑ի ճիշտ soundtrack‑ի պես։ "
        "Բայց Սևանի լավագույն պահը մայրամուտն է։ Երբ արևը սկսում է իջնել "
        "հարավ‑արևմտյան կողմից, ջուրը նախ ոսկեգույն, հետո մոխրագույն‑կապույտ "
        "է դառնում, ու թվում է, թե ամբողջ լիճը մի պահ կանգ է առնում։ "
        "Ափամերձ սրճարաններից մեկի տախտամածին նստած, բաժակ գինիով կամ "
        "սուրճով ձեռքիդ, chill երաժշտությամբ ֆոնին, մայրամուտ Սևանի վրա "
        "դառնում է Հայաստանի ամենահուզիչ «ոչինչ չանելու» պահերից մեկը։ "
        "Ճանապարհին կամ ճանապարհ դուրս գալուց առաջ Սևանավանք մի բաց թողնես. "
        "Ժ. դ. կառույցների ծածկոցից վեր նայեցած լճի լայն տեսարանը, ու "
        "մի փոքր հնագույն քարե եկեղեցու ու կապույտ ջրի այդ կոնտրաստը "
        "Հայաստանի ամենաճանաչելի կադրերից է, ու ճիշտ հասկանում ես ինչու։"
    ),
    "description_en": (
        "Lake Sevan is one of those places in Armenia where time starts moving "
        "differently. The moment you arrive at the shore, the air already feels "
        "lighter and cleaner, the sound shifts to water and wind, and in the "
        "distance Sevanavank monastery stands on its peninsula like it has been "
        "watching over the whole lake for centuries – because it has. "
        "In summer the shore fills with life: people swimming off the rocks or "
        "stretching out on the sand, playing frisbee, or simply sitting by the "
        "water with no particular plan. The cafes and bars along the beach run "
        "through the season, offering cold beer, tan (Armenian yogurt drink), "
        "fresh fish straight off an open fire, and a chill playlist that sounds "
        "exactly like the right soundtrack for a slow afternoon. "
        "But the best moment at Sevan is the sunset. As the sun drops toward the "
        "southwest, the water turns gold first, then a deep blue-grey, and the "
        "whole lake seems to pause for a second. Sitting on the terrace of one "
        "of the lakeside cafes, a glass of wine or coffee in hand, music low in "
        "the background, watching the light fade over Sevan becomes one of "
        "Armenia's most memorable do-nothing moments. "
        "On the way in or out, do not skip Sevanavank: the wide view of the lake "
        "from the top of the monastery steps, the contrast between the ancient "
        "stone church and the endless blue water below, is one of the most "
        "recognizable images of Armenia, and standing there you immediately "
        "understand why."
    ),
},
{
    "id": "van-ardi-winery",
    "category": "armenia",
    "subcategory": "other",
    "title_hy": "Van Ardi Winery",
    "title_en": "Van Ardi Winery",
    "location_hy": "Հայաստան, Ոսկեհատ գյուղ, Արարատի մարզ",
    "location_en": "Voskehat village, Armavir region, Armenia",
    "maps_url": "https://maps.app.goo.gl/dvdSD8S6KaHfHTJE7",
    "rating": 4.7,
    "thumb": "/static/img/places/van-ardi-sunset-vineyard.jpg",
    "images": [
        "/static/img/places/van-ardi-sunset-vineyard.jpg",
        "/static/img/places/van-ardi-vineyard-terrace.jpg",
        "/static/img/places/van-ardi-wine-tasting.jpg",
    ],
    "short_hy": "Հայկական գինի՝ անմիջապես Արարատյան դաշտի այգիներից",
    "short_en": "Armenian wine straight from Ararat Valley vineyards",
    "description_hy": (
        "Van Ardi‑ն այն գինու տները չի, որտեղ գնում ես պարզապես բաժակ գինի "
        "խմելու։ Սա այն վայրն է, որտեղ հասկանում ես, թե ինչ է նշանակում "
        "«հայկական գինու terroir»՝ Արարատ լեռան ստվերում, Արարատյան դաշտի "
        "բաց արևի տակ, հազարամյա խաղողի սորտերով, որ ուրիշ տեղ գրեթե "
        "չես գտնի։ "
        "Այգիներից անմիջապես սկսվում է ամեն ինչ․ Voskehat, Kangun, Areni, "
        "Haghtanak՝ հայկական autochtone սորտեր, որոնք Van Ardi‑ի թիմը "
        "մշակում է minimal intervention փիլիսոփայությամբ՝ որ խաղողն ինքն "
        "արտահայտի իր ծագումը, ոչ թե խեղդվի ծանր oak‑ի կամ ավելորդ "
        "տեխնոլոգիայի մեջ։ "
        "Tasting‑ը կարող ես անցկացնել cellar‑ում կամ բաց տարածքում՝ "
        "Արարատ լեռան տեսարանով ֆոնին, ինչը ուղղակի անհնար է ignore անել։ "
        "Յուրաքանչյուր բաժակի հետ բացատրում են՝ ինչ այգուց, ինչ տարեկան, "
        "ինչ ոճ․ սա ոչ թե tour է, այլ կենդանի խոսակցություն գինու, "
        "հողի ու Հայաստանի մասին։ "
        "Եթե ուզում ես Հայաստանի wine culture‑ն իր ամենաազնիվ ձևով "
        "ճաշակել՝ առանց Grand Tour‑ի ծանրոցի, Van Ardi‑ն հենց այն "
        "կոմպակտ, անկեղծ ու հիշվող կես‑օրյա ծրագիրն է, "
        "որ Երևանից ընդամենը մի ժամ հեռու է։"
    ),
    "description_en": (
        "Van Ardi is not the kind of winery you visit just to have a glass of "
        "wine. It is the place where you begin to understand what Armenian wine "
        "terroir actually means: in the shadow of Mount Ararat, under the open "
        "sun of the Ararat Valley, with ancient grape varieties that you will "
        "barely find anywhere else in the world. "
        "Everything starts in the vineyard: Voskehat, Kangun, Areni, Haghtanak "
        "– Armenian autochthonous varieties that the Van Ardi team cultivates "
        "with a minimal intervention philosophy, letting the grapes express their "
        "origin rather than being overwhelmed by heavy oak or unnecessary "
        "technology. The results are wines that feel honest and precise, with "
        "a character that is unmistakably tied to this specific corner of "
        "the Caucasus. "
        "The tasting can be arranged in the cellar or outside, with Mount Ararat "
        "as a backdrop that is simply impossible to ignore. With each glass "
        "the team walks you through the vineyard source, the vintage, the style "
        "– this is not a scripted tour but a real conversation about wine, soil "
        "and Armenia. "
        "If you want to experience Armenian wine culture in its most honest form, "
        "without the weight of a grand organized tour, Van Ardi is exactly that "
        "compact, genuine and memorable half-day trip that sits just an hour "
        "from Yerevan, with one of the most dramatic mountain views in the "
        "country as a bonus."
    ),
},
{
    "id": "poloz-mukuch",
    "category": "armenia",
    "subcategory": "restaurants",
    "title_hy": "Պոլոզ Մուկուչ",
    "title_en": "Poloz Mukuch",
    "location_hy": "Հայաստան, Գյումրի, Վարդանանց հրապարակ 1",
    "location_en": "1 Vardananc Square, Gyumri, Armenia",
    "maps_url": "https://maps.app.goo.gl/bmZTmogSTztRqxTM9",
    "rating": 4.8,
    "thumb": "/static/img/places/poloz-mukuch-food-table.jpg",
    "images": [
        "/static/img/places/poloz-mukuch-food-table.jpg",
        "/static/img/places/poloz-mukuch-exterior.webp",
        "/static/img/places/poloz-mukuch-interior.jpg",
    ],
    "short_hy": "Գյումրիի հումորն ու խաշլաման մեկ սեղանի շուրջ",
    "short_en": "Gyumri humour and khashlama around one table",
    "description_hy": (
        "Գյումրի գնալ ու Պոլոզ Մուկուչ չայցելել՝ մոտավորապես նույնն է, ինչ "
        "Փարիզ գնալ ու Էյֆելյան աշտարակը բաց թողնելը։ Ոչ թե Գյումրիի "
        "լավագույն ռեստորանն է, այլ Գյումրիի բնավորության մի մաս, "
        "վայր, որտեղ քաղաքի հումորը, հյուրընկալությունն ու "
        "ուտելիքի հանդեպ լուրջ վերաբերմունքը մի տեղ են հավաքվել։ "
        "Ռեստորանն ինքնին Գյումրու հին քաղաքի սրտում է՝ սև տուֆ "
        "քարե շենք, փայտե լուսամուտներ, ներսում՝ երկար սեղաններ, "
        "ուժեղ լույս ու մթնոլորտ, որ ավելի շատ ընտանեկան հարսանիք "
        "է հիշեցնում, քան ֆորմալ ռեստորան։ "
        "Մենյուի կենտրոնում խաշն է ու խաշլաման՝ Գյումրիի "
        "գաստրոնոմիկ հպարտությունը։ Խաշը՝ ավանդական, ծանր, "
        "հոտավետ, մատուցվում է ռուշ հացով, սխտորով ու չոր "
        "գինիով, կամ ավելի ճիշտ՝ կոնյակով, ինչպես Գյումրիում "
        "վայել է։ Խաշլաման՝ փափուկ, հյութալի, բանջարեղենի "
        "հետ եփած, այն ուտեստն է, որի համար նստում ես ու "
        "հասկանում, թե ինչու են ասում՝ «Գյումրու ձեռքը ուրիշ բան "
        "է»։ "
        "Բայց Պոլոզ Մուկուչը ոչ միայն ուտելիք է, այլ ամբողջ "
        "performance․ մատուցողները կատակում են, հյուրերն "
        "արձագանքում են, ու հաճախ երեկոն վերածվում է "
        "ինքնաբուխ ճաշկերույթի՝ անծանոթ մարդկանց հետ մեկ "
        "սեղանի շուրջ, ովքեր կես ժամ հետո արդեն ծանոթ են "
        "թվում։ Սա Գյումրու հյուրընկալության կենտրոնացված "
        "ձևն է, ու հենց դրա համար մարդիկ հատուկ Երևանից "
        "գալիս են այստեղ։"
    ),
    "description_en": (
        "Going to Gyumri without visiting Poloz Mukuch is roughly the same as "
        "going to Paris and skipping the Eiffel Tower. It is not just Gyumri's "
        "best restaurant – it is a part of the city's character, a place where "
        "the local humour, hospitality and serious attitude toward food all come "
        "together under one roof. "
        "The restaurant sits in the heart of old Gyumri: a black tuff stone "
        "building with wooden windows, long communal tables inside, strong warm "
        "light and an atmosphere that feels more like a family wedding than a "
        "formal dining room. The moment you sit down you understand this is not "
        "the kind of place where you eat quickly and leave. "
        "At the centre of the menu is khash and khashlama – Gyumri's "
        "gastronomic pride. Khash is served the traditional way: heavy, "
        "fragrant, with lavash bread, raw garlic and a shot of dry wine or, "
        "more accurately, cognac, as is proper in Gyumri. The khashlama is "
        "tender, slow-cooked with vegetables and herbs, the kind of dish "
        "that makes you understand why people say the hands in Gyumri cook "
        "differently. "
        "But Poloz Mukuch is not only about food – it is a full performance. "
        "The waiters joke with the guests, the guests joke back, and evenings "
        "here often turn into spontaneous feasts where strangers at the next "
        "table feel like old friends half an hour later. This is Gyumri "
        "hospitality in its most concentrated form, and it is exactly why "
        "people make the trip from Yerevan just to eat here."
    ),
},
{
    "id": "dilijan-forest-cafe",
    "category": "armenia",
    "subcategory": "cafes",
    "title_hy": "Դիլիջանի անտառային սրճարան/բար",
    "title_en": "Dilijan Forest Cafe & Bar",
    "location_hy": "Հայաստան, Դիլիջան, Մյասնիկյան 5, շ. 28",
    "location_en": "28, 5 Myasnikyan St, Dilijan, Armenia",
    "maps_url": "https://maps.app.goo.gl/D7Dy1DB5hEBpouCh7",
    "rating": 4.4,
    "thumb": "/static/img/places/dilijan-forest-cafe-table.jpg",
    "images": [
        "/static/img/places/dilijan-forest-cafe-table.jpg",
        "/static/img/places/dilijan-forest-cafe-exterior.jpg",
        "/static/img/places/dilijan-forest-cafe-interior.jpg",
    ],
    "short_hy": "Անտառի մեջ սուրճ, մառախուղ ու հանգիստ",
    "short_en": "Coffee, mist and silence deep in the forest",
    "description_hy": (
        "Դիլիջանն ինքնին արդեն բնության մեջ ապրելու զգացողություն է, բայց "
        "անտառային սրճարանը դա մի աստիճան ավելի խոր է տանում։ Մյասնիկյան "
        "փողոցի անտառապատ հատվածում թաքնված՝ սա այն վայրն է, որտեղ "
        "գալիս ես առավոտյան մառախուղի մեջ, պատվիրում ես տաք սուրճ կամ "
        "թեյ, ու հասկանում ես, որ ձեռքիդ բաժակով ու ծառերի "
        "միջով ֆիլտրվող լույսով շրջապատված, Երևանի բոլոր deadlines‑ները "
        "հանկարծ շատ հեռու են թվում։ "
        "Ինտերիերը ջերմ է ու բնական՝ փայտ, բույսեր, "
        "հանգիստ անկյուններ, շատ բնական լույս ու "
        "անտառ նայող պատուհաններ, որոնք ամռանն ու աշնանը "
        "գրեթե կախարդական են։ Mенюն պարզ է, բայց ազնիվ՝ "
        "specialty սուրճ, տեղական թեյեր՝ Դիլիջանի խոտաբույսերով, "
        "տնական ըմպելիքներ, թեթև խորտիկներ ու անուշեղեն, "
        "ամեն ինչ այն մասշտաբով, որ ուտելու, ոչ թե ցուցադրելու համար է։ "
        "Երեկոյան տեղը վերածվում է մեղմ բարի՝ անտառային "
        "ֆոնով, մեղմ երաժշտությամբ ու լույսերով, որ շատ "
        "ավելի հաճելի է, քան ցանկացած Երևանյան rooftop bar, "
        "պարզապես ուրիշ լոգիկայով ու ուրիշ ռիթմով։ "
        "Եթե Դիլիջանում ես ու ուզում ես մի տեղ, ուր կարող ես "
        "երկու ժամ նստել գիրք կարդալ, ֆոտո անել, կամ "
        "պարզապես ոչինչ չանել անտառի ձայների ֆոնին, "
        "սա հենց այն վայրն է։"
    ),
    "description_en": (
        "Dilijan already feels like living inside nature, but the forest cafe "
        "takes that one level deeper. Hidden in the wooded stretch of "
        "Myasnikyan Street, this is the kind of place you arrive at on a misty "
        "morning, order a warm coffee or herbal tea, and suddenly realise that "
        "with a cup in your hands and light filtering through the trees, every "
        "deadline back in Yerevan feels very far away. "
        "The interior is warm and natural: wood, plants, quiet corners, plenty "
        "of natural light and forest-facing windows that in summer and autumn "
        "are almost magical. The menu is simple but honest – specialty coffee, "
        "local herbal teas made with Dilijan plants, homemade drinks, light "
        "snacks and desserts, all at a scale that feels like it was made to be "
        "enjoyed, not photographed. "
        "In the evenings the space shifts into a gentle bar mood: soft music, "
        "warm low lighting and the forest still visible through the windows, "
        "which makes it feel more atmospheric than most rooftop bars in Yerevan "
        "– just on a completely different rhythm and logic. "
        "If you are in Dilijan and need a place to sit for two hours with a "
        "book, take slow photos, or simply do nothing with the sounds of the "
        "forest in the background, this is exactly that place."
    ),
},
{
    "id": "jermuk-spa",
    "category": "armenia",
    "subcategory": "other",
    "title_hy": "Ջերմուկ՝ տաք ջրեր, առողջարան և հանգիստ երեկո",
    "title_en": "Jermuk: thermal waters, spa and a quiet evening",
    "location_hy": "Հայաստան, Ջերմուկ, Մյասնիկյան 27",
    "location_en": "27 Myasnikyan Street, Jermuk, Armenia",
    "maps_url": "https://maps.app.goo.gl/PaLF2jsqfafAZXFq5",
    "rating": 4.2,
    "thumb": "/static/img/places/jermuk-spa-lounge-evening.jpg",
    "images": [
        "/static/img/places/jermuk-spa-lounge-evening.jpg",
        "/static/img/places/jermuk-spa-pool-interior.jpeg",
        "/static/img/places/spa-hotel-exterior.webp",
    ],
    "short_hy": "Տաք ջրեր, լեռնային օդ ու լիարժեք հանգիստ Ջերմուկում",
    "short_en": "Thermal waters, mountain air and total rest in Jermuk",
    "description_hy": (
        "Ջերմուկը Հայաստանի այն վայրն է, ուր գնում ես «մի քանի օրով հանգստանալու» "
        "ու հետ գալիս այնպիսի զգացողությամբ, կարծես մարմինդ reset արել ես։ "
        "Ծովի մակերևույթից 2080 մ բարձրության վրա գտնվող այս լեռնային քաղաքը "
        "հայտնի է իր բնական հանքային ջրերով, որոնք ոչ միայն հայկական "
        "«Ջերմուկ» ապրանքանիշի հիմքն են, այլև օգտագործվում են "
        "բուժական ու spa պրոցեդուրաների մեջ՝ ուղղակի բնական աղբյուրներից։ "
        "Առողջարանում կամ հյուրանոցային spa‑ում մտնելուն պես "
        "ջրի ջերմությունը, լեռնային լռությունն ու "
        "մարմնիդ ծանրությունը, որ կամաց հալվում է ջրի մեջ, "
        "հասկացնում են, թե ինչու են մարդիկ հատուկ "
        "Ջերմուկ գալիս վերականգնվելու և ոչ թե պարզապես "
        "«տուրիստական» հանգստի։ "
        "Քաղաքն ինքնին հանգիստ է ու կոմպակտ. "
        "կենտրոնական պողոտան, հայտնի ջրախմբարանը "
        "ուր կարող ես անմիջապես աղբյուրից հանքային ջուր խմել "
        "փոքրիկ բաժակով, Ջերմուկի ջրվեժը, անտառային "
        "զբոսանքի երթուղիներ ու երեկոյան լռություն, "
        "որ Երևանից հետո զգում ես ֆիզիկապես։ "
        "Հյուրանոցներն ու առողջարանները առաջարկում են "
        "ամբողջական package՝ տաք bassein, մերսում, "
        "ֆիզիոթերապիա, հանքային լոգանքներ ու "
        "ճաշարան, որտեղ ուտում ես հանգիստ ու "
        "առանց շտապելու։ "
        "Ջերմուկը Հայաստանի wellness retreat‑ն է, "
        "որ գոյություն ունի Սովետական ժամանակներից, "
        "բայց մինչ օրս պահպանել է այն մաքուր, "
        "անկեղծ հանգստի մթնոլորտը, "
        "որ ոչ մի մոդայիկ spa resort չի կարող "
        "ամբողջովին կրկնօրինակել։"
    ),
    "description_en": (
        "Jermuk is the kind of place in Armenia you go to for a few days of rest "
        "and come back feeling like your body has been properly reset. Sitting at "
        "2080 metres above sea level, this quiet mountain town is known for its "
        "natural mineral waters – the same source behind Armenia's famous Jermuk "
        "water brand – which are also used in therapeutic and spa treatments "
        "drawn directly from natural springs. "
        "The moment you step into a sanatorium or hotel spa, the warmth of the "
        "thermal water, the mountain silence and the slow heaviness leaving your "
        "body make it immediately clear why people come here specifically to "
        "recover, not just to sightsee. "
        "The town itself is calm and compact: the central promenade, the famous "
        "drinking gallery where you can sip mineral water straight from the "
        "source in a small cup, the Jermuk waterfall, forest walking trails and "
        "an evening quiet that you feel physically after time in Yerevan. "
        "Hotels and sanatoria offer full packages: heated pools, massage, "
        "physiotherapy, mineral baths and a dining room where meals happen "
        "slowly and without rush. "
        "Jermuk is Armenia's wellness retreat, one that has existed since Soviet "
        "times but has kept the clean, unpretentious atmosphere of genuine rest "
        "that no trendy spa resort can fully replicate. Sometimes the real thing "
        "is simply the real thing."
    ),
},
{
    "id": "calumet-yerevan",
    "category": "yerevan",
    "subcategory": "pubs",
    "title_hy": "Calumet՝ փոքր սրահ, մեծ երաժշտություն",
    "title_en": "Calumet: small room, big music",
    "location_hy": "Երևան, Պուշկին փողոց",
    "location_en": "Pushkin St, Yerevan",
    "maps_url": "https://maps.app.goo.gl/ScP9M8a1Zukxx2vVA",
    "rating": 4.8,
    "thumb": "/static/img/places/calumet-table-drinks-food.jpg",
    "images": [
        "/static/img/places/calumet-table-drinks-food.jpg",
        "/static/img/places/calumet-live-music.jpg",
        "/static/img/places/calumet-bar-interior.jpg",
    ],
    "short_hy": "Փոքր սրահ, մեծ ձայն ու Երևանի լավագույն live երաժշտությունը",
    "short_en": "Tiny room, loud sound and Yerevan's best live music",
    "description_hy": (
        "Կան վայրեր, որոնք մեծ են իրենց չափերով, ու կան վայրեր, "
        "որոնք մեծ են իրենց էությամբ։ Calumet‑ը երկրորդ տեսակից է։ "
        "Պուշկին փողոցի փոքրիկ, մութ սրահը Երևանի ամենաազնիվ "
        "live music venue‑ներից մեկն է, ուր բեմն ու հանդիսատեսը "
        "գրեթե շնչում են միմյանց վրա, ու դա հենց այն է, "
        "ինչ տեղն անկրկնելի է դարձնում։ "
        "Ժանրային սահմաններ գրեթե չկան՝ blues, rock, jazz, "
        "funk, ethno, acoustic sets, անգամ փորձարարական "
        "ծրագրեր, և բոլորն էլ այստեղ հնչում են ուրիշ կերպ, "
        "քան մեծ բեմերի վրա, որովհետև փոքր տարածությունը "
        "երաժշտությունն ուղղակի կնքում է սրահի մեջ՝ "
        "առանց կորստի, առանց հեռավորության։ "
        "Բարը պարզ է ու ազնիվ՝ գարեջուր, գինի, կոկտեյլներ, "
        "ոչ մի ավելորդ շուք, ամբողջ ուշադրությունը բեմի վրա է։ "
        "Հաճախ կոնցերտներն անսպասելիորեն երկար են ձգվում, "
        "երբ բենդն ու հանդիսատեսն «ընկնում են» ռիթմի մեջ ու "
        "ոչ ոք չի ուզում կանգ առնել։ "
        "Calumet‑ը Երևանի այն underground heart‑ն է, "
        "որ գոյատևում է ոչ թե մարքեթինգով, "
        "այլ բերանացի պատմություններով ու "
        "մի անգամ լսելուց հետո անպայման հետ գալու "
        "ցանկությամբ։"
    ),
    "description_en": (
        "Some places are big in size, and some places are big in spirit. "
        "Calumet is firmly the second kind. This small, dimly lit room on "
        "Pushkin Street is one of Yerevan's most honest live music venues, "
        "where the stage and the audience are close enough to almost breathe "
        "on each other – and that is precisely what makes it irreplaceable. "
        "There are no strict genre boundaries here: blues, rock, jazz, funk, "
        "ethno, acoustic sets, even experimental nights, and all of them sound "
        "different than they would on a large stage, because the small space "
        "seals the music inside the room with nowhere for it to escape or "
        "dissolve into distance. "
        "The bar is simple and unpretentious – beer, wine, cocktails, no excess "
        "glamour – because the whole point of the evening is the stage. "
        "Concerts here often run longer than planned, when the band and the "
        "crowd fall into the same rhythm and nobody wants to stop. "
        "Calumet is the underground heart of Yerevan's music scene, one that "
        "survives not through marketing but through word of mouth and the simple "
        "fact that once you have been, you will want to come back. "
        "The kind of place that feels like a secret even when it is full."
    ),
},
{
    "id": "dargett-brewpub",
    "category": "yerevan",
    "subcategory": "bars",
    "title_hy": "Dargett գարեջրատուն",
    "title_en": "Dargett Craft Beer & Eatery",
    "location_hy": "Երևան, Արամ փողոց 72",
    "location_en": "72 Aram Street, Yerevan",
    "maps_url": "https://maps.app.goo.gl/iKPmd8JVE2kLYQGx8",
    "rating": 4.7,
    "thumb": "/static/img/places/dargett-beer-flight.jpeg",
    "images": [
        "/static/img/places/dargett-beer-flight.jpeg",
        "/static/img/places/dargett-brewpub-interior.jpg",
        "/static/img/places/dargett-food-and-beer.jpg",
    ],
    "short_hy": "Երևանի craft գարեջրի հիմնական հասցեն",
    "short_en": "Yerevan's home address for craft beer",
    "description_hy": (
        "Եթե Երևանում craft գարեջուր ես ուզում, Dargett‑ը այն տեղն է, "
        "ուր բոլոր ճանապարհները տանում են։ Արամ փողոցի 72 հասցեում "
        "գտնվող այս brewpub‑ը Հայաստանի craft beer մշակույթի "
        "առաջամարտիկներից է, ու տարիների ընթացքում դարձել է "
        "ոչ միայն վայր, այլ հղում կետ։ "
        "Կռունկների շարքը բարի հետևում ասում է ամեն ինչ՝ "
        "IPA, stout, wheat, sour, seasonal specials, "
        "ամեն ինչ պատրաստված տեղում, հայկական "
        "հումքով ու հստակ ձեռագրով։ Գարեջուրն այստեղ "
        "ոչ թե ուղղակի ըմպելիք է, այլ ոճ. "
        "կարող ես նստել բարի մոտ ու մատուցողին "
        "խնդրել օգնի ընտրել, և նա կբացատրի "
        "յուրաքանչյուր կռունկի պատմությունը "
        "առանց շտապելու։ "
        "Ուտեստները լրացնում են գարեջուրը, "
        "ոչ թե մրցում դրա հետ՝ burger‑ներ, "
        "nachos, wings, flatbread‑ներ, "
        "ամեն ինչ craft kitchen‑ի տրամաբանությամբ՝ "
        "բավականաչափ լուրջ, որ ամբողջ ճաշ անես, "
        "բայց բավականաչափ թեթև, որ երկրորդ "
        "բաժակից հետո էլ հարմարավետ լինես։ "
        "Ինտերիերը industrial է ու ջերմ "
        "միաժամանակ՝ բաց աղյուս, փայտ, "
        "բարձր առաստաղ ու երաժշտություն, "
        "որ հնչում է ճիշտ մակարդակով, "
        "ոչ չափազանց բարձր ու ոչ անտեսելի "
        "աղմուկ։ Շաբաթ‑կիրակի երեկոյան "
        "Dargett‑ը Երևանի craft scene‑ի "
        "կենդանի կենտրոնն է, բայց "
        "շաբաթվա ցանկացած երեկո "
        "կարող ես գալ ու "
        "նույն հաճույքն ստանալ։"
    ),
    "description_en": (
        "If you are looking for craft beer in Yerevan, Dargett is where all "
        "roads lead. Located at 72 Aram Street, this brewpub is one of the "
        "pioneers of Armenia's craft beer culture and has over the years become "
        "not just a venue but a reference point. "
        "The row of taps behind the bar says everything: IPA, stout, wheat, "
        "sour, seasonal specials – all brewed on site, with Armenian ingredients "
        "and a clear identity. The beer here is not just a drink but a statement, "
        "and if you sit at the bar and ask the staff to help you choose, they "
        "will walk you through every tap without rushing. "
        "The food complements the beer rather than competing with it: burgers, "
        "nachos, wings, flatbreads, all following craft kitchen logic – serious "
        "enough for a full meal but light enough that you still feel comfortable "
        "after your second pint. "
        "The interior is industrial and warm at the same time: exposed brick, "
        "wood, high ceilings and music at exactly the right level – present but "
        "never overwhelming. On weekend evenings Dargett is the living centre "
        "of Yerevan's craft scene, loud with conversation and clinking glasses, "
        "but on any weeknight it is equally good: quieter, easier to get a "
        "seat at the bar, and just as worth the visit."
    ),
},
{
    "id": "simona-home-bar",
    "category": "yerevan",
    "subcategory": "bars",
    "title_hy": "Simona Home Bar",
    "title_en": "Simona Home Bar",
    "location_hy": "Երևան, Արամ փողոց 80",
    "location_en": "80 Aram Street, Yerevan",
    "maps_url": "https://maps.app.goo.gl/dTjYCtmmiFmUorN99",
    "rating": 4.5,
    "thumb": "/static/img/places/simona-bar-counter.webp",
    "images": [
        "/static/img/places/simona-bar-counter.webp",
        "/static/img/places/simona-bar-cocktails.webp",
        "/static/img/places/simona-bar-interior.jpg",
    ],
    "short_hy": "Տնային ջերմությամբ բար՝ Արամ փողոցի վրա",
    "short_en": "A bar that actually feels like someone's home",
    "description_hy": (
        "Simona Home Bar‑ը արդեն անունով ասում է, թե ինչ ես ստանալու. "
        "ոչ թե ֆորմալ բար, ոչ թե night club, "
        "այլ տնային մթնոլորտ, որտեղ "
        "մտնելուն պես ուզում ես բաճկոնդ հանել, "
        "անկյունային բազկաթոռ գտնել ու "
        "մնալ ավելի երկար, քան նախատեսել էիր։ "
        "Արամ փողոցի 80 հասցեն Dargett‑ից ընդամենը "
        "մի քանի շենք հեռու է, բայց երկու վայրերն "
        "ամբողջովին ուրիշ ռիթմ ունեն. "
        "Dargett‑ը energy է, Simona‑ն՝ հանգստություն։ "
        "Կոկտեյլները handcrafted են ու մտածված, "
        "ամեն ինչ balance‑ով ու ազնիվ ingredient‑ներով, "
        "ոչ թե sweet‑ness‑ով թաքցնելու տրամաբանությամբ։ "
        "Գինու ցուցակն էլ կոմպակտ է, բայց ճիշտ ընտրված, "
        "ու եթե չգիտես ինչ ուզում ես, "
        "բարմենն ուղղորդում է առանց ճնշելու։ "
        "Ուտեստները թեթև են ու համապատասխանում են "
        "bar snack տրամաբանությանը, "
        "ոչ թե full restaurant menu‑ի, "
        "ինչն ավելի է ընդգծում, որ սա "
        "խմելու, զրուցելու ու "
        "հանգստանալու վայր է, "
        "ոչ թե ճաշի։ "
        "Երեկոյան Simona‑ն լցվում է "
        "մարդկանցով, ովքեր ուզում են "
        "հանգիստ conversation‑ի մթնոլորտ, "
        "ոչ թե բարձր երաժշտություն ու "
        "մեծ ամբոխ. հենց դա է "
        "դարձնում այն Երևանի "
        "ամենահաճելի neighborhood bar‑երից մեկը։"
    ),
    "description_en": (
        "Simona Home Bar tells you exactly what to expect right in the name: "
        "not a formal bar, not a club, but a space with the warmth of someone's "
        "home, where you walk in, take off your jacket, find a corner armchair "
        "and end up staying longer than you planned. "
        "The address at 80 Aram Street puts it just a few buildings down from "
        "Dargett, but the two places operate on completely different rhythms: "
        "Dargett is energy, Simona is ease. "
        "The cocktails are handcrafted and considered, built on balance and "
        "honest ingredients rather than sweetness to mask shortcuts. The wine "
        "list is compact but well chosen, and if you are not sure what you want "
        "the bartender will guide you without pressure. "
        "The food is light and follows bar snack logic rather than a full "
        "restaurant menu, which only reinforces the point: this is a place for "
        "drinking, talking and unwinding, not for a sit-down dinner. "
        "In the evenings Simona fills with people who want conversation over "
        "noise, a good drink over a spectacle, and a bar that feels personal "
        "rather than anonymous. That combination makes it one of the most "
        "genuinely pleasant neighborhood bars in Yerevan, the kind of place "
        "that locals quietly consider their own."
    ),
},
{
    "id": "stop-club-yerevan",
    "category": "yerevan",
    "subcategory": "clubs",
    "title_hy": "Stop Club",
    "title_en": "Stop Club",
    "location_hy": "Երևան, Մոսկովյան փողոց 37",
    "location_en": "37 Moskovyan Street, Yerevan",
    "maps_url": "https://maps.app.goo.gl/XXLtWWqqAmmcQdVHA",
    "rating": 4.4,
    "thumb": "/static/img/places/stop-club-bar.jpg",
    "images": [
        "/static/img/places/stop-club-bar.jpg",
        "/static/img/places/stop-club-live-band.webp",
        "/static/img/places/stop-club-stage.jpg",
    ],
    "short_hy": "Մոսկովյանի վրա՝ live երաժշտություն, բար ու գիշերային ռիթմ",
    "short_en": "Live music, bar and late-night energy on Moskovyan",
    "description_hy": (
        "Stop Club‑ը Մոսկովյան փողոցի այն հասցեն է, "
        "ուր Երևանի գիշերային կյանքն ու live "
        "երաժշտությունը հանդիպում են կոմպակտ, "
        "էներգետիկ տարածքում։ "
        "Ակումբն ունի իր հստակ բնավորությունը. "
        "ոչ չափազանց մեծ, ոչ չափազանց փոքր, "
        "բեմը բավականաչափ մոտ, որ live set‑ի "
        "ժամանակ զգաս ամեն նոտա, "
        "բայց տարածքն էլ բավականաչափ ազատ, "
        "որ շնչես ու շարժվես։ "
        "Ծրագրերը բազմազան են՝ "
        "rock, alternative, electronic, "
        "DJ sets, թեմատիկ երեկոներ, "
        "ու հաճախ հենց այստեղ են "
        "հայտնվում Երևանի indie scene‑ի "
        "հետաքրքիր անունները՝ մինչ "
        "ավելի մեծ բեմեր նվաճելը։ "
        "Բարը լավ է կառուցված. "
        "գարեջուր, կոկտեյլներ, shots, "
        "ամեն ինչ արագ ու առանց "
        "ավելորդ բյուրոկրատիայի, "
        "ինչպես club bar‑ում վայել է։ "
        "Գները հասանելի են, մթնոլորտը "
        "անկեղծ, ու հանդիսատեսն "
        "խառն է՝ երաժիշտներ, "
        "ուսանողներ, locals, "
        "ովքեր պարզապես ուզում են "
        "լավ երեկո՝ առանց dress code‑ի "
        "ու VIP table‑ների։ "
        "Stop Club‑ը Երևանի այն "
        "underground‑ish վայրերից է, "
        "որ գոյատևում է բովանդակությամբ, "
        "ոչ թե glamour‑ով, ու "
        "հենց դրա համար էլ "
        "մարդիկ հետ են գալիս։"
    ),
    "description_en": (
        "Stop Club is the address on Moskovyan Street where Yerevan's nightlife "
        "and live music meet in a compact, energetic space. The club has a clear "
        "character: not too big, not too small, with the stage close enough that "
        "during a live set you feel every note, but enough room to breathe and "
        "move. "
        "The programme is varied: rock, alternative, electronic, DJ sets, themed "
        "nights, and this is often where interesting names from Yerevan's indie "
        "scene appear before moving on to larger stages. It has that quality of "
        "feeling genuinely underground without being inaccessible. "
        "The bar is well set up: beer, cocktails, shots, everything served "
        "quickly and without unnecessary fuss, as a proper club bar should be. "
        "Prices are reasonable, the atmosphere is unpretentious, and the crowd "
        "is mixed: musicians, students, locals who simply want a good evening "
        "without dress codes, VIP tables or cover charges that require "
        "justification. "
        "Stop Club is one of those Yerevan venues that survives on content "
        "rather than glamour, and that is exactly why people keep coming back. "
        "If you want to feel the city's nightlife from the inside rather than "
        "from behind a velvet rope, this is a reliable and honest place to start."
    ),
},
{
    "id": "garage-club-gyumri",
    "category": "armenia",
    "subcategory": "clubs",
    "title_hy": "Garage Club (Գյումրի)",
    "title_en": "Garage Club (Gyumri)",
    "location_hy": "Հայաստան, Գյումրի, Գյումրիի կոմերցիոն կենտրոն",
    "location_en": "Gyumri Commercial Center, Gyumri, Armenia",
    "maps_url": "https://maps.app.goo.gl/eab9pbeteAvP5kpY6",
    "rating": 4.3,
    "thumb": "/static/img/places/garage-club-crowd.jpg",
    "images": [
        "/static/img/places/garage-club-crowd.jpg",
        "/static/img/places/garage-club-bar.jpg",
        "/static/img/places/garage-club-stage.jpg",
    ],
    "short_hy": "Գյումրիի գիշերային կյանքի կենտրոնը",
    "short_en": "The beating heart of Gyumri's nightlife",
    "description_hy": (
        "Եթե Գյումրիում ես ու ուզում ես հասկանալ, "
        "թե ինչպես է քաղաքն ապրում գիշերը, "
        "Garage Club‑ը հենց այն հասցեն է, "
        "ուր այդ պատասխանը կգտնես։ "
        "Գյումրիի կոմերցիոն կենտրոնում "
        "տեղակայված ակումբն ունի "
        "industrial warehouse տրամաբանություն. "
        "բարձր առաստաղ, մեծ բաց տարածք, "
        "բեմ ու dance floor, որ "
        "Գյումրու մասշտաբով լուրջ venue է։ "
        "Garage‑ի ծրագրերը բազմազան են՝ "
        "local DJ‑ներ, հրավիրված հյուր "
        "արտիստներ Երևանից, live band‑եր, "
        "թեմատիկ party‑ներ ու "
        "փառատոնային հատուկ երեկոներ։ "
        "Երաժշտությունը հիմնականում "
        "electronic, techno, house տիրույթում է, "
        "բայց Garage‑ը բաց է "
        "ժանրային փորձերի նկատմամբ, "
        "ու հաճախ հենց այստեղ են "
        "Գյումրու երիտասարդ "
        "երաժիշտներն ու DJ‑ները "
        "իրենց առաջին լուրջ set‑ը անում։ "
        "Բարը straightforward է՝ "
        "գարեջուր, կոկտեյլներ, "
        "ուժեղ խմիչքներ, "
        "ողջամիտ գներով ու "
        "բավականաչափ արագ service‑ով, "
        "որ dance floor‑ից "
        "երկար չհեռանաս։ "
        "Garage Club‑ը Գյումրու "
        "proof է, որ "
        "Հայաստանի երկրորդ քաղաքն "
        "ունի իր սեփական, "
        "ազնիվ գիշերային "
        "scene, որ Երևանի "
        "ստվերում չի ապրում, "
        "այլ ունի իր "
        "հստակ դեմքը։"
    ),
    "description_en": (
        "If you are in Gyumri and want to understand how the city lives at night, "
        "Garage Club is the address where you will find that answer. Located in "
        "the Gyumri Commercial Center, the club follows an industrial warehouse "
        "logic: high ceilings, a large open floor, a proper stage and a dance "
        "floor that, by Gyumri's scale, makes it a serious venue. "
        "The programme is varied: local DJs, guest artists from Yerevan, live "
        "bands, themed parties and special festival nights. The music sits "
        "mainly in the electronic, techno and house range, but Garage is open "
        "to genre experiments, and this is often where Gyumri's young musicians "
        "and DJs play their first serious sets in front of a real crowd. "
        "The bar is straightforward: beer, cocktails, spirits, at reasonable "
        "prices and with fast enough service that you do not spend too long away "
        "from the dance floor. "
        "Garage Club is Gyumri's proof that Armenia's second city has its own "
        "genuine nightlife scene, one that does not live in Yerevan's shadow "
        "but has its own clear identity, its own crowd and its own energy. "
        "A night here feels distinctly Gyumri: loud, warm, slightly rough "
        "around the edges and completely unpretentious."
    ),
},
{
    "id": "kami-music-club",
    "category": "yerevan",
    "subcategory": "clubs",
    "title_hy": "Kami Music Club",
    "title_en": "Kami Music Club",
    "location_hy": "Երևան, Աբովյան փողոց 18",
    "location_en": "18 Abovyan St, Yerevan",
    "maps_url": "https://maps.app.goo.gl/4CdqKKUQBV1Bk1Pf9",
    "rating": 4.6,
    "thumb": "/static/img/places/kami-club-stage.jpeg",
    "images": [
        "/static/img/places/kami-club-stage.jpeg",
        "/static/img/places/kami-club-interior.jpeg",
        "/static/img/places/kami-club-bar.jpg",
    ],
    "short_hy": "Աբովյանի վրա՝ Երևանի ամենաէներգետիկ music club‑ը",
    "short_en": "Yerevan's most energetic music club on Abovyan",
    "description_hy": (
        "Kami Music Club‑ը Երևանի այն հասցեն է, "
        "ուր գնում ես պարելու, ոչ թե նայելու։ "
        "Աբովյան փողոցի 18 հասցեում, "
        "քաղաքի կենտրոնի սրտում, "
        "ակումբն ունի sound system, "
        "որ լուրջ է վերաբերվում երաժշտությանը, "
        "dance floor, որ լցվելուն պես "
        "ստեղծում է իր սեփական էներգիան, "
        "ու բեմ, որտեղ հայտնվում են "
        "թե՛ տեղական, թե՛ միջազգային "
        "հյուր արտիստներ։ "
        "Kami‑ի ծրագրային տրամաբանությունը "
        "ավելի բարձր մակարդակի է, "
        "քան Երևանի շատ ակումբների. "
        "հյուր DJ‑ների ու live act‑երի "
        "ընտրությունը մտածված է, "
        "ժանրային բազմազանությունը "
        "հստակ՝ electronic, house, "
        "techno, R&B թեմատիկ գիշերներ, "
        "ու հատուկ փառատոնային "
        "line‑up‑ներ, որոնք "
        "Երևանի club scene‑ի "
        "իրադարձություններ են դառնում։ "
        "Ինտերիերը մտածված է. "
        "լուսավորությունը, ձայնի "
        "ուղղությունը, բարի "
        "տեղադրությունը, "
        "VIP zone‑երը, "
        "ամեն ինչ կառուցված է "
        "երկար, հարմարավետ "
        "գիշերվա տրամաբանությամբ։ "
        "Բարն ունի cocktail menu, "
        "bottle service, "
        "premium spirits, "
        "ու staff, որ "
        "աշխատում է արագ "
        "անգամ peak hour‑ին։ "
        "Եթե Երևանում ես "
        "ու ուզում ես "
        "club experience, "
        "որ international "
        "standard‑ներին "
        "հասնի, Kami‑ն "
        "հենց այդ տեղն է։"
    ),
    "description_en": (
        "Kami Music Club is the address in Yerevan you go to when you want to "
        "dance, not just watch. Located at 18 Abovyan Street in the heart of "
        "the city centre, the club has a sound system that takes music seriously, "
        "a dance floor that generates its own energy once it fills up, and a "
        "stage where both local and international guest artists perform. "
        "Kami operates at a higher programming level than many Yerevan clubs: "
        "the selection of guest DJs and live acts is considered and deliberate, "
        "with clear genre variety across electronic, house, techno and R&B "
        "themed nights, plus special festival lineups that become genuine events "
        "in the city's club scene. "
        "The interior is well thought out: the lighting design, sound direction, "
        "bar placement and VIP zones are all built around the logic of a long, "
        "comfortable night rather than just filling a space. "
        "The bar carries a full cocktail menu, bottle service and premium "
        "spirits, with staff that manages to work quickly even at peak hours. "
        "The crowd skews toward a stylish, music-conscious audience, which "
        "gives the evenings a certain energy that is hard to manufacture "
        "artificially. "
        "If you are in Yerevan and want a club experience that reaches "
        "international standards without leaving Armenia, Kami is the "
        "most reliable answer to that question."
    ),
},
{
    "id": "diamond-restaurant-yerevan",
    "category": "yerevan",
    "subcategory": "restaurants",
    "title_hy": "Diamond Restaurant",
    "title_en": "Diamond Restaurant",
    "location_hy": "Երևան, Աբովյան փողոց",
    "location_en": "Abovyan St, Yerevan",
    "maps_url": "https://maps.app.goo.gl/Uufwxize46Poojnb6",
    "rating": 4.4,
    "thumb": "/static/img/places/diamond-restaurant-table.jpg",
    "images": [
        "/static/img/places/diamond-restaurant-table.jpg",
        "/static/img/places/diamond-restaurant-terrace.jpg",
        "/static/img/places/diamond-restaurant-view-night.jpg",
    ],
    "short_hy": "Հայկական ու միջազգային խոհանոց՝ Աբովյանի էլեգանտ հասցեում",
    "short_en": "Armenian and international cuisine at an elegant Abovyan address",
    "description_hy": (
        "Diamond Restaurant‑ը Աբովյան փողոցի "
        "այն հասցեն է, ուր գնում ես, "
        "երբ ռեստորանից ակնկալում ես "
        "ոչ միայն ուտելիք, "
        "այլ ամբողջական երեկո։ "
        "Ինտերիերն էլեգանտ է ու մտածված, "
        "ոչ թե ցուցադրական շքեղություն, "
        "այլ ճաշակ, որ ստեղծում է "
        "հարմարավետ, բայց ֆորմալ "
        "բավականաչափ մթնոլորտ՝ "
        "թե՛ business dinner‑ի, "
        "թե՛ հատուկ ընտանեկան "
        "առիթի, թե՛ ռոմանտիկ "
        "ընթրիքի համար։ "
        "Մենյուն հավասարակշռում է "
        "հայկական ավանդական խոհանոցն "
        "ու միջազգային ուտեստները. "
        "մի կողմից՝ ճիշտ պատրաստված "
        "dolma, khorovats, "
        "տեղական ձուկ ու "
        "հայկական բանջարեղենային "
        "ուտեստներ, մյուս կողմից՝ "
        "European‑style entrée‑ներ, "
        "steak, pasta, seafood, "
        "ամեն ինչ kitchen‑ի "
        "ուշադրությամբ ու "
        "presentation‑ի հստակ "
        "մակարդակով։ "
        "Գինու ցուցակն ընդգրկուն է՝ "
        "հայկական winery‑ներ "
        "կողք կողքի միջազգային "
        "label‑ների հետ, "
        "ու sommelier‑ը կամ "
        "մատուցողն ուղղորդում է "
        "առանց ճնշելու։ "
        "Սպասարկումը professional է "
        "ու ուշադիր, "
        "ինչն Diamond‑ի "
        "ամենաուժեղ կողմերից "
        "մեկն է. "
        "նկատում ես, երբ "
        "բաժակը գրեթե դատարկ է, "
        "ու հարցնում են "
        "նախքան ոստայնը կուռ "
        "փռելը։ "
        "Եթե Երևանում ես "
        "ու ուզում ես "
        "մի ճաշ, որ "
        "հիշվի, Diamond‑ը "
        "հուսալի ու "
        "ճիշտ ընտրություն է։"
    ),
    "description_en": (
        "Diamond Restaurant is the address on Abovyan Street you go to when "
        "you expect more from a restaurant than just food – when you want a "
        "complete evening. The interior is elegant and considered, not "
        "ostentatious luxury but a clear sense of taste that creates an "
        "atmosphere comfortable enough to relax in but formal enough for a "
        "business dinner, a family occasion or a romantic night out. "
        "The menu balances traditional Armenian cuisine with international "
        "dishes: on one side, well-prepared dolma, khorovats, local fish and "
        "Armenian vegetable plates; on the other, European-style entrées, "
        "steak, pasta and seafood, all executed with kitchen attention and a "
        "consistent level of presentation. "
        "The wine list is broad, placing Armenian wineries alongside "
        "international labels, and the staff guides you through it without "
        "pressure. Service at Diamond is one of its strongest points: "
        "professional and attentive in the way that matters – they notice "
        "when your glass is nearly empty and ask before the tablecloth "
        "needs adjusting. "
        "The crowd here tends to be a mix of Yerevan locals celebrating "
        "something, business guests and travellers who want a reliable "
        "upscale dinner without the risk of disappointment. "
        "If you are in Yerevan and want one meal that you will actually "
        "remember, Diamond is a confident and honest choice."
    ),
},
{
    "id": "tsirаni-garden-restaurant",
    "category": "yerevan",
    "subcategory": "restaurants",
    "title_hy": "Ծիրանի garden-ռեստորան",
    "title_en": "Tsirаni Garden Restaurant",
    "location_hy": "Երևան, Արինջ, Բաբաջանյան 3-րդ թաղ. 1, M15",
    "location_en": "Babajanyan block 3, 1, M15, Arinj, Yerevan",
    "maps_url": "https://maps.app.goo.gl/LyFVpj3CJVdcfDpT6",
    "rating": 4.5,
    "thumb": "/static/img/places/tsirani-garden-overview.jpg",
    "images": [
        "/static/img/places/tsirani-garden-overview.jpg",
        "/static/img/places/tsirani-garden-pavilion.jpg",
        "/static/img/places/tsirani-garden-food.jpg",
    ],
    "short_hy": "Բաց այգի, հայկական սեղան ու ծիրանի ծառերի ստվեր",
    "short_en": "Open garden, Armenian table and apricot tree shade",
    "description_hy": (
        "Ծիրանի garden‑ռեստորանը Արինջ թաղամասում "
        "այն վայրն է, ուր Երևանի շոգ ամռան "
        "կեսօրը հանկարծ հանելուի լինում է. "
        "բաց այգի, ծառերի ստվեր, "
        "թեթև քամի ու երկար սեղան, "
        "որի վրա հայկական ուտեստներն "
        "ափսե առ ափսե հայտնվում են "
        "կարծես ինքնաբերաբար։ "
        "Ռեստորանի հիմնական ուժը "
        "garden format‑ն է. "
        "ոչ indoor, ոչ rooftop, "
        "այլ իրական բաց տարածք "
        "կանաչով, ծաղիկներով ու "
        "բնական լույսով, "
        "որտեղ երեկոյան մոմերն "
        "ու fairy lights‑ը "
        "ստեղծում են մթնոլորտ, "
        "որ photography‑ի համար "
        "իդեալական է, "
        "բայց ամենից կարևորը՝ "
        "ուղղակի հաճելի է։ "
        "Մենյուն հայկական է "
        "ու սեզոնային. "
        "թարմ բանջարեղեն, "
        "տնական աղցաններ, "
        "խորոված միս ու ձուկ, "
        "հայկական հացեղեն, "
        "ամեն ինչ այն "
        "ծանոթ, տնային ոճով, "
        "որ լավ garden "
        "ռեստորանում "
        "ճիշտ է ու տեղին։ "
        "Մատուցումը ջերմ է "
        "ու ընտանեկան. "
        "մեծ ծրագրերի, "
        "հարսանյաց ու "
        "հոբելյանների համար "
        "ռեստորանն ունի "
        "փորձ ու հարմարավետ "
        "տարողություն, "
        "բայց նույնքան "
        "հաճելի է "
        "փոքր ընկերական "
        "ճաշի համար, "
        "ուր ուղղակի "
        "ուզում ես "
        "ամռան երեկոն "
        "դրսում անցկացնել "
        "լավ ուտելիքի "
        "ու հանգիստ "
        "զրույցի հետ։"
    ),
    "description_en": (
        "Tsirани Garden Restaurant in the Arinj district is the kind of place "
        "where a hot Yerevan summer afternoon suddenly becomes manageable: an "
        "open garden, shade from the trees, a light breeze and a long table "
        "where Armenian dishes appear plate by plate as if on their own. "
        "The restaurant's main strength is its garden format: not indoor, not "
        "a rooftop, but a real open space with greenery, flowers and natural "
        "light, where in the evenings candles and warm string lights create an "
        "atmosphere that is ideal for photography but more importantly simply "
        "pleasant to be in. "
        "The menu is Armenian and seasonal: fresh vegetables, homemade salads, "
        "grilled meat and fish, Armenian bread and pastries, all in that "
        "familiar, home-style register that feels exactly right in a good "
        "garden restaurant. Nothing overengineered, everything honest. "
        "The service is warm and family-oriented: the restaurant has experience "
        "with large events, weddings and anniversaries and the capacity to "
        "handle them comfortably, but it works equally well for a small group "
        "dinner where you simply want to spend a summer evening outside with "
        "good food and easy conversation. "
        "If you are looking for a Yerevan restaurant that combines a genuinely "
        "beautiful outdoor setting with solid Armenian cooking, Tsirани is "
        "one of the more reliable and atmospheric answers to that search."
    ),
},
{
    "id": "dolmama-restaurant",
    "category": "yerevan",
    "subcategory": "restaurants",
    "title_hy": "Dolmama – Armenia's Restaurant",
    "title_en": "Dolmama – Armenia's Restaurant",
    "location_hy": "Երևան, Պուշկին փողոց 10",
    "location_en": "10 Pushkin St, Yerevan",
    "maps_url": "https://maps.app.goo.gl/hMxFvk7mh6SpFrJ98",
    "rating": 4.8,
    "thumb": "/static/img/places/dolmama-dolma.jpg",
    "images": [
        "/static/img/places/dolmama-dolma.jpg",
        "/static/img/places/dolmama-interior.jpg",
        "/static/img/places/dolmama-table.jpg",
    ],
    "short_hy": "Հայկական խոհանոցի ամենաազնիվ հասցեն Երևանում",
    "short_en": "The most honest address for Armenian cuisine in Yerevan",
    "description_hy": (
        "Կան ռեստորաններ, որ բացվում ու փակվում են, "
        "ու կան ռեստորաններ, որ դառնում են հղում կետ։ "
        "Dolmama‑ն երկրորդ տեսակից է։ "
        "Պուշկին փողոցի 10 հասցեն Երևանում "
        "արդեն տարիներ շարունակ նշանակում է "
        "մի բան՝ հայկական խոհանոցն "
        "իր լավագույն, ամենամտածված ձևով։ "
        "Ռեստորանը հաճախ առաջինն է, "
        "որ հիշատակվում է, երբ "
        "հարցնում են «ուր տանեմ "
        "կարևոր հյուրին Երևանում», "
        "ու դա պատահական չէ։ "
        "Մենյուն հայկական ավանդական "
        "ուտեստների modern interpretation‑ն է. "
        "dolma՝ բազմաթիվ տարբերակներով, "
        "ամեն մեկը մի փոքր ուրիշ, "
        "տեղական բանջարեղեն ու "
        "խոտաբույսեր՝ շուկայից, "
        "հայկական մսային ուտեստներ "
        "ու ձուկ՝ ճիշտ seasoning‑ով "
        "ու presentation‑ով, "
        "անուշեղեն, որ "
        "հայկական քաղցրավենիքի "
        "ավանդույթը ժամանակակից "
        "ձևով է մատուցում։ "
        "Ամռանը բակային տարածքը "
        "բացվում է, ու Dolmama‑ն "
        "ստանում է բոլորովին "
        "ուրիշ շնչառություն. "
        "հին Երևանի բակ, "
        "ծառեր, մոմեր, "
        "ու հայկական երաժշտություն "
        "ֆոնին, ամեն ինչ "
        "միասին ստեղծում է "
        "փորձ, որ "
        "դժվար է Երևանում "
        "կրկնօրինակել։ "
        "Սպասարկումը professional է "
        "ու ջերմ, "
        "wine list‑ը ամբողջովին "
        "հայկական, "
        "ու մատուցողները "
        "գիտեն ամեն "
        "շիշի մասին "
        "ասելու բան։ "
        "Dolmama‑ն այն ռեստորանն է, "
        "ուր Հայաստանն "
        "ու հայկական "
        "ուտելիքի մշակույթն "
        "ամենից հստակ "
        "ու ամենից հպարտ "
        "ձևով են ներկայացված։"
    ),
    "description_en": (
        "Some restaurants open and close, and some become reference points. "
        "Dolmama is firmly the second kind. The address at 10 Pushkin Street "
        "has meant one thing in Yerevan for years: Armenian cuisine in its "
        "most thoughtful and carefully considered form. "
        "It is often the first name that comes up when someone asks where to "
        "take an important guest in Yerevan, and that is not an accident. "
        "The menu is a modern interpretation of traditional Armenian dishes: "
        "dolma in multiple variations, each slightly different from the last, "
        "local vegetables and herbs sourced from the market, Armenian meat "
        "dishes and fish with precise seasoning and presentation, and desserts "
        "that bring Armenian sweet traditions into a contemporary register. "
        "In summer the courtyard opens, and Dolmama takes on a completely "
        "different quality: an old Yerevan yard, trees overhead, candles on "
        "the tables and Armenian music in the background, all combining into "
        "an experience that is genuinely difficult to replicate anywhere else "
        "in the city. "
        "The service is professional and warm, the wine list is entirely "
        "Armenian, and the staff know something worth saying about every "
        "bottle. "
        "Dolmama is the restaurant where Armenia and Armenian food culture "
        "are presented in their clearest and most confident form – the kind "
        "of place that reminds you why this cuisine deserves the same "
        "serious attention as any other in the world."
    ),
},
{
    "id": "yasaman-sevan-restaurant",
    "category": "armenia",
    "subcategory": "restaurants",
    "title_hy": "Yasaman Sevan's Restaurant",
    "title_en": "Yasaman Sevan's Restaurant",
    "location_hy": "Հայաստան, Գեղարքունիքի մարզ, Ծովագյուղ, Սևանա լիճ",
    "location_en": "Tsovagyugh, Lake Sevan, Gegharkunik region, Armenia",
    "maps_url": "https://maps.app.goo.gl/xucG6Wwj8L6joWsg8",
    "rating": 4.5,
    "thumb": "/static/img/places/yasaman-sevan-fish.webp",
    "images": [
        "/static/img/places/yasaman-sevan-fish.webp",
        "/static/img/places/yasaman-sevan-interior.webp",
        "/static/img/places/yasaman-sevan-terrace.jpg",
    ],
    "short_hy": "Թարմ իշխան ու Սևանի տեսարան՝ ուղղակի ջրի եզրին",
    "short_en": "Fresh ishkhan and lake views right at the water's edge",
    "description_hy": (
        "Yasaman Sevan's Restaurant‑ը այն վայրն է, "
        "ուր Սևանի ձուկն ու Սևանի "
        "տեսարանը մեկ սեղանի շուրջ "
        "են հավաքվում։ "
        "Ծովագյուղի ափին տեղակայված՝ "
        "ռեստորանն ունի այն "
        "անմիջական կապը ջրի հետ, "
        "որ Սևանի ափամերձ "
        "վայրերի ամենաուժեղ "
        "ատուն է. "
        "տեղ ես նստում, "
        "նայում ես լիճը, "
        "ու գիտես, որ "
        "ափսեի ձուկը "
        "նույն ջրից է։ "
        "Մենյուի հիմքը "
        "իշխանն է՝ "
        "Հայաստանի ազգային ձուկը, "
        "Սևանի հպարտությունը, "
        "որ այստեղ մատուցվում է "
        "մի քանի ձևով՝ "
        "թխած, խաշած, "
        "կրակի վրա, "
        "ամեն անգամ թարմ "
        "ու առանց ավելորդ "
        "բարդությունների, "
        "որովհետև լավ ձուկը "
        "բարդ պատրաստման "
        "կարիք չունի։ "
        "Կողմնակի ուտեստները "
        "հայկական են ու "
        "սեզոնային՝ "
        "թարմ աղցաններ, "
        "բանջարեղենային "
        "կողմնակի ուտեստներ, "
        "հայկական հաց, "
        "ամեն ինչ այն "
        "պարզ, ազնիվ "
        "ոճով, որ "
        "ձկան ռեստորանում "
        "ճիշտ է ու "
        "տեղին։ "
        "Ամռանը տեռասն "
        "բացվում է, "
        "ու Yasaman‑ը "
        "դառնում է "
        "Սևանի ափի "
        "ամենահաճելի "
        "ճաշի վայրերից "
        "մեկը. "
        "արև, ջուր, "
        "թարմ իշխան "
        "ու բաժակ "
        "սպիտակ գինի, "
        "սա Սևանի "
        "ճիշտ կերպն է "
        "ճաշակելու։"
    ),
    "description_en": (
        "Yasaman Sevan's Restaurant is the place where Lake Sevan's fish and "
        "Lake Sevan's view come together at the same table. Sitting right on "
        "the shore in Tsovagyugh, the restaurant has that direct connection to "
        "the water that is the strongest asset of any lakeside venue: you sit "
        "down, look out at the lake, and you know that the fish on your plate "
        "came from the same water you are looking at. "
        "The menu centres on ishkhan – Armenia's national fish and Sevan's "
        "pride – served in several ways: baked, poached, grilled over open "
        "fire, always fresh and without unnecessary complexity, because good "
        "fish does not need elaborate preparation to make its point. "
        "The side dishes are Armenian and seasonal: fresh salads, vegetable "
        "plates, Armenian bread, everything in that simple and honest register "
        "that is exactly right for a fish restaurant by the water. "
        "In summer the terrace opens fully, and Yasaman becomes one of the "
        "most pleasant lunch spots on the Sevan shore: sun on the water, "
        "fresh ishkhan on the plate, a glass of cold white wine in hand. "
        "That combination is the correct way to experience Lake Sevan, "
        "and Yasaman delivers it with consistency and without pretension."
    ),
},
{
    "id": "sherep-restaurant",
    "category": "yerevan",
    "subcategory": "restaurants",
    "title_hy": "Sherep Restaurant",
    "title_en": "Sherep Restaurant",
    "location_hy": "Երևան, Ամիրյան փողոց 1",
    "location_en": "1 Amiryan St, Yerevan",
    "maps_url": "https://maps.app.goo.gl/7RfRRwqRzJECcWJdA",
    "rating": 4.6,
    "thumb": "/static/img/places/sherep-restaurant-table.webp",
    "images": [
        "/static/img/places/sherep-restaurant-table.webp",
        "/static/img/places/sherep-restaurant-open-kitchen.jpg",
        "/static/img/places/sherep-restaurant-interior.jpg",
    ],
    "short_hy": "Ամիրյանի վրա՝ հայկական խոհանոց modern հայացքով",
    "short_en": "Armenian cuisine through a modern lens on Amiryan Street",
    "description_hy": (
        "Sherep‑ը Ամիրյան փողոցի 1 հասցեում "
        "Երևանի այն ռեստորաններից է, "
        "որ հայկական խոհանոցին "
        "նայում է ոչ թե "
        "ետ, այլ առաջ։ "
        "Ոչ թե ավանդույթի "
        "պահպանում ради ավանդույթի, "
        "այլ ճաշակ ու "
        "հետաքրքրություն, թե "
        "ինչ կարող է "
        "լինել հայկական "
        "ingredient‑ը ժամանակակից "
        "kitchen‑ի ձեռքում։ "
        "Մենյուն սեզոնային է "
        "ու փոփոխվող. "
        "տեղական շուկայից "
        "բերված բանջարեղեն, "
        "հայկական խոտաբույսեր "
        "ու համեմունքներ, "
        "մսային ու ձկան "
        "ուտեստներ, որ "
        "ճանաչելի են "
        "իրենց ծագումով, "
        "բայց놀랍  են "
        "իրենց մատուցմամբ։ "
        "Portion‑ները ճիշտ "
        "չափի են, "
        "presentation‑ը մտածված, "
        "ու ամեն ափսե "
        "ասում է, որ "
        "kitchen‑ում կա "
        "մեկը, ով "
        "ոչ միայն "
        "պատրաստում է, "
        "այլ մտածում։ "
        "Բարը solid է՝ "
        "հայկական գինիներ, "
        "արհեստագործական "
        "կոկտեյլներ, "
        "ու craft beer‑ի "
        "ընտրություն, "
        "ամեն ինչ "
        "նույն մտածված "
        "ոճով, ինչ "
        "խոհանոցը։ "
        "Ինտերիերը ջերմ է "
        "ու ժամանակակից, "
        "ոչ թե "
        "ցուցադրական, "
        "այլ հարմարավետ "
        "ու կենտրոնացված "
        "ուտելիքի ու "
        "զրույցի վրա։ "
        "Sherep‑ը Երևանի "
        "այն ռեստորանն է, "
        "ուր հասկանում ես "
        "որ հայկական "
        "խոհանոցն ունի "
        "ասելու բան "
        "ոչ միայն "
        "ավանդույթի, "
        "այլ նաև "
        "ապագայի մասին։"
    ),
    "description_en": (
        "Sherep at 1 Amiryan Street is one of those Yerevan restaurants that "
        "looks at Armenian cuisine not backward but forward. Not preservation "
        "of tradition for its own sake, but genuine curiosity about what "
        "Armenian ingredients can become in the hands of a modern kitchen "
        "that actually thinks about what it is doing. "
        "The menu is seasonal and changes regularly: vegetables from local "
        "markets, Armenian herbs and spices, meat and fish dishes that are "
        "recognisable in their origin but surprising in their execution. "
        "Portions are well judged, presentation is considered without being "
        "theatrical, and every plate suggests that someone in the kitchen "
        "is not just cooking but making decisions. "
        "The bar matches the kitchen in approach: Armenian wines, "
        "craft cocktails, a selection of craft beer, all chosen with the "
        "same editorial eye as the food menu. "
        "The interior is warm and contemporary without being showy, "
        "built around comfort and conversation rather than Instagram backdrops. "
        "Sherep is the kind of Yerevan restaurant where you leave "
        "understanding that Armenian cuisine has something to say not only "
        "about where it has been but about where it is going, and that "
        "the conversation is worth having over a long, unhurried dinner "
        "on Amiryan Street."
    ),
} 
]
