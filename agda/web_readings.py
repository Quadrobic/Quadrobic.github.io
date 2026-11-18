"""Readings selected for a specific shared idea in the linked passage.

A link identifies the stated point of affinity, not agreement with an entire
system or evidence of authorial influence. Empirical limits remain explicit.
Do not add a source solely because it disputes the treatise or shares a word.
"""

KINDS = {
    'tradition': ('Традиция', 'Tradition'),
    'context': ('Контекст', 'Context'),
    'parallel': ('Близкая мысль', 'Related idea'),
    'study': ('Исследование', 'Study'),
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


reading('tattvartha', [9, 11, 28, 'sadhana'],
    'Umāsvāti. Tattvārtha Sūtra / That Which Is, trans. Nathmal Tatia (1994; Yale reissue 2011)', 'tradition',
    'Гл. 6 различает приток со страстью и без неё; 8.1 называет причины связывания, включая страсти и небрежность. Здесь находятся джайнские основания различения асравы и бандхи в §11.',
    'Chapter 6 distinguishes influx with and without passion; 8.1 includes passions and heedlessness among the causes of bondage. These are the Jain sources for §11’s distinction between asrava and bandha.',
    'https://yalebooks.co.uk/book/9780300165296/that-which-is/')

reading('dundas', [28, 'sadhana'],
    'Paul Dundas. The Jains, 2nd ed. (Routledge, 2002)', 'context',
    'Описание джайнских обетов, общинной и мирской практики. Полезно для понятий дхармы и авашьяк в тексте.',
    'An account of Jain vows, communal life, and lay practice, relevant to the text’s dharma and avashyaka vocabulary.',
    'https://www.routledge.com/The-Jains/Dundas/p/book/9780415266062')

reading('jaini', [11, 29, 'sadhana'],
    'Padmanabh S. Jaini. The Jaina Path of Purification (1979)', 'context',
    'Страсти и связывание кармой; ахимса, внимательность и очищение через практику. Близко к связке хватки, небрежности и работы над причинением вреда.',
    'Passions and karmic bondage; ahimsa, attentiveness, and purification through practice. Closely related to the text’s treatment of grip, heedlessness, and harmful action.')

reading('long', [28, 'sadhana'],
    'Jeffery D. Long. Jainism: An Introduction (2009)', 'context',
    'Джайнистские понятия живого, ненасилия и повседневной дисциплины: контекст дхармы и Садханы.',
    'Jain accounts of living beings, nonviolence, and daily discipline: context for dharma and Sadhana.')

reading('matilal', [4, 35],
    'Bimal Krishna Matilal. The Central Philosophy of Jainism (Anekāntavāda) (1981)', 'context',
    'Одну форму рассматривают с разных сторон; высказывание сохраняет смысл вместе с условиями и точкой зрения. Прямое чтение к сьядваде и множеству голосов.',
    'A form is approached from different standpoints; a statement retains its conditions and perspective. Direct reading for syadvada and the plurality of voices.',
    'https://jainqq.org/explore/001129/1')

reading('chapple', [29],
    'Christopher Key Chapple. Nonviolence to Animals, Earth, and Self in Asian Traditions (SUNY, 1993)', 'context',
    'Ахимса распространяет внимание к чужой жизни на животных, землю и самого действующего. Прямая связь с ненасилием как способом отношения к живому в §29. Это этическое чтение, а не физиологическое доказательство.',
    'Ahimsa extends care for life to animals, earth, and the acting person. Directly related to §29’s nonviolence as a way of relating to living beings. An ethical reading, rather than physiological evidence.',
    'https://digitalcommons.lmu.edu/theo_fac/64/')

reading('guseva', [8, 28, 'sadhana'],
    'Н. Р. Гусева. Джайнизм (Наука, 1968)', 'context',
    'Русскоязычное изложение джайнских понятий кармы, ненасилия и аскетической практики.',
    'A Russian-language account of Jain karma, nonviolence, and ascetic practice.')

reading('shah', [28],
    'Natubhai Shah. Jainism: The World of Conquerors (1998)', 'context',
    'Джайнистская этика и уклад общины: обеты, забота о живом и дисциплина повседневности.',
    'Jain ethics and communal practice: vows, care for living beings, and daily discipline.')

reading('triadic-heart', [14],
    'Paul E. Muller-Ortega. The Triadic Heart of Śiva (SUNY, 1989)', 'context',
    'Мистическое сердце как средоточие сознания и проявления в кашмирском шиваизме. Близкое чтение к Хридае как живому присутствию, которое предшествует объяснению себя.',
    'The mystical heart as the focus of consciousness and manifestation in Kashmir Shaivism. Closely related to Hridaya as living presence before self-explanation.')

reading('spanda', [14, 6],
    'Mark S. G. Dyczkowski. The Doctrine of Vibration (SUNY, 1987); Jaideva Singh. Spanda-Kārikās (1980)', 'context',
    'Спанда - живая пульсация сознания и сила проявления. Близко к Шакти как выражению движения и к присутствию мистического сердца; речь о метафизике, не о физической частоте.',
    'Spanda as the living pulsation of consciousness and power of manifestation. Close to Shakti as expression of movement and to mystical presence; a metaphysical account, not a physical frequency.',
    'https://doi.org/10.1515/9781438401744')

reading('recognition-heart', [14],
    'Jaideva Singh. Pratyabhijñāhṛdayam (1963)', 'parallel',
    'Узнавание собственной природы как уже присутствующей, а не создаваемой усилием. Близко к тому, что практика настраивает слушание Хридаи, но не учреждает само сердце.',
    'Recognition of one’s nature as already present rather than produced by effort. Close to practice attuning the hearing of Hridaya without bringing the heart itself into existence.')

reading('yoga-sutras', ['sadhana'],
    'Edwin F. Bryant. The Yoga Sūtras of Patañjali (2009)', 'parallel',
    'Дисциплина внимания, практика и освобождение в классической йоге. Параллель к работе пути, не историческое происхождение квадробики.',
    'Attention, practice, and liberation in classical yoga. A comparison for discipline, not a historical origin of quadrobics.')

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
    'Река сохраняет узнаваемость через смену вод; устойчивость и перемена принадлежат одному движению. Близко к непрерывности Русла.',
    'The river remains recognizable through changing waters; persistence and change belong to one movement. Close to the continuity of the Riverbed.')

