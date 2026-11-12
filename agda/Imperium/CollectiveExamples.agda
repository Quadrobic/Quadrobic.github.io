{-# OPTIONS --safe --without-K #-}

module Imperium.CollectiveExamples where

open import Imperium.DeathStar
open import Imperium.Empire using (Three; a; b; c)
open import Data.Nat using (ℕ)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.Definitions using (DecidableEquality)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_; yes; no)

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

-- Качественные метки примера, НЕ физическое измерение энергии.
-- Намерение и действенное направление различены: хватка может действовать
-- и у того, кто намерен вернуться. Наличие силы не даёт приказа над другим.
data Influence : Set where
  quiet shakti kashaya : Influence

record Contribution : Set where
  constructor contribution
  field
    intention : Choice
    influence : Influence

Profile : Set
Profile = Three → Contribution

ReturnPower : Profile → Three → Set
ReturnPower input p = (Contribution.intention (input p) ≡ reclaim) ×
  (Contribution.influence (input p) ≡ shakti)

GripPower : Profile → Three → Set
GripPower input p = Contribution.influence (input p) ≡ kashaya

-- Демонстрационная, а НЕ объявленная законом трактата инстанция:
-- есть действенная Шакти → взрыв возможен; есть действенная кашая →
-- заточение возможно. При столкновении допускаются оба исхода.
-- Ядро CollectiveRule допускает и более точный будущий закон арбитража.
Possible : (Three → Position) → Profile → Outcome → Set
Possible positions input explosion = Σ Three (λ p → positions p ≡ inside × ReturnPower input p)
Possible positions input enclosure = Σ Three (λ p → positions p ≡ inside × GripPower input p)

possibility-rule : CollectiveRule Three
possibility-rule = record
  { Input = Profile
  ; choice = λ input p → Contribution.intention (input p)
  ; ReturningPower = ReturnPower ; GrippingPower = GripPower
  ; Responds = Possible
  ; explosion-origin = λ _ _ effective → effective
  ; enclosure-origin = λ _ _ effective → effective
  }

circle : Circle
circle = record
  { Person = Three ; BedIdentity = Three ; Shape = ℕ ; member = a
  ; person-equality = three-equality
  ; riverbed = λ p → p ; initial-outline = λ _ → 0
  ; rule = possibility-rule
  }

at-edge : Gathering circle
at-edge = approach (initial circle)

edge-safe : EscapeInvariant at-edge
edge-safe = admissible-preserves (approach-step refl) allow-approach (initial-escape circle)

-- Только a даёт Шакти. b и c не обязаны голосовать так же.
one-shakti : Profile
one-shakti a = contribution reclaim shakti
one-shakti b = contribution surrender quiet
one-shakti c = contribution surrender quiet

shakti-effective : EffectiveOutcome at-edge one-shakti explosion
shakti-effective = a , refl , (refl , refl)

shared-return : Gathering circle
shared-return = burst at-edge (λ _ → 2)

single-shakti-step : RawStep at-edge shared-return
single-shakti-step = resolve-step refl one-shakti explosion shakti-effective (λ _ → 2)

single-shakti-admissible : Admissible single-shakti-step
single-shakti-admissible = allow-explosion

single-shakti-frees-all : EscapeInvariant shared-return
single-shakti-frees-all = admissible-preserves single-shakti-step single-shakti-admissible edge-safe

-- Все намерены вернуться, но только b несёт действенную кашаю.
one-kashaya : Profile
one-kashaya a = contribution reclaim quiet
one-kashaya b = contribution reclaim kashaya
one-kashaya c = contribution reclaim quiet

kashaya-effective : EffectiveOutcome at-edge one-kashaya enclosure
kashaya-effective = b , refl , refl

shared-capture : Gathering circle
shared-capture = compress at-edge

single-kashaya-step : RawStep at-edge shared-capture
single-kashaya-step = compression-step at-edge refl one-kashaya kashaya-effective

single-kashaya-traps : ∀ p → ¬ MayLeave shared-capture p
single-kashaya-traps p = compression-blocks at-edge p refl

single-kashaya-inadmissible : ¬ Admissible single-kashaya-step
single-kashaya-inadmissible = compression-not-admissible at-edge refl one-kashaya kashaya-effective

-- Одна и та же сцена с конкурирующими вкладами: демонстрационное правило
-- не выбирает победителя. В обоих случаях исход ОБЩИЙ, не набор личных дверей.
contested : Profile
contested a = contribution reclaim shakti
contested b = contribution reclaim kashaya
contested c = contribution reclaim quiet

contested-explosion : RawStep at-edge shared-return
contested-explosion = resolve-step refl contested explosion (a , refl , (refl , refl)) (λ _ → 2)

contested-enclosure : RawStep at-edge shared-capture
contested-enclosure = resolve-step refl contested enclosure (b , refl , refl) (λ _ → 0)

-- Прежняя теорема независимости результатов неверна. У c в этих двух
-- профилях совпадают даже все данные вклада, но общий результат разный.
same-c-contribution : one-kashaya c ≡ contested c
same-c-contribution = refl

c-free-from-another : MayLeave shared-return c
c-free-from-another = single-shakti-frees-all c

c-trapped-by-another : ¬ MayLeave shared-capture c
c-trapped-by-another = single-kashaya-traps c

shared-outcomes-differ : ¬ (Gathering.gate shared-return c ≡ Gathering.gate shared-capture c)
shared-outcomes-differ ()

-- Позднейший общий взрыв может освободить весь захваченный круг.
-- Старая плохая ночь от этого не становится допустимой задним числом.
rekindled : Gathering circle
rekindled = approach shared-capture

later-shakti-effective : EffectiveOutcome rekindled one-shakti explosion
later-shakti-effective = a , refl , (refl , refl)

later-shared-return : Gathering circle
later-shared-return = burst rekindled (λ _ → 3)

later-explosion-step : RawStep rekindled later-shared-return
later-explosion-step = resolve-step refl one-shakti explosion later-shakti-effective (λ _ → 3)

later-explosion-frees-all : EscapeInvariant later-shared-return
later-explosion-frees-all = explosion-frees-all rekindled (λ _ → 3)
