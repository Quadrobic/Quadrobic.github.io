{-# OPTIONS --safe --without-K #-}

module Imperium.DeathStar where

open import Data.Empty using (⊥; ⊥-elim)
open import Data.Unit using (⊤; tt)
open import Data.Nat using (ℕ; zero; suc)
open import Data.Product using (Σ; _×_; _,_; proj₁; proj₂)
open import Data.Sum using (_⊎_; inj₁; inj₂)
open import Relation.Binary.Definitions using (DecidableEquality)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; sym; trans; cong)
open import Relation.Nullary using (¬_; yes; no)

data Phase : Set where
  assembling brink aftermath : Phase

data Position : Set where
  inside outside : Position

data Gate : Set where
  unlocked shut : Gate

data Authority : Set where
  own center : Authority

data Choice : Set where
  reclaim surrender : Choice

-- Общий исход не совпадает с личным выбором. Один катализатор способен
-- изменить положение всех оставшихся, не выбирая их внутренний путь за них.
data Outcome : Set where
  explosion enclosure : Outcome

-- Открытый контракт столкновения сил. Input может содержать личные решения,
-- условные меры вкладов или качественные свидетельства. Никакой арифметики
-- Шакти/кашаи и правила «что всегда побеждает» ядро не постулирует.
record CollectiveRule (Person : Set) : Set₁ where
  field
    Input : Set
    choice : Input → Person → Choice
    ReturningPower GrippingPower : Input → Person → Set
    Responds : (Person → Position) → Input → Outcome → Set
    explosion-origin : ∀ positions input → Responds positions input explosion →
      Σ Person (λ p → positions p ≡ inside × ReturningPower input p)
    enclosure-origin : ∀ positions input → Responds positions input enclosure →
      Σ Person (λ p → positions p ≡ inside × GrippingPower input p)

-- Состав и идентичности Русел — контракт представления. Правило общего
-- ответа передаётся отдельно и явно, а не прячется в доказательствах.
record Circle : Set₁ where
  field
    Person BedIdentity Shape : Set
    member : Person
    person-equality : DecidableEquality Person
    riverbed : Person → BedIdentity
    initial-outline : Person → Shape
    rule : CollectiveRule Person

-- MayLeave/Detains не поля с произвольными значениями: возможность выхода
-- ниже определяется наличием настоящего перехода Exit.
record Gathering (C : Circle) : Set where
  constructor gathering
  field
    phase : Phase
    position : Circle.Person C → Position
    gate : Circle.Person C → Gate
    authority : Circle.Person C → Authority
    outline : Circle.Person C → Circle.Shape C
open Gathering

bed : ∀ {C} → Gathering C → Circle.Person C → Circle.BedIdentity C
bed {C} _ = Circle.riverbed C

-- Это равенство верно по выбору представления, не по динамической теореме.
bed-by-representation : ∀ {C} (g h : Gathering C) p → bed g p ≡ bed h p
bed-by-representation g h p = refl

initial : (C : Circle) → Gathering C
initial C = gathering assembling (λ _ → inside) (λ _ → unlocked)
  (λ _ → own) (Circle.initial-outline C)

update : ∀ {C} {A : Set} → (Circle.Person C → A) → Circle.Person C → A → Circle.Person C → A
update {C} f p value q with Circle.person-equality C p q
... | yes _ = value
... | no _ = f q

update-self : ∀ {C} {A : Set} (f : Circle.Person C → A) p value →
  update {C} f p value p ≡ value
update-self {C} f p value with Circle.person-equality C p p
... | yes _ = refl
... | no p≠p = ⊥-elim (p≠p refl)

leave : ∀ {C} → Gathering C → Circle.Person C → Gathering C
leave {C} g p = record g { position = update {C} (position g) p outside }

-- После плохой ночи новое собственное движение при опоре может вновь
-- открыть выход. Это не объявляет прошлый захват допустимым задним числом.
recover : ∀ {C} → Gathering C → Circle.Person C → Gathering C
recover {C} g p = record g
  { gate = update {C} (gate g) p unlocked
  ; authority = update {C} (authority g) p own
  }

approach : ∀ {C} → Gathering C → Gathering C
approach g = record g { phase = brink }

reframe : ∀ {C} → Gathering C → (Circle.Person C → Circle.Shape C) → Gathering C
reframe g shape = record g { outline = shape }