reading('conatus', [6],
    'Baruch Spinoza. Ethics, III, propositions 6–7 (1677)', 'parallel',
    'Каждая вещь стремится сохранять своё бытие; это стремление выражает её действительную сущность. Близко к внутреннему основанию воли к жизни в §6.',
    'Each thing strives to persist in being; this striving expresses its actual essence. Close to the inward basis of the will to life in §6.')

reading('bergson', [6, 3],
    'Henri Bergson. Creative Evolution (1907)', 'parallel',
    'Творчество живого и новизна длительности. Философская параллель, не современная биологическая проверка жизненного порыва.',
    'Living creativity and novelty in duration. A philosophical comparison, not contemporary biological validation of a vital impulse.')

reading('whitehead', [2, 8],
    'Alfred North Whitehead. Process and Reality (1929)', 'parallel',
    'Событие и становление вместо первенства неподвижной вещи. Процессуальная метафизика даёт собеседника, но не доказательство Истока.',
    'Events and becoming rather than the primacy of static things. Process metaphysics offers an interlocutor, not proof of the Source.')

reading('tao', [6, 36, 3],
    'Ursula K. Le Guin. Tao Te Ching: A Book About the Way and the Power of the Way (1997)', 'parallel',
    'Путь, вода и действие без насилия над ходом вещей. Литературное переложение Лао-цзы; его не следует принимать за единственный перевод традиции.',
    'The way, water, and action without forcing the course of things. A literary rendering of Laozi, not the tradition’s sole translation.')

reading('schrodinger', [2],
    'Erwin Schrödinger. What Is Life? (1944)', 'parallel',
    'Физический вопрос об устойчивости живого. Исторический мост между жизнью и порядком, не отождествление термодинамики с волей.',
    'A physical inquiry into the persistence of life. A historical bridge between life and order, not an identification of thermodynamics with will.')

