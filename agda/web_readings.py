"""Contextual bibliography, kept separate from formal claim statuses.

A reading is not evidence of influence unless the author has said so. Historical
sources, comparisons, empirical studies, objections, and fictional imagery have
separate labels. Missing URLs are intentional: never invent a source link.
"""

KINDS = {
    'tradition': ('Традиция', 'Tradition'),
    'context': ('Контекст', 'Context'),
    'parallel': ('Параллель', 'Parallel'),
    'study': ('Исследование', 'Study'),
    'critique': ('Возражение / граница', 'Objection / limit'),
    'image': ('Источник образов', 'Imagery'),
}

CATALOG = {}
CONNECTIONS = {}


def reading(key, sections, title, kind, ru, en, href=None):
    if key in CATALOG or kind not in KINDS:
        raise ValueError(f'Invalid reading: {key}')
    CATALOG[key] = dict(id=key, title=title, kind=kind, ru=ru, en=en)
    if href:
        CATALOG[key]['href'] = href
    for section in sections:
        CONNECTIONS.setdefault(str(section), []).append(key)


reading('tattvartha', [8, 9, 11, 28, 31, 'sadhana'],
    'Umāsvāti. Tattvārtha Sūtra / That Which Is, trans. Nathmal Tatia (1994; Yale reissue 2011)', 'tradition',
    'Гл. 6: приток со страстью и без неё; 8.1: пять причин связывания. Кармическая материя и освобождение здесь принадлежат джайнскому учению. Книга переосмысляет их через Русло и возвращение к жизни.',
    'Chapter 6 distinguishes influx with and without passion; 8.1 names five causes of bondage. Karmic matter and liberation belong to Jain doctrine. The treatise reworks them through the Riverbed and renewed life.',
    'https://yalebooks.co.uk/book/9780300165296/that-which-is/')
reading('dundas', [1, 8, 28, 30, 31, 'sadhana'],
    'Paul Dundas. The Jains, 2nd ed. (Routledge, 2002)', 'context',
    'История, многообразие общин, аскетическая и мирская жизнь. Позволяет различить исторический джайнизм и самостоятельную космологию этой книги.',
    'History, diverse communities, ascetic and lay life. A way to distinguish historical Jainism from this book’s independent cosmology.',
    'https://www.routledge.com/The-Jains/Dundas/p/book/9780415266062')
reading('jaini', [8, 13, 28, 29, 31, 37, 'sadhana'],
    'Padmanabh S. Jaini. The Jaina Path of Purification (1979)', 'context',
    'Джива, карма, обеты, очищение и освобождение. Особенно важен контраст: сиддха в классическом учении освобождена от воплощений, а здесь имя получает иной смысл.',
    'Jiva, karma, vows, purification, and liberation. The contrast matters: the classical siddha is free from rebirth, whereas this book gives the name a different meaning.')
reading('long', [8, 28, 'sadhana'],
    'Jeffery D. Long. Jainism: An Introduction (2009)', 'context',
    'Введение в историю, философию и практику джайнизма; ориентир для терминов, а не подтверждение всех их авторских переосмыслений.',
    'An introduction to Jain history, philosophy, and practice: orientation for the vocabulary, not endorsement of every authorial reinterpretation.')
reading('matilal', [4, 17, 35],
    'Bimal Krishna Matilal. The Central Philosophy of Jainism (Anekāntavāda) (1981)', 'context',
    'Многосторонность и обусловленное высказывание. Сьядвада не означает, что любые несовместимые ответы одинаково верны: важно, с какой стороны и при каких условиях сказано.',
    'Many-sidedness and conditional predication. Syadvada does not make every incompatible answer equally true: standpoint and conditions matter.',
    'https://jainqq.org/explore/001129/1')
reading('chapple', [29, 33],
    'Christopher Key Chapple. Nonviolence to Animals, Earth, and Self in Asian Traditions (SUNY, 1993)', 'context',
    'Ахимса в отношениях с животными, землёй и собой. Этический и исторический контекст; не свидетельство физиологической невозможности причинить вред.',
    'Ahimsa toward animals, earth, and oneself. Ethical and historical context, not evidence that inflicting harm becomes physiologically impossible.',
    'https://digitalcommons.lmu.edu/theo_fac/64/')
reading('guseva', [8, 28, 'sadhana'],
    'Н. Р. Гусева. Джайнизм (Наука, 1968)', 'context',
    'Русскоязычное историческое введение. Его время и исследовательская перспектива отличаются от позднейших работ по джайнизму.',
    'A Russian-language historical introduction. Its period and scholarly perspective differ from later Jain studies.')
reading('shah', [28, 31],
    'Natubhai Shah. Jainism: The World of Conquerors (1998)', 'context',
    'Широкая картина учения и жизни общин; дополнительное чтение рядом с Джайни и Дандасом.',
    'A broad account of doctrine and communal life; further reading alongside Jaini and Dundas.')
reading('triadic-heart', [14],
    'Paul E. Muller-Ortega. The Triadic Heart of Śiva (SUNY, 1989)', 'context',
    'Сердце в недвойственном шиваизме Кашмира. Это контекст имени Хридаи; мистическое сердце книги не тождественно целой системе Абхинавагупты.',
    'The heart in nondual Kashmir Shaivism. Context for Hridaya’s name; this book’s mystical heart is not identical with Abhinavagupta’s entire system.')
reading('spanda', [6, 14],
    'Mark S. G. Dyczkowski. The Doctrine of Vibration (SUNY, 1987); Jaideva Singh. Spanda-Kārikās (1980)', 'context',
    'Спанда как пульсация и проявление сознания. Сопоставление с Шакти не превращает метафизическую пульсацию в измеримую физическую частоту.',
    'Spanda as pulsation and manifestation of consciousness. Comparing it with Shakti does not turn metaphysical pulsation into a measurable physical frequency.',
    'https://doi.org/10.1515/9781438401744')