outcome-gate : Outcome → Gate
outcome-gate explosion = unlocked
outcome-gate enclosure = shut

outcome-authority : Outcome → Authority
outcome-authority explosion = own
outcome-authority enclosure = center

-- Общая реакция затрагивает всех, кто ещё участвует. Выбор каждого остаётся
-- его выбором, но дверь больше НЕ вычисляется отдельно из его бюллетеня.
resolve : ∀ {C} → Gathering C → Outcome →
  (Circle.Person C → Circle.Shape C) → Gathering C
resolve {C} g outcome shape = gathering aftermath (position g) gate′ authority′ shape
  where
    gate′ : Circle.Person C → Gate
    gate′ p with position g p
    ... | outside = unlocked
    ... | inside = outcome-gate outcome

    authority′ : Circle.Person C → Authority
    authority′ p with position g p
    ... | outside = own
    ... | inside = outcome-authority outcome

compress : ∀ {C} → Gathering C → Gathering C
compress g = resolve g enclosure (outline g)

burst : ∀ {C} → Gathering C → (Circle.Person C → Circle.Shape C) → Gathering C
burst g shape = resolve g explosion shape

-- Участник-катализатор — свидетель действенного вклада, не правитель круга.
EffectiveOutcome : ∀ {C} → Gathering C → CollectiveRule.Input (Circle.rule C) → Outcome → Set
EffectiveOutcome {C} g input outcome =
  CollectiveRule.Responds (Circle.rule C) (position g) input outcome

-- Выход — исполнимое локальное действие одного участника. Не требуется
-- ни общего решения, ни согласия центра, ни завершения ритуала.
data Exit {C : Circle} (g : Gathering C) (p : Circle.Person C) : Gathering C → Set where
  depart : position g p ≡ inside → gate g p ≡ unlocked → Exit g p (leave g p)

exit-arrives-outside : ∀ {C} {g h : Gathering C} {p} → Exit g p h → position h p ≡ outside
exit-arrives-outside {C} {g} {p = p} (depart _ _) = update-self {C} (position g) p outside

MayLeave : ∀ {C} → Gathering C → Circle.Person C → Set
MayLeave {C} g p = (position g p ≡ outside) ⊎ Σ (Gathering C) (Exit g p)

-- Ушедший уже свободен; оставшийся может совершить Exit.
EscapeInvariant : ∀ {C} → Gathering C → Set
EscapeInvariant g = ∀ p → MayLeave g p

OpenAccess : ∀ {C} → Gathering C → Set
OpenAccess g = ∀ p → position g p ≡ inside → gate g p ≡ unlocked

inside≢outside : ¬ (inside ≡ outside)
inside≢outside ()

shut≢open : ¬ (shut ≡ unlocked)
shut≢open ()

access⇒escape : ∀ {C} {g : Gathering C} → OpenAccess g → EscapeInvariant g
access⇒escape {g = g} access p with position g p in at
... | outside = inj₁ refl
... | inside = inj₂ (leave g p , depart at (access p at))

escape⇒access : ∀ {C} {g : Gathering C} → EscapeInvariant g → OpenAccess g
escape⇒access safe p at with safe p
... | inj₁ gone = ⊥-elim (inside≢outside (trans (sym at) gone))
... | inj₂ (_ , depart _ opened) = opened

initial-access : ∀ C → OpenAccess (initial C)
initial-access C _ _ = refl

initial-escape : ∀ C → EscapeInvariant (initial C)
initial-escape C = access⇒escape (initial-access C)

-- Физически возможные переходы включают и плохой исход. У RawStep НЕТ
-- встроенного требования EscapeInvariant, а у resolve-step нет общего «да».
data RawStep {C : Circle} (g : Gathering C) : Gathering C → Set where
  approach-step : phase g ≡ assembling → RawStep g (approach g)
  exit-step : ∀ {p h} → Exit g p h → RawStep g h
  reframe-step : (shape : Circle.Person C → Circle.Shape C) → RawStep g (reframe g shape)
  recover-step : (p : Circle.Person C) → phase g ≡ aftermath → RawStep g (recover g p)
  rekindle-step : phase g ≡ aftermath → RawStep g (approach g)
  resolve-step : phase g ≡ brink → (input : CollectiveRule.Input (Circle.rule C)) →
    (outcome : Outcome) → EffectiveOutcome g input outcome →
    (shape : Circle.Person C → Circle.Shape C) → RawStep g (resolve g outcome shape)

