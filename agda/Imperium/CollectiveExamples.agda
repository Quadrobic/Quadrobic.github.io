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

-- Qualitative example labels, NOT physical measurements of energy.
-- Intention and effective influence are distinct: grasping can act even in someone
-- who intends to return. Effective influence confers no right to command others.
data Influence : Set where
  quiet life-force grasping-force : Influence

record Contribution : Set where
  constructor contribution
  field
    intention : Choice
    influence : Influence

Profile : Set
Profile = Three → Contribution

ReturnPower : Profile → Three → Set
ReturnPower input p = (Contribution.intention (input p) ≡ reclaim) ×
  (Contribution.influence (input p) ≡ life-force)

GripPower : Profile → Three → Set
GripPower input p = Contribution.influence (input p) ≡ grasping-force

-- A demonstration instance, NOT a law asserted by the treatise:
-- an effective life-force contribution makes explosion possible; effective grasping
-- makes enclosure possible. Competing contributions admit either outcome.
-- CollectiveRule permits a more specific future arbitration rule.
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

-- Only a contributes life force. Neither b nor c must make the same choice.
one-life-force : Profile
one-life-force a = contribution reclaim life-force
one-life-force b = contribution surrender quiet
one-life-force c = contribution surrender quiet

life-force-effective : EffectiveOutcome at-edge one-life-force explosion
life-force-effective = a , refl , (refl , refl)

shared-return : Gathering circle
shared-return = burst at-edge (λ _ → 2)

single-life-force-step : RawStep at-edge shared-return
single-life-force-step = resolve-step refl one-life-force explosion life-force-effective (λ _ → 2)

single-life-force-admissible : Admissible single-life-force-step
single-life-force-admissible = allow-explosion

single-life-force-frees-all : EscapeInvariant shared-return
single-life-force-frees-all = admissible-preserves single-life-force-step single-life-force-admissible edge-safe

-- Everyone intends to return, but only b contributes effective grasping force.
one-grasping-force : Profile
one-grasping-force a = contribution reclaim quiet
one-grasping-force b = contribution reclaim grasping-force
one-grasping-force c = contribution reclaim quiet

grasping-force-effective : EffectiveOutcome at-edge one-grasping-force enclosure
grasping-force-effective = b , refl , refl

shared-capture : Gathering circle
shared-capture = compress at-edge

single-grasping-force-step : RawStep at-edge shared-capture
single-grasping-force-step = compression-step at-edge refl one-grasping-force grasping-force-effective

single-grasping-force-traps : ∀ p → ¬ MayLeave shared-capture p
single-grasping-force-traps p = compression-blocks at-edge p refl

single-grasping-force-inadmissible : ¬ Admissible single-grasping-force-step
single-grasping-force-inadmissible = compression-not-admissible at-edge refl one-grasping-force grasping-force-effective

-- The same scene with competing contributions: this demonstration rule
-- selects no winner. Both outcomes are SHARED, not separate personal doors.
contested : Profile
contested a = contribution reclaim life-force
contested b = contribution reclaim grasping-force
contested c = contribution reclaim quiet

contested-explosion : RawStep at-edge shared-return
contested-explosion = resolve-step refl contested explosion (a , refl , (refl , refl)) (λ _ → 2)

contested-enclosure : RawStep at-edge shared-capture
contested-enclosure = resolve-step refl contested enclosure (b , refl , refl) (λ _ → 0)

-- The former outcome-independence theorem is false. Even c's complete
-- contribution is identical in these profiles, yet the collective result differs.
same-c-contribution : one-grasping-force c ≡ contested c
same-c-contribution = refl

c-free-from-another : MayLeave shared-return c
c-free-from-another = single-life-force-frees-all c

c-trapped-by-another : ¬ MayLeave shared-capture c
c-trapped-by-another = single-grasping-force-traps c

shared-outcomes-differ : ¬ (Gathering.gate shared-return c ≡ Gathering.gate shared-capture c)
shared-outcomes-differ ()

-- A later collective explosion can free the entire captive circle.
-- This does not retroactively make the earlier harmful transition admissible.
rekindled : Gathering circle
rekindled = approach shared-capture

later-life-force-effective : EffectiveOutcome rekindled one-life-force explosion
later-life-force-effective = a , refl , (refl , refl)

later-shared-return : Gathering circle
later-shared-return = burst rekindled (λ _ → 3)

later-explosion-step : RawStep rekindled later-shared-return
later-explosion-step = resolve-step refl one-life-force explosion later-life-force-effective (λ _ → 3)

later-explosion-frees-all : EscapeInvariant later-shared-return
later-explosion-frees-all = explosion-frees-all rekindled (λ _ → 3)