reading('recognition-heart', [14, 22],
    'Jaideva Singh. Pratyabhijñāhṛdayam (1963)', 'parallel',
    'Узнавание и сердце в кашмирском шиваизме. Параллель к узнаванию своего движения, а не основание считать традиции одним учением.',
    'Recognition and the heart in Kashmir Shaivism. A comparison for recognizing one’s movement, not grounds for treating the traditions as one doctrine.')
reading('garfield', [5],
    'Jay L. Garfield. The Fundamental Wisdom of the Middle Way (Oxford, 1995)', 'critique',
    'Мадхьямака критикует свабхаву как независимую самосущую природу. Свабхава книги означает собственное движение; совпадение слова не устраняет различия учений.',
    'Madhyamaka criticizes svabhava as independent intrinsic existence. Here Svabhava names one’s own movement; a shared word does not erase doctrinal differences.',
    'https://doi.org/10.1093/oso/9780195103175.001.0001')
reading('tambiah', [32, 39],
    'Stanley J. Tambiah. World Conqueror and World Renouncer (Cambridge, 1976)', 'context',
    'Буддийская царская власть и отречение в тайском историческом контексте. Чакравартин и колесо здесь помогают увидеть масштаб авторского переворота образа властителя.',
    'Buddhist kingship and renunciation in Thai historical context. The wheel-turning ruler helps reveal the scale of this book’s reversal of sovereign imagery.',
    'https://www.cambridge.org/core/books/world-conqueror-and-world-renouncer/234CDB8B861966ABDEAC394C5A8A76A1')
reading('yoga-sutras', [13, 36, 'sadhana'],
    'Edwin F. Bryant. The Yoga Sūtras of Patañjali (2009)', 'parallel',
    'Дисциплина внимания, практика и освобождение в классической йоге. Параллель к работе пути, не историческое происхождение квадробики.',
    'Attention, practice, and liberation in classical yoga. A comparison for discipline, not a historical origin of quadrobics.')
reading('modern-yoga', [18, 20, 36, 'sadhana'],
    'Mark Singleton. Yoga Body (Oxford, 2010); Joseph S. Alter. Yoga in Modern India (2004)', 'context',
    'История современных телесных практик: форма, которую принимают за вневременную, складывается в определённых общественных условиях. Квадробика здесь - самостоятельный выбор пути.',
    'Histories of modern bodily practices: supposedly timeless forms develop under particular social conditions. Quadrobics here is an independent choice of practice.')
reading('raft', [1, 'conclusion'],
    'Alagaddūpama Sutta, MN 22, trans. Ñāṇamoli & Bodhi, The Middle Length Discourses (1995)', 'parallel',
    'Образ плота: учение служит переправе, а не становится ношей после неё. Параллель к книге как раме вокруг двери.',
    'The raft serves a crossing rather than becoming a burden afterward. A comparison for the book as a frame around a door.',
    'https://wisdomexperience.org/ebook/the-middle-length-discourses-of-the-buddha/contents/')
reading('zhuangzi', [1, 'conclusion'],
    'Zhuangzi, ch. 26, trans. Burton Watson', 'parallel',
    'Ловушка нужна ради рыбы, слова - ради смысла. Родственный жест освобождения от средства, когда оно уже исполнило работу.',
    'The trap serves the fish, words serve meaning. A related gesture of releasing a means once it has done its work.')
reading('ladder', [1, 'conclusion'],
    'Ludwig Wittgenstein. Tractatus Logico-Philosophicus, 6.54, 7 (1921)', 'parallel',
    'Лестница, которую отбрасывают, поднявшись по ней, и граница высказывания. Философская параллель, не тождество апофатик.',
    'The ladder discarded after climbing and the limit of saying. A philosophical comparison, not an identity between apophatic teachings.')
reading('heraclitus', [1, 3, 7],
    'Charles H. Kahn. The Art and Thought of Heraclitus (1979)', 'parallel',
    'Единство перемены и устойчивости, речной образ. Историческое чтение Гераклита не сводится к лозунгу о всеобщем хаосе.',
    'Change, persistence, and river imagery. A historical reading of Heraclitus is more than a slogan about universal chaos.')
reading('conatus', [6],
    'Baruch Spinoza. Ethics, III, propositions 6–7 (1677)', 'parallel',
    'Конатус: стремление вещи сохранять своё бытие. Родство с волей к жизни не означает совпадения с Шакти или морального оправдания любого желания.',
    'Conatus: a thing’s striving to persist in being. Affinity with the will to life implies neither identity with Shakti nor moral approval of every desire.')
reading('schopenhauer', [6, 27],
    'Arthur Schopenhauer. The World as Will and Representation (1818/1819)', 'critique',
    'Воля, страдание и отрицание воли. Важный собеседник именно в расхождении: книга выбирает новое движение жизни, не объявляя страдание его целью.',
    'Will, suffering, and denial of the will. A significant interlocutor through disagreement: this book chooses renewed life without making suffering its purpose.')
reading('bergson', [3, 6],
    'Henri Bergson. Creative Evolution (1907)', 'parallel',
    'Творчество живого и новизна длительности. Философская параллель, не современная биологическая проверка жизненного порыва.',
    'Living creativity and novelty in duration. A philosophical comparison, not contemporary biological validation of a vital impulse.')
reading('whitehead', [1, 2, 8],
    'Alfred North Whitehead. Process and Reality (1929)', 'parallel',
    'Событие и становление вместо первенства неподвижной вещи. Процессуальная метафизика даёт собеседника, но не доказательство Истока.',
    'Events and becoming rather than the primacy of static things. Process metaphysics offers an interlocutor, not proof of the Source.')
reading('lossky', [1],
    'В. Н. Лосский. Очерк мистического богословия Восточной Церкви (1944)', 'parallel',
    'Апофатическое богословие: отрицание не исчерпывает непостижимого. Христианский богословский контекст отличается от безличного Истока этой книги.',
    'Apophatic theology: negation does not exhaust the incomprehensible. Its Christian theological setting differs from this book’s impersonal Source.')
reading('tao', [3, 6, 36],
    'Ursula K. Le Guin. Tao Te Ching: A Book About the Way and the Power of the Way (1997)', 'parallel',
    'Путь, вода и действие без насилия над ходом вещей. Литературное переложение Лао-цзы; его не следует принимать за единственный перевод традиции.',
    'The way, water, and action without forcing the course of things. A literary rendering of Laozi, not the tradition’s sole translation.')
