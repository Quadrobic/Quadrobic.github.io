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

-- Один и тот же круг допускает два разных хода событий.
three-equality : DecidableEquality Three
three-equality a a = yes refl
three-equality a b = no (λ ())
three-equality a c = no (λ ())
three-equality b a = no (λ ())
three-equality b b = yes refl
three-equality b c = no (λ ())
three-equality c a = no (λ ())
three-equality c b = no (λ ())
three-equality c c = yes refl

circle : Circle
circle = record
  { Person = Three ; BedIdentity = Three ; Shape = ℕ ; member = a
  ; person-equality = three-equality
  ; riverbed = λ p → p ; initial-outline = λ _ → 0
  }

at-edge : Gathering circle
at-edge = approach (initial circle)

edge-safe : EscapeInvariant at-edge
edge-safe = admissible-preserves (approach-step refl) allow-approach (initial-escape circle)

a-left : Gathering circle
a-left = leave at-edge a

a-exits-before-choice : Exit at-edge a a-left
a-exits-before-choice = depart refl refl

-- Чужой выход не выносит b из круга и не лишает его возможности выйти.
b-stays-inside : Gathering.position a-left b ≡ inside
b-stays-inside = refl

a-already-outside : Gathering.position a-left a ≡ outside
a-already-outside = exit-arrives-outside a-exits-before-choice

individual-ballot : Three → Choice
individual-ballot a = surrender -- уже ушедшему это разрешено
individual-ballot b = reclaim
individual-ballot c = reclaim

remaining-return : ReturningChoices a-left individual-ballot
remaining-return a ()
remaining-return b _ = refl
remaining-return c _ = refl

returned-state : Gathering circle
returned-state = resolve a-left individual-ballot (λ _ → 2)

successful-trace : Trace (initial circle) returned-state
successful-trace = then-step (approach-step refl) allow-approach
  (then-step (exit-step a-exits-before-choice) allow-exit
    (then-step (resolve-step refl individual-ballot (λ _ → 2))
      (allow-resolve remaining-return) done))

successful-still-free : EscapeInvariant returned-state
successful-still-free = trace-preserves successful-trace (initial-escape circle)

can-leave : MayLeave returned-state b
can-leave = successful-still-free b

same-riverbed-identity : bed returned-state b ≡ bed (initial circle) b
same-riverbed-identity = bed-by-representation returned-state (initial circle) b

changed-riverbed : Gathering.outline returned-state b ≡ 2
changed-riverbed = refl

-- Не только отказ признать плохой шаг допустимым: он существует как RawStep.
bad-step : RawStep at-edge (compress at-edge)
bad-step = compression-step at-edge refl

bad-is-not-safe : ¬ EscapeInvariant (compress at-edge)
bad-is-not-safe = compression-violates at-edge b refl

bad-is-not-admissible : ¬ Admissible bad-step
bad-is-not-admissible = compression-not-admissible at-edge b refl refl

-- Смешанный исход: один вернулся к себе, другой отдал себя центру.
-- Никакой общий голос не заменяет их разные решения.
mixed-ballot : Three → Choice
mixed-ballot a = reclaim
mixed-ballot b = surrender
mixed-ballot c = reclaim

mixed-state : Gathering circle
mixed-state = resolve at-edge mixed-ballot (λ _ → 1)

mixed-step : RawStep at-edge mixed-state
mixed-step = resolve-step refl mixed-ballot (λ _ → 1)

mixed-a-free : MayLeave mixed-state a
mixed-a-free = inj₂ (leave mixed-state a , depart refl refl)

mixed-a-own : Gathering.authority mixed-state a ≡ own
mixed-a-own = refl

mixed-b-center : Gathering.authority mixed-state b ≡ center
mixed-b-center = refl

mixed-b-captured : Captured mixed-state b
mixed-b-captured = refl , refl , refl

mixed-b-not-free : ¬ MayLeave mixed-state b
mixed-b-not-free = blocked-cannot-leave b refl refl

-- Помощь после плохого исхода восстанавливает мой выход, но не соседский.
recovery-step : RawStep mixed-state (recover mixed-state b)
recovery-step = recover-step b refl

recovery-allowed : Admissible recovery-step
recovery-allowed = allow-recover

recovered-b-free : MayLeave (recover mixed-state b) b
recovered-b-free = recovery-reopens mixed-state b

-- После сжатия всего круга починить одну дверь недостаточно для всех.
only-b-recovered : Gathering circle
only-b-recovered = recover (compress at-edge) b

a-still-captured : Captured only-b-recovered a
a-still-captured = refl , refl , refl

one-recovery-not-all : ¬ EscapeInvariant only-b-recovered
one-recovery-not-all safe = blocked-cannot-leave a refl refl (safe a)

-- Произвольный общий плохой шаг нельзя объявить безопасным для всех.
not-every-raw-step-preserves : ¬ (∀ {g h : Gathering circle} →
  RawStep g h → EscapeInvariant g → EscapeInvariant h)
not-every-raw-step-preserves = raw-preservation-false circle

-- Состав остаётся тем же, но все уже ушли: нельзя выдумывать захваченного.
all-left : Gathering circle
all-left = leave (leave a-left b) c

no-one-active : ReturningChoices all-left (λ _ → surrender)
no-one-active a ()
no-one-active b ()
no-one-active c ()

empty-center-harms-no-one : Admissible (compression-step all-left refl)
empty-center-harms-no-one = allow-resolve no-one-active

-- Бесконечный ход не обязан закончиться: безопасность не равна завершению.
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

-- Общее возвращение снимает власть центра у каждого, включая ушедшего a.
successful-own-center : ∀ p → Gathering.authority returned-state p ≡ own
successful-own-center a = refl
successful-own-center b = refl
successful-own-center c = refl

recovered-b-own : Gathering.authority (recover mixed-state b) b ≡ own
recovered-b-own = refl
