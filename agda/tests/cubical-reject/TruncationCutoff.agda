{-# OPTIONS --safe --cubical #-}
module TruncationCutoff where
open import Cubical.HITs.PropositionalTruncation using (∥_∥₁)
open import Imperium.Core using (History; Siddha)
-- A truncated witness is not a concrete cutoff witness.
bad : ∀ (h : History) → ∥ Siddha h ∥₁ → Siddha h
bad h truncated = truncated