reading('schrodinger', [6],
    'Erwin Schrödinger. What Is Life? (1944)', 'parallel',
    'Физический вопрос об устойчивости живого. Исторический мост между жизнью и порядком, не отождествление термодинамики с волей.',
    'A physical inquiry into the persistence of life. A historical bridge between life and order, not an identification of thermodynamics with will.')
reading('prigogine', [2],
    'Ilya Prigogine & Isabelle Stengers. Order Out of Chaos (1984)', 'parallel',
    'Диссипативные структуры сохраняются благодаря обмену и потоку. Это точка сравнения с пламенем; кристалл не становится от этого физически мёртвым или злым.',
    'Dissipative structures persist through exchange and flow. A comparison for flame; crystals do not thereby become physically dead or evil.')
reading('autopoiesis', [10],
    'Humberto Maturana & Francisco Varela. Autopoiesis and Cognition (1980); Evan Thompson. Mind in Life (2007)', 'parallel',
    'Живое поддерживает собственную организацию и границу. Такой край не равен психологической стене; сходство не доказывает устройство поля страха.',
    'Living systems sustain their organization and boundary. Such a boundary differs from a psychological wall; the comparison does not prove the fear field’s structure.')
reading('england', [6],
    'Jeremy L. England. Statistical Physics of Self-Replication (J. Chem. Phys. 139, 2013)', 'study',
    'Термодинамические ограничения самовоспроизведения при заданных предпосылках. Из них не следует желание материи жить или необходимость духовного пути.',
    'Thermodynamic constraints on self-replication under specified assumptions. They entail neither matter’s desire to live nor the necessity of a spiritual path.',
    'https://arxiv.org/abs/1209.1179')
reading('kauffman', [2, 6],
    'Stuart Kauffman. At Home in the Universe (1995)', 'parallel',
    'Самоорганизация и возникновение порядка в сложных системах. Параллель к рождению формы, не физическая биография Истока.',
    'Self-organization and emerging order in complex systems. A comparison for form’s emergence, not a physical biography of the Source.')
reading('dyson', [27],
    'Freeman J. Dyson. Time without End: Physics and Biology in an Open Universe (Rev. Mod. Phys. 51, 1979)', 'critique',
    'Условное рассуждение о далёком будущем жизни в открытой Вселенной. Это историческая космологическая модель, а не установленный окончательный сценарий и не доказательство бессмертия.',
    'A conditional account of life’s far future in an open universe. A historical cosmological model, not an established final scenario or proof of immortality.',
    'https://doi.org/10.1103/RevModPhys.51.447')
reading('stellar-elements', [39],
    'E. M. Burbidge, G. R. Burbidge, W. A. Fowler & F. Hoyle. Synthesis of the Elements in Stars (Rev. Mod. Phys. 29, 1957); Carl Sagan. Cosmos (1980)', 'context',
    'Звёздный нуклеосинтез даёт физическую опору образам углерода, кальция и железа. Не всё вещество тела возникло в звёздах: значительная часть водорода первична. Исход круга отсюда не выводится.',
    'Stellar nucleosynthesis grounds the imagery of carbon, calcium, and iron. Not all bodily matter originated in stars: much hydrogen is primordial. The circle’s outcome does not follow from this.',
    'https://doi.org/10.1103/RevModPhys.29.547')
reading('rovelli', [4],
    'Carlo Rovelli. Relational Quantum Mechanics (1996); Helgoland (2020)', 'parallel',
    'Относительность квантового описания к взаимодействующей системе. Это не сьядвада и не доказательство зависимости физической реальности от человеческого мнения.',
    'Quantum descriptions relative to interacting systems. This is neither syadvada nor proof that physical reality depends on human opinion.',
    'https://arxiv.org/abs/quant-ph/9609002')
reading('shubin', [19, 25],
    'Neil Shubin. Your Inner Fish (2008)', 'context',
    'Общая эволюционная история тел и конечностей. Она не подтверждает память прошлых воплощений или существование конкретного внутреннего зверя.',
    'The shared evolutionary history of bodies and limbs. It does not establish memories of past lives or a particular inner beast.')
reading('jung-shadow', [21, 23, 24],
    'C. G. Jung. Aion (CW 9ii, ch. II); Two Essays on Analytical Psychology (CW 7)', 'context',
    'Тень и персона - важный контекст авторского замысла. Тень не состоит только из злого; различение зверя и тени здесь остаётся собственным решением книги.',
    'Shadow and persona are important context for the author’s project. The shadow is not only evil; distinguishing beast from shadow remains this book’s own choice.',
    'https://iaap.org/resources/academic-resources/collected-works-abstracts/volume-9-2-aion-researches-phenomenology-self/')
reading('jung-further', [23, 26],
    'C. G. Jung. The Archetypes and the Collective Unconscious (CW 9i); Answer to Job (CW 11); Man and His Symbols (1964); Memories, Dreams, Reflections (1962/1963)', 'parallel',
    'Архетипы, символ и работа с отвергнутым. Это историческая психологическая и мифопоэтическая перспектива, не доказательство буквальной памяти звериных жизней.',
    'Archetypes, symbols, and engagement with what was rejected. A historical psychological and mythopoetic perspective, not proof of literal memories of animal lives.')
reading('shadow-readings', [23],
    'Robert Bly. A Little Book on the Human Shadow (1988); Connie Zweig & Jeremiah Abrams, eds. Meeting the Shadow (1991); Robert A. Johnson. Owning Your Own Shadow (1991)', 'parallel',
    'Разные способы говорить о признании тени. Популярные и терапевтические разработки юнгианской мысли; ни одна не даёт права исполнять всякое найденное побуждение.',
    'Ways of describing acknowledgment of the shadow. Popular and therapeutic developments of Jungian thought; none licenses acting on every discovered impulse.')