-- Допустимость оценивает общий результат, а не единодушие личных решений.
-- Взрыв при действенном вкладе одной Дживы допустим и без общего reclaim.
-- Возможность заточения остаётся в RawStep, но не становится нормой.
data Admissible {C : Circle} {g : Gathering C} : ∀ {h} → RawStep g h → Set where
  allow-approach : ∀ {ready} → Admissible (approach-step ready)
  allow-exit : ∀ {p h} {e : Exit g p h} → Admissible (exit-step e)
  allow-reframe : ∀ {shape} → Admissible (reframe-step shape)
  allow-recover : ∀ {p ready} → Admissible (recover-step p ready)
  allow-rekindle : ∀ {ready} → Admissible (rekindle-step ready)
  allow-explosion : ∀ {ready input effective shape} →
    Admissible (resolve-step ready input explosion effective shape)

-- Доказательство для выхода требует рассмотреть, кто ушёл: сам p или другой.
leave-access : ∀ {C} {g : Gathering C} {p h} → OpenAccess g → Exit g p h → OpenAccess h
leave-access {C} {g} {p} access (depart at opened) q q-inside
  with Circle.person-equality C p q
... | yes _ = ⊥-elim (inside≢outside (sym q-inside))
... | no _ = access q q-inside

recover-access : ∀ {C} {g : Gathering C} p → OpenAccess g → OpenAccess (recover g p)
recover-access {C} {g} p access q at with Circle.person-equality C p q
... | yes _ = refl
... | no _ = access q at

burst-access : ∀ {C} (g : Gathering C) shape → OpenAccess (burst g shape)
burst-access g shape p at rewrite at = refl

-- Инвариант цели не записан в Admissible. Теорема разбирает реальные
-- локальные действия и общий взрыв; гарантии для всех RawStep НЕТ.
admissible-preserves : ∀ {C} {g h : Gathering C} (step : RawStep g h) →
  Admissible step → EscapeInvariant g → EscapeInvariant h
admissible-preserves (approach-step _) allow-approach safe = access⇒escape (escape⇒access safe)
admissible-preserves (exit-step e) allow-exit safe = access⇒escape (leave-access (escape⇒access safe) e)
admissible-preserves (reframe-step _) allow-reframe safe = access⇒escape (escape⇒access safe)
admissible-preserves {C} {g} (recover-step p _) allow-recover safe =
  access⇒escape (recover-access {C} {g} p (escape⇒access safe))
admissible-preserves (rekindle-step _) allow-rekindle safe = access⇒escape (escape⇒access safe)
admissible-preserves {g = g} (resolve-step _ input explosion effective shape) allow-explosion safe =
  access⇒escape (burst-access g shape)

-- Конечная история: в каждом её префиксе инвариант сохраняется.
data Trace {C : Circle} (g : Gathering C) : Gathering C → Set where
  done : Trace g g
  then-step : ∀ {h k} (step : RawStep g h) → Admissible step → Trace h k → Trace g k

trace-preserves : ∀ {C} {g h : Gathering C} → Trace g h → EscapeInvariant g → EscapeInvariant h
trace-preserves done safe = safe
trace-preserves (then-step step allowed rest) safe =
  trace-preserves rest (admissible-preserves step allowed safe)

-- Бесконечное наблюдение хода: возможность выйти у каждого на КАЖДОМ шаге.
record Run (C : Circle) : Set where
  field
    state : ℕ → Gathering C
    step : ∀ t → RawStep (state t) (state (suc t))
    allowed : ∀ t → Admissible (step t)

run-preserves : ∀ {C} (r : Run C) → EscapeInvariant (Run.state r 0) →
  ∀ t → EscapeInvariant (Run.state r t)
run-preserves r safe zero = safe
run-preserves r safe (suc t) =
  admissible-preserves (Run.step r t) (Run.allowed r t) (run-preserves r safe t)

-- Для настоящего шага сжатия нужно свидетельство действенной кашаи,
-- а не доказательство того, что ВСЕ выбрали surrender.
compression-step : ∀ {C} (g : Gathering C) → phase g ≡ brink →
  (input : CollectiveRule.Input (Circle.rule C)) → EffectiveOutcome g input enclosure →
  RawStep g (compress g)
