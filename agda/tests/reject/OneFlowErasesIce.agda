{-# OPTIONS --safe --without-K #-}
module OneFlowErasesIce where
open import Imperium.Core using (flow)
open import Imperium.IceDynamics
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- One attentive act does not erase an arbitrary accumulated trace.
bad : step 3 flow ≡ 0
bad = refl