reading('von-franz-stein', [23, 26],
    'Marie-Louise von Franz. Shadow and Evil in Fairy Tales (1974); Murray Stein. Jung’s Map of the Soul (1998)', 'parallel',
    'Сказка как поле различения тени и разрушительного действия; карта юнгианских понятий для дальнейшего чтения.',
    'Fairy tales as a setting for distinguishing shadow from destructive action; a map of Jungian concepts for further reading.')
reading('jung-criticism', [21, 23],
    'Sonu Shamdasani. Jung and the Making of Modern Psychology (2003); Richard Noll. The Jung Cult (1994)', 'critique',
    'Исторический анализ и спорная критическая интерпретация. Эти книги не равнозначны по подходу и выводам; они помогают не выдавать юнгианские понятия за бесспорные экспериментальные факты.',
    'Historical analysis and a contested critical interpretation. Their approaches and conclusions differ; they help prevent presenting Jungian concepts as uncontested experimental facts.')
reading('winnicott', [20, 22],
    'D. W. Winnicott. Ego Distortion in Terms of True and False Self (1960)', 'context',
    'Ложное я как организация приспособления к требованиям окружения. Клинический собеседник маски; ложное я не означает просто ложь, а истинное я не тождественно Свабхаве.',
    'The false self as an organization of compliance with the environment. A clinical interlocutor for the mask; false self does not simply mean lying, nor true self Svabhava.',
    'https://doi.org/10.1093/med:psych/9780190271381.003.0023')
reading('goffman', [10, 20, 22],
    'Erving Goffman. The Presentation of Self in Everyday Life (1959)', 'parallel',
    'Представление себя во встрече. Социальная роль сама по себе не ложь и не болезнь; различение книги касается её затвердевания и права её менять.',
    'Presenting oneself in encounters. A social role is not inherently a lie or illness; the book asks about its hardening and the right to change it.')
reading('looking-glass', [10, 22],
    'Charles H. Cooley. Human Nature and the Social Order (1902); Jean-Paul Sartre. Being and Nothingness (1943)', 'parallel',
    'Зеркальное я и чужой взгляд. Здесь сопоставлены разные объяснения того, как другой участвует в отношении к себе; они не образуют единой психологической теории.',
    'The looking-glass self and the other’s gaze. Distinct accounts of how others enter self-relation, not a single psychological theory.')
reading('perls', [22],
    'Fritz Perls, Ralph Hefferline & Paul Goodman. Gestalt Therapy (1951)', 'context',
    'Интроекция: проглоченное, но не усвоенное. Ссылка ведёт к предисловиям и контексту книги; это клиническая метафора, не экспериментальная проверка §22.',
    'Introjection: swallowing without assimilation. The link supplies introductions and context; this is a clinical metaphor, not an experimental test of §22.',
    'https://gestalt.org/phgintro.htm')
reading('rogers', [14, 22],
    'Carl R. Rogers. On Becoming a Person (1961)', 'parallel',
    'Конгруэнтность и отношение, в котором возможно слышать себя. Самоузнавание не даёт другому права окончательно назвать Дживу.',
    'Congruence and a relationship in which one can hear oneself. Self-recognition gives no other person the right to define the jiva finally.')
reading('gendlin', [14, 16],
    'Eugene T. Gendlin. Focusing (1978)', 'parallel',
    'Телесно ощущаемый смысл ещё не найденных слов. Параллель к слушанию, не отождествление felt sense с мистическим сердцем и не правило безошибочности ощущений.',
    'A bodily felt sense before words are found. A comparison for listening, not an identification with the mystical heart or a rule that sensations cannot mislead.')
reading('reich', [18],
    'Wilhelm Reich. Character Analysis (1933)', 'critique',
    'Исторический образ характерного и телесного панциря. Его нельзя принимать за установленную физиологию или переносить сюда позднейшие представления об оргоне.',
    'A historical account of character and bodily armor. It must not be treated as established physiology or used to import later claims about orgone.')
reading('lieberman', [16, 22],
    'Matthew D. Lieberman et al. Putting Feelings into Words (Psychological Science 18, 2007)', 'study',
    'Называние эмоций сопровождалось меньшей реакцией миндалины на эмоциональные изображения. Это не универсальное обещание субъективного облегчения и не доказательство исцеления чужими словами.',
    'Labeling emotions was associated with lower amygdala responses to emotional images. This promises neither universal subjective relief nor healing through another’s words.',
    'https://sanlab.psych.ucla.edu/wp-content/uploads/sites/31/2016/03/Lieberman_2007_PsychScience.pdf')
reading('wegner', [21],
    'Daniel M. Wegner et al. Paradoxical Effects of Thought Suppression (1987); Wegner. Ironic Processes of Mental Control (1994)', 'study',
    'Подавление мысли способно усилить её возвращение при определённых условиях. Эксперименты не доказывают, что всякое вытесненное содержание непременно вернётся или говорит истину.',
    'Thought suppression can increase its return under particular conditions. These experiments do not prove that every rejected content must return or speaks the truth.',
    'https://dtg.sites.fas.harvard.edu/DANWEGNER/pub/Wegner%2CSchneider%2CCarter%2C%26White%201987.pdf')
reading('gross', [21],
    'James J. Gross. The Emerging Field of Emotion Regulation (1998); Gross & Robert W. Levenson. Emotional Suppression (1993)', 'study',
    'Скрыть выражение, изменить переживание и изменить физиологическую реакцию - разные задачи. Внешняя неподвижность не удостоверяет внутренней тишины.',
    'Hiding expression, changing experience, and changing physiological response are distinct tasks. Outward stillness does not certify inward quiet.')
reading('act', [13, 'sadhana'],
    'Steven C. Hayes, Kirk D. Strosahl & Kelly G. Wilson. Acceptance and Commitment Therapy (1999; 2nd ed. 2012)', 'parallel',
    'Принятие переживания не требует исполнять его требование: действие можно выбирать по ценностям. Это терапевтическая параллель, не обоснование метафизики книги.',
    'Accepting an experience need not mean obeying its demand: action can follow values. A therapeutic comparison, not support for the book’s metaphysics.')