compression-step g ready input effective = resolve-step ready input enclosure effective (outline g)

blocked-cannot-leave : ∀ {C} {g : Gathering C} p → position g p ≡ inside →
  gate g p ≡ shut → ¬ MayLeave g p
blocked-cannot-leave p at closed (inj₁ gone) = inside≢outside (trans (sym at) gone)
blocked-cannot-leave p at closed (inj₂ (_ , depart _ opened)) = shut≢open (trans (sym closed) opened)

-- Нужен свидетель оставшегося: пустой круг / все уже ушли никого не удержит.
compression-blocks : ∀ {C} (g : Gathering C) p → position g p ≡ inside → ¬ MayLeave (compress g) p
compression-blocks g p at = blocked-cannot-leave p at closed
  where
    closed : gate (compress g) p ≡ shut
    closed rewrite at = refl

compression-violates : ∀ {C} (g : Gathering C) p → position g p ≡ inside → ¬ EscapeInvariant (compress g)
compression-violates g p at safe = compression-blocks g p at (safe p)

compression-not-admissible : ∀ {C} (g : Gathering C) ready input
  (effective : EffectiveOutcome g input enclosure) →
  ¬ Admissible (compression-step g ready input effective)
compression-not-admissible g ready input effective ()

-- Равенства представления: исход общий, хотя участники и их выборы различны.
resolve-inside-gate : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ inside →
  gate (resolve g outcome shape) p ≡ outcome-gate outcome
resolve-inside-gate g outcome shape p at rewrite at = refl

resolve-outside-gate : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ outside →
  gate (resolve g outcome shape) p ≡ unlocked
resolve-outside-gate g outcome shape p gone rewrite gone = refl

resolve-inside-authority : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ inside →
  authority (resolve g outcome shape) p ≡ outcome-authority outcome
resolve-inside-authority g outcome shape p at rewrite at = refl

resolve-outside-authority : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ outside →
  authority (resolve g outcome shape) p ≡ own
resolve-outside-authority g outcome shape p gone rewrite gone = refl

-- Плохой исход нарушает инвариант даже у безопасного исходного круга.
-- При одном общем исходе нельзя раздать оставшимся независимые двери.
shared-inside-gates : ∀ {C} (g : Gathering C) outcome shape p q →
  position g p ≡ inside → position g q ≡ inside →
  gate (resolve g outcome shape) p ≡ gate (resolve g outcome shape) q
shared-inside-gates g outcome shape p q p-at q-at =
  trans (resolve-inside-gate g outcome shape p p-at)
        (sym (resolve-inside-gate g outcome shape q q-at))

raw-preservation-false : ∀ {C} (g : Gathering C) ready input
  (effective : EffectiveOutcome g input enclosure) → EscapeInvariant g →
  ¬ (∀ {h} → RawStep g h → EscapeInvariant g → EscapeInvariant h)
raw-preservation-false {C} g ready input effective safe preserve =
  compression-violates g p at (preserve (compression-step g ready input effective) safe)
  where
    origin = CollectiveRule.enclosure-origin (Circle.rule C) (position g) input effective
    p = proj₁ origin
    at = proj₁ (proj₂ origin)

-- Свидетель плохого текущего исхода, НЕ окончательный приговор будущему.
Captured : ∀ {C} → Gathering C → Circle.Person C → Set
Captured g p = (phase g ≡ aftermath) × (position g p ≡ inside) × (gate g p ≡ shut)

compression-captures : ∀ {C} (g : Gathering C) p → position g p ≡ inside → Captured (compress g) p
compression-captures g p at = refl , at , closed
  where
    closed : gate (compress g) p ≡ shut
    closed rewrite at = refl

-- Общий взрыв освобождает и того, кто не стал катализатором.
explosion-frees-all : ∀ {C} (g : Gathering C) shape → EscapeInvariant (burst g shape)
explosion-frees-all g shape = access⇒escape (burst-access g shape)

recovery-reopens : ∀ {C} (g : Gathering C) p → MayLeave (recover g p) p
recovery-reopens {C} g p with position g p in at
... | outside = inj₁ refl
... | inside = inj₂ (leave (recover g p) p , depart at (update-self {C} (gate g) p unlocked))
