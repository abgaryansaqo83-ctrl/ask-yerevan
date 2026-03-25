# backend/sights_data.py

from typing import List, Dict, Any

SIGHTS = [

    # ══════════════════════════════════════════
    #  ՀԱՅԱՍՏԱՆ (category: "armenia")
    # ══════════════════════════════════════════

    {
        "id": "garni",
        "category": "armenia",
        "title_hy": "Գառնիի հեթանոսական տաճար",
        "title_en": "Garni Pagan Temple",
        "location_hy": "Կոտայքի մարզ, Գառնի, 2215",
        "location_en": "Kotayk Province, Garni, 2215",
        "maps_url": "https://maps.app.goo.gl/Kz1TYsPcFTybEkzY8",
        "rating": 4.9,
        "thumb": "static/img/sights/garni-new.jpg",
        "images": [
            "static/img/sights/garni-old.jpg",
            "static/img/sights/garni-new.jpg",
        ],
        "short_hy": "Հայաստանի միակ պահպանված հելլենիստական տաճարը՝ կառուցված I դարում",
        "short_en": "Armenia's only surviving Hellenistic pagan temple, built in the 1st century AD",
        "description_hy": """
<h3>Պատմություն</h3>
<p>Գառնիի տաճարը կառուցվել է I դարում հայ թագավոր Տրդատ I-ի օրոք՝ հելլենիստական ճարտարապետական ավանդույթով։ Սա Հայաստանի միակ պահպանված հեթանոսական տաճարն է՝ արևի աստված Միհրին նվիրված։</p>
<p>1679 թ. ուժեղ երկրաշարժից տաճարը ավերվել է, իսկ 1969–1975 թթ. վերակառուցվել է անաստիլոզ մեթոդով՝ հիմնականում բնօրինակ քարերով։</p>
<h3>Ինչ տեսնել</h3>
<p>24 իոնական սյուն, նրբագեղ ֆրիզ, Գառնու կիրճի և «Քարերի սիմֆոնիայի» տեսարան, ինչպես նաև մոտակա հռոմեական բաղնիքի խճանկար։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 28 կիլոմետր։ Ավտոբուս կամ մարշրուտկա Մասիվի ավտոկայանից, կամ մեքենայով՝ Գառնի տանող գլխավոր ճանապարհով (M4/M10 ուղղությամբ)։</p>
""",
        "description_en": """
<h3>History</h3>
<p>The Garni Pagan Temple was built in the 1st century AD by Armenian king Tiridates I in Hellenistic style. It is the only surviving pagan temple in Armenia, dedicated to the sun god Mihr.</p>
<p>The temple was destroyed by a powerful earthquake in 1679 and reconstructed in 1969–1975 using the anastylosis method, largely with its original stones.</p>
<h3>What to See</h3>
<p>24 Ionic columns, an elegant frieze, dramatic views over the Garni gorge and the “Symphony of Stones”, plus the mosaic floor of a nearby Roman‑era bathhouse.</p>
<h3>How to Get There</h3>
<p>About 28 km from central Yerevan. Take a bus or marshrutka from the Masiv bus station, or drive via the main road towards Garni (M4/M10 direction).</p>
""",
    },

    {
        "id": "lake-sevan",
        "category": "armenia",
        "title_hy": "Սևանա լիճ",
        "title_en": "Lake Sevan",
        "location_hy": "Գեղարքունիքի մարզ",
        "location_en": "Gegharkunik Province",
        "maps_url": "https://maps.app.goo.gl/kzYrTEPJPcHF6UDx5",
        "rating": 4.8,
        "thumb": "static/img/sights/Lake_Sevan.jpg",
        "images": [
            "static/img/sights/Lake_Sevan.jpg",
            "static/img/sights/Lake_Sevan1.jpg",
            "static/img/sights/Lake_Sevan3.png",
        ],
        "short_hy": "Հայկական լեռնաշխարհի «կապույտ աչքը»՝ 1900 մ բարձրության վրա",
        "short_en": "The “blue eye” of the Armenian highlands at 1,900 m elevation",
        "description_hy": """
<h3>Ընդհանուր</h3>
<p>Սևանա լիճը գտնվում է մոտ 1,900 մ բարձրության վրա և Կովկասի ամենամեծ լճերից մեկն է․ մակերեսը մոտ 1,242 կմ² է։ Ամռանը լիճը լողի, ջրային սպորտի և ձկնորսության գլխավոր կենտրոններից է։</p>
<p>Ամենահայտնի ձկնատեսակը Սևանի իշխանն է՝ լճի էնդեմիկ տեսակ, որը մատուցվում է ափամերձ գրեթե բոլոր ռեստորաններում։</p>
<h3>Ինչ անել</h3>
<p>Լողափեր, ջրային սպորտ, նավակով զբոսանք, Սևանավանք, արևամուտի դիտում, Նորատուսի խաչքարեր, ճամբարային հանգիստ Սևանի կամ Ծովինարի ափերին։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 65 կմ։ Ավտոբուսներ Կիլիկիայի ավտոկայանից, կամ մեքենայով՝ M4 մայրուղիով դեպի Սևան։</p>
""",
        "description_en": """
<h3>Overview</h3>
<p>Lake Sevan sits at around 1,900 m above sea level and is one of the largest high‑altitude freshwater lakes in the world, with a surface area of about 1,242 km². In summer it becomes a hub for swimming, water sports and fishing.</p>
<p>The most prized catch is Sevan trout (ishkhan), an endemic species served in restaurants all along the shore.</p>
<h3>What to Do</h3>
<p>Swim at the beaches, try water sports, take a boat trip, visit Sevanavank monastery, watch the sunset, see the khachkars at Noratus and camp along the Sevan or Tsovinar shores.</p>
<h3>How to Get There</h3>
<p>About 65 km from Yerevan. Take a bus from Kilikia bus station, or drive via the M4 highway towards Sevan.</p>
""",
    },

    {
        "id": "parz-lake",
        "category": "armenia",
        "title_hy": "Պարզ լիճ",
        "title_en": "Parz Lake",
        "location_hy": "Տավուշի մարզ, Դիլիջան ազգային պարկ",
        "location_en": "Tavush Province, Dilijan National Park",
        "maps_url": "https://maps.app.goo.gl/vb7AK3yCqG6NkmYj6",
        "rating": 4.6,
        "thumb": "static/img/sights/parz-lake-mirror.jpg",
        "images": [
            "static/img/sights/parz-lake-mirror.jpg",
            "static/img/sights/parz-lake-forest-trail.jpg",
            "static/img/sights/parz-lake-hiking.webp",
        ],
        "short_hy": "Անտառի մեջ թաքնված հայելային լիճ՝ 1330 մ բարձրության վրա",
        "short_en": "A mirror‑still lake hidden in the forest at 1,330 m elevation",
        "description_hy": """
<h3>Բնույթ</h3>
<p>Պարզ լիճը գտնվում է մոտ 1,330 մ բարձրության վրա՝ Դիլիջանի ազգային պարկի խորքում։ Լճի շուրջը անցնող շուրջ 2 կմ անտառային արահետը հարմար է ընտանիքների և թեթև (light) hiking-ի համար։</p>
<p>Ամռանը հնարավոր է pedal boat կամ նավակ վարձել, ձուկ որսալ, նկատել անտառի կենդանիներին և թռչուններին։</p>
<h3>Ինչ անել</h3>
<p>Անտառային հանգիստ զբոսանք, արահետ դեպի Գոշավանք, լճի հայելային մակերեսի լուսանկարում, բացօթյա կաֆե և պիկնիկի գոտիներ։</p>
<h3>Ինչպես հասնել</h3>
<p>Դիլիջանից մոտ 7 կմ․ taxi-ով կամ մեքենայով անտառային ճանապարհով՝ Parz Lake / Պարզ լիճ ցուցանակների ուղղությամբ։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Parz Lake sits at about 1,330 m inside Dilijan National Park. A gentle 2 km loop trail around the lake is family‑friendly and perfect for light hiking.</p>
<p>In summer you can rent pedal boats or rowboats, fish and spot local wildlife in the surrounding forest.</p>
<h3>What to Do</h3>
<p>Take forest walks, follow the trail towards Goshavank, photograph the mirror‑like lake surface, watch birds and relax at the outdoor cafés and picnic areas.</p>
<h3>How to Get There</h3>
<p>About 7 km from Dilijan town by taxi or car along the forest road signposted for Parz Lake.</p>
""",
    },
    {
        "id": "garni-gorge",
        "category": "armenia",
        "title_hy": "Գառնիի կիրճ — բազալտե սյուներ",
        "title_en": "Garni Gorge — Basalt Columns",
        "location_hy": "Կոտայքի մարզ, Գառնի, 2215",
        "location_en": "Kotayk Province, Garni, 2215",
        "maps_url": "https://maps.app.goo.gl/yD5cc6rufBt2qu298",
        "rating": 4.7,
        "thumb": "static/img/sights/garni-gorge-columns.jpg",
        "images": [
            "static/img/sights/garni-gorge-columns.jpg",
            "static/img/sights/garni-gorge-river.jpg",
            "static/img/sights/garni-gorge-wide.jpg",
        ],
        "short_hy": "Հրաբխային բազալտե «օրգանի խողովակներ»՝ Ազատ գետի ձորում",
        "short_en": "Volcanic basalt 'organ pipes' rising from the Azat River gorge",
        "description_hy": """
<h3>Երկրաբանական հրաշք</h3>
<p>Ազատ գետի կողմից հազարավոր տարիների ընթացքում քանդակված այս ձորի պատերը պատված են բազալտե վեցանկյուն սյուներով՝ մինչև 40–50 մետր բարձրությամբ։ Այդ պատճառով էլ վայրը հաճախ կոչում են «Քարերի սիմֆոնիա» կամ «Basalt Organ»։</p>
<p>Սյուները ձևավորվել են հին լավայի դանդաղ սառչելու և ճաքճքելու արդյունքում՝ ստեղծելով գրեթե կատարյալ երկրաչափական կառուցվածք։ Ձմռանը ճեղքերում կուտակված ջուրը սառչում է, սյուները պատվում են սառույցով, և ամբողջ կիրճը դառնում է գրեթե անիրական, ֆիլմի դեկորի նման տեսարան։</p>
<h3>Գործնական</h3>
<p>Կիրճը հասանելի է նույն օրը, ինչ Գառնիի տաճարը․ կարող ես իջնել մեքենայով քարապատ ճանապարհով կամ քայլել գյուղից ներքև՝ հին կամրջի կողմից։ Ճանապարհը մոտ 3–4 կմ է, ցանկալի է հագնել ամուր, փակ տակացուով կոշիկներ։ Սա «վայրի» բնություն է՝ առանց ասֆալտապատ արահետների, բայց ամեն մի կանգառ արժի արված քայլը։</p>
""",
        "description_en": """
<h3>Geological Wonder</h3>
<p>The Garni Gorge has been carved by the Azat River over thousands of years. Its walls are lined with hexagonal basalt columns up to 40–50 m tall, often referred to as the “Symphony of Stones” or the “Basalt Organ”, formed by ancient volcanic activity and slow cooling.</p>
<p>In winter, water seeping through the cracks freezes and coats the columns in ice, turning the whole gorge into a surreal, otherworldly landscape.</p>
<h3>Practical Info</h3>
<p>You can visit the gorge on the same day as the Garni Temple: either drive down the cobblestone road into the canyon or walk from the village via the old bridge. Expect roughly 3–4 km on foot and wear sturdy shoes. This is wild nature with no paved paths, but every turn of the road rewards you with new views.</p>
""",
    },

    {
        "id": "kari-lake",
        "category": "armenia",
        "title_hy": "Քարի լիճ",
        "title_en": "Kari Lake",
        "location_hy": "Արագածոտնի մարզ, Արագած լեռ",
        "location_en": "Aragatsotn Province, Mount Aragats",
        "maps_url": "https://maps.app.goo.gl/vJ2ePCcn4KgNJ7dv6",
        "rating": 4.7,
        "thumb": "static/img/sights/kari-lake-main.jpg",
        "images": [
            "static/img/sights/kari-lake-main.jpg",
            "static/img/sights/kari-lake-shore.jpg",
            "static/img/sights/kari-lake-trail.webp",
        ],
        "short_hy": "Բարձր լեռնային լիճ՝ 3200 մ բարձրության վրա, Հայաստանի ամենաբարձր մեքենայով հասանելի կետերից մեկը",
        "short_en": "Alpine lake at 3,200 m on Mount Aragats — one of the highest road-accessible points in Armenia",
        "description_hy": """
<h3>Բնույթ</h3>
<p>Քարի լիճը գտնվում է մոտ 3,200 մետր բարձրության վրա՝ Արագած լեռան հարավային լանջին։ Նույնիսկ ամռանը լճի ափերին հաճախ պահվում է ձյունը, և ստացվում է ֆանտաստիկ հակադրություն՝ սառը, մուգ կապույտ ջուր և սպիտակ բարձունքներ։</p>
<p>Մոտակայքում են Ամբերդ ամրոցը և Բյուրականի աստղադիտարանը, այնպես որ կարելի է մեկ օրում համատեղել պատմական, բնական և գիտական կանգառներ։</p>
<h3>Ինչ անել</h3>
<p>Քարի լիճը Արագածի հարավային գագաթ բարձրանալու դասական մեկնարկային կետն է․ এখանից է սկսվում արահետը դեպի 3,800+ մ բարձրության գագաթ։ Կարելի է նաև պարզապես շրջել լճի ափին, լուսանկարել սուր լեռնային պանորամաները, հետևել ամպերին և, եթե եղանակը թույլ է տալիս, գիշերով նայել աստղերին գրեթե բաց երկնքի տակ։</p>
<h3>Ինչպես հասնել</h3>
<p>Ապարանից կամ Բյուրականի կողմից մեքենայով՝ ոլորապտույտ լեռնային, բայց ամբողջությամբ ասֆալտապատ ճանապարհով մինչև հենց լճի ափը։ Գարնան սկզբին և աշնան վերջում ցանկալի է բարձրացումից առաջ ստուգել եղանակը և ճանապարհի վիճակը, երբեմն հարկավոր է բարձր անցողունակությամբ մեքենա։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Kari Lake sits at around 3,200 m on the southern slope of Mount Aragats. Even in summer you may find patches of snow along its shores, creating a striking contrast between deep blue water and white ridges.</p>
<p>Amberd Fortress and the Byurakan Astrophysical Observatory are both nearby, so it is easy to combine mountain scenery with history and science in a single day trip.</p>
<h3>What to Do</h3>
<p>Use Kari Lake as the classic starting point for hiking to the southern summit of Aragats (over 3,800 m), enjoy panoramic photography, watch the clouds drifting below you and, in clear weather, stay for stargazing in the crisp mountain air.</p>
<h3>How to Get There</h3>
<p>Reachable by car from Aparan or Byurakan via a winding but fully paved mountain road that climbs all the way to the lakeshore. In early spring and late autumn, check road conditions in advance; a high‑clearance vehicle can be useful when there is snow or ice.</p>
""",
    },

    {
        "id": "dilijan-town",
        "category": "armenia",
        "title_hy": "Դիլիջան",
        "title_en": "Dilijan",
        "location_hy": "Տավուշի մարզ, Դիլիջան",
        "location_en": "Tavush Province, Dilijan",
        "maps_url": "https://maps.app.goo.gl/tkgAU2P3q9YJ4bN27",
        "rating": 4.7,
        "thumb": "static/img/sights/dilijan-old-street.webp",
        "images": [
            "static/img/sights/dilijan-old-street.webp",
            "static/img/sights/dilijan-town-view.jpg",
            "static/img/sights/dilijan-city-park.jpg",
        ],
        "short_hy": "Հայաստանի «Փոքր Շվեյցարիա»՝ կանաչ անտառներով և XIX դարի փողոցներով",
        "short_en": "Armenia's 'Little Switzerland' — lush forests, 19th‑century streets and fresh mountain air",
        "description_hy": """
<h3>Ընդհանուր</h3>
<p>Դիլիջանը հաճախ անվանում են Հայաստանի «Փոքր Շվեյցարիա»․ շրջակա լեռները ծածկված են խիտ անտառներով, իսկ հին թաղամասերում պահպանվել են 19-րդ դարի տներն ու փայտե պատշգամբները։ Քաղաքը համարվում է հանգստի և ստեղծագործ միջավայրի կենտրոն, ներառված է նաև ՅՈՒՆԵՍԿՕ-ի ստեղծագործ քաղաքների ցանցում։</p>
<p>Հին Դիլիջանի սիրտը Շարամբեյանի փողոցն է՝ քարե տներ, փայտե բաց պատշգամբներ, արհեստագործական խանութներ և փոքրիկ սրճարաններ, որտեղ կարելի է տեսնել, թե ինչպես են վարպետները աշխատում փայտի, կավի կամ գորգի հետ։</p>
<h3>Ինչ անել</h3>
<p>Քայլել հին փողոցներով, այցելել Դիլիջանի քաղաքային զբոսայգին, գնալ Պարզ լիճ, ինչպես նաև շրջակայքի վանքեր՝ Հաղարծին, Գոշավանք, Ջուխթակ վանք։ Եթե սիրում ես քայլարշավներ, Դիլիջանի ազգային պարկի արահետները տալիս են տարբեր բարդության երթուղիներ՝ կարճ զբոսանքներից մինչև ամբողջօրյա hiking։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 100 կմ․ ավտոբուսներ և մինիավտոբուսներ Կիլիկիայի ավտոկայանից, կամ մեքենայով՝ M4/M6 մայրուղիներով դեպի Դիլիջան։ Ճանապարհը անցնում է Սևանի ափերով և լեռնանցքով, այնպես որ ճանապարհն ինքնին փոքրիկ շրջագայություն է։</p>
""",
        "description_en": """
<h3>Overview</h3>
<p>Dilijan is often called Armenia's "Little Switzerland", known for its 19th‑century houses with wooden balconies, dense surrounding forests and cool mountain air. It is also part of the UNESCO Creative Cities network and has become a hub for art, crafts and slow travel.</p>
<p>The heart of old Dilijan is Sharambeyan Street, lined with restored stone houses, traditional balconies, artisan workshops and cozy cafés where you can watch woodcarvers, potters and weavers at work.</p>
<h3>What to Do</h3>
<p>Stroll through the old quarter and city park, visit nearby monasteries like Haghartsin, Goshavank and Jukhtak, and spend time on the trails of Dilijan National Park. Parz Lake is an easy half‑day escape, perfect to combine with a relaxed evening back in town.</p>
<h3>How to Get There</h3>
<p>About 100 km from Yerevan. Take a bus or minibus from Kilikia bus station, or drive via the M4/M6 highways. The route passes Lake Sevan and climbs through a mountain pass, so the journey itself feels like the start of the trip.</p>
""",
    },

    {
        "id": "gyumri-old-town",
        "category": "armenia",
        "title_hy": "Գյումրի — հին քաղաքամաս",
        "title_en": "Gyumri — Old Town",
        "location_hy": "Շիրակի մարզ, Գյումրի",
        "location_en": "Shirak Province, Gyumri",
        "maps_url": "https://maps.app.goo.gl/VysdV5so6QB8oNv59",
        "rating": 4.6,
        "thumb": "static/img/sights/gyumri-old-street.jpg",
        "images": [
            "static/img/sights/gyumri-old-street.jpg",
            "static/img/sights/gyumri-town-view.jpg",
            "static/img/sights/gyumri-balcony-yard.jpg",
        ],
        "short_hy": "Հայաստանի երկրորդ քաղաքը՝ 19-րդ դարի քարե ճարտարապետությամբ ու կենդանի մշակութային միջավայրով",
        "short_en": "Armenia's second city — 19th‑century stone architecture, vibrant art scene and a strong cultural heartbeat",
        "description_hy": """
<h3>Քաղաք</h3>
<p>Գյումրին Հայաստանի երկրորդ ամենամեծ քաղաքն է, որտեղ հինը գրեթե բառացիորեն քայլում է կողքիդ․ Կումայրիի պատմական թաղամասում կան հարյուրավոր 19-րդ դարի շենքեր՝ կառուցված սև և կարմիր տուֆ քարով։ Քաղաքը դեռ կրում է 1988 թ. երկրաշարժի հետքերը, բայց հենց այդ խառնուրդն է՝ ցավի ու ուժի, որ նրան տալիս է իր առանձնահատուկ բնավորությունը։</p>
<p>Վարդանանց հրապարակը, Աբովյան փողոցը, հին բակերն ու փոքրիկ սրճարանները ստեղծում են այն մթնոլորտը, որի համար Գյումրին շատերի սիրելի քաղաքն է․ այստեղ զգացվում է և՛ հումորը, և՛ հյուրընկալությունը, և՛ կենդանի բակային կյանքը։</p>
<h3>Ինչ անել</h3>
<p>Քայլել հին քաղաքում, այցելել Գյումրու պատմության թանգարանը, Ձիթողցյանի տուն-թանգարանը, Ասլամազյան քույրերի պատկերասրահը, նստել տեղական ռեստորաններում, փորձել գյումրեցի խոհանոցը և երեկոյան լսել կենդանի ժողովրդական երաժշտություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 126 կմ։ Գնացք՝ Սասունցի Դավիթ կայարանից, ավտոբուսներ և միկրոավտոբուսներ՝ Կիլիկիայի ավտոկայանից, կամ մեքենայով՝ M1 մայրուղիով դեպի հյուսիս։ Ճանապարհին բացվում են Արագածի և Շիրակի դաշտի տեսարաններ։</p>
""",
        "description_en": """
<h3>The City</h3>
<p>Gyumri is Armenia's second largest city, famous for its 19th‑century red and black tuff stone buildings in the historic Kumayri district. The city still bears the marks of the 1988 earthquake, which only adds to its sense of resilience and character.</p>
<p>A walk around Vardanants Square, Abovyan Street and the surrounding courtyards reveals ornate balconies, old workshop signs and lively neighborhood life, from kids playing outside to neighbors chatting across balconies.</p>
<h3>What to Do</h3>
<p>Explore the old town on foot, visit the Gyumri History Museum, the Dzitoghtsyan Social Life Museum and the Aslamazyan Sisters Gallery, then try hearty local dishes in traditional restaurants and look for venues with live folk or jazz music in the evening.</p>
<h3>How to Get There</h3>
<p>About 126 km from Yerevan. Take a train from Sasuntsi David station, a bus from Kilikia bus station, or drive via the M1 highway north towards Gyumri.</p>
""",
    },
    {
        "id": "khndzoresk",
        "category": "armenia",
        "title_hy": "Խնձորեսկ — քարայրային գյուղ",
        "title_en": "Khndzoresk — Cave Village",
        "location_hy": "Սյունիքի մարզ, 3207",
        "location_en": "Syunik Province, 3207",
        "maps_url": "https://maps.app.goo.gl/Zv5CrsEWET2n88iQ8",
        "rating": 4.8,
        "thumb": "static/img/sights/khndzoresk-bridge.jpg",
        "images": [
            "static/img/sights/khndzoresk-bridge.jpg",
            "static/img/sights/khndzoresk-caves.jpg",
            "static/img/sights/khndzoresk-gorge-view.jpg",
        ],
        "short_hy": "Ձորի պատերին կտրված հնագույն քարայրներ, կախովի կամուրջ ու լքված Հին Խնձորեսկ գյուղը",
        "short_en": "A gorge full of ancient cave dwellings, a swinging bridge, and the ghost of Old Khndzoresk",
        "description_hy": """
<h3>Ինչ է</h3>
<p>Խնձորեսկը ձորի ժայռերին փորված հնագույն քարայրային գյուղ է, որտեղ մարդիկ ապրում էին մինչև XX դարի կեսերը։ Ձորի մեջ կա 160-ից ավելի քարայր, ինչպես նաև եկեղեցի, դպրոց և պահեստային տարածքներ։</p>
<p>Հիմա գյուղի կենտրոնը կապված է ձորի երկու ափերի հետ կախովի ճոճ կամուրջով, որն ինքնին արդեն փոքրիկ արկած է։ Բնության և պատմության այս համադրությունը տալիս է «Վայրի Հայաստան» տրամադրությունն ու ձորի ֆանտաստիկ տեսարաններ։</p>
<h3>Ինչ անել</h3>
<p>Անցնել կախովի կամուրջով, ուսումնասիրել քարայրերը, լուսանկարել ձորի շերտավոր պատերը։ Մոտակայքում է Տաթևի վանքը, այնպես որ հնարավոր է ամբողջ Սյունիքյան ուղևորությունը կազմել մեկ օրում կամ երկու կետ հաջորդաբար այցելել։</p>
<h3>Ինչպես հասնել</h3>
<p>Գորիս քաղաքից մոտ 8 կմ՝ taxi-ով կամ մեքենայով լեռնային ճանապարհով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Khndzoresk is an ancient cave village carved into the walls of a dramatic gorge, inhabited until the mid‑20th century. The gorge contains over 160 caves along with a church, a school and storage rooms still visible today.</p>
<p>The two sides of the village are now connected by a long swinging suspension bridge — a small adventure in itself and unlike anything else in Armenia, with sweeping gorge views in every direction.</p>
<h3>What to Do</h3>
<p>Cross the swinging bridge, explore the cave dwellings, and photograph the layered gorge walls. Tatev Monastery is nearby, making it easy to combine both into a single Syunik day trip.</p>
<h3>How to Get There</h3>
<p>About 8 km from Goris town by taxi or car along a mountain road.</p>
""",
    },

    {
        "id": "karahunj",
        "category": "armenia",
        "title_hy": "Քարահունջ — Հայկական Սթոունհենջ",
        "title_en": "Karahunj — Armenian Stonehenge",
        "location_hy": "Սյունիքի մարզ, Սիսիան քաղաքի մոտ",
        "location_en": "Syunik Province, near Sisian town",
        "maps_url": "https://maps.app.goo.gl/L2qdmcdacpLixyYh7",
        "rating": 4.5,
        "thumb": "static/img/sights/karahunj-circle-view.jpg",
        "images": [
            "static/img/sights/karahunj-circle-view.jpg",
            "static/img/sights/karahunj-stone-hole.webp",
            "static/img/sights/karahunj-dramatic-sky.jpg",
        ],
        "short_hy": "7500-ամյա կամենկայի կոմплեքս — աշխարհի ամենահին աստղադիտարաններից մեկը",
        "short_en": "A 7,500-year-old megalithic complex — one of the world's oldest astronomical observatories",
        "description_hy": """
<h3>Ինչ է</h3>
<p>Քարահունջը 200-ից ավելի կանգնած մեծ քարերի համախումբ է, որոնցից շատերի վրա կան հատուկ անցքեր։ Գիտնականների մի մասի կարծիքով՝ սա աշխարհի ամենահին աստղադիտարաններից մեկն է՝ մոտ 7,500 տարի առաջ կառուցված, ինչը Սթոունհենջից 3,500 տարով հին է։</p>
<p>Նույնիսկ եթե աստղագիտական ծագման վարկածը վիճելի է, վայրի մթնոլորտն ու Սիսիանի դաշտի ֆոնին կանգնած քարերի տեսարանն ինքնին հուզիչ են ու անմոռանալի։</p>
<h3>Ինչ անել</h3>
<p>Ուսումնասիրել քարերի ու անցքերի դասավորությունը, այցելել փոքրիկ visitor center, գիշերը մնալ բաց երկնքի տակ աստղ դիտելու (լույսի աղտոտվածությունը նվազագույն է), ու միացնել Սիսիան կամ Տաթև ուղևորությանը։</p>
<h3>Ինչպես հասնել</h3>
<p>Սիսիան քաղաքից մոտ 3 կմ՝ taxi-ով կամ մեքենայով։ Սիսիանն ինքը Երևանից 200 կմ հեռու է M2 մայրուղիով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Karahunj is a complex of over 200 standing stones, many of which have carefully drilled holes through them. Scholars believe it may be one of the world's oldest astronomical observatories, dating back around 7,500 years — potentially 3,500 years older than Stonehenge.</p>
<p>Even setting aside the astronomical debate, the atmosphere of the site is striking: ancient stones rising from the Sisian plain under an open sky, with almost no light pollution at night.</p>
<h3>What to Do</h3>
<p>Explore the stone circles and study the alignments, visit the small on‑site visitor centre, stay after dark for stargazing, and combine the visit with Sisian town or a Tatev day trip.</p>
<h3>How to Get There</h3>
<p>About 3 km from Sisian town by taxi or car. Sisian itself is 200 km from Yerevan via the M2 highway.</p>
""",
    },

    {
        "id": "amberd-fortress",
        "category": "armenia",
        "title_hy": "Ամբերդ — լեռնային բերդ ու եկեղեցի",
        "title_en": "Amberd — Mountain Fortress & Church",
        "location_hy": "Արագածոտնի մարզ, Արագած լեռ, 2300 մ",
        "location_en": "Aragatsotn Province, Mount Aragats, 2,300 m",
        "maps_url": "https://maps.app.goo.gl/tcJNJUGVbU61UVRs9",
        "rating": 4.6,
        "thumb": "static/img/sights/amberd-fortress-main.jpg",
        "images": [
            "static/img/sights/amberd-fortress-main.jpg",
            "static/img/sights/amberd-fortress-church.jpg",
            "static/img/sights/amberd-fortress-view.jpg",
        ],
        "short_hy": "2300 մ բարձրության վրա կառուցված լեռնային բերդ ու եկեղեցի՝ Արագածի լանջին, X–XIII դդ.",
        "short_en": "A mountaintop fortress and church at 2,300 m on the slopes of Aragats, 10th–13th centuries",
        "description_hy": """
<h3>Պատմություն</h3>
<p>Ամբերդը X–XIII դարերում կառուցված լեռնային բերդ ու եկեղեցի է, որը գտնվում է Արագած լեռան ժայռոտ, կտրուկ հրվանդանի վրա՝ 2,300 մ բարձրության վրա։ Ամրոցը պաշտպանում էր Հայաստանի հյուսիսային սահմանամերձ տարածքները, իսկ դրա դիրքից բացվում են Արարատյան դաշտի լայն տեսարաններ։</p>
<p>Դարերի ընթացքում Ամբերդը անցել է բյուզանդացիների, սելջուկ թուրքերի ու մոնղոլների ձեռքով, բայց կառույցի մեծ մասն ու եկեղեցին պահպանվել են մինչ օրս։</p>
<h3>Ինչ անել</h3>
<p>Քայլել բերդի պարիսպների երկայնքով, մտնել եկեղեցի, վայելել Արագածի ու Արարատի պանորամաները, մոտիկ գտնվող Մեծ Աղբյուրի ջրվեժ, ինչպես նաև համատեղել Քարի լճի hiking-ի հետ՝ մեկ Արագած-day trip ձևաչափով։</p>
<h3>Ինչպես հասնել</h3>
<p>Բյուրական քաղաքից մոտ 18 կմ՝ լեռնային ճանապարհով։ Գարնան սկզբին և աշնան վերջին ցանկալի է բարձր անցողունակությամբ մեքենա։</p>
""",
        "description_en": """
<h3>History</h3>
<p>Amberd is a fortress and church complex built between the 10th and 13th centuries, perched on a dramatic rocky promontory at 2,300 m on the slopes of Mount Aragats. It guarded the northern Armenian borderlands and commanded sweeping views over the Ararat plain.</p>
<p>Over the centuries Amberd passed through Byzantine, Seljuk and Mongol hands, yet much of the fortress walls and the church have survived to this day.</p>
<h3>What to Do</h3>
<p>Walk the fortress perimeter, enter the church, take in panoramic views of Aragats and Mount Ararat, visit the nearby Mets Aghbyur waterfall, and combine the trip with a hike from Kari Lake for a full Aragats day out.</p>
<h3>How to Get There</h3>
<p>About 18 km from Byurakan by mountain road. A high‑clearance or 4WD vehicle is recommended in early spring and late autumn.</p>
""",
    },

    {
        "id": "shaki-waterfall",
        "category": "armenia",
        "title_hy": "Շաքիի ջրվեժ",
        "title_en": "Shaki Waterfall",
        "location_hy": "Սյունիքի մարզ, Շաքի գյուղ",
        "location_en": "Syunik Province, Shaki village",
        "maps_url": "https://maps.app.goo.gl/yf95w1TD2DrqKYEy6",
        "rating": 4.6,
        "thumb": "static/img/sights/shaki-waterfall-main.webp",
        "images": [
            "static/img/sights/shaki-waterfall-main.webp",
            "static/img/sights/shaki-waterfall-close.jpg",
            "static/img/sights/shaki-waterfall-trail.jpg",
        ],
        "short_hy": "18 մ բարձրությամբ ջրվեժ՝ բազալտե ժայռային ամֆիթատրոնի մեջ, Կապան–Գորիս ճանապարհի մոտ",
        "short_en": "An 18-metre waterfall set in a basalt rock amphitheatre, near the Kapan–Goris road",
        "description_hy": """
<h3>Բնույթ</h3>
<p>Շաքիի ջրվեժը 18 մ բարձրությամբ է, և ջուրն ընկնում է բազալտե ժայռերով կազմված բնական ամֆիթատրոնի մեջ, ինչի շնորհիվ ստեղծվում է արտառոց ակուստիկա — ջրի ձայնը բառացիորեն live performance է հնչում։</p>
<p>Ջրվեժը գտնվում է Կապան և Գորիս քաղաքների կիսով ճանապարհին, ուստի հարմար է Տաթևի ուղևորության հետ միացնելու համար՝ մեկ Սյունիք-day trip ձևաչափով։</p>
<h3>Ինչ անել</h3>
<p>Մոտենալ ջրվեժին ու զգալ ջրի ուժն ու ձայնը, լուսանկարել բազալտե պատերը, քայլել կարճ անտառային արահետով, ապա շարունակել Գորիս քաղաք և Տաթևի վանք։</p>
<h3>Ինչպես հասնել</h3>
<p>Կապան–Գորիս մայրուղուց ցուցանակով թեքվել դեպի Շաքի գյուղ։ Գորիսից մոտ 6 կմ, Կապանից մոտ 100 կմ՝ մեքենայով։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Shaki Waterfall drops 18 metres into a natural basalt amphitheatre, creating extraordinary acoustics — the sound of the water genuinely feels like a live performance echoing off the rock walls.</p>
<p>It sits roughly halfway between Kapan and Goris, making it an easy stop to combine with a Tatev monastery day trip through Syunik.</p>
<h3>What to Do</h3>
<p>Stand beside the falls and feel the spray, photograph the basalt walls, walk the short forest trail, then continue on to Goris town and Tatev Monastery.</p>
<h3>How to Get There</h3>
<p>Signposted off the Kapan–Goris highway at Shaki village. About 6 km from Goris and 100 km from Kapan by car.</p>
""",
    },

    {
        "id": "old-khot",
        "category": "armenia",
        "title_hy": "Հին Խոտ — լքված գյուղ",
        "title_en": "Old Khot — Abandoned Village",
        "location_hy": "Վայոց Ձորի մարզ",
        "location_en": "Vayots Dzor Province",
        "maps_url": "https://maps.app.goo.gl/zbPBbZtMuabD2EEL9",
        "rating": 4.4,
        "thumb": "static/img/sights/old-khot-village-view.jpg",
        "images": [
            "static/img/sights/old-khot-village-view.jpg",
            "static/img/sights/old-khot-houses-detail.jpg",
            "static/img/sights/old-khot-gorge-trail.jpg",
        ],
        "short_hy": "Լքված գյուղ ձորի մեջ — XIX դ. կարմիր քարից կառուցված տների մնացորդներ ու վայրի արահետ",
        "short_en": "An abandoned village in a gorge — 19th-century stone ruins and a hauntingly beautiful trail",
        "description_hy": """
<h3>Ինչ է</h3>
<p>Հին Խոտը XX դարի սկզբին լքված գյուղ է, որտեղ պահպանվել են XIX դարի կարմիր տուֆ քարից կառուցված տների մնացորդները։ Գտնվում է Տաթևի մոտ և հասանելի է ձորի արահետով։</p>
<p>Նոր Խոտ գյուղը կառուցվել է մի փոքր հեռու, իսկ հին մասը մնացել է գրեթե անձեռնմխելի — կատարյալ է «beaten path-ից դուրս» ճամփորդությունների ու մթնոլորտային լուսանկարների համար, հատկապես ձմռանը կամ աշնանը։</p>
<h3>Ինչ անել</h3>
<p>Ձորի արահետով զբոսանք, լքված տների ու փողոցների ուսումնասիրություն, Տաթևի ձորի ու Գորիսի հետ կոմբինացիա, լեռնային արահետի ու ձորի լուսանկարում։</p>
<h3>Ինչպես հասնել</h3>
<p>Տաթևից մոտ 15 կմ, Գորիսից մոտ 25 կմ՝ մեքենայով լեռնային ճանապարհով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Old Khot is a village abandoned in the early 20th century, preserving the ruins of 19th‑century red tuff stone houses along a gorge trail near Tatev Monastery.</p>
<p>The new village was rebuilt nearby, but the old section remains beautifully untouched — ideal for off‑the‑beaten‑path exploration and atmospheric photography, especially in autumn or winter.</p>
<h3>What to Do</h3>
<p>Walk the gorge trail, explore the stone ruins and overgrown streets, combine the visit with the Tatev gorge area and Goris town, and photograph the layered mountain and gorge scenery.</p>
<h3>How to Get There</h3>
<p>About 15 km from Tatev and 25 km from Goris by car along a mountain road.</p>
""",
    },

    {
        "id": "vorotan-gorge",
        "category": "armenia",
        "title_hy": "Որոտանի ձոր — Սատանայի կամուրջ",
        "title_en": "Vorotan Gorge — Devil's Bridge",
        "location_hy": "Սյունիքի մարզ, Գորիս–Կապան ճանապարհի մոտ",
        "location_en": "Syunik Province, near Goris–Kapan road",
        "maps_url": "https://maps.app.goo.gl/1QPA1MxSKvnZYi1f7",
        "rating": 4.7,
        "thumb": "static/img/sights/vorotan-gorge-view.webp",
        "images": [
            "static/img/sights/vorotan-gorge-view.webp",
            "static/img/sights/devils-bridge-overview.webp",
            "static/img/sights/devils-bridge-pools.webp",
        ],
        "short_hy": "Բնական կամենկայի կամուրջ ու ձորի կապույտ-կանաչ լողավազաններ — Հայաստանի ամենավայրի վայրերից մեկը",
        "short_en": "A natural stone arch over turquoise river pools — one of Armenia's most dramatic landscapes",
        "description_hy": """
<h3>Ինչ է</h3>
<p>Որոտանի ձորը Սատանայի կամուրջով Հայաստանի ամենատպավորիչ բնական վայրերից մեկն է։ Բնական կամենկայի կամուրջն առաջացել է Որոտան գետի ջրերի հազարամյա կրծոտման արդյունքում, իսկ կամուրջի տակ կազմվել են փիրուզագույն լողավազաններ, որտեղ ամռանը կարելի է լողալ։</p>
<p>Ձորի պատերը, վայրի գետի ձայնը ու հեռավոր, ուրիշ աշխարհ հիշեցնող մթնոլորտը հիանալի են Տաթևի ու Խնձորեսկի հետ մեկ երկարօրյա Սյունիք ուղևորությամբ համատեղելու համար։</p>
<h3>Ինչ անել</h3>
<p>Կանգնել բնական կամուրջի վրա, ամռանը լողալ լողավազաններում, լուսանկարել ձորի պանորամաները, ապա շարունակել Տաթև–Խնձորեսկ կոմբինացիան նույն օրը։</p>
<h3>Ինչպես հասնել</h3>
<p>Գորիսից մոտ 20 կմ, Կապանից մոտ 80 կմ։ Ցուցանակով հասանելի Գորիս–Կապան մայրուղուց։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Vorotan Gorge with its Devil's Bridge is one of Armenia's most spectacular natural landmarks. The natural stone arch was carved by the erosive force of the Vorotan River over thousands of years, and turquoise pools have formed in the rock below — swimmable in summer.</p>
<p>The sheer gorge walls, the wild river sounds and the remote atmosphere make this a highlight of Syunik, combining easily with Tatev and Khndzoresk in a single long day trip.</p>
<h3>What to Do</h3>
<p>Stand on the natural arch, swim in the pools in summer, photograph the panoramic gorge scenery, then continue to Tatev and Khndzoresk for a full Syunik day.</p>
<h3>How to Get There</h3>
<p>About 20 km from Goris and 80 km from Kapan. Signposted off the Goris–Kapan highway.</p>
""",
    },
    {
        "id": "dsegh-village",
        "category": "armenia",
        "title_hy": "Դսեղ — Հովհաննես Թումանյանի ծննդավայր",
        "title_en": "Dsegh — Birthplace of Hovhannes Tumanyan",
        "location_hy": "Լոռու մարզ, Դսեղ գյուղ",
        "location_en": "Lori Province, Dsegh village",
        "maps_url": "https://maps.app.goo.gl/cqNNnuGhSJApqP8k7",
        "rating": 4.5,
        "thumb": "static/img/sights/dsegh-village-view.jpg",
        "images": [
            "static/img/sights/dsegh-village-view.jpg",
            "static/img/sights/dsegh-forest-trail.jpg",
            "static/img/sights/dsegh-canyon-view.jpg",
        ],
        "short_hy": "Մեծ բանաստեղծ Հովհաննես Թումանյանի ծննդավայրը՝ Ձորամերի կիրճի եզրին, Լոռու անտառներում",
        "short_en": "Birthplace of Armenia's beloved poet Tumanyan, set above a dramatic canyon in Lori's forests",
        "description_hy": """
<h3>Գյուղը և բանաստեղծը</h3>
<p>Դսեղը Հայաստանի ամենասիրելի բանաստեղծ Հովհաննես Թումանյանի (1869) ծննդավայրն է։ Գյուղը գտնվում է Լոռու մարզի կանաչ անտառներում՝ Ձորամերի կիրճի եզրի մոտ, ու հենց այս լանդշաֆտն է, որ ոգեշնչել է Թումանյանի բալլադներն ու վեպերը։</p>
<p>Կարելի է մեքենայով հասնել կիրճի պանորամային կետ, անտառային արահետներով զբոսնել ու այցելել Թումանյանի տուն-թանգարան, որտեղ ցուցադրված են բանաստեղծի կյանքին ու ստեղծագործությանը վերաբերող նյութեր։</p>
<h3>Ինչ անել</h3>
<p>Թումանյանի տուն-թանգարան, կիրճի տեսարան, անտառային արահետներով զբոսանք, կիրճի ու գյուղի լուսանկարում, բնակչական Դսեղի մթնոլորտ։</p>
<h3>Ինչպես հասնել</h3>
<p>Վանաձորից մոտ 35 կմ, Երևանից մոտ 175 կմ՝ մեքենայով Լոռու մարզի ուղղությամբ։</p>
""",
        "description_en": """
<h3>Village & Poet</h3>
<p>Dsegh is the birthplace of Hovhannes Tumanyan (1869), Armenia's most beloved poet. The village sits in Lori's green forests above a dramatic canyon — the very landscape that inspired his ballads and epics.</p>
<p>Drive to the canyon rim for panoramic views, walk the forest trails, and visit the Tumanyan house‑museum, where exhibits trace the poet's life and literary legacy.</p>
<h3>What to Do</h3>
<p>Tumanyan House‑Museum, canyon viewpoint, forest trail walks, gorge photography, and soaking in the authentic atmosphere of a living Lori village.</p>
<h3>How to Get There</h3>
<p>About 35 km from Vanadzor and 175 km from Yerevan by car toward Lori Province.</p>
""",
    },

    {
        "id": "arpi-lake",
        "category": "armenia",
        "title_hy": "Արփի լիճ — Ազգային պարկ",
        "title_en": "Lake Arpi — National Park",
        "location_hy": "Շիրակի մարզ, Ամասիայի շրջան",
        "location_en": "Shirak Province, near Amasia",
        "maps_url": "https://maps.app.goo.gl/qeuM9rAqQFv7HLpk9",
        "rating": 4.4,
        "thumb": "static/img/sights/arpi-lake-main.jpg",
        "images": [
            "static/img/sights/arpi-lake-main.jpg",
            "static/img/sights/arpi-lake-shore.jpg",
            "static/img/sights/arpi-lake-birds.jpg",
        ],
        "short_hy": "Հայաստանի ամենամեծ լեռնային ճահճուտը և birdwatching-ի դրախտ՝ Շիրակի մարզում",
        "short_en": "Armenia's largest highland wetland and a birdwatching paradise in Shirak Province",
        "description_hy": """
<h3>Բնույթ</h3>
<p>Արփի լիճը Հայաստանի ամենամեծ լեռնային ճահճուտն է ու ազգային պարկ։ Ծառայում է որպես գաղթող թռչունների կանգառ-հանգրվան, ինչի պատճառով հատկապես գարնանը ու աշնանը birdwatching-ի համար իդեալական վայր է։</p>
<p>Լիճը գտնվում է Շիրակի լեռնային հարթավայրում՝ Գյումրիից մեկ ժամ վերև։ Մթնոլորտն այստեղ յուրահատուկ է — բաց, ամայի, ու բնությունն ու լռությունը ճնշող կերպով ներկա են։</p>
<h3>Ինչ անել</h3>
<p>Birdwatching, լճի ափի երկայնքով զբոսանք, լեռնային ճահճուտի լանդշաֆտի լուսանկարում, Ամասիա գյուղ, Գյումրիի հետ կոմբինացիա։</p>
<h3>Ինչպես հասնել</h3>
<p>Գյումրիից մոտ 40 կմ մեքենայով։ Ամասիա շրջանից մոտ 5 կմ՝ լճի ուղղությամբ։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Lake Arpi is Armenia's largest highland wetland and a designated national park. It serves as a key stop for migratory birds, making it a birdwatching paradise — especially in spring and autumn when the lake draws rare and diverse species.</p>
<p>Set in the Shirak highlands above Gyumri, the landscape feels raw and open, a place where nature and silence genuinely take over.</p>
<h3>What to Do</h3>
<p>Birdwatching, lakeside walks, highland wetland photography, visit Amasia village nearby, and combine with a trip to Gyumri.</p>
<h3>How to Get There</h3>
<p>About 40 km from Gyumri by car. From Amasia village it is roughly 5 km further toward the lake.</p>
""",
    },

    {
        "id": "gosh-lake",
        "category": "armenia",
        "title_hy": "Գոշ լիճ",
        "title_en": "Gosh Lake",
        "location_hy": "Տավուշի մարզ, Գոշ գյուղի մոտ",
        "location_en": "Tavush Province, near Gosh village",
        "maps_url": "https://maps.app.goo.gl/2xDwD5Kktr1qAJry8",
        "rating": 4.5,
        "thumb": "static/img/sights/gosh-lake-main.jpg",
        "images": [
            "static/img/sights/gosh-lake-main.jpg",
            "static/img/sights/gosh-lake-reflection.jpg",
            "static/img/sights/gosh-lake-trail.jpg",
        ],
        "short_hy": "Անտառի մեջ թաքնված հանդարտ լիճ՝ մենավոր ու կոկիկ, Գոշավանքի մոտ",
        "short_en": "A secluded forest lake near Goshavank — quiet, pristine, perfect for hikers",
        "description_hy": """
<h3>Բնույթ</h3>
<p>Գոշ լիճը Տավուշի մարզի անտառի մեջ թաքնված մի վայր է, որ մնում է հիմնականում անհայտ զանգվածային զբոսաշրջիկների համար։ Մոտակայքում է XII դ. Գոշավանքը, ու կոմբինացիան ստեղծում է Տավուշի հիանալի ամբողջ օրը։</p>
<p>Անտառային լռությունը, լճի հայելային արտացոլումն ու բացակայ ամբոխը հատկապես գրավիչ են հանգստություն փնտրող հայքերի ու լուսանկարիչների համար։</p>
<h3>Ինչ անել</h3>
<p>Գոշավանք, լճի ափի արահետ, արտացոլման լուսանկարում, անտառային զբոսանք, Դիլիջան ու Պարզ լճի հետ կոմբինացիա։</p>
<h3>Ինչպես հասնել</h3>
<p>Դիլիջանից մոտ 12 կմ՝ Գոշ գյուղի ուղղությամբ։ Դիլիջանն ինքը Երևանից 100 կմ հեռու է։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Gosh Lake is a secluded forest lake in Tavush Province that remains largely off the tourist radar. The 12th‑century Goshavank monastery is just nearby, making the two together an excellent full Tavush day out.</p>
<p>The forest silence, mirror‑like reflections and near‑total absence of crowds make it particularly rewarding for hikers and photographers seeking tranquility.</p>
<h3>What to Do</h3>
<p>Visit Goshavank, walk the lakeside trail, photograph the reflections, explore the surrounding forest, and combine with Dilijan town and Parz Lake.</p>
<h3>How to Get There</h3>
<p>About 12 km from Dilijan toward Gosh village. Dilijan itself is 100 km from Yerevan.</p>
""",
    },
    {
        "id": "jermuk-waterfall",
        "category": "armenia",
        "title_hy": "Ջերմուկի ջրվեժ",
        "title_en": "Jermuk Waterfall",
        "location_hy": "Վայոց Ձորի մարզ, Ջերմուկ, 3701",
        "location_en": "Vayots Dzor Province, Jermuk, 3701",
        "maps_url": "https://maps.app.goo.gl/LLhjxpTJXzgkUfkg7",
        "rating": 4.6,
        "thumb": "static/img/sights/jermuk-waterfall-main.webp",
        "images": [
            "static/img/sights/jermuk-waterfall-main.webp",
            "static/img/sights/jermuk-waterfall-close.jpg",
            "static/img/sights/jermuk-waterfall-gorge.webp",
        ],
        "short_hy": "70 մ բարձրությամբ ջրվեժ՝ Ջերմուկ հանքային ջրերի քաղաքի սրտում",
        "short_en": "A 70-metre waterfall at the heart of Jermuk — Armenia's famous mineral water spa town",
        "description_hy": """
<h3>Ջրվեժը և քաղաքը</h3>
<p>Ջերմուկի ջրվեժը 70 մ բարձրությամբ է և գտնվում է Արփա գետի ձորի մեջ՝ հանդիսանալով քաղաքի բնական կենտրոնը։ Շուրջը հանքային ջրի աղբյուրներ են, սպա-հյուրանոցներ ու պրոմենադ։ Ջերմուկը Հայաստանի ամենահայտնի հանքային ջրի ու հանգստի քաղաքն է։</p>
<p>Ջրվեժի մոտ ձևավորված մառախուղն ու ձորի օզոնն ակնհայտ են, հենց մոտենում ես։ Ափի երկայնքով ձգվող պրոմենադից ջրի ձայնը լսվում է ամբողջ քաղաքում։</p>
<h3>Ինչ անել</h3>
<p>Ջրվեժի մոտ զբոսնել, հանքային ջուր խմել աղբյուրներից, հանգստյան spa պրոցեդուրաներ, ձորի պրոմենադ, Ջերմուկ քաղաքի ու շրջակայքի ուսումնասիրություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 170 կմ՝ M2 մայրուղիով մինչև Վայք, ապա ցուցանակներով դեպի Ջերմուկ։</p>
""",
        "description_en": """
<h3>Waterfall & Town</h3>
<p>The Jermuk Waterfall drops 70 metres into the Arpa River gorge — the natural centrepiece of the town. Surrounding it are mineral spring fountains, spa hotels and a riverside promenade. Jermuk is Armenia's most famous mineral water resort.</p>
<p>The mist from the falls and the gorge ozone are palpable the moment you approach. The sound of the water carries across the whole town from the promenade along the rim.</p>
<h3>What to Do</h3>
<p>Walk to the waterfall, drink mineral water straight from the springs, try spa treatments, stroll the gorge promenade and explore Jermuk town and its surroundings.</p>
<h3>How to Get There</h3>
<p>About 170 km from Yerevan via the M2 highway toward Vayk, then follow the signs to Jermuk.</p>
""",
    },

    {
        "id": "byurakan-observatory",
        "category": "armenia",
        "title_hy": "Բյուրականի աստղաֆիզիկական աստղադիտարան",
        "title_en": "Byurakan Astrophysical Observatory",
        "location_hy": "Արագածոտնի մարզ, Բյուրական, 0213",
        "location_en": "Aragatsotn Province, Byurakan, 0213",
        "maps_url": "https://maps.app.goo.gl/hj55E82zk4A4vWdp6",
        "rating": 4.5,
        "thumb": "static/img/sights/byurakan-observatory-main.webp",
        "images": [
            "static/img/sights/byurakan-observatory-main.webp",
            "static/img/sights/byurakan-observatory-night.jpg",
            "static/img/sights/byurakan-observatory-complex.jpg",
        ],
        "short_hy": "ԽՍՀՄ-ի ամենամեծ աստղաֆիզիկական աստղադիտարանը՝ Արագածի լանջին, հիմնված 1946-ին",
        "short_en": "The USSR's greatest astrophysical observatory on the slopes of Aragats, founded in the 1940s",
        "description_hy": """
<h3>Աստղադիտարանի մասին</h3>
<p>Բյուրականի աստղաֆիզիկական աստղադիտարանը հիմնադրվել է 1946-ին ակադեմիկոս Վիկտոր Համբարձումյանի կողմից։ Խորհրդային Միության ամենամեծ աստղաֆիզիկական կենտրոններից մեկն էր, ու մինչ օրս շարունակում է գործել։ Ի դեպ, զբոսաշրջիկների համար կազմակերպվում են ուղեկցորդային շրջայցեր, իսկ նախնական ամրագրմամբ հնարավոր է նաև աստղադիտակով երկնքի դիտում։</p>
<p>Երեկոյան աստղադիտման նստաշրջանն իսկական տիեզերական փորձառություն է Արագածի ստորոտին։ Հարմար է Քարի լճի ու Ամբերդի հետ կոմբինացնել մեկ Արագած-day trip-ում։</p>
<h3>Ինչ անել</h3>
<p>Ուղեկցորդային շրջայց, աստղադիտակով երկնքի դիտում (նախնական ամրագրմամբ), երեկոյան աստղ դիտում, Ամբերդ ամրոցի հետ կոմբինացիա, Արագածի լանդշաֆտ։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 50 կմ, Աշտարակ քաղաքից մոտ 20 կմ մեքենայով։ Ճանապարհը ցուցանակով հասանելի է Բյուրական–Արագածոտն ճանապարհով։</p>
""",
        "description_en": """
<h3>About the Observatory</h3>
<p>Founded in 1946 by academician Viktor Ambartsumyan, Byurakan was the greatest astrophysical observatory in the Soviet Union and remains scientifically active today. Guided tours are available for visitors, and telescope viewing sessions can be arranged with advance booking.</p>
<p>An evening stargazing session here is a genuine space experience on the slopes of Aragats. Best combined with Kari Lake and Amberd fortress in a single day trip.</p>
<h3>What to Do</h3>
<p>Guided observatory tour, telescope viewing (pre‑booked), evening stargazing, Amberd fortress combination, and Aragats landscape.</p>
<h3>How to Get There</h3>
<p>About 50 km from Yerevan and 20 km from Ashtarak by car. Signposted on the Byurakan–Aragatsotn road.</p>
""",
    },

    {
        "id": "khosrov-reserve",
        "category": "armenia",
        "title_hy": "Խոսրովի անտառ — Հայաստանի ամենահին արգելոց",
        "title_en": "Khosrov Forest Reserve — Armenia's Oldest Protected Area",
        "location_hy": "Արարատի մարզ, Գառնի–Խոսրով շրջան",
        "location_en": "Ararat Province, Garni–Khosrov area",
        "maps_url": "https://maps.app.goo.gl/kKcbo4zrSbHPkLgV7",
        "rating": 4.5,
        "thumb": "static/img/sights/khosrovi_antar.jpg",
        "images": [
            "static/img/sights/khosrovi_antar.jpg",
            "static/img/sights/khosrovi_dzor.jpg",
            "static/img/sights/khosrovi_jrvej.jpg",
        ],
        "short_hy": "IV դ. հաստատված արգելոց՝ Հայաստանի ամենահինը, ալպյան trekking-ի ու վայրի բնության համար",
        "short_en": "A nature reserve established in the 4th century — Armenia's oldest, with wild trekking trails",
        "description_hy": """
<h3>Արգելոցը</h3>
<p>Խոսրովի անտառը IV դ. հաստատվել է Արշակունի Խոսրով III թագավորի կողմից — աշխարհի ամենահին արգելոցներից մեկը։ Հանրության համար հասանելի է թույլտվությամբ կամ լիցենզավորված ուղեկցորդի հետ։ Անտառի ընդերքով հոսում են Աստղիկ, Վահագն ու Խոսրով գետերի ձորերը՝ ստեղծելով եզակի լեռնաանտառային էկոհամակարգ։</p>
<p>Սա Հայաստանի ամենավայրի ձևն է՝ լեռնային անտառ, խոր ձորեր, ազատ շրջող կենդանիներ ու ծառերի մեջ թաքնված հնագույն ավերակներ։</p>
<h3>Ինչ անել</h3>
<p>Trekking թույլատրված արահետներով (նախնական ամրագրմամբ), ձորի զբոսանք, կենդանիների դիտում, ալպյան լանդշաֆտի լուսանկարում։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 40 կմ՝ Գառնի ուղղությամբ։ Հասանելի է բացառապես լիցենզավորված ուղեկցորդի հետ կամ պաշտոնական թույլտվությամբ։</p>
""",
        "description_en": """
<h3>The Reserve</h3>
<p>Khosrov Forest Reserve was established by Arshakuni king Khosrov III in the 4th century AD — one of the oldest protected natural areas in the world. Access requires a permit or a licensed guide. The gorges of the Astghik, Vahagn and Khosrov rivers run through dense mountain forest, creating a unique alpine ecosystem.</p>
<p>This is Armenia at its wildest: mountain forest, deep gorges, roaming wildlife and ancient ruins hidden among the trees.</p>
<h3>What to Do</h3>
<p>Trekking on permitted trails (pre‑arranged), gorge walks, wildlife spotting and alpine landscape photography.</p>
<h3>How to Get There</h3>
<p>About 40 km from Yerevan toward Garni. Access with a licensed guide or official permit only.</p>
""",
    },
    {
        "id": "zvartnots",
        "category": "armenia",
        "title_hy": "Զվարթնոց տաճար",
        "title_en": "Zvartnots Cathedral Ruins & Museum",
        "location_hy": "Վաղարշապատ, Արմավիրի մարզ",
        "location_en": "Armavir Province, near Vagharshapat",
        "maps_url": "https://maps.app.goo.gl/eiLm35KKrJJ4QEoG8",
        "rating": 4.6,
        "thumb": "static/img/sights/zvartnots-new.jpg",
        "images": [
            "static/img/sights/zvartnots-old.png",
            "static/img/sights/zvartnots-new.jpg",
            "static/img/sights/zvartnots.jpg",
        ],
        "short_hy": "Զվարթնոց տաճար – ավերակներ և բացօթյա թանգարան",
        "short_en": "A UNESCO World Heritage Site — the ruins of Armenia's greatest 7th-century cathedral",
        "description_hy": """
<h3>Պատմություն</h3>
<p>Զվարթնոց տաճարը կառուցվել է 641–661 թթ․ կաթողիկոս Ներսես Շինարարի նախաձեռնությամբ՝ VII դարի Հայաստանի ամենամեծ և ամենամեծահոգի ճարտարապետական ծրագրերից մեկը։ Տաճարը, ըստ ամենայնի, ավերվել է X դարում, իսկ նրա ավերակները ներառվել են ՅՈՒՆԵՍԿՕ-ի համաշխարհային ժառանգության ցանկում 2000 թ.-ից։</p>
<h3>Ի՞նչ տեսնել</h3>
<p>Շրջանաձև հատակագիծ, կիսավեր սյունաշարեր, քանդակազարդ քարե խավարման մասեր, բաց դաշտ և հորիզոնում Արարատը՝ պարզ օրերին։ Տարածքում կարելի է տեսնել նաև խաչքարեր ու մանրաքանդակներ, որոնք պատկերացում են տալիս տաճարի հարուստ հարդարման մասին։</p>
<h3>Թանգարան</h3>
<p>Տարածքի փոքր թանգարանում ցուցադրվում են պեղումների ժամանակ գտնված քարե տարրեր, մոդելներ և տարբեր վերակազմությունների գծագրեր։ Լավ է համադրել այցը Էջմիածնի Մայր Տաճարի, Հռիփսիմեի և Գայանեի հետ՝ մեկ օրվա ընթացքում։</p>
<h3>Ինչպես հասնել</h3>
<p>Մոտ 20 կմ Երևանից և 2 կմ Էջմիածնից։ Կարելի է հասնել Էջմիածին գնացող ավտոբուսներով կամ մեքենայով։</p>
""",
        "description_en": """
<h3>History</h3>
<p>Zvartnots Cathedral was built in 641–661 AD by Catholicos Nerses III — the greatest and most ambitious architectural project of 7th-century Armenia. Destroyed by an earthquake in the 10th century, its ruins were added to the UNESCO World Heritage List in 2000.</p>
<h3>What to See</h3>
<p>Intricate carved decorations, ancient fresco fragments, a circular floor plan, partially reconstructed columns, and panoramic views of Mount Ararat as backdrop.</p>
<h3>Museum</h3>
<p>The on-site museum preserves carved elements and architectural fragments. Best combined with Etchmiadzin and Hripsime on a single day trip.</p>
<h3>How to Get There</h3>
<p>20 km from Yerevan, 2 km from Etchmiadzin. Bus toward Etchmiadzin or by car.</p>
""",
    },

    # ══════════════════════════════════════════
    #  ԵՐԵՎԱՆ (category: "yerevan")
    # ══════════════════════════════════════════

    {
        "id": "cascade",
        "category": "yerevan",
        "title_hy": "Կասկադ համալիր",
        "title_en": "Cascade",
        "location_hy": "Երևան, Կենտրոն, Մոսկովյան 10",
        "location_en": "Yerevan, Kentron, 10 Moskovyan Street",
        "maps_url": "https://maps.app.goo.gl/THTFRi4a4cW2qHKx9",
        "rating": 4.8,
        "thumb": "static/img/sights/kaskad_amrane.jpg",
        "images": [
            "static/img/sights/kaskad_amrane.jpg",
            "static/img/sights/kaskad_gisher.jpg",
            "static/img/sights/kaskad_tamanyan.jpg",
        ],
        "short_hy": "Կասկադ – աստիճաններ, արվեստ և Երևանի պանորամա",
        "short_en": "Yerevan's iconic landmark — stone cascade, open-air sculpture park and the city's best panoramic view",
        "description_hy": """
<h3>Ի՞նչ է</h3>
<p>Կասկադը Երևանի ամենահայտնի խորհրդանիշներից է․ երկար քարակերտ աստիճանաշար, որը միացնում է քաղաքի կենտրոնը Հաղթանակ զբոսայգու և Մայր Հայաստան արձանի հետ։ Տասնամյակների ընթացքում այն դարձել է քաղաքի «նստասենյակը»՝ տեղ, որտեղ մարդիկ հավաքվում են քայլելու, մարզվելու, արևամուտ նայելու և պարզապես քաղաքի կյանքը վերևից զգալու համար։</p>
<p>Կասկադի ներսում գործում է ժամանակակից արվեստի կենտրոն՝ Կաֆեսճյան արվեստի թանգարանը, որի սրահներում և աստիճանների երկայնքով ցուցադրվում են ժամանակակից քանդակներ և ինստալացիաներ՝ դարձնելով տարածքը բացօթյա և ներքին արվեստի տարածք մեկտեղ։</p>
<h3>Ի՞նչ անել</h3>
<p>Բարձրանալ մինչև վերին terrasse՝ տեսնելու քաղաքի և Արարատի պանորաման, քայլել բացօթյա քանդակների միջև, տեսնել Ալեքսանդր Թամանյանի արձանը Կասկադի ներքևի մասում և վայելել երեկոյան Երևանը՝ լույսերով ու կենդանի երաժշտությամբ։</p>
<h3>Ինչպես հասնել</h3>
<p>Քաղաքի կենտրոնում՝ Մոսկովյան 10 հասցեով։ Կարելի է հեշտությամբ հասնել քայլելով, տաքսիով կամ-autobusov՝ կախված, թե որտեղից ես գալիս։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Cascade is one of Yerevan's most iconic landmarks — a giant stairway of white limestone opened in the 1980s and still being expanded. Over decades it has become the city's living room: people gather here to exercise, stroll, and watch the sunset.</p>
<p>Inside the Cascade complex is the Cafesjian Museum — an open-air and indoor modern art museum with monumental sculptures lining the terraces and galleries within.</p>
<h3>What to Do</h3>
<p>Climb to the top terrace for the city panorama, visit Cafesjian Museum, admire outdoor sculptures, see the Tamanyan monument, evening stroll with Yerevan lit up below.</p>
<h3>How to Get There</h3>
<p>Right in the city centre at Moskovyan 10. Easily walkable, by taxi or bus.</p>
""",
    },

    {
        "id": "matenadaran",
        "category": "yerevan",
        "title_hy": "Մատենադարան – Մեսրոպ Մաշտոցի անվան հին ձեռագրերի ինստիտուտ",
        "title_en": "Matenadaran — Mesrop Mashtots Institute of Ancient Manuscripts",
        "location_hy": "Երևան, Մեսրոպ Մաշտոցի պողոտա 53, 0009",
        "location_en": "Yerevan, 53 Mashtots Avenue, 0009",
        "maps_url": "https://maps.app.goo.gl/of4VcLWJ4XnfWshv6",
        "rating": 4.7,
        "thumb": "static/img/sights/bmatenadaran.jpg",
        "images": [
            "static/img/sights/bmatenadaran.jpg",
            "static/img/sights/matenadarangrqer.jpeg",
            "static/img/sights/matenadaranners.jpg",
        ],
        "short_hy": "Մատենադարան – հայկական հին ձեռագրերի տուն",
        "short_en": "One of the world's greatest repositories of Armenian manuscripts — a UNESCO Memory of the World site",
        "description_hy": """
<h3>Ի՞նչ է</h3>
<p>Մատենադարանը նստած է Մաշտոցի պողոտայի վերևում՝ քարե ամրոցի պես․ դրսից՝ զանգվածային բազալտե շենք, ներսում՝ աշխարհի ամենամեծ հավաքածուներից մեկը հայկական ձեռագրերի, մանրանկարների և արխիվային գրքերի։ Մուտքի առաջ դիմավորում են Մեսրոպ Մաշտոցի և նրա աշակերտ Կորյունի արձանները՝ հիշեցնելով, որ այս վայրը ամբողջությամբ կառուցված է գրի և հիշողության գաղափարի շուրջ։</p>
<p>Հավաքածուում կան հազարավոր ձեռագիր հատորներ տարբեր դարերից՝ Ավետարաններ, գիտական աշխատություններ, բժշկության, աստղագիտության, քարտեզագրության գրքեր, երաժշտական նոտագրեր և գունավոր մանրանկարներ, որտեղ յուրաքանչյուր էջ մի ամբողջ աշխարհ է։ Շատ ձեռագրեր անցել են պատերազմների, հրդեհների և երկար ճանապարհների միջով ու հիմա պահվում են այստեղ՝ հատուկ պայմաններում։</p>
<h3>Ձեռագրերի սրահներում</h3>
<p>Գլխավոր ցուցասրահներում ցուցադրված են ամենակարևոր նմուշները՝ այբուբենի վաղ օրինակներ, լուսավորված էջեր ապակու տակ, ձեռագրեր, որոնք հայտնի են ոչ միայն իրենց տեքստով, այլ նաև գրագրությամբ ու նկարազարդումներով։ Բացատրական տեքստերն ու էքսկուրսավարների պատմությունները օգնում են «կարդալ» այն, ինչ տեսնում ես՝ սիմվոլների իմաստից մինչև այն, թե ինչպես էր պատրաստվում մագաղաթը կամ ներկերը։</p>
<h3>Զբոսանք և մթնոլորտ</h3>
<p>Ցուցասրահներից դուրս Մատենադարանը նաև գիտական ինստիտուտ է, որտեղ մասնագետները ամեն օր աշխատում են ձեռագրերի հետ՝ վերականգնում, թվայնացնում և ուսումնասիրում դրանք։ Թանգարանային այցից հետո հաճելի է մի քանի րոպե նստել Մատենադարանի առաջ գտնվող աստիճաններին ու նայել դեպի քաղաքի կենտրոն, երբեմն էլ՝ շենքերի արանքով երևացող Արարատին։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանի կենտրոնում՝ Մեսրոպ Մաշտոցի պողոտա 53։ Մոտ 10 րոպե քայլելու ճանապարհ Երիտասարական մետրոյի կայարանից կամ ցանկացած տաքսիով՝ «Մատենադարան» ասելով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Matenadaran is one of the world's greatest repositories of ancient manuscripts — over 23,000 manuscripts and 500,000 historical documents. It has been on UNESCO's Memory of the World register since 1997.</p>
<p>The building was constructed in 1959 against the backdrop of Mount Ararat — a masterpiece of Soviet classical architecture, fronted by the iconic statue of Mesrop Mashtots.</p>
<h3>What to See</h3>
<p>5th-century Gospels, miniature paintings, manuscripts showing the invention of the Armenian alphabet, and rotating UNESCO exhibits.</p>
<h3>Tours</h3>
<p>Guided tours available in Armenian, English, and Russian. Pre-booking recommended: +374 10-56-25-78 or online.</p>
<h3>How to Get There</h3>
<p>City centre at 53 Mashtots Avenue. 10-minute walk from Yeritasardakan metro station.</p>
""",
    },
]
