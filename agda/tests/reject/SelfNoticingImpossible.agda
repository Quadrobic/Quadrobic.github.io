{-# OPTIONS --safe --without-K #-}
module SelfNoticingImpossible where
open import Imperium.Witness
open import Relation.Binary.PropositionalEquality using (_≡_; refl)

-- An ambiguous window does not make ALL self-noticing impossible.
bad : Observation.feeling noticed-grip ≡ alive
bad = refl