reading('prigogine', [2],
    'Ilya Prigogine & Isabelle Stengers. Order Out of Chaos (1984)', 'parallel',
    'Диссипативная форма держится обменом и потоком: её устойчивость существует благодаря продолжающемуся изменению. Близкая физическая параллель к образу пламени.',
    'A dissipative form persists through exchange and flow: its stability depends on ongoing change. A close physical comparison for the image of flame.')

reading('autopoiesis', [10],
    'Humberto Maturana & Francisco Varela. Autopoiesis and Cognition (1980); Evan Thompson. Mind in Life (2007)', 'parallel',
    'Живое само поддерживает организацию и границу процессами собственной жизни. Это близко к различению живого края и стены в §10.',
    'Living systems sustain their organization and boundary through their own vital processes. Closely related to §10’s distinction between a living boundary and a wall.')

reading('kauffman', [2],
    'Stuart Kauffman. At Home in the Universe (1995)', 'parallel',
    'Самоорганизация и возникновение порядка в сложных системах. Параллель к рождению формы, не физическая биография Истока.',
    'Self-organization and emerging order in complex systems. A comparison for form’s emergence, not a physical biography of the Source.')

reading('stellar-elements', [38, 39],
    'E. M. Burbidge, G. R. Burbidge, W. A. Fowler & F. Hoyle. Synthesis of the Elements in Stars (Rev. Mod. Phys. 29, 1957); Carl Sagan. Cosmos (1980)', 'context',
    'Звёздный нуклеосинтез даёт физическую опору образам углерода, кальция и железа. Не всё вещество тела возникло в звёздах: значительная часть водорода первична. Исход круга отсюда не выводится.',
    'Stellar nucleosynthesis grounds the imagery of carbon, calcium, and iron. Not all bodily matter originated in stars: much hydrogen is primordial. The circle’s outcome does not follow from this.',
    'https://doi.org/10.1103/RevModPhys.29.547')

reading('jung-shadow', [21, 23, 24],
    'C. G. Jung. Aion (CW 9ii, ch. II); Two Essays on Analytical Psychology (CW 7)', 'context',
    'Тень и персона - важный контекст авторского замысла. Тень не состоит только из злого; различение зверя и тени здесь остаётся собственным решением книги.',
    'Shadow and persona are important context for the author’s project. The shadow is not only evil; distinguishing beast from shadow remains this book’s own choice.',
    'https://iaap.org/resources/academic-resources/collected-works-abstracts/volume-9-2-aion-researches-phenomenology-self/')

reading('jung-further', [23],
    'C. G. Jung. The Archetypes and the Collective Unconscious (CW 9i); Answer to Job (CW 11); Man and His Symbols (1964); Memories, Dreams, Reflections (1962/1963)', 'parallel',
    'Архетипы, символ и работа с отвергнутым. Это историческая психологическая и мифопоэтическая перспектива, не доказательство буквальной памяти звериных жизней.',
    'Archetypes, symbols, and engagement with what was rejected. A historical psychological and mythopoetic perspective, not proof of literal memories of animal lives.')

reading('shadow-readings', [23],
    'Robert Bly. A Little Book on the Human Shadow (1988); Connie Zweig & Jeremiah Abrams, eds. Meeting the Shadow (1991); Robert A. Johnson. Owning Your Own Shadow (1991)', 'parallel',
    'Разные способы говорить о признании тени. Популярные и терапевтические разработки юнгианской мысли; ни одна не даёт права исполнять всякое найденное побуждение.',
    'Ways of describing acknowledgment of the shadow. Popular and therapeutic developments of Jungian thought; none licenses acting on every discovered impulse.')

reading('von-franz-stein', [23],
    'Marie-Louise von Franz. Shadow and Evil in Fairy Tales (1974); Murray Stein. Jung’s Map of the Soul (1998)', 'parallel',
    'Сказка как поле различения тени и разрушительного действия; карта юнгианских понятий для дальнейшего чтения.',
    'Fairy tales as a setting for distinguishing shadow from destructive action; a map of Jungian concepts for further reading.')

