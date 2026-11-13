{-# OPTIONS --safe --without-K #-}
module ExplosionIsDeparture where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (shared-return)
open import Imperium.Empire using (b)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- Opening the shared passage does not perform b's personal departure.
bad : Gathering.position shared-return b ≡ outside
bad = refl
