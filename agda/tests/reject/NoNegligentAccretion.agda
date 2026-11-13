{-# OPTIONS --safe --without-K #-}
module NoNegligentAccretion where
open import Imperium.Core using (pramada)
open import Imperium.IceDynamics
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- Heedless repetition is a binding cause even without an explicit grip.
bad : step 0 pramada ≡ 0
bad = refl
