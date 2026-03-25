# backend/sights_data.py

# -*- coding: utf-8 -*-
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
        # garni
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
<p>24 Ionic columns, an elegant frieze, dramatic views over the Garni gorge and the "Symphony of Stones", plus the mosaic floor of a nearby Roman-era bathhouse.</p>
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
<h3>Ակնարկ</h3>
<p>Սևանա լիճը գտնվում է ծովի մակերևույթից մոտ 1900 մ բարձրության վրա եւ աշխարհի ամենամեծ բարձրադիր քաղցրահամ լճերից է՝ մոտ 1242 կм² մակերեսով։ Ամռանը վերածվում է լողի, ջրային սպորտի ու ձկնորսության կենտրոնի։</p>
<p>Լիճը նման է Հայաստանի կապույտ աչքին՝ հսկայական հայելի, որը փոխում է գույնը ըստ օրվա ժամի ու եղանակի. առավոտյան բաց կապույտ, կեսօրին՝ պայծառ ու շողացող, մայրամուտին՝ կարմրագույն։</p>
<p>Ափերին կան լողափեր, հանգստյան տներ ու փոքր գյուղեր։ Կարելի է լողալ, նավակ վարել, ճաշակել հայտնի Սևանի կարմրախայտ ձուկը՝ իշխանը, ինչպես նաև վրան խփել ափին։</p>
<h3>Ինչ անել</h3>
<p>Լողափերում լողալ, ջրային սպորտ, նավակային զբոսանք, Սևանավանք վանք, մայրամուտ, Նորատուսի խաչքարեր, վրանային կեցություն ափին։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 65 կմ։ Ավտոբուս Կիլիկիա ավտոկայանից, կամ մեքենայով M4 մայրուղով Սևան ուղղությամբ։</p>
""",
        "description_en": """
<h3>Overview</h3>
<p>Lake Sevan sits at around 1,900 m above sea level and is one of the largest high-altitude freshwater lakes in the world, with a surface area of about 1,242 km². In summer it becomes a hub for swimming, water sports and fishing.</p>
<p>The lake is like Armenia's blue eye — a huge mirror set between mountains that changes colour with the time of day and the seasons: pale blue in the morning, bright and sparkling at noon, and glowing crimson at sunset.</p>
<p>The shores are lined with beaches, resorts and small villages. You can swim, take a boat out, relax in small bays, listen to the wind moving the waves and camp along the shore. Try the famous Sevan trout — ishkhan — an endemic species served in restaurants all along the shore.</p>
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
<h3>Բնություն</h3>
<p>Փառ լիճը գտնվում է մոտ 1330 մ բարձրության վրա՝ Դիլիջանի ազգային պարկի անտառների մեջ։ Լճի շուրջ կա մոտ 2 կմ թեթև արշավային երթուղի, հարմար ընտանիքի համար։</p>
<p>Ամռանը կարելի է նավակ կամ պեդալ-նավ վարձել, ձկնորսություն անել ու դիտել անտառային կենդանիներին։</p>
<p>Գարնանը բլուրները վառ կանաչ են, աշնանը՝ ոսկեգույն ու կարմիր։ Ամռանն անգամ այստեղ ավելի հով է, քան քաղաքում, ու մի ժամ լճի ափին կարող է տաս ժամ հանգստի պես զգացվել։</p>
<h3>Ինչ անել</h3>
<p>Անտառային զբոսանք, Գոշավանք տանող արահետ, լճի հայելային մակերեսի լուսանկարչություն, թռչունների դիտում, բացօթյա սրճարաններ ու պիկնիկ գոտիներ։</p>
<h3>Ինչպես հասնել</h3>
<p>Դիլիջան քաղաքից մոտ 7 կм՝ տաքսիով կամ մեքենայով անտառային ճանապարհով, որը ցուցանշված է Փառ լճի ուղղությամբ։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Parz Lake sits at about 1,330 m inside Dilijan National Park. A gentle 2 km loop trail around the lake is family-friendly and perfect for light hiking.</p>
<p>In summer you can rent pedal boats or rowboats, fish and spot local wildlife in the surrounding forest.</p>
<p>In spring the hills turn bright green, in autumn the forest becomes gold and red. Even in summer it usually feels cooler here than in the city — an hour by the lake often feels like a whole day of real rest.</p>
<h3>What to Do</h3>
<p>Take forest walks, follow the trail towards Goshavank, photograph the mirror-like lake surface, watch birds and relax at the outdoor cafés and picnic areas.</p>
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
<p>Ազատ գետն Ամիասնդ տարիների ընթացքում փորել է Գառնու կիրճը, որի պատերին կան 40–50 մ բարձրության վեցանկյուն բազալտե սյուներ՝ հայտնի որպես «Քարերի սիմֆոնիա» կամ Basalt Organ։ Դրանք ձևավորվել են հնագույն հրաբխային ակտիվության և դանդաղ սառեցման արդյունքում։</p>
<p>Ձմռանը ճեղքերից ներս թափանցող ջուրը սառչում ու ծածկում է սյուները սառույցով, կիրճը վերածելով անիրական, ֆանտաստիկ լանդշաֆտի։</p>
<p>Կարելի է կիրճ մտնել Գառնիի տաճարի հետ նույն օրը՝ կա՛մ մեքենայով կոպտաքար ճանապարհով, կա՛մ գյուղից հին կամուրջով քայլելով։ Ճանապարհի ամեն քայլ նոր տեսարան է բացում։</p>
<h3>Գործնական տեղեկատվություն</h3>
<p>Մոտ 3–4 կմ քայլ, ասֆալտ ճանապարհ չկա, հարկ ա հարմար կոշիկ հագնել։ Կիրճ մտնելուց հետո ուղղակի կանգ ես առնում ու երկար ժամ ուղղակի նայում սյուներին։</p>
""",
        "description_en": """
<h3>Geological Wonder</h3>
<p>The Garni Gorge has been carved by the Azat River over thousands of years. Its walls are lined with hexagonal basalt columns up to 40–50 m tall, often referred to as the "Symphony of Stones" or the "Basalt Organ", formed by ancient volcanic activity and slow cooling.</p>
<p>In winter, water seeping through the cracks freezes and coats the columns in ice, turning the whole gorge into a surreal, otherworldly landscape.</p>
<p>Just below the Temple of Garni, the road drops into a canyon where one of Armenia's most surreal landscapes is hiding — a vertical wall of perfectly shaped hexagonal basalt columns, hanging from the cliff like the pipes of a giant church organ.</p>
<h3>Practical Info</h3>
<p>You can visit the gorge on the same day as the Garni Temple — either drive down the cobblestone road into the canyon or walk from the village via the old bridge. Expect roughly 3–4 km on foot and wear sturdy shoes. This is wild nature with no paved paths, but every turn of the road rewards you with new views.</p>
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
        # kari-lake
        "description_hy": """
<h3>Բնություն</h3>
<p>Քարի լիճը գտնվում է Արագած լեռան հարավային լանջին՝ մոտ 3200 մ բարձրության վրա։ Ամռանն անգամ ափին կարող ես ձյուն գտնել, ինչը հիանալի հակադրություն է ստեղծում կապույտ ջրի հետ։</p>
<p>Ամբերդ բերդն ու Բյուրականի աստղադիտարանն այստեղից մոտ են, ուստի հեշտ է մի օրվա մեջ լեռնային բնություն, պատմություն ու գիտություն համատեղել։</p>
<p>Լիճը լեռ բարձրանալու դասական մեկնակետն է. Արագածի հարավային գագաթ տանող արշավային արահետը սկսվում է հենց ջրի մոտ ու արագ բարձրանում անհարթ, հրաբխային տեղանք։ Նույնիսկ եթե գագաթ չես հասնի, արահետի կարճ հատվածն արդեն լճի ու շրջակա լեռների լայն տեսարան է բացում։</p>
<p>Բարձրության պատճառով օդը թարմ ու սուր է, ջուրը՝ սառը անգամ հուլիսին։ Շատ այցելուների համար իսկական հաճույք է պարզապես ափին նստել, դիտել ջրի վրա փոփոխվող լույսը ու զգալ, թե ամենօրյա կյանքը որքան հեռու է մնացել։</p>
<h3>Ինչ անել</h3>
<p>Արագածի հարավային գագաթ արշավ (3800 մ+), լուսանկարչություն, աստղադիտում մաքուր լեռնային օդում, Ամբերդ բերդի հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Հասանելի է մեքենայով Ապարանից կամ Բյուրականից՝ ոլոռնուած, բայց ամբողջությամբ ասֆալտապատ լեռնային ճանապարհով մինչև ափ։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Kari Lake sits at around 3,200 m on the southern slope of Mount Aragats. Even in summer you may find patches of snow along its shores, creating a striking contrast between deep blue water and white ridges.</p>
<p>Amberd Fortress and the Byurakan Astrophysical Observatory are both nearby, so it is easy to combine mountain scenery with history and science in a single day trip.</p>
<p>Kari Lake is also the classic starting point for hiking to the southern summit of Aragats — the trail to the peak begins right by the water and quickly climbs into rough, volcanic terrain. Even if you don't plan to reach the summit, a short walk up the path gives you increasingly wide views over the lake and the surrounding mountains.</p>
<p>Because of the altitude, the air is sharp and refreshing, and the lake water stays ice-cold even in July. For most people the real luxury here is simply sitting by the shore, watching the light change on the water and feeling how far everyday life has suddenly moved away.</p>
<h3>What to Do</h3>
<p>Use Kari Lake as the starting point for hiking to the southern summit of Aragats (3,800 m+), enjoy panoramic photography, stargazing in the crisp mountain air, and combine with Amberd fortress and Byurakan observatory.</p>
<h3>How to Get There</h3>
<p>Reachable by car from Aparan or Byurakan via a winding but fully paved mountain road that climbs all the way to the lakeshore. In early spring and late autumn check road conditions in advance.</p>
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
        # dilijan-town
        "description_hy": """