reading('winnicott', [22, 20],
    'D. W. Winnicott. Ego Distortion in Terms of True and False Self (1960)', 'context',
    'Ложное я как организация приспособления к требованиям окружения. Клинический собеседник маски; ложное я не означает просто ложь, а истинное я не тождественно Свабхаве.',
    'The false self as an organization of compliance with the environment. A clinical interlocutor for the mask; false self does not simply mean lying, nor true self Svabhava.',
    'https://doi.org/10.1093/med:psych/9780190271381.003.0023')

reading('goffman', [22, 20, 10],
    'Erving Goffman. The Presentation of Self in Everyday Life (1959)', 'parallel',
    'Представление себя во встрече. Социальная роль сама по себе не ложь и не болезнь; различение книги касается её затвердевания и права её менять.',
    'Presenting oneself in encounters. A social role is not inherently a lie or illness; the book asks about its hardening and the right to change it.')

reading('perls', [22],
    'Fritz Perls, Ralph Hefferline & Paul Goodman. Gestalt Therapy (1951)', 'context',
    'Интроекция: проглоченное, но не усвоенное. Ссылка ведёт к предисловиям и контексту книги; это клиническая метафора, не экспериментальная проверка §22.',
    'Introjection: swallowing without assimilation. The link supplies introductions and context; this is a clinical metaphor, not an experimental test of §22.',
    'https://gestalt.org/phgintro.htm')

reading('rogers', [17, 22],
    'Carl R. Rogers. On Becoming a Person (1961)', 'parallel',
    'Конгруэнтность, открытость опыту и отношения, в которых человеку не приходится заслуживать право быть собой. Близко к уменьшению разрыва между личным переживанием и жизнью среди других.',
    'Congruence, openness to experience, and relationships in which one need not earn the right to be oneself. Close to the narrowing gap between personal experience and life with others.')

reading('gendlin', [14, 15, 16],
    'Eugene T. Gendlin. Focusing (1978)', 'parallel',
    'Внимание к телесно ощущаемому смыслу, ожидание собственных слов и проверка их отклика. Инструкции уступают самому процессу: готовый ответ не должен заменять слушание. Близкое практическое чтение к §14–16.',
    'Attending to bodily felt meaning, waiting for one’s own words, and checking their resonance. Instructions yield to the process itself: a ready answer must not replace listening. Closely related to the practice in §14–16.',
    'https://focusing.org/sixsteps')

