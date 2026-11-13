{-# OPTIONS --safe --without-K #-}
module FutureIsNow where
open import Imperium.Core
open import Imperium.Checks using (future-free)
open import Relation.Binary.PropositionalEquality using (refl)
bad : SiddhaFrom future-free 0
bad = λ _ _ → refl