reading('mindfulness', ['sadhana'],
    'Jon Kabat-Zinn. Full Catastrophe Living (1990); Kristin Neff. Self-Compassion (Self and Identity 2, 2003)', 'parallel',
    'Внимание и отношение к собственной трудности без самоприговора. Современные практики сопоставлены с Самайикой и Кайотсаргой, не объявлены их источником или заменой.',
    'Attention and responding to one’s difficulty without self-condemnation. Modern practices are compared with Samayika and Kayotsarga, not presented as their origin or replacement.')
reading('ryan-connell', [22],
    'Richard M. Ryan & James P. Connell. Perceived Locus of Causality and Internalization (JPSP 57, 1989)', 'study',
    'Различение причин действия: внешнее давление, внутреннее принуждение, признанная ценность. Помогает уточнить зависимость от одобрения; не устанавливает срок жизни заёмной формы.',
    'Distinguishes reasons for action: external pressure, internal coercion, and an endorsed value. It clarifies approval dependence without setting an expiry date for borrowed forms.',
    'https://selfdeterminationtheory.org/SDT/documents/1989_RyanConnell.pdf')
reading('deci-1994', [22],
    'Edward L. Deci, Haleh Eghrari, Brian C. Patrick & Dean R. Leone. Facilitating Internalization (1994)', 'study',
    'Исследование условий усвоения: понятный смысл действия, признание чувств и возможность выбора. Заимствованное способно стать своим; интроекция не обязана исчезнуть от течения времени.',
    'Studies conditions of internalization: meaningful rationale, acknowledging feelings, and choice. What is borrowed can become one’s own; introjection need not disappear with time.',
    'https://selfdeterminationtheory.org/SDT/documents/1994_DeciEghrariPatLeone.pdf')
reading('sdt', [22],
    'Edward L. Deci & Richard M. Ryan. The “What” and “Why” of Goal Pursuits (2000); Ryan & Deci. Self-Determination Theory (2017)', 'context',
    'Интроецированная и интегрированная регуляция различаются способом принятия, а не тем, впервые ли мысль появилась у самой Дживы. Автономия не равна изоляции.',
    'Introjected and integrated regulation differ in how something is endorsed, not whether the jiva first invented it. Autonomy does not mean isolation.')
reading('closure', [22],
    'Arie W. Kruglanski & Donna M. Webster. Motivated Closing of the Mind: “Seizing” and “Freezing” (1996)', 'context',
    'Поспешное принятие и удержание ответа при потребности в определённости. Сходство слов с хваткой и льдом - продуктивная параллель, не тождество механизмов и не диагноз страдающему.',
    'Urgently adopting and preserving an answer under need for closure. The vocabulary’s affinity with grip and ice is a comparison, not an identity of mechanisms or a diagnosis of suffering.',
    'https://fitelson.org/current/seizing.pdf')
reading('bowlby', [12, 22],
    'John Bowlby. A Secure Base (1988)', 'parallel',
    'Надёжная опора позволяет исследовать мир, не предписывая каждый шаг. Параллель к помощи спутника; не всякая зависимость от другого становится захватом.',
    'A secure base enables exploration without prescribing every step. A comparison for companionship; dependence on another is not always captivity.')
reading('merleau-ponty', [18, 19],
    'Maurice Merleau-Ponty. Phenomenology of Perception (1945)', 'parallel',
    'Тело как способ быть в мире и начало пространственной ориентации. Это философское описание, не экспериментальное доказательство действия четырёх опор.',
    'The body as a way of being in the world and the basis of spatial orientation. A philosophical account, not experimental proof of four-support practice.')
reading('vertical-metaphor', [19],
    'George Lakoff & Mark Johnson. Metaphors We Live By (1980)', 'parallel',
    'Пространственные метафоры власти и положения. Связь верха с контролем усваивается в опыте; сама вертикаль не делает тело властителем.',
    'Spatial metaphors of power and position. Associations of height with control are learned in experience; standing upright does not itself make a ruler.')
reading('schubert', [19],
    'Thomas W. Schubert. Your Highness: Vertical Positions as Perceptual Symbols of Power (JPSP 89, 2005); Steffen R. Giessner & Schubert. High in the Hierarchy (2007)', 'study',
    'Связь вертикального расположения с суждениями о власти в экспериментальных задачах. Из неё не следует, что наклон головы устраняет власть или четырёхопорная поза меняет личность.',
    'Vertical position and judgments of power in experimental tasks. This does not imply that bowing removes power or four-support posture changes personality.',
    'https://www.igroup.org/schubert/papers/schubert_jpsp05.pdf')
reading('grounded-cognition', [18, 20],
    'Paula M. Niedenthal. Embodying Emotion (Science 316, 2007); Lawrence W. Barsalou. Grounded Cognition (2008)', 'context',
    'Обзоры участия восприятия и действия в эмоциях и мышлении. Общая рамка не удостоверяет любую телесную практику и не делает метафору буквальной анатомией.',
    'Reviews of perception and action in emotion and cognition. A general framework does not validate every bodily practice or turn metaphor into literal anatomy.')
reading('body-order', [18],
    'Marcel Mauss. Techniques of the Body (1935); Pierre Bourdieu. The Logic of Practice (1980); Michel Foucault. Discipline and Punish (1975)', 'context',
    'Обученные способы держаться, габитус и дисциплина тел. Разные общественные механизмы помогают прочесть «порядок записан в теле», не сводя каждую привычку к подавлению.',
    'Learned bodily techniques, habitus, and bodily discipline. Distinct social accounts illuminate “order written into the body” without reducing every habit to repression.')
reading('movement-learning', [20, 'sadhana'],
    'Moshe Feldenkrais. Awareness Through Movement (1972); F. M. Alexander. The Use of the Self (1932)', 'parallel',
    'Замечать привычное движение и пробовать другое. Исторические практические сопоставления; не доказательство терапевтической эффективности квадробики.',
    'Noticing familiar movement and trying alternatives. Historical practical comparisons, not proof of quadrobics’ therapeutic efficacy.')
