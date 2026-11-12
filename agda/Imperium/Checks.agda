{-# OPTIONS --safe --without-K #-}

module Imperium.Checks where

open import Imperium.Axioms
open import Imperium.Core
open import Imperium.Signs
open import Imperium.Empire
open import Imperium.Roles
open import Imperium.Protection
open import Imperium.Structure
open import Imperium.DeathStar
open import Imperium.CollectiveExamples
open import Data.Empty using (⊥)
open import Data.Unit using (⊤; tt)
open import Data.Nat using (ℕ; zero; suc; z≤n; s≤s)
open import Data.Product using (proj₁; _,_)
open import Data.Sum using (inj₁; inj₂)
open import Relation.Binary.Definitions using (DecidableEquality)
open import Data.Maybe using (just)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_; yes; no)

-- Когда-нибудь свободна ≠ свободна сейчас.
future-free : History
future-free = thaw 1 (λ _ → grip)

later-free : EventuallySiddha future-free
later-free = 1 , thaw-late 1 (λ _ → grip)

not-free-now : ¬ SiddhaFrom future-free 0
not-free-now p = grip≢flow (p 0 z≤n)

-- Много окон не превращает наблюдение в знание всей истории.
many-windows : Sustained (Life.observed calm-gripping) 0 12 10
many-windows = calm-gripping-sustained 0 12 10 (s≤s z≤n) (s≤s z≤n)

-- Разные формы опоры совместимы: нетранзитивность не требование учения.
-- Для транзитивной модели тоже есть экземпляр Empire со всеми его полями.
transitive-model : Empire
transitive-model = allSupportEmpire

-- Локальный выход до общего решения по-прежнему возможен.
a-left : Gathering circle
a-left = leave at-edge a

a-exits-before-choice : Exit at-edge a a-left
a-exits-before-choice = depart refl refl

b-stays-inside : Gathering.position a-left b ≡ inside
b-stays-inside = refl

a-already-outside : Gathering.position a-left a ≡ outside
a-already-outside = exit-arrives-outside a-exits-before-choice

-- Одной действенной Шакти a достаточно для общего возвращения b и c,
-- хотя они не сделали того же личного выбора. Это конкретный свидетель,
-- а не универсальное правило победы любой Шакти над любой кашаей.
successful-trace : Trace (initial circle) shared-return
successful-trace = then-step (approach-step refl) allow-approach
  (then-step single-shakti-step single-shakti-admissible done)

successful-still-free : EscapeInvariant shared-return
successful-still-free = trace-preserves successful-trace (initial-escape circle)

can-leave : MayLeave shared-return b
can-leave = successful-still-free b

same-riverbed-identity : bed shared-return b ≡ bed (initial circle) b
same-riverbed-identity = bed-by-representation shared-return (initial circle) b

changed-riverbed : Gathering.outline shared-return b ≡ 2
changed-riverbed = refl

bad-step : RawStep at-edge shared-capture
bad-step = single-kashaya-step

bad-is-not-safe : ¬ EscapeInvariant shared-capture
bad-is-not-safe = compression-violates at-edge b refl

bad-is-not-admissible : ¬ Admissible bad-step
bad-is-not-admissible = single-kashaya-inadmissible

-- Даже своё reclaim не защищает a от общего заточения, вызванного b.
a-wanted-return : Contribution.intention (one-kashaya a) ≡ reclaim
a-wanted-return = refl

a-captured-by-b : Captured shared-capture a
a-captured-by-b = compression-captures at-edge a refl

-- Возможны разные наборы вкладов и конкурирующие силы, но не независимые
-- исходы для участников одного и того же общего resolve.
common-gates : ∀ p q → Gathering.gate shared-capture p ≡ Gathering.gate shared-capture q
common-gates p q = shared-inside-gates at-edge enclosure (λ _ → 0) p q refl refl

-- Отдельная местная помощь не тождественна общему взрыву.
only-b-recovered : Gathering circle
only-b-recovered = recover shared-capture b

local-recovery-step : RawStep shared-capture only-b-recovered
local-recovery-step = recover-step b refl

local-recovery-allowed : Admissible local-recovery-step
local-recovery-allowed = allow-recover

recovered-b-free : MayLeave only-b-recovered b
recovered-b-free = recovery-reopens shared-capture b

a-still-captured : Captured only-b-recovered a
a-still-captured = refl , refl , refl

local-repair-not-all : ¬ EscapeInvariant only-b-recovered
local-repair-not-all safe = blocked-cannot-leave a refl refl (safe a)

-- Но последующее действенное движение одной Дживы может освободить ВСЕХ.
reopening-step : RawStep shared-capture rekindled
reopening-step = rekindle-step refl

reopening-allowed : Admissible reopening-step
reopening-allowed = allow-rekindle

later-all-free : EscapeInvariant later-shared-return
later-all-free = later-explosion-frees-all

not-every-raw-step-preserves : ¬ (∀ {g h : Gathering circle} →
  RawStep g h → EscapeInvariant g → EscapeInvariant h)
not-every-raw-step-preserves preserve =
  raw-preservation-false at-edge refl one-kashaya kashaya-effective edge-safe preserve

-- Уже покинувшие круг не захватываются обратно общим исходом.
all-left : Gathering circle
all-left = leave (leave a-left b) c

no-outside-catalyst : ∀ input outcome → ¬ EffectiveOutcome all-left input outcome
no-outside-catalyst input explosion (a , () , _)
no-outside-catalyst input explosion (b , () , _)
no-outside-catalyst input explosion (c , () , _)
no-outside-catalyst input enclosure (a , () , _)
no-outside-catalyst input enclosure (b , () , _)
no-outside-catalyst input enclosure (c , () , _)

quiet-run : Run circle
quiet-run = record
  { state = λ _ → initial circle
  ; step = λ _ → reframe-step (Circle.initial-outline circle)
  ; allowed = λ _ → allow-reframe
  }

always-free : ∀ t → EscapeInvariant (Run.state quiet-run t)
always-free = run-preserves quiet-run (initial-escape circle)

-- Цельность не стирает зверя; возвращение не удерживает его в тени.
beast-identity : Beast.identity (acknowledge (beast 7 rejected)) ≡ 7
beast-identity = refl

no-longer-shadow : ¬ InShadow (acknowledge (beast 7 rejected))
no-longer-shadow = acknowledged-not-shadow (beast 7 rejected)

-- Стена снята, но собственный край цел.
same-edge : Boundary.edge (lower-wall (boundary 7 (just 2))) ≡ 7
same-edge = refl

-- Достаточное минимальное ограничение не равно числу угрозы и не безвредно.
minimal-not-equal : ¬ (Problem.restriction (scenario 3) hold ≡ Problem.threat (scenario 3))
minimal-not-equal = proportional-is-not-equality

released-but-not-undone : level sample 1 ≡ 0
released-but-not-undone = sample-released

damage-remains : Episode.damage sample 2 ≡ 1
damage-remains = wound-not-erased

-- Общий взрыв снимает власть центра у всех, не переписывая их намерений.
successful-own-center : ∀ p → Gathering.authority shared-return p ≡ own
successful-own-center a = refl
successful-own-center b = refl
successful-own-center c = refl
