{-# OPTIONS --safe --without-K #-}
module FlowHasNoEffect where
open import Imperium.Core using (flow)
open import Imperium.IceDynamics
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- Repeated flow changes existing ice under the chosen dynamical contract.
bad : run 3 3 (λ _ → flow) ≡ 3
bad = refl