reading('bakhtin', [18, 20],
    'М. М. Бахтин. Творчество Франсуа Рабле и народная культура средневековья и Ренессанса (1965)', 'parallel',
    'Карнавал и материально-телесный низ как переворот официальной высоты. Литературная параллель, не теория лечебной позы.',
    'Carnival and the material bodily lower stratum as a reversal of official height. A literary comparison, not a theory of therapeutic posture.')
reading('posture-limits', [19, 20],
    'Eva Ranehill et al. Assessing the Robustness of Power Posing (2015)', 'critique',
    'Репликация не воспроизвела заявленные гормональные эффекты и склонность к риску, хотя самоощущение власти изменилось. Это ограничивает сильные обещания о позах, но не доказывает отсутствие любых телесных эффектов.',
    'The replication did not reproduce claimed hormonal or risk-taking effects, though felt power changed. This limits strong posture claims without disproving every bodily effect.',
    'https://www.zne.uzh.ch/dam/jcr%3Ae5fc4c3c-d50e-4aa9-96ab-4389e426d20d/%20Psychological%20Science-2015-Ranehill-0956797614553946.pdf')
reading('facial-limits', [20],
    'E.-J. Wagenmakers et al. Registered Replication Report: Strack, Martin, & Stepper (1988) (2016)', 'critique',
    'Многоцентровая репликация не воспроизвела конкретный эффект мимической обратной связи. Она не исследовала маски квадробики и не даёт ни подтверждения, ни опровержения её полного замысла.',
    'A multilab replication did not reproduce a particular facial-feedback effect. It did not study quadrobic masks and neither validates nor refutes the whole practice.',
    'https://doi.org/10.1177/1745691616674458')
reading('trauma-books', [18],
    'Bessel van der Kolk. The Body Keeps the Score (2014); Peter A. Levine. Waking the Tiger (1997)', 'critique',
    'Популярные клинические рассказы о теле и травме. По их образам нельзя заключать, что воспоминание буквально хранится в определённой мышце; выводы и методы требуют отдельной оценки.',
    'Popular clinical accounts of body and trauma. Their imagery does not establish that a memory is literally stored in a particular muscle; claims and methods need separate evaluation.')
reading('totemism', [24, 26],
    'Claude Lévi-Strauss. Totemism (1962); Émile Durkheim. The Elementary Forms of Religious Life (1912)', 'context',
    'Тотем, классификация и общность в разных антропологических объяснениях. Внутренний зверь этой книги не обозначает любую тотемическую традицию.',
    'Totem, classification, and community in distinct anthropological accounts. This book’s inner beast does not stand for every totemic tradition.')
reading('descola-viveiros', [24],
    'Philippe Descola. Beyond Nature and Culture (2005); Eduardo Viveiros de Castro. Cosmological Deixis and Amerindian Perspectivism (1998)', 'parallel',
    'Разные способы различать человеческое и нечеловеческое. Сопоставление не превращает конкретные культуры в свидетельства универсального учения о внутренних зверях.',
    'Different ways of distinguishing human and nonhuman. Comparison does not turn particular cultures into witnesses for a universal doctrine of inner beasts.')
reading('ingold-harvey', [25],
    'Tim Ingold. The Perception of the Environment (2000); Graham Harvey. Animism (2005)', 'parallel',
    'Навык, среда и отношения с нечеловеческими существами. Слушание зверя сопоставляется с отношением, а не с присвоением чужой культуры.',
    'Skill, environment, and relations with nonhuman beings. Listening to the beast is compared with relationship, not appropriation of another culture.')
reading('eliade', [24, 26],
    'Mircea Eliade. Shamanism: Archaic Techniques of Ecstasy (1951)', 'context',
    'Исторически влиятельная сравнительная схема. Её обобщения не заменяют различий между традициями и не удостоверяют переживания практикующего.',
    'A historically influential comparative scheme. Its generalizations do not replace differences between traditions or certify a practitioner’s experiences.')
reading('nagel', [24],
    'Thomas Nagel. What Is It Like to Be a Bat? (1974)', 'critique',
    'Предел доступа к чужому опыту. Представить зверя изнутри не значит доказать, что переживаешь именно то, что переживает другое животное.',
    'Limits of access to another’s experience. Imagining a beast from within does not establish that one experiences what another animal experiences.')
reading('animal-encounters', [24, 29],
    'Donna Haraway. When Species Meet (2008); Jacques Derrida. The Animal That Therefore I Am (2006); James Hillman. Animal Presences (2008)', 'parallel',
    'Встреча с животным, взгляд другого и животные образы. Внутреннее узнавание не заменяет внимания к нужде живого существа снаружи.',
    'Encounters with animals, another’s gaze, and animal imagery. Inner recognition does not replace attending to a living creature’s actual needs.')
reading('de-waal', [24, 29],
    'Frans de Waal. Are We Smart Enough to Know How Smart Animals Are? (2016)', 'parallel',
    'Исследование животных требует задач, учитывающих их собственные возможности. Сопоставление с отказом мерить всякую жизнь одной человеческой мерой.',
    'Studying animals requires tasks attentive to their own capacities. A comparison for refusing to measure every life by one human standard.')
reading('animal-identities', [24, 25],
    'Kathleen C. Gerbasi et al. Furries from A to Z (2008); Joseph P. Laycock. We Are Spirits of Another Sort (2012)', 'context',
    'Разные исследования фурри и терианских самоописаний. Эти группы, внутренние звери книги и квадроберы не тождественны; данные об одной группе нельзя переносить на остальные.',
    'Distinct studies of furry and therian self-descriptions. These groups, the book’s inner beasts, and quadrobers are not identical; findings cannot simply transfer between them.')
reading('ritual-process', [30, 38, 'sadhana'],
    'Arnold van Gennep. The Rites of Passage (1909); Victor Turner. The Ritual Process (1969)', 'context',
    'Порог, переход и коммунитас помогают прочесть Час Растворения. Общий порог не гарантирует равенства после него и не описывает всякий ритуал одинаково.',
    'Threshold, transition, and communitas illuminate the Hour of Dissolution. A shared threshold guarantees neither equality afterward nor a single account of every ritual.')