<h3>Ակնարկ</h3>
<p>Դիլիջանն հաճախ անվանում են «Հայաստանի փոքրիկ Շվեյցարիան»՝ 19-րդ դարի փայտե պատշգամբներով տներով, խիտ անտառներով ու զով լեռնային օդով։ Քաղաքը ՅՈՒՆԵՍԿՕ-ի ստեղծագործական քաղաքների ցանցի անդամ է ու դարձել է արվեստի, արհեստների ու դանդաղ ճամփորդությունների կենտրոն։</p>
<p>Հին Դիլիջանի սիրտը Շարամբեյան փողոցն է՝ վերականգնված քարե շենքերով, ավանդական պատշգամբներով, արհեստանոցներով ու հարմարավետ սրճարաններով, որտեղ կարող ես դիտել փայտագործ, կավագործ ու ջուլհակ արհեստավորներին։</p>
<p>Քաղաքի կենտրոնում Դիլիջանի քաղաքային պարկն է՝ փոքր լճով, բարձրահասակ ծառերով ու ոլոռնուած արահետներով։ Աշնանը պարկն ամբողջությամբ ոսկեգույն ու կարմիր է, գարնանը՝ վառ կանաչ։</p>
<p>Դիլիջանը հիանալի հենակետ է շրջակա տարածքի ուսումնասիրման համար՝ Հաղարծին, Գոշավանք, Փառ լիճ, ազգային պարկի արահետներ։ Բայց նույնիսկ առանց քաղաքից դուրս գալու, Շարամբեյան ու պարկ անցկացրած մի օրը բավական է հասկանալու, թե ինչու Դիլիջանն անվանում են Հայաստանի փոքրիկ Շվեյցարիան։</p>
<h3>Ինչ անել</h3>
<p>Հին թաղամաս ու քաղաքային պարկ, Հաղարծին ու Գոշավանք վանքեր, Դիլիջանի ազգային պարկի արահետներ, Փառ լիճ, արհեստանոցներ Շարամբեյանում։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 100 կմ։ Ավտոբուս կամ մինիբուս Կիլիկիա ավտոկայանից, կամ մեքենայով M4/M6 մայրուղիներով։</p>
""",
        "description_en": """
