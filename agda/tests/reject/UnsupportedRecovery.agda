{-# OPTIONS --safe --without-K #-}
module UnsupportedRecovery where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (shared-capture)
open import Imperium.Empire using (a; b)
open import Relation.Binary.PropositionalEquality using (refl)
-- Another captive has no open passage and cannot supply this support witness.
bad : Support shared-capture b
bad = supported-by a (λ ()) refl