reading('collective-rhythm', [38, 'sadhana'],
    'Barbara Ehrenreich. Dancing in the Streets (2006); William H. McNeill. Keeping Together in Time (1995)', 'context',
    'Совместное движение, ритм и общность в истории. Один ритм способен связывать людей; это ещё не определяет, чему служит возникшая связь.',
    'Shared movement, rhythm, and community in history. One rhythm can bind people without determining what the resulting bond serves.')
reading('synchrony', [30, 38],
    'Scott S. Wiltermuth & Chip Heath. Synchrony and Cooperation (2009); Michael J. Hove & Jane L. Risen. It’s All in the Timing (2009)', 'study',
    'В исследованных задачах совместный ритм связан с сотрудничеством и расположением. Отсюда не следуют нравственная правота группы или безопасность растворения в ней.',
    'In the studied tasks, shared timing relates to cooperation and affiliation. Neither the group’s moral rightness nor safety of merging into it follows.',
    'https://www2.psych.ubc.ca/~schaller/Psyc591Readings/WiltermuthHeath2009.pdf')
reading('konvalinka', [38],
    'Ivana Konvalinka et al. Synchronized Arousal between Performers and Related Spectators in a Fire-Walking Ritual (PNAS 108, 2011)', 'study',
    'Динамика сердечного ритма сближалась у участников и связанных с ними зрителей. Это не буквальное слияние сердцебиений в один удар и не опыт квадробического круга.',
    'Heart-rate dynamics showed coupling between performers and related spectators. This is not literal fusion into one heartbeat or a study of a quadrobic circle.',
    'https://pmc.ncbi.nlm.nih.gov/articles/PMC3100954/')
reading('xygalatas', [38],
    'Dimitris Xygalatas et al. Extreme Rituals Promote Prosociality (2013)', 'study',
    'Просоциальное поведение после конкретного ритуала. Результат не является советом усиливать боль или рисковать: сила переживания не удостоверяет оттаивание.',
    'Prosocial behavior after a particular ritual. The result is no recommendation to intensify pain or risk: intensity does not certify thawing.',
    'https://doi.org/10.1177/0956797612472910')
reading('crowd-identity', [38, 39],
    'Gustave Le Bon. The Crowd (1895); Stephen Reicher, Russell Spears & Tom Postmes. A Social Identity Model of Deindividuation Phenomena (1995)', 'critique',
    'Исторический образ толпы сопоставлен с иной моделью: в группе идентичность может перестраиваться вокруг общих норм, а не исчезать. Чувство единства само по себе не доказывает потери или сохранения собственного голоса.',
    'A historical crowd image meets another model: group identity may reorganize around shared norms rather than vanish. Felt unity alone proves neither loss nor preservation of one’s voice.',
    'https://doi.org/10.1080/14792779443000049')
reading('canetti-lotman', [38, 39],
    'Elias Canetti. Crowds and Power (1960); Ю. М. Лотман. Культура и взрыв (1992)', 'parallel',
    'Кристалл толпы и взрыв культуры. Сильные самостоятельные образы, которые можно читать рядом со Звездой Смерти, не смешивая их значения.',
    'Crowd crystals and cultural explosion. Strong independent images to read alongside the Death Star without conflating their meanings.')
reading('arendt', [30, 33],
    'Hannah Arendt. The Human Condition (1958); On Violence (1970)', 'parallel',
    'Совместное действие, власть и насилие. У Арендт власть может означать способность действовать вместе; в трактате «власть» часто означает присвоение. Сходство вопросов не делает словари тождественными.',
    'Acting together, power, and violence. For Arendt, power can mean the capacity to act together; here it often means appropriation. Shared questions do not make the vocabularies identical.')
reading('weber-michels', [32, 35],
    'Max Weber. Economy and Society (1922); Robert Michels. Political Parties (1911)', 'critique',
    'Харизма, её превращение в учреждение и склонность организации к олигархии. Отсутствие наследного трона не освобождает Империю от проверки того, кто фактически решает.',
    'Charisma, its routinization, and organizational tendencies toward oligarchy. Absence of a hereditary throne does not exempt the Empire from examining who actually decides.')
reading('freeman', [30, 35],
    'Jo Freeman. The Tyranny of Structurelessness (1972)', 'critique',
    'Необъявленная структура скрывает круг тех, кто принимает решения. Для Империи это прямое испытание: правила, поручения и возможность отзыва должны оставаться видимыми для всех, кого они затрагивают.',
    'Unacknowledged structure conceals the circle that makes decisions. A direct test for the Empire: rules, delegated tasks, and recall must remain visible to those affected.',
    'https://www.jofreeman.com/joreen/tyranny.htm')
reading('ostrom', [34, 35],
    'Elinor Ostrom. Governing the Commons (1990)', 'parallel',
    'Общие правила, участие, наблюдение и разрешение споров. Порядок может служить совместной жизни без требования единого властвующего центра.',
    'Shared rules, participation, monitoring, and conflict resolution. Order can serve common life without requiring one sovereign center.')
reading('rhizome', [35],
    'Gilles Deleuze & Félix Guattari. A Thousand Plateaus (1980)', 'parallel',
    'Ризома как образ связи без единственного ствола. Образ грибницы не доказывает отсутствия власти внутри реальной сети.',
    'The rhizome as connection without a single trunk. Mycelial imagery does not prove that an actual network has no power relations.')
reading('bounded-choice', [32, 35],
    'Robert J. Lifton. Thought Reform and the Psychology of Totalism (1961); Janja Lalich. Bounded Choice (2004); Eileen Barker. The Making of a Moonie (1984); Lifton. Destroying the World to Save It (1999)', 'critique',
    'Разные исследования замкнутых систем авторитета и религиозного участия. Их не используют как ярлык для любой общины: здесь они испытывают возможность возражения, независимой связи и выхода.',
    'Distinct studies of closed authority systems and religious participation. Not labels for every community; here they test possibilities of dissent, independent relationships, and exit.')