<h3>Overview</h3>
<p>Dilijan is often called Armenia's Little Switzerland — known for its 19th-century houses with wooden balconies, dense surrounding forests and cool mountain air. It is part of the UNESCO Creative Cities network and has become a hub for art, crafts and slow travel.</p>
<p>The heart of old Dilijan is Sharambeyan Street, lined with restored stone houses, traditional balconies, artisan workshops and cosy cafés where you can watch woodcarvers, potters and weavers at work.</p>
<p>In the centre of town, Dilijan City Park offers a different kind of calm — a small lake, tall trees, winding paths and benches where locals come to chat, walk dogs or let kids run around. In autumn the park explodes in reds and golds, in spring it turns bright green.</p>
<p>Dilijan makes a perfect base for exploring the wider area — Haghartsin and Goshavank monasteries, the trails of Dilijan National Park and Parz Lake. But even if you never leave the town, a day spent wandering the old street and sitting in the park is enough to understand why people call Dilijan Armenia's Little Switzerland.</p>
<h3>What to Do</h3>
<p>Stroll through the old quarter and city park, visit Haghartsin and Goshavank monasteries, explore Dilijan National Park trails, Parz Lake, and artisan workshops on Sharambeyan Street.</p>
<h3>How to Get There</h3>
<p>About 100 km from Yerevan. Take a bus or minibus from Kilikia bus station, or drive via the M4/M6 highways.</p>
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
        # gyumri-old-town
        "description_hy": """
<h3>Քաղաքը</h3>
<p>Գյումրին Հայաստանի երկրորդ մեծ քաղաքն է՝ հայտնի 19-րդ դարի կարմիր ու սև տուֆե շենքերով Քումայրի պատմական թաղամասում։ Քաղաքը դեռ կրում է 1988 թ. երկրաշարժի հետքերը, ինչն ավելացնում է նրա ուժի ու բնավորության զգացողությունը։</p>
<p>Վարդանանց հրապարակի, Աբովյան ու Ռիժկովի փողոցների շուրջ զբոսնելիս կտեսնես ոլոռնուած պատշգամբներ, հին արհեստանոցային ցուցանակներ ու կենդանի թաղամասային կյանք։</p>
<p>Բակ մտիր ու կտեսնես կախված լվացք, խաղացող երեխաներ, հարևաններ, որ խոսում են պատշգամբներից. Գյումրու հայտնի հումորն ու ջերմությունն ապրում են հենց այս անկյուններում։</p>
<p>Եթե սիրում ես քաղաքներ, որ մի փոքր անկատար են, մի փոքր հնամաշ, բայց հոգով լի, Գյումրու հին թաղամասն անփոխարինելի կանգառ է։ Այն տեղ է, ուր կծրագրես կիսօրյա այց ու կմնաս գիշերակաց, որ երեկոյան կրկին զբոսնես փողոցներով։</p>
<h3>Ինչ անել</h3>
<p>Հին թաղամաս ոտքով, Գյումրու պատմության թանգարան, Ձիթողցյան թանգարան, Ասլամազյան քույրերի պատկերասրահ, ավանդական ճաշատեսակներ, երաժշտական երեկոներ։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 126 կմ։ Գնացք Սասունցի Դավիթ կայարանից, ավտոբուս Կիլիկիա ավտոկայանից, կամ մեքենայով M1 մայրուղով դեպի հյուսիս։</p>
""",
        "description_en": """
<h3>The City</h3>
<p>Gyumri is Armenia's second largest city, famous for its 19th-century red and black tuff stone buildings in the historic Kumayri district. The city still bears the marks of the 1988 earthquake, which only adds to its sense of resilience and character.</p>
<p>A walk around Vardanants Square, Abovyan Street and the surrounding courtyards reveals ornate balconies, old workshop signs and lively neighbourhood life.</p>
<p>Step into a courtyard and you might see laundry hanging, children playing and neighbours chatting across balconies — Gyumri's famous sense of humour and warmth lives in these hidden corners just as much as on the main streets.</p>
<p>If you like cities that are a bit imperfect, a bit weathered, but full of soul, Gyumri's old town is an essential stop. It is the kind of place where you plan a half-day visit and end up staying overnight, just to wander the streets again in the evening light.</p>
<h3>What to Do</h3>
<p>Explore the old town on foot, visit the Gyumri History Museum, the Dzitoghtsyan Museum and the Aslamazyan Sisters Gallery, then try hearty local dishes and look for venues with live folk or jazz music in the evening.</p>
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
<h3>Ինչ է սա</h3>
<p>Խնձորեսկը հին քարայր-գյուղ է, որի բնակիչները մինչև 20-րդ դարի կեսերը ապրել են կիրճի պատերում փորված քարայրներում։ Կիրճը պարունակում է ավելի քան 160 քարայր, ինչպես նաև եկեղեցի, դպրոց ու պահեստային սենյակներ, որոնք դեռ տեսանելի են։</p>
<p>Գյուղի երկու կողմերը հիմա կապված են երկար կախովի կամուրջով, ինչն ինքնին փոքրիկ արկած է. կանգնած կամուրջի մեջտեղում՝ տեսնում ես ժայռերին ցրված քարայրները եւ զգում, թե որքան դրամատիկ է լանդշաֆտն ըստ էության։</p>
<p>Քարայրների մի մասը հեշտ մատչելի է, եւ դեռ պահպանված են առօրյա կյանքի հետքեր. մրոտված առաստաղներ, պատերին փորված խորշեր, կիսավեր սենյակներ, որտեղ ընտանիքներ են եփել, քնել ու կենդանիներ պահել։</p>
<p>Խնձորեսկն իդեալական է, եթե սիրում ես վայրեր, որ մի փոքր վայրի են, մի փոքր հում։ Կիրճ իջնելու արահետը, կամուրջի թեթև օրորոցը ու քարայրների ներսի լռությունը միասին տալիս են փորձ, որ հիշում ես դեռ երկար։</p>
<h3>Ինչ անել</h3>
<p>Կախովի կամուրջ, քարայրների ուսումնասիրություն, լուսանկարչություն, Տաթև վանքի հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Գորիս քաղաքից մոտ 8 կм՝ տաքսիով կամ մեքենայով լեռնային ճանապարհով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Khndzoresk is an ancient cave village carved into the walls of a dramatic gorge, inhabited until the mid-20th century. The gorge contains over 160 caves along with a church, a school and storage rooms still visible today.</p>
<p>The two sides of the village are now connected by a long swinging suspension bridge — a small adventure in itself — and unlike anything else in Armenia, with sweeping gorge views in every direction.</p>
<p>Some of the caves are easy to enter and still show traces of everyday life — soot-blackened ceilings, niches carved into the walls, half-collapsed rooms where families once cooked, slept and kept animals.</p>
<p>Khndzoresk is perfect if you like places that are a bit wild and a bit raw. The path down into the gorge, the gentle sway of the bridge and the silence inside the caves all combine into an experience that stays with you long after you leave.</p>
<h3>What to Do</h3>
<p>Cross the swinging bridge, explore the cave dwellings, photograph the layered gorge walls, and combine with Tatev Monastery for a full Syunik day trip.</p>
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
<h3>Ինչ է սա</h3>
<p>Քարահունջը, հայտնի նաև որպես Զորաց Քարեր, ավելի քան 200 կանգուն քարերի համալիր է, որոնցից շատերի գագաթին կան կատարյալ կլոր անցքեր։ Գիտնականները ենթադրում են, որ այն կարող է լինել աշխարհի ամենահին աստղագիտական դիտարաններից մեկը՝ մոտ 7500 տարեկան, հնարավոր է Սթոունհենջից 3500 տարի ավելի հին։</p>
<p>Քարերի միջով քայլելիս նկատում ես շարքեր, ներքին շրջաններ, ձեռքեր, որ ձգվում են հիմնական խմբից, ու մենակ կանգուն քարեր, որ կարծես շատ կանխամտածված ուղղություններ ցույց են տալիս։ Արշալույսին ու մայրամուտին լույսը ճեղքերով ու անցքերով անցնում է ու երկար ստվերներ գցում, ամբողջ վայրը վերածելով բնական լուսային ինստալյացիայի։</p>
<p>Քարահունջ այցելելը վահանակների ու թանգարանների մասին չէ, այն բաց երկնքի, քամու ու քարերի մասին է։ Մեծ ենթակառուցվածք չկա, ուղղակի սարավանդն ու հորիզոնը, ինչն հեշտ է պատկերացնել, թե ինչպես են հազարավոր տարիներ առաջ մարդիկ կանգնել նույն տեղում, նայել նույն հորիզոնին ու կարդացել երկինքը։</p>
<h3>Ինչ անել</h3>
<p>Քարե շրջանակների ու դասավորությունների ուսումնասիրություն, փոքր այցելուների կենտրոն, մութ ընկնելուց հետո աստղադիտում, Սիսիան քաղաքի ու Տաթևի հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Սիսիան քաղաքից մոտ 3 կմ՝ տաքսիով կամ մեքենայով։ Սիսիանն ինքը Երևանից մոտ 200 կմ է՝ M2 մայրուղով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Karahunj is a complex of over 200 standing stones, many of which have carefully drilled holes through them. Scholars believe it may be one of the world's oldest astronomical observatories, dating back around 7,500 years — potentially 3,500 years older than Stonehenge.</p>
<p>As you walk between the stones, you notice lines, inner circles, arms extending from the main group and solitary stones that seem to point in very deliberate directions. At sunrise and sunset the light slices through the gaps and holes, casting long shadows and turning the whole site into a natural light installation.</p>
<p>Visiting Karahunj is not about museums or signboards — it is about open sky, wind and stones. There are no big facilities here, just the plateau and the view, which makes it easy to imagine how people thousands of years ago stood in the same place, looking at the same horizon and reading the sky in a language we no longer fully understand.</p>
<h3>What to Do</h3>
<p>Explore the stone circles and alignments, visit the small on-site visitor centre, stay after dark for stargazing, and combine with Sisian town or a Tatev day trip.</p>
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
<p>Ամբերդն ամրոց-եկեղեցու համալիր է, կառուցված 10–13-րդ դարերում, ծայրահեղ ժայռոտ հրվանդանի վրա՝ 2300 մ բարձրության վրա, Արագածի լանջին, ուր հանդիպում են երկու խոր կիրճ։ Այն հսկել է հյուսիսային հայկական անցուղիները։</p>
<p>Ամրոցն իր ձեռքով անցել են բյուզանդացիները, սելջուկները ու մոնղոլները, սակայն պատերի ու եկեղեցու մեծ մասը մինչ օրս կանգուն է։</p>
<p>Ամրոցի ծայրով քայլելիս ուղղակի ներքև ես նայում կիրճը ու հեռվում Արարատն ու Արագածի գագաթներն ես տեսնում։ Հեշտ է հասկանալ, թե ինչու հենց այս վայրն ընտրվեց ամրոցի համար։</p>
<p>Տեղական ավանդույթը լրացուցիչ դրամա է ավելացնում. ըստ մի տարբերակի, մի կին հրաժարվել է անձնատուր լինելուց ու ընտրել ամրոցը թողնելն ու կիրճի խորքն իջնելը։ Ամբերդում, ամպամած երեկոյան, երբ մառախուղ է բարձրանում հովտից, այդ ավանդույթն ավելի իրական է թվում։</p>
<h3>Ինչ անել</h3>
<p>Ամրոցի պարագծով զբոսանք, եկեղեցու այց, Արագածի ու Արարատի համայնապատկեր, Մեծ Աղբյուր ջրվեժ, Կարի լճի հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Բյուրականից մոտ 18 կմ՝ լեռնային ճանապարհով։ Վաղ գարնանը ու ուշ աշնանը խորհուրդ է տրվում բարձր անցողունակության մեքենա։</p>
""",
        "description_en": """
<h3>History</h3>
<p>Amberd is a fortress and church complex built between the 10th and 13th centuries, perched on a dramatic rocky promontory at 2,300 m on the slopes of Mount Aragats, where two deep gorges meet. It guarded the northern Armenian borderlands.</p>
<p>Over the centuries Amberd passed through Byzantine, Seljuk and Mongol hands, yet much of the fortress walls and the church have survived to this day.</p>
<p>Walking along the edges of the fortress, you look straight down into the gorge and out towards the peaks of Aragats and Mount Ararat — it is easy to see why this place was chosen as a stronghold.</p>
<p>Local stories add extra drama — some versions tell of a woman who refused to surrender to the attacking army and chose to leave the safety of the fortress, disappearing into the depths of the gorge. On a cloudy evening, when mist rises from the valley and the silence feels almost theatrical, that legend feels very present.</p>
<h3>What to Do</h3>
<p>Walk the fortress perimeter, enter the church, take in panoramic views of Aragats and Mount Ararat, visit the nearby Mets Aghbyur waterfall, and combine with a hike from Kari Lake for a full Aragats day out.</p>
<h3>How to Get There</h3>
<p>About 18 km from Byurakan by mountain road. A high-clearance vehicle is recommended in early spring and late autumn.</p>
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
<h3>Բնություն</h3>
<p>Շաքիի ջրվեժը Հայաստանի ամենագեղեցիկ ու մատչելի ջրվեժներից մեկն է։ Ջուրն ընկնում է մոտ 18 մ բարձրությունից՝ բազալտե եզրի վրայից, բաժանվելով բազմաթիվ բարակ հոսքերի, որոնք միասին ձևավորում են հզոր սպիտակ վարագույր։ Կայանատեղիից կարճ զբոսանքից հետո հանկարծ լսում ես ջրի որոտը, նույնիսկ նախքան ջրվեժն ինքը կտեսնես։</p>
<p>Ըստ ավանդույթի՝ ջրվեժը կոչվել է Շաքի անունով՝ գեղեցիկ աղջկա, ով մերժել է օտար նվաճողի ոտնձգությունները, բարձրացել ժայռի գագաթ ու ցած նետվել։ Ընկնելիս նրա զգեստը բացվել ու վերածվել է հոսող ջրվեժի։</p>
<p>Ջրվեժ տանող արահետը կարճ է ու դժվար չէ, ինչն այն դարձնում է կատարյալ կանգառ Տաթև ճամփորդության ճանապարհին։ Կարելի է ջրի կողքի քարերին մոտ կանգնել, մի փոքր թրջվել, դրամատիկ լուսանկարներ անել ու նստել՝ պարզապես դիտելով ջրվեժի անդադար շարժը, որ երկար է հիշվում։</p>
<h3>Ինչ անել</h3>
<p>Ջրվեժի մոտ կանգնել ու զգալ ցողը, բազալտե պատերի լուսանկարչություն, կարճ անտառային արահետ, Գորիս ու Տաթև վանք շարունակել։</p>
<h3>Ինչպես հասնել</h3>
<p>Կապան-Գորիս մայրուղուց ցուցանշված Շաքի գյուղի մոտ։ Գորիսից մոտ 6 կմ, Կապանից՝ մոտ 100 կմ մեքենայով։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Shaki Waterfall is one of Armenia's most beautiful and accessible waterfalls. The water drops about 18 metres from a basalt ledge, breaking into dozens of thin streams that together form a powerful white curtain. After a short walk from the parking area, you suddenly hear the roar of the water before you even see the falls.</p>
<p>A local legend says the waterfall is named after a beautiful girl called Shaki. When a foreign conqueror tried to take her by force, she climbed to the top of the cliff and jumped rather than surrender. As she fell, her long dress opened and turned into a flowing cascade.</p>
<p>The trail to the waterfall is short and not difficult, which makes Shaki a perfect stop on the way to or from Tatev. You can walk right up to the rocks beside the water, get a little wet, take dramatic photos and then sit for a few minutes just watching the constant movement of the falls.</p>
<h3>What to Do</h3>
<p>Stand beside the falls and feel the spray, photograph the basalt walls, walk the short forest trail, then continue to Goris town and Tatev Monastery.</p>
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
<h3>Ինչ է սա</h3>
<p>Հին Խոտը գյուղ է, որ լքվել է 20-րդ դարի սկզբին՝ պահպանելով 19-րդ դարի կարմիր տուֆե տների 廃կողմերը՝ Տաթև վանքի մոտ կիրճի արահետի երկայնքով։</p>
<p>Նոր գյուղը վերակառուցվել է մոտ, բայց հին հատվածը մնացել է անձեռնմխելի. հարմար անծանոթ ուղիների ուսումնասիրության ու մթնոլորտային լուսանկարչության համար, հատկապես աշնանը ու ձմռանը։</p>
<p>Հին Խոտ հասնելը պահանջում է որոշ ջանք, բայց պարգևն անկոտրուն է. նեղ արահետներ, փլված պատեր, դռներ, որ բացվում են ուղղակի օդի վրա, ու ամեն շրջադարձ կիրճի ու ժայռերին կառչած գյուղի նոր անկյուն է բացում։</p>
<h3>Ինչ անել</h3>
<p>Կիրճի արահետ, քարե ավերակների ուսումնասիրություն, Տաթևի կիրճային տարածքի հետ համատեղ ուղևորություն, մթնոլորտային լուսանկարչություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Տաթևից մոտ 15 կմ ու Գորիսից 25 կմ՝ լեռնային ճանապարհով մեքենայով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>Old Khot is a village abandoned in the early 20th century, preserving the ruins of 19th-century red tuff stone houses along a gorge trail near Tatev Monastery.</p>
<p>The new village was rebuilt nearby, but the old section remains beautifully untouched — ideal for off-the-beaten-path exploration and atmospheric photography, especially in autumn or winter.</p>
<p>Reaching Old Khot takes some effort, but the reward is powerful — narrow paths wind between collapsed walls, doorways open onto nothing but air, and every turn reveals another angle of the gorge and the village clinging to its cliffs.</p>
<p>If you love hidden, slightly wild places with real stories etched into the stones, Old Khot is a must-visit stop in the Tatev area.</p>
<h3>What to Do</h3>
<p>Walk the gorge trail, explore the stone ruins, combine the visit with the Tatev gorge area and Goris town, and photograph the layered mountain and gorge scenery.</p>
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
<h3>Ինչ է սա</h3>
<p>Որոտան կիրճը Սյունիքի ամենադրամատիկ բնական լանդշաֆտներից մեկն է. գետն ու «Թաթևի թևեր» ճոպանուղին հետևում են կիրճի եզրով, ու դիտահրապարակներից բացվում է անդունդի ամբողջ խորությունը։</p>
<p>Կիրճի հատակին, Տաթևի ուղղությամբ, Սատանի կամուրջն է՝ բնական ժայռե կամար, գետի կողմից հազարավոր տարիների ընթացքում փորված։ Ժամանակակից ասֆալտե ճանապարհն անցնում է կամարի վրայով, ներքևում ջուրն անցնում է նեղ ճեղքով։ Վաղ այցելուները, տեսնելով նման հսկա կամուրջ առանց մարդկային կառուցապատողի, որոշել են, որ այն սատանայի գործ է, ու անունն այդպես էլ մնացել է։</p>
<p>Կամուրջի տակ թաքնված են տաք հանքային աղբյուրներ ու փոքր բնական ավազաններ. հանքային ջուրը ժայռերը ներկել է կանաչ, դեղին ու նարնջագույն երանգներով, ու ցուրտ օրերին գոլորշի է բարձրանում ջրի վրա։</p>
<p>Որոտան կիրճն ու Սատանի կամուրջն հեշտ են Տաթևի ու «Թաթևի թևեր»-ի հետ նույն օրն այցելել. վերևից կիրճի լայն տեսարան, ներքևից ջրի, ժայռի ու տաք աղբյուրների հետ անմիջական շփում։</p>
<h3>Ինչ անել</h3>
<p>Բնական կամարի վրա կանգնել, ամռանը ավազաններում լողալ, կիրճի լուսանկարչություն, Տաթև ու Խնձորեսկ շարունակել։</p>
<h3>Ինչպես հասնել</h3>
<p>Գորիսից մոտ 20 կմ ու Կապանից 80 կմ։ Ցուցանշված Գորիս-Կապան մայրուղուց։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Vorotan Gorge is one of Syunik's most spectacular natural landmarks. The river cuts deep into the plateau, creating steep cliffs and dizzying drops, while the Wings of Tatev cableway traces the rim above. From the viewpoints you see the gorge open up in front of you and understand just how deep it really is.</p>
<p>At the bottom of the canyon lies Devils Bridge — a natural rock arch carved by the river over thousands of years. An asphalt road runs across the top, while below the water squeezes through a narrow passage. Early visitors who saw such a huge bridge with no human builder decided it must be the work of the devil — hence the name.</p>
<p>Hidden beneath the bridge are warm mineral springs and natural pools. The mineral-rich water has stained the rocks in shades of green, yellow and orange, and steam rises on cool days. Adventurous visitors climb down to soak in the pools, listening to the muffled sound of cars overhead and the constant rush of the river beside them.</p>
<p>Vorotan Gorge fits perfectly into the same day as Tatev and the cableway — sweeping canyon views from above combined with close-up encounters with water, rock and hot springs below.</p>
<h3>What to Do</h3>
<p>Stand on the natural arch, swim in the pools in summer, photograph the gorge scenery, then continue to Tatev and Khndzoresk for a full Syunik day.</p>
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
<h3>Բանաստեղծի գյուղ</h3>
<p>Դսեղը Հովհաննես Թումանյանի՝ Հայաստանի սիրելի բանաստեղծի ծննդավայրն է։ Գյուղը գտնվում է Լոռու կանաչ անտառներում՝ դրամատիկ կիրճի վրա, հենց այն լանդշաֆտը, որ ոգեշնչել է նրա բալլադներն ու էպոսները։</p>
<p>Գյուղի կենտրոնում Թումանյանի տուն-թանգարանն է, որ պահպանում է մանկության տան մթնոլորտը. փայտե պատշգամբ, պարզ սենյակներ ու իրեր, որ Անուշի, Շունն ու կատուն կամ Գիքորի աշխարհները շատ ավելի մոտ են դարձնում։ Դուրս արի, ու րոպեների ընթացքում արդեն արահետների վրա ես, որ տանում են դաշտեր ու անտառներ, որ ոգեշնչել են նրան։</p>
<p>Դսեղի շուրջ կան մի քանի նշված արահետներ ու դիտահրապարակներ. օղաձև արշավային երթուղիներ, որ անցնում են մարգագետիններով ու անտառով, բերում Դեբեդ կիրճի եզր։ Այնտեղից ներքև ես նայում հեռու գետը ու կանաչ բլուրների շերտերը, հատկապես գեղեցիկ աշնանը, երբ գույները պայթում են, ու ամռանը, երբ անտառը ստվեր է տալիս։</p>
<p>Եթե ուզում ես Հայաստանի ավելի հանգիստ, քնարական կողմը ճանաչել, Դսեղն իդեալական վայր է դանդաղելու համար։ Պետք չեն ատրակցիոններ կամ ճոպանուղիներ. պարզապես զբոսիր գյուղի փողոցներով, նստիր կիրճի մոտ, լսիր ծառերի մեջ քամին ու հասկացիր, թե ինչու Թումանյանի տողերից շատերը կարծես գրված են հենց այս լանդշաֆտի մասին։</p>
<h3>Ինչ անել</h3>
<p>Թումանյանի տուն-թանգարան, կիրճի դիտահրապարակ, անտառային արշավ, Դեբեդ կիրճի լուսանկարչություն, կենդանի Լոռու գյուղի մթնոլորտ։</p>
<h3>Ինչպես հասնել</h3>
<p>Վանաձորից մոտ 35 կմ ու Երևանից մոտ 175 կմ մեքենայով՝ դեպի Լոռու մարզ։</p>
""",
        "description_en": """
<h3>Village of a Poet</h3>
<p>Dsegh is the birthplace of Hovhannes Tumanyan — Armenia's most beloved poet. The village sits in Lori's green forests above a dramatic canyon, the very landscape that inspired his ballads and epics.</p>
<p>In the centre of the village, Tumanyan's house-museum preserves the atmosphere of his childhood home — a wooden balcony, simple rooms and objects that make the worlds of Anush, The Dog and the Cat or Gikor feel much closer. Step outside, and within minutes you are already on paths leading into the fields and forests that inspired him.</p>
<p>Around Dsegh there are several marked trails and viewpoints — loop hikes that wind through meadows and woodland, past springs and small stone bridges, and eventually bring you to the edge of Debed Canyon. From there you look down at the river far below and across layers of green hills, especially beautiful in autumn when the colours explode and in summer when the forest offers cool shade.</p>
<p>If you want to experience the quieter, more lyrical side of Armenia, Dsegh is a perfect place to slow down. You don't need attractions or rides here — just walk the village streets, sit on a bench near the canyon, listen to the wind in the trees and understand why so many of Tumanyan's lines feel like they were written with this landscape in mind.</p>
<h3>What to Do</h3>
<p>Tumanyan House-Museum, canyon viewpoint, forest trail walks, Debed Canyon photography, and soaking in the authentic atmosphere of a living Lori village.</p>
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
<h3>Բնություն</h3>
<p>Արփի լիճը Հայաստանի ամենամեծ բարձրադիր ճահճուտն է ու ազգային պարկ։ Այն գտնվում է Շիրակի բարձրավանդակում՝ Գյումրուց հյուսիս, Վրաստանի սահմանի մոտ։ Մեծ հանգստավայրեր կամ աղմկոտ լողափեր չկան, ուղղակի ջուր, լայն երկնք, փոքր գյուղեր ու լռություն։</p>
<p>Լիճն ու շրջակայքը կազմում են ազգային պարկ ու թռչունների կարևոր բնօրրան։ Գարնանը ու ամռանը կարելի է տեսնել բազմաթիվ տեսակներ, որ բնադրում ու կերակրվում են ճահճուտների շուրջ, իսկ աշնանը լիճը դառնում է գաղթող հոտերի կանգառ։ Թռչուններ դիտողների կամ ուղղակի երկինքը դիտողների համար Արփի լիճը հատուցիչ վայր է։</p>
<p>Արփի լիճ այց կատարելն ավելի շատ փախուստի ու հանգստի մասին է, քան ակտիվ ծրագրի։ Քայլիր ափով, նստիր խոտի մեջ, լսիր քամու ու թռչունների ձայնը ու դիտիր ջրի վրա փոփոխվող լույսը։ Եթե ուզում ես Հայաստանի ավելի քիչ այցելված, անկեղծ ու խաղաղ կողմը տեսնել, Արփի լիճն իդեալական ավելացում է երթուղուդ։</p>
<h3>Ինչ անել</h3>
<p>Թռչունների դիտում, ափային զբոսանք, բարձրավանդակային ճահճուտի լուսանկարչություն, Ամասիա գյուղ, Գյումրու հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Գյումրուց մոտ 40 կմ մեքենայով։ Ամասիա գյուղից լիճ հասնելու համար ևս մոտ 5 կմ։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Lake Arpi is Armenia's largest highland wetland and a designated national park, spread across the open Shirak plateau near the border with Georgia. There are no big resorts or party beaches here — just water, wide skies, small villages and the feeling that you are very far from city noise.</p>
<p>The lake and its surroundings form an important habitat for birds. In spring and summer you can see many species nesting and feeding around the wetlands, while in autumn it becomes a stopover for migrating flocks. For anyone interested in birdwatching — or simply in watching the sky — Lake Arpi is a rewarding place to be.</p>
<p>A visit to Lake Arpi is more about escape than activity. Walk along the shore, sit in the grass, listen to the wind and birds and watch the light change on the water. If you want to see a different, less-visited side of Armenia — honest, understated and peaceful — this is an excellent place to add to your route.</p>
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
<h3>Բնություն</h3>
<p>Գոշ լիճը Տավուշի մարզի անտառային լիճ է, որ հիմնականում դուրս է մնում զբոսաշրջային ուղիներից։ 12-րդ դարի Գոշավանք վանքը հենց մոտ է, ինչն ունի Տավուշ-day-trip-ի լավ համադրություն։</p>
<p>Անտառի լռությունը, հայելային արտացոլումները ու ամբոխի գրեթե բացակայությունն այն հատկապես հատուցիչ են դարձնում արշավողների ու լուսանկարիչների համար, ովքեր փնտրում են հանգստություն։</p>
<p>Լիճ հասնելու համար անտառային արահետով ես քայլում. փափուկ հող, արմատներ, ժայռեր, փոքր առուներ ու մամուռի կտորներ։ Փառ լճի համեմատ, որ շատ հեշտ մատչելի է, Գոշ լիճն ավելի փոքրիկ արկած է. պետք է քայլել ու վաստակել, ու հենց դա է պահում մթնոլորտն անդորրով, երբ հասնում ես։</p>
<p>Եթե արդեն այցելել ես Փառ լիճ ու ուզում ես Դիլիջանի ավելի վայրի կողմն ապրել, Գոշ լիճը հաջորդ տրամաբանական քայլն է. այն վայր է, ուր հեշտ է ժամանակի հետևից կորցնել, հատկապես եթե ափին հանգիստ նստես ու դիտես, թե ինչպես անտառն ինքն իրեն ջրի մակերեսին ներկում ու վերաներկում է։</p>
<h3>Ինչ անել</h3>
<p>Գոշավանք, ափային արահետ, արտացոլումների լուսանկարչություն, շրջակա անտառի ուսումնասիրություն, Դիլիջան ու Փառ լճի հետ համատեղ ուղևորություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Դիլիջանից մոտ 12 կմ՝ Գոշ գյուղ ուղղությամբ։ Դիլիջանն ինքը Երևանից 100 կմ է։</p>
""",
        "description_en": """
<h3>Nature</h3>
<p>Gosh Lake is a secluded forest lake in Tavush Province that remains largely off the tourist radar. The 12th-century Goshavank monastery is just nearby, making the two together an excellent full Tavush day out.</p>
<p>The forest silence, mirror-like reflections and near-total absence of crowds make it particularly rewarding for hikers and photographers seeking tranquility.</p>
<p>To reach the lake you follow a forest trail — soft earth, roots, rocks, small streams and patches of moss. Compared to Parz Lake, which is very easy to access, Gosh Lake feels more like a little adventure — you have to walk and earn it, and that effort is exactly what keeps the atmosphere peaceful when you arrive.</p>
<p>If you have already visited Parz Lake and want to experience Dilijan's wilder side, Gosh Lake is the next logical step. It is the kind of spot where you can easily lose track of time — especially if you sit quietly on the shore and watch the forest slowly paint and repaint itself on the surface of the water.</p>
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
<h3>Ջրվեժ-քաղաք</h3>
<p>Ջերմուկի ջրվեժը մոտ 70 մ բարձրությունից ընկնում է Արփա գետի կիրճի մեջ՝ բաժանվելով բարակ հոսքերի, որ սահում են ժայռի վրայով մազերի պես։ Հենց դա է ոգեշնչել տեղական մականունը՝ «ջրահարսի մազեր»։</p>
<p>Ըստ ավանդույթի՝ ջրահարս է ապրել այստեղ ու սիրահարվել մահկանացուի։ Երբ արգելել են տեսնվել նրա հետ, ջրահարսն ընտրել է անհետանալ ժայռի մեջ, ու ուղղակի նրա երկար մազերն են մնացել՝ հավիտյան հոսելով որպես ջրվեժ։</p>
<p>Ջրվեժը գտնվում է Ջերմուկ քաղաքի հենց ներքևում՝ նեղ կիրճում։ Վերևում հանքային ջրի սանատորիումներ ու պուրակներ են, ներքևում լանդշաֆտն հանկարծ վայրի է դառնում՝ ժայռե ժայռուտ ու Արփա գետը կիրճի միջով։ Կամուրջից ու դիտահրապարակներից կա ջրվեժի ու կիրճի տպավորիչ տեսարան։</p>
<p>Ջերմուկ այցն ամենալավն է համատեղել հանգստի ու բնության. ժամանակ անցկացնել սպայում, ճաշակել հանքային ջուրը հանքային ջրի պատկերասրահում, հետո ջրվեժ իջնել ու ճաշել դեմքիդ ու ձեռքերիդ վրա ծածկվող ցողը։</p>
<h3>Ինչ անել</h3>
<p>Ջրվեժ, հանքային ջրի պատկերասրահ, սպա բուժման փորձ, կիրճի ափամերձ արահետ, Ջերմուկ քաղաքի ու շրջակայքի ուսումնասիրություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 170 կմ՝ M2 մայրուղով դեպի Վայք, հետո ցուցանշված ճանապարհով դեպի Ջերմուկ։</p>
""",
        "description_en": """
<h3>Waterfall Town</h3>
<p>The Jermuk Waterfall drops 70 metres into the Arpa River gorge — the natural centrepiece of the town. The water splits into dozens of thin streams that slide down the cliff like strands of hair, inspiring its local nickname "the Mermaid's Hair waterfall".</p>
<p>According to legend, a water maiden once lived here and fell in love with a mortal. When she was forbidden to see him, she chose to disappear into the rock, and only her long hair remained, flowing forever as the waterfall.</p>
<p>The waterfall lies in a narrow gorge just below the spa town of Jermuk. Above are sanatoriums, hot springs and parks — below, the landscape suddenly becomes wild, with steep cliffs and the Arpa River rushing through the canyon. From the bridge and viewpoints you get impressive angles of both the falls and the gorge.</p>
<p>A visit to Jermuk works best as a mix of wellness and nature — spend time in the spa, taste the mineral waters at the gallery, and then walk down to the waterfall to feel cool mist on your face. It is one of those places where being there — listening to the water and feeling the scale of the cliff — leaves a much stronger impression than any photo.</p>
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
<p>Բյուրականի աստղաֆիզիկական աստղադիտարանը հիմնադրվել է 1946 թ. ակադեմիկոս Վիկտոր Համբարձումյանի կողմից ու Խորհրդային Միությունում ամենամեծ աստղաֆիզիկական աստղադիտարանն էր։ Այն մինչ օրս գործող գիտական կենտրոն է ու բաց է այցելուների համար։</p>
<p>Ցերեկն կարելի է զբոսնել տարածքով, մոտից տեսնել տարբեր գմբեթները ու լսել այստեղ արված հայտնագործությունների պատմությունները։ Ուղեկցված այցերի ժամանակ երբեմն հնարավոր է ներս մտնել ու տեսնել աստղադիտակները, ու կազմակերպել աստղադիտում՝ կանխավ ամրագրելով։</p>
<p>Արագածի լանջին, Բյուրական գյուղի մոտ, Բյուրականը նման է փոքրիկ գիտական քաղաքի. ծառերի ու ցածր շինությունների մեջ ցրված աստղադիտակի գմբեթներ, բոլորը ձևավորված գիշերային երկնքի ուսումնասիրության համար։ Ծանոթ աստղագետ Համբարձումյանն ու նրա թիմը կազմեցին կարևոր աստղային ու գալակտիկական կատալոգներ ու ողջ աշխարհից գիտնականներ ընդունեցին։</p>
<p>Գիշերն աստղադիտարանն իսկապես կախարդական է դառնում. քաղաքային լույսերը հեռու են, օդը՝ մաքուր, ու Ծիր Կաթինն հաճախ ողջ երկնքով ձգվում է տեսանելի։ Եթե հետաքրքրված ես տիեզերքով, գիտությամբ կամ ուղղակի մութ երկնքի տակ աստղադիտումով, Բյուրականն Հայաստանի ամենահիշվող վայրերից մեկն է։</p>
<h3>Ինչ անել</h3>
<p>Ուղեկցված տեսք, աստղադիտակի դիտում (կանխավ ամրագրել), երեկոյան աստղադիտում, Ամբերդ բերդի հետ համատեղ ուղևորություն, Արագածի լանդշաֆտ։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 50 կմ ու Աշտարակից 20 կմ մեքենայով։ Ցուցանշված Բյուրական-Արագածոտն ճանապարհով։</p>
""",
        "description_en": """
<h3>About the Observatory</h3>
<p>Founded in 1946 by academician Viktor Ambartsumyan, Byurakan was the greatest astrophysical observatory in the Soviet Union and remains scientifically active today. Guided tours are available for visitors, and telescope viewing sessions can be arranged with advance booking.</p>
<p>During the day you can walk around the grounds, see different domes up close and hear stories about the discoveries made here. On guided visits it is sometimes possible to step inside and see some of the telescopes, getting a sense of what it is like to work nights in this quiet, high-altitude setting with the sky as your main companion.</p>
<p>Perched on the slopes of Mount Aragats near Byurakan village, the observatory looks like a small scientific town — telescope domes scattered among trees and low buildings. Ambartsumyan and his team compiled important stellar and galactic catalogues and hosted scientists from all over the world.</p>
<p>At night the observatory becomes truly magical — city lights are far away, the air is clear, and the Milky Way often stretches visibly across the sky. If you are interested in space, science or just stargazing under a really dark sky, Byurakan is one of the most memorable places you can visit in Armenia.</p>
<h3>What to Do</h3>
<p>Guided observatory tour, telescope viewing (pre-booked), evening stargazing, Amberd fortress combination, and Aragats landscape.</p>
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
<h3>Արգելոցի մասին</h3>
<p>Խոսրովի անտառ պետական արգելոցը հիմնադրվել է Արշակունի թագավոր Խոսրով III-ի կողմից մ.թ. IV դ.՝ աշխարհի ամենահին պահպանվող բնական տարածքներից մեկը։ Մուտքը պահանջում է թույլտվություն կամ լիցենզավորված ուղեկցորդ։ Աստղիկ, Վահագն ու Խոսրով գետերի կիրճերն անցնում են խիտ լեռնային անտառով՝ ձևավորելով յուրահատուկ ալպիական էկոհամակարգ։</p>
<p>Սա Հայաստանն իր ամենավայրի տեսքով է՝ լեռնային անտառ, խոր կիրճեր, վայրի բնություն ու հնագույն ավերակներ՝ ծառերի մեջ թաքնված։ Կիսաանապատ բլուրներ, ժայռոտ կիրճեր, անտառածածկ լանջեր ու փոքր ջրվեժներ հանդիպում են նույն լանդշաֆտի ներսում։</p>
<p>Արգելոցն սովորական բաց ազգային պարկ չէ, բայց կան հատուկ հանրային արահետներ ու ուղեկցված երթուղիներ, այդ թվում արշավներ դեպի Աստղիկ ու Վահագն ջրվեժներ ու Գառնու տարածքը արգելոցի արտաքին հատվածների հետ կապող երթուղիներ։</p>
<p>Եթե արդեն տեսել ես Գառնի ու ուզում ես մի փոքր ավելի խոր մտնել Հայաստանի վայրի բնություն՝ առանց բազմօրյա արշավի, Խոսրովի արգելոցի մատչելի արահետներն իդեալական հաջորդ քայլն են. ավելի քիչ մեքենաներ, ավելի շատ ժայռ ու լռություն, ու ուժեղ զգացողություն, որ քաղաքից շատ հեռու ես։</p>
<h3>Ինչ անել</h3>
<p>Թույլատրված արահետներով արշավ (կազմակերպված), կիրճային զբոսանք, վայրի բնության դիտում ու ալպիական լանդշաֆտի լուսանկարչություն։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 40 կմ՝ Գառնի ուղղությամբ։ Մուտք՝ բացառապես լիցենզավորված ուղեկցորդի կամ պաշտոնական թույլտվության հետ։</p>
""",
        "description_en": """
<h3>The Reserve</h3>
<p>Khosrov Forest Reserve was established by Arshakuni king Khosrov III in the 4th century AD — one of the oldest protected natural areas in the world. Access requires a permit or a licensed guide. The gorges of the Astghik, Vahagn and Khosrov rivers run through dense mountain forest, creating a unique alpine ecosystem.</p>
<p>This is Armenia at its wildest — mountain forest, deep gorges, roaming wildlife and ancient ruins hidden among the trees. Semi-desert hills, rocky gorges, forested slopes and small waterfalls all meet within the same landscape.</p>
<p>The reserve is not a regular open national park, but there are specific public trails and guided routes that visitors can join, including hikes toward Astghik and Vahagn waterfalls and routes that link the Garni area with the outer parts of the reserve.</p>
<p>If you have already seen Garni and want to push a bit deeper into Armenia's wild side without committing to a multi-day trek, the accessible trails
    },
    {
        "id": "zvartnots",
        "category": "armenia",
        "title_hy": "Զվարթնոց տաճարի ավերակներ և թանգարան",
        "title_en": "Zvartnots Cathedral Ruins Museum",
        "location_hy": "Արմավիրի մարզ, Էջմիածնի շրջակայք",
        "location_en": "Armavir Province, near Vagharshapat",
        "maps_url": "https://maps.app.goo.gl/eiLm35KKrJJ4QEoG8",
        "rating": 4.6,
        "thumb": "static/img/sights/zvartnots-new.jpg",
        "images": [
            "static/img/sights/zvartnots-old.png",
            "static/img/sights/zvartnots-new.jpg",
            "static/img/sights/zvartnots.jpg",
        ],
        "short_hy": "ՅՈՒՆԵՍԿՕ-ի Համաշխարհային ժառանգության ցանկում ընդգրկված 7-րդ դարի տաճարի ավերակներ",
        "short_en": "A UNESCO World Heritage Site – the ruins of Armenia's greatest 7th-century cathedral",
        "description_hy": """
