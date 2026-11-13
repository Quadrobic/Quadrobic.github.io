{-# OPTIONS --safe --without-K #-}
module SelfSupport where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (shared-return)
open import Imperium.Empire using (b)
open import Relation.Binary.PropositionalEquality using (refl)
-- An open passage does not turn the recipient into their own OTHER companion.
bad : Support shared-return b
bad = supported-by b (λ equality → equality) refl