reading('invented-religion', [35, 39],
    'Carole M. Cusack. Invented Religions (2010); Adam Possamai. In Search of New Age Spiritualities (2005); Markus A. Davidsen. Fiction-Based Religion (2013); David Chidester. Authentic Fakes (2005)', 'context',
    'Как современные религиозные формы работают с вымыслом и популярной культурой. Академическая карта для проекта, не приговор о подлинности внутреннего опыта.',
    'How modern religious forms engage fiction and popular culture. An academic map for the project, not a verdict on the authenticity of inward experience.')
reading('evangelion', [10, 26, 27, 29, 38],
    'Hideaki Anno et al. Neon Genesis Evangelion (1995–1996); The End of Evangelion (1997); Rebuild of Evangelion (2007–2021)', 'image',
    'Заявленный автором источник образов границы, комплементации и общего растворения. Это художественное родство; поле страха и исход круга в книге получают собственные правила.',
    'An author-acknowledged source for boundary, complementation, and collective dissolution imagery. An artistic affinity; the fear field and circle’s outcome have their own rules here.',
    'https://www.evangelion.jp/movie.html')
reading('hedgehogs', [10],
    'Arthur Schopenhauer. Parerga and Paralipomena II (1851), the porcupine parable', 'parallel',
    'Близость согревает и ранит; расстояние приходится искать заново. Самостоятельный философский образ, знакомый и через «Евангелион».',
    'Closeness warms and wounds; distance must be found anew. An independent philosophical image also familiar through Evangelion.')
reading('anime-studies', [26, 38],
    'Susan J. Napier. Anime from Akira to Howl’s Moving Castle (2005); Hiroki Azuma. Otaku: Japan’s Database Animals (2001)', 'context',
    'Культурный контекст аниме и его читательских миров. Не универсальный ключ к каждому образу и не замена самим произведениям.',
    'Cultural context for anime and its audiences. Neither a universal key to every image nor a substitute for the works themselves.')
reading('star-wars', [33],
    'George Lucas et al. Star Wars (from 1977); BioWare. Star Wars: Knights of the Old Republic (2003)', 'image',
    'Заявленный автором источник тёмного канона. Кодекс ситхов относится к расширенной вселенной и представлен в Knights of the Old Republic; это не реплика из фильма 1977 года. Книга переосмысляет силу через защиту чужого Русла.',
    'An author-acknowledged source of dark-canon imagery. The Sith Code belongs to the expanded universe and appears in Knights of the Old Republic, not as a line in the 1977 film. Here strength is reworked through protection of another’s Riverbed.')
reading('campbell', [33, 38],
    'Joseph Campbell. The Hero with a Thousand Faces (1949); Campbell & Bill Moyers. The Power of Myth (1988)', 'parallel',
    'Переход, испытание и возвращение. Сравнительная схема мифа не устанавливает единого смысла всех историй и не делает обрушение обязательным этапом пути.',
    'Transition, trial, and return. A comparative mythic scheme neither fixes every story’s meaning nor makes collapse a compulsory stage.')
reading('dune', [10],
    'Frank Herbert. Dune (1965)', 'parallel',
    'Литания против страха - художественный собеседник. Различить и выдержать страх не значит объявить любую его весть ложной.',
    'The litany against fear offers a literary interlocutor. Distinguishing and enduring fear does not mean declaring every warning false.')
reading('earthsea-dispossessed', [21, 30],
    'Ursula K. Le Guin. A Wizard of Earthsea (1968); The Dispossessed (1974)', 'parallel',
    'Признание тени и трудности общества без трона. Литературные собеседники, не доказательства психологической или общественной модели.',
    'Acknowledging the shadow and the difficulties of a society without a throne. Literary interlocutors, not proofs of a psychological or social model.')
reading('miyazaki', [24, 29],
    'Hayao Miyazaki. Nausicaä of the Valley of the Wind (1984); Princess Mononoke (1997)', 'parallel',
    'Чужая жизнь остаётся самостоятельной даже там, где человек узнаёт в ней своё. Сострадание не требует свести все стороны конфликта к одному голосу.',
    'Another life remains independent even where a human recognizes something familiar. Compassion does not require reducing every side of a conflict to one voice.')

reading('mead-self', [8, 9, 22],
    'George Herbert Mead. Mind, Self, and Society, §22: The “I” and the “me” (1934)', 'parallel',
    'Различение отвечающего «Я» и социально организованного «Мне». Это не тождество Свабхавы и Русла: у Мида «Я» тоже принадлежит социальному процессу и узнаётся после действия, а не даётся как неизменная природа.',
    'Distinguishes the responding “I” from the socially organized “me”. This is not an identity with Svabhava and Riverbed: Mead’s “I” also belongs to social process and becomes known after action, not as an unchanging nature.',
    'https://brocku.ca/MeadProject/Mead/pubs2/mindself/Mead_1934_22.html')
reading('cooley-self', [8],
    'Charles H. Cooley. Human Nature and the Social Order, ch. V (1902; revised ed. 1922)', 'parallel',
    '«Зеркальное я» включает воображаемое впечатление о себе и воображаемое суждение другого. Оно объясняет участие связи в образе себя, но не делает чужой взгляд прозрачным или безошибочным. Ссылка ведёт к пересмотренному изданию.',
    'The looking-glass self includes imagined appearance and imagined judgment by another. It illuminates relationship in self-image without making another’s gaze transparent or infallible. The link is to the revised edition.',
    'https://brocku.ca/MeadProject/Cooley/Cooley_1902/Cooley_1902f.html')



def export_readings():
    """Resolve shared entries once per section; reject broken catalog references."""
    for item in CATALOG.values():
        if not all(item.get(key) for key in ('title', 'ru', 'en')):
            raise ValueError(f'Incomplete bilingual reading: {item["id"]}')
        if item.get('href') and not item['href'].startswith('https://'):
            raise ValueError(f'Invalid reading URL: {item["id"]}')
    for section, keys in CONNECTIONS.items():
        if len(set(keys)) != len(keys):
            raise ValueError(f'Duplicate readings for section {section}')
    return {section: [CATALOG[key] for key in keys]
            for section, keys in CONNECTIONS.items()}