<h3>Պատմություն</h3>
<p>Զվարթնոց տաճարը կառուցվել է 641-661 թթ. կաթողիկոս Ներսես Շինողի կողմից, VII դ. Հայաստանի ամենամեծ ու ամենահամարձակ ճարտարապետական ծրագիրը։ X դ. երկրաշարժից ավերվել է, ու 2000 թ. ավելացվել ՅՈՒՆԵՍԿՕ-ի Համաշխարհային ժառանգության ցանկում։</p>
<p>Անունը կապված է «զվարթ» բառի հետ, ինչը նշանակում է ուրախ կամ պայծառ, ու «զվարթաց»՝ երկնային զորքեր հասկացության հետ, ինչն անվանը տալիս է «հրեշտակների բնակարան» իմաստ։ Շրջանաձև հատակագծով, բաց սյունաշարերով ու վերևից ֆիլտրվող լույսով, տաճարը ձևավորվել էր որպես տարածք, ուր ճարտարապետությունն ու լույսը միասին են աշխատում։</p>
<p>Նույնիսկ ավերակ վիճակում այդ սկզբնական հավակնոտությունը շատ հստակ զգացվում է։ Հիմնապատերի վերականգնված ուրվագծերը, պահպանված քանդակված քարերը ու օղակաձև հատակագիծը պատկերացում են տալիս սկզբնական ծավալների ու մեծության մասին։</p>
<p>Տեղամասի թանգարանը պահպանում է փորագրված տարրեր ու ճարտարապետական բեկորներ։ Լավ է համադրել այցելությունը Էջմիածնի գլխավոր տաճարի ու Ս. Հռիփսիմեի հետ՝ մեկ օրվա մեջ։</p>
<h3>Ինչ անել</h3>
<p>Շրջել ավերակների մեջ, ուսումնասիրել սյուների ու քանդակների մանրամասները, այցելել տեղամասի թանգարան, լուսանկարել Արարատի տեսարանով ֆոնը և Զվարթնոցը համադրել Էջմիածնի ու Հռիփսիմեի հետ մեկ օրվա ուղևորության մեջ։</p>
<h3>Ինչպես հասնել</h3>
<p>Երևանից մոտ 20 կմ, Էջմիածնից մոտ 2 կմ։ Կարելի է հասնել ավտոբուսով Էջմիածին ուղղությամբ կամ մեքենայով։</p>
""",
        "description_en": """
