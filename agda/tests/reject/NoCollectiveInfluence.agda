{-# OPTIONS --safe --without-K #-}
module NoCollectiveInfluence where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (at-edge; shared-capture)
open import Imperium.Empire using (a)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- Дверь a не остаётся прежней, когда кашая b заточает весь круг.
bad : Gathering.gate shared-capture a ≡ Gathering.gate at-edge a
bad = refl