reading('lieberman', [22, 16],
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

reading('act', ['sadhana', 13],
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

reading('sdt', [16, 22, 30],
    'Edward L. Deci & Richard M. Ryan. The “What” and “Why” of Goal Pursuits (2000); Ryan & Deci. Self-Determination Theory (2017)', 'context',
    'Собственный выбор и связь с другими поддерживают друг друга. Принятое ради одобрения отличается от усвоенного как собственная ценность: автономия не требует одиночества.',
    'Choice and relatedness support one another. Acting for approval differs from integrating a value as one’s own: autonomy does not require solitude.',
    'https://doi.org/10.1207/S15327965PLI1104_01')

reading('closure', [22],
    'Arie W. Kruglanski & Donna M. Webster. Motivated Closing of the Mind: “Seizing” and “Freezing” (1996)', 'context',
    'Потребность в определённости побуждает быстро принять доступный ответ и затем ограждать его от пересмотра. Прямая связь с заёмной ясностью, которая становится хваткой в §22.',
    'A need for closure encourages seizing an available answer and then protecting it from revision. Directly related to borrowed clarity becoming a grip in §22.',
    'https://fitelson.org/current/seizing.pdf')

reading('bowlby', [22, 12],
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

reading('movement-learning', ['sadhana', 20],
    'Moshe Feldenkrais. Awareness Through Movement (1972); F. M. Alexander. The Use of the Self (1932)', 'parallel',
    'Замечать привычное движение и пробовать другое. Исторические практические сопоставления; не доказательство терапевтической эффективности квадробики.',
    'Noticing familiar movement and trying alternatives. Historical practical comparisons, not proof of quadrobics’ therapeutic efficacy.')

reading('bakhtin', [18, 20],
    'М. М. Бахтин. Творчество Франсуа Рабле и народная культура средневековья и Ренессанса (1965)', 'parallel',
    'Карнавал и материально-телесный низ как переворот официальной высоты. Литературная параллель, не теория лечебной позы.',
    'Carnival and the material bodily lower stratum as a reversal of official height. A literary comparison, not a theory of therapeutic posture.')

reading('descola-viveiros', [24],
    'Philippe Descola. Beyond Nature and Culture (2005); Eduardo Viveiros de Castro. Cosmological Deixis and Amerindian Perspectivism (1998)', 'parallel',
    'Разные способы различать человеческое и нечеловеческое. Сопоставление не превращает конкретные культуры в свидетельства универсального учения о внутренних зверях.',
    'Different ways of distinguishing human and nonhuman. Comparison does not turn particular cultures into witnesses for a universal doctrine of inner beasts.')

reading('ingold-harvey', [24, 25],
    'Tim Ingold. The Perception of the Environment (2000); Graham Harvey. Animism (2005)', 'parallel',
    'Навык, среда и отношения с нечеловеческими существами. Слушание зверя сопоставляется с отношением, а не с присвоением чужой культуры.',
    'Skill, environment, and relations with nonhuman beings. Listening to the beast is compared with relationship, not appropriation of another culture.')

reading('animal-encounters', [29, 24],
    'Donna Haraway. When Species Meet (2008); Jacques Derrida. The Animal That Therefore I Am (2006); James Hillman. Animal Presences (2008)', 'parallel',
    'Встреча с животным, взгляд другого и животные образы. Внутреннее узнавание не заменяет внимания к нужде живого существа снаружи.',
    'Encounters with animals, another’s gaze, and animal imagery. Inner recognition does not replace attending to a living creature’s actual needs.')

reading('de-waal', [29, 24],
    'Frans de Waal. Are We Smart Enough to Know How Smart Animals Are? (2016)', 'parallel',
    'Исследование животных требует задач, учитывающих их собственные возможности. Сопоставление с отказом мерить всякую жизнь одной человеческой мерой.',
    'Studying animals requires tasks attentive to their own capacities. A comparison for refusing to measure every life by one human standard.')

reading('ritual-process', [38, 'sadhana'],
    'Arnold van Gennep. The Rites of Passage (1909); Victor Turner. The Ritual Process (1969)', 'context',
    'Порог, переход и коммунитас помогают прочесть Час Растворения. Общий порог не гарантирует равенства после него и не описывает всякий ритуал одинаково.',
    'Threshold, transition, and communitas illuminate the Hour of Dissolution. A shared threshold guarantees neither equality afterward nor a single account of every ritual.')

reading('collective-rhythm', ['sadhana', 38],
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

reading('crowd-identity', [38, 39],
    'Stephen Reicher, Russell Spears & Tom Postmes. A Social Identity Model of Deindividuation Phenomena (1995)', 'context',
    'Общая идентичность меняет отношения и действие участников, не сводясь к исчезновению всякой идентичности. Близко к различению общего исхода и сохраняющегося личного пути.',
    'Shared identity changes participants’ relations and actions without simply abolishing identity. Close to the distinction between a collective outcome and each person’s continuing path.',
    'https://doi.org/10.1080/14792779443000049')

reading('freeman', [35],
    'Jo Freeman. The Tyranny of Structurelessness (1972)', 'context',
    'Вместо скрытого круга решающих - явные правила, подотчётные поручения и распределённые возможности участия. Близко к тому, как §35 отличает отсутствие трона от отсутствия устройства.',
    'Explicit rules, accountable delegation, and distributed participation replace a hidden decision-making circle. Close to §35’s distinction between having no throne and having no structure.',
    'https://www.jofreeman.com/joreen/tyranny.htm')

reading('ostrom', [35, 34],
    'Elinor Ostrom. Governing the Commons (1990)', 'parallel',
    'Общие правила, участие, наблюдение и разрешение споров. Порядок может служить совместной жизни без требования единого властвующего центра.',
    'Shared rules, participation, monitoring, and conflict resolution. Order can serve common life without requiring one sovereign center.')

reading('rhizome', [35],
    'Gilles Deleuze & Félix Guattari. A Thousand Plateaus (1980)', 'parallel',
    'Ризома как образ связи без единственного ствола. Образ грибницы не доказывает отсутствия власти внутри реальной сети.',
    'The rhizome as connection without a single trunk. Mycelial imagery does not prove that an actual network has no power relations.')

reading('evangelion', [29, 27, 10, 26, 38],
    'Hideaki Anno et al. Neon Genesis Evangelion (1995–1996); The End of Evangelion (1997); Rebuild of Evangelion (2007–2021)', 'image',
    'Заявленный автором источник образов границы, комплементации и общего растворения. Это художественное родство; поле страха и исход круга в книге получают собственные правила.',
    'An author-acknowledged source for boundary, complementation, and collective dissolution imagery. An artistic affinity; the fear field and circle’s outcome have their own rules here.',
    'https://www.evangelion.jp/movie.html')

reading('hedgehogs', [10],
    'Arthur Schopenhauer. Parerga and Paralipomena II (1851), the porcupine parable', 'parallel',
    'Близость согревает и ранит; расстояние приходится искать заново. Самостоятельный философский образ, знакомый и через «Евангелион».',
    'Closeness warms and wounds; distance must be found anew. An independent philosophical image also familiar through Evangelion.')

reading('star-wars', [33],
    'George Lucas et al. Star Wars (from 1977); BioWare. Star Wars: Knights of the Old Republic (2003)', 'image',
    'Заявленный автором источник тёмного канона. Кодекс ситхов относится к расширенной вселенной и представлен в Knights of the Old Republic; это не реплика из фильма 1977 года. Книга переосмысляет силу через защиту чужого Русла.',
    'An author-acknowledged source of dark-canon imagery. The Sith Code belongs to the expanded universe and appears in Knights of the Old Republic, not as a line in the 1977 film. Here strength is reworked through protection of another’s Riverbed.')

reading('earthsea-dispossessed', [30, 21],
    'Ursula K. Le Guin. A Wizard of Earthsea (1968); The Dispossessed (1974)', 'parallel',
    'Признание тени и трудности общества без трона. Литературные собеседники, не доказательства психологической или общественной модели.',
    'Acknowledging the shadow and the difficulties of a society without a throne. Literary interlocutors, not proofs of a psychological or social model.')

reading('miyazaki', [29, 24],
    'Hayao Miyazaki. Nausicaä of the Valley of the Wind (1984); Princess Mononoke (1997)', 'parallel',
    'Чужая жизнь остаётся самостоятельной даже там, где человек узнаёт в ней своё. Сострадание не требует свести все стороны конфликта к одному голосу.',
    'Another life remains independent even where a human recognizes something familiar. Compassion does not require reducing every side of a conflict to one voice.')

reading('mead-self', [9, 22],
    'George Herbert Mead. Mind, Self, and Society, §22: The “I” and the “me” (1934)', 'parallel',
    'Образ себя складывается через принятие отношения других, а собственный ответ не исчерпывается этим образом. Связь относится к эго и социальному узнаванию себя в §9 и §22.',
    'The self-image develops through taking others’ attitudes, while one’s response is not exhausted by that image. The connection concerns ego and social self-recognition in §9 and §22.',
    'https://brocku.ca/MeadProject/Mead/pubs2/mindself/Mead_1934_22.html')

reading('cooley-self', [8, 22],
    'Charles H. Cooley. Human Nature and the Social Order, ch. V (1902; revised ed. 1922)', 'parallel',
    'Человек узнаёт себя через представление о том, как его видят и оценивают другие. Близко к участию встречи в образе собственного Русла; воображаемый взгляд ещё нуждается в действительном ответе.',
    'People understand themselves through imagining how others see and judge them. Close to encounter shaping the image of one’s Riverbed; an imagined gaze still needs an actual response.',
    'https://brocku.ca/MeadProject/Cooley/Cooley_1902/Cooley_1902f.html')

reading('kagan-feedback', [18, 20],
    'Brett J. Kagan et al. In vitro neurons learn and exhibit sentience when embodied in a simulated game-world (Neuron, 2022)', 'study',
    'В установке DishBrain активность культуры нейронов управляла действием в симуляции, а результат возвращался стимуляцией. Структурированная замкнутая обратная связь была важна для наблюдавшегося обучения. Это параллель к изменению через собственное действие и ответ, не доказательство телесной практики. Опыт не устанавливает, что всякая адаптация вне такого контура невозможна; кодирование среды и правила обратной связи задавали исследователи.',
    'In DishBrain, neuronal culture activity controlled action in a simulation, with outcomes returned as stimulation. Structured closed-loop feedback mattered for the observed learning. This parallels change through action and response, rather than proving the bodily practice. It does not establish that all adaptation outside such a loop is impossible; researchers designed the environmental encoding and feedback rules.',
    'https://doi.org/10.1016/j.neuron.2022.09.001')

reading('edge-chaos', [2],
    'Nils Bertschinger & Thomas Natschläger. Real-time computation at the edge of chaos in recurrent neural networks (Neural Computation, 2004)', 'parallel',
    'В исследованных рекуррентных сетях сложные вычисления временных рядов становились возможны близ границы упорядоченной и хаотической динамики. Это ограниченный результат для моделей сетей. Живой берег в трактате - философский образ способности сохранять след и принимать новое, не измеренное критическое состояние Дживы.',
    'In the recurrent networks studied, complex time-series computations became possible near the boundary between ordered and chaotic dynamics. This is a limited result for network models. The treatise’s living bank is a philosophical image of retaining traces while receiving novelty, not a measured critical state of the jiva.',
    'https://doi.org/10.1162/089976604323057443')


reading('aurobindo-own-nature', [5, 28],
    'Sri Aurobindo. Essays on the Gita, Second Series, ch. XX: Swabhava and Swadharma (1928; CWSA 19)', 'parallel',
    'Собственная природа выражается собственным законом действия; чужая, даже безупречно исполненная форма не заменяет этого закона. Близкое чтение к Свабхаве и дхарме как выражению своего движения.',
    'One’s own nature expresses itself through its own law of action; even a perfectly performed borrowed form cannot replace it. Close to Svabhava and dharma as the expression of one’s movement.',
    'https://www.sriaurobindoashram.org/sriaurobindo/downloadpdf.php?id=34#page=518')
reading('aurobindo-free-action', [31, 34],
    'Sri Aurobindo. Essays on the Gita, First Series, ch. XVIII: The Divine Worker (1922; CWSA 19)', 'parallel',
    'Свобода от эгоистического присвоения не требует прекращения действия. Можно оставаться в мире и действовать, не связываясь сделанным: близко к деятельной свободе сиддхи и служению без платы за право быть.',
    'Freedom from egoistic appropriation need not end action. One can remain in the world and act without bondage to one’s works: close to the siddha’s active freedom and service without earning the right to exist.',
    'https://www.sriaurobindoashram.org/sriaurobindo/downloadpdf.php?id=34#page=188')
reading('gendlin-partnerships', [20, 30, 32],
    'Eugene T. Gendlin. Focusing Partnerships (The Focusing Folio 6(2), 1987)', 'parallel',
    'Внимательное присутствие другого помогает собственному процессу; каждый распоряжается своим временем, а роли слушающего и говорящего меняются. Близко к опоре без командования и к спутничеству как самостоятельной практике.',
    'Another’s attentive presence supports one’s own process; each person controls their time, and listening roles alternate. Close to support without command and companionship as a practice in its own right.',
    'https://focusing.org/gendlin/docs/gol_2063.html')
reading('gendlin-obedience', [15, 22, 32],
    'Eugene T. Gendlin. The Obedience Pattern (Studies in Formative Spirituality 5(2), 1984)', 'parallel',
    'Помощь нужна внутреннему движению, но подмена его чужим решением останавливает именно то, чему собирались помочь. Слушание требует диалога и с наставником, и с внутренним голосом, претендующим на всю власть.',
    'Help serves an inward process, yet replacing it with another’s decision obstructs precisely what needed support. Listening requires dialogue with both a guide and an inner voice claiming total authority.',
    'https://focusing.org/gendlin/docs/gol_2057.html')


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