<h3>History</h3>
<p>Zvartnots Cathedral was built in 641–661 AD by Catholicos Nerses III – the greatest and most ambitious architectural project of 7th-century Armenia. Destroyed by an earthquake in the 10th century, its ruins were added to the UNESCO World Heritage List in 2000.</p>
<p>The name is linked to the word “zvart”, meaning joyful or bright, and to the idea of “zvartats” – the heavenly hosts – giving the name a sense of “dwelling place of the angels”. With its circular plan, open colonnades and light filtering from above, the cathedral was designed as a space where architecture and light work together.</p>
<p>Even in ruins the feeling of that original ambition is still very present. The reconstructed outlines of the foundations and the surviving carved blocks give visitors a clear sense of the original volume and grandeur.</p>
<p>The on-site museum preserves carved elements and architectural fragments. Best combined with Etchmiadzin and Hripsime on a single day trip.</p>
<h3>What to See</h3>
<p>Intricate carved decorations, ancient fresco fragments, a circular floor plan, partially reconstructed columns, and panoramic views of Mount Ararat as backdrop.</p>
<h3>How to Get There</h3>
<p>About 20 km from Yerevan, 2 km from Etchmiadzin. Bus toward Etchmiadzin or by car.</p>
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
<h3>Ինչ է սա</h3>
<p>Կասկադը Երևանի ամենաիկոնիկ վայրերից մեկն է՝ սպիտակ կրաքարե հսկայական աստիճանաշարք, որ բացվել է 1980-ականներին ու դեռ ընդլայնվում է։ Տասնամյակների ընթացքում վերածվել է քաղաքի «ննջասենյակի»՝ մարդիկ գալիս են մարզվելու, զբոսնելու ու մայրամուտ դիտելու։</p>
<p>Կասկադի համալիրի ներսում Ճաֆէսճեանի թանգարանն է՝ բացօթյա ու ներքին ժամանակակից արվեստի թանգարան, հսկայական քանդակներով ու տեռասների ու պատկերասրահների ներսում ցուցադրություններով։</p>
<p>Կասկադի ստորոտում Թամանյան հրապարակն է, ուր ժամանակակից քանդակները բաց երկնքի տակ դարձրել են տարածքը քաղաքի ամենասիրված հանդիպման կետերից մեկը։ Ստեղծագործական տնտեսության զարգացողի հետ հրապարակի շուրջ հայտնվել են արտ-կաֆե, ռեստորաններ ու գալերեաներ, ու ամբողջ կոմպլեքսն ավելի կենդանի ու բազմազան է դարձել։</p>
<p>Եթե Երևանում առաջին անգամ ես, Կասկադն ամենալավ վայրերից մեկն է սկսելու. առավոտյան ավելի հանգիստ է ու կատարյալ ամբողջ ճանապարհը վեր բարձրանալու համար, իսկ երեկոյան աստիճաններին նստած մարդկանց, կենդանի երաժշտության ու քաղաքի լույսերի համադրությունն արտացոլում է Երևանի ամենաեռանդուն կողմը։</p>
<h3>Ինչ անել</h3>
<p>Գագաթ բարձրանալ քաղաքի համայնապատկերի համար, Ճաֆէսճեանի թանգարան, բացօթյա քանդակներ, Թամանյանի հուշարձան, երեկոյան զբոսանք լուսավոր Երևանով։</p>
<h3>Ինչպես հասնել</h3>
<p>Քաղաքի կենտրոնում՝ Մոսկովյան 10։ Հեշտ հասանելի ոտքով, տաքսիով կամ ավտոբուսով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Cascade is one of Yerevan's most iconic landmarks — a giant stairway of white limestone opened in the 1980s and still being expanded. Over decades it has become the city's living room — people gather here to exercise, stroll, and watch the sunset.</p>
<p>Inside the Cascade complex is the Cafesjian Museum — an open-air and indoor modern art museum with monumental sculptures lining the terraces and galleries within.</p>
<p>At the bottom, Tamanyan Square has become one of the city's most popular meeting points, with contemporary sculptures under the open sky, art cafés, restaurants and galleries surrounding the area. The whole complex has grown more vibrant and diverse over the years.</p>
<p>If it is your first time in Yerevan, the Cascade is one of the best places to start — in the morning it is quieter and perfect for walking all the way up, while in the evening the combination of people sitting on the steps, live music and city lights captures a lot of what makes Yerevan feel alive.</p>
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
            "static/img/sights/matenadaran_grqer.jpeg",
            "static/img/sights/matenadaran_ners.jpg",
        ],
        "short_hy": "Մատենադարան – հայկական հին ձեռագրերի տուն",
        "short_en": "One of the world's greatest repositories of Armenian manuscripts — a UNESCO Memory of the World site",
        "description_hy": """
<h3>Ինչ է սա</h3>
<p>Մատենադարանը աշխարհի ամենամեծ հնագույն ձեռագրերի պահոցներից մեկն է՝ ավելի քան 23 000 ձեռագիր ու 500 000 պատմական փաստաթուղթ։ 1997 թ. ի վեր գտնվում է ՅՈՒՆԵՍԿՕ-ի «Աշխարհի հիշողություն» ծրագրի ցուցակում։</p>
<p>Շենքը կառուցվել է 1959 թ.՝ Արարատ լեռի ֆոնին, Սովետական դասական ճարտարապետության գլուխգործոց, ու ճակատից ողջունում է Մեսրոպ Մաշտոցի պատկերավոր արձանը։ Մաշտոցյան պողոտայի վերջում ու Երևանի կենտրոնում գտնվելով, Մատենադարանն ու Մաշտոցի արձանն արդեն ինքնին Երևանի ամենաճանաչելի տեսարժան վայրն են։</p>
<p>Ցուցադրությունն ընդգրկում է V դ. Ավետարաններ, մանրանկարչություն, հայոց այբուբենի ստեղծումը ցույց տվող ձեռագրեր ու ՅՈՒՆԵՍԿՕ-ի պտտվող ցուցադրություններ։ Ձեռագրերից շատերն անցել են պատերազմների, հրդեհների ու երկար ճամփորդությունների միջով ու հիմա պահվում են մանրամասն պատմություններով, թե ինչպես են փրկվել։</p>
<p>Եթե հետաքրքրված ես պատմությամբ, լեզվով կամ ուղղակի ուզում ես հասկանալ, թե ինչու հայոց այբուբենն ինքնության այդքան կարևոր մաս է, Մատենադարանն անփոխարինելի կանգառ է Երևանում։</p>
<h3>Ինչ տեսնել</h3>
<p>V դ. Ավետարաններ, մանրանկարչություն, հայոց այբուբենի ստեղծման ձեռագրեր, ՅՈՒՆԵՍԿՕ-ի ցուցադրություններ։</p>
<h3>Շրջայցեր</h3>
<p>Հայերեն, անգլերեն ու ռուսերեն ուղեկցված շրջայցեր։ Կանխավ ամրագրելը խորհուրդ է տրվում՝ +374 10-56-25-78 կամ օնլայն։</p>
<h3>Ինչպես հասնել</h3>
<p>Քաղաքի կենտրոնում՝ Մաշտոցի պողոտա 53։ Երիտասարդական մետրոյի կայարանից 10 րոպե ոտքով։</p>
""",
        "description_en": """
<h3>What Is It</h3>
<p>The Matenadaran is one of the world's greatest repositories of ancient manuscripts — over 23,000 manuscripts and 500,000 historical documents. It has been on UNESCO's Memory of the World register since 1997.</p>
<p>The building was constructed in 1959 against the backdrop of Mount Ararat — a masterpiece of Soviet classical architecture, fronted by the iconic statue of Mesrop Mashtots. Standing at the top of Mashtots Avenue, the building and statue are already among Yerevan's most recognisable landmarks.</p>
<p>The main exhibition halls show 5th-century Gospels, miniature paintings, manuscripts showing the invention of the Armenian alphabet, and rotating UNESCO exhibits. Many manuscripts survived wars, fires and long journeys and are now preserved here with detailed stories about how they were saved.</p>
<p>If you are interested in history, language or just want to understand why the Armenian alphabet is such an important part of identity here, Matenadaran is an essential stop in Yerevan. It works equally well as a deep dive with a guided tour or as a shorter visit to walk through the main halls and feel the atmosphere of a house built for books.</p>
<h3>Tours</h3>
<p>Guided tours available in Armenian, English and Russian. Pre-booking recommended — +374 10-56-25-78 or online.</p>
<h3>How to Get There</h3>
<p>City centre at 53 Mashtots
    },
]
