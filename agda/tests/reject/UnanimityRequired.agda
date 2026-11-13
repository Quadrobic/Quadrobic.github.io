{-# OPTIONS --safe --without-K #-}
module UnanimityRequired where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (Contribution; one-shakti)
open import Imperium.Empire using (b)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- A collective explosion has occurred; this does not imply b's agreement.
bad : Contribution.intention (one-shakti b) ≡ reclaim
bad = refl
