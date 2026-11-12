{-# OPTIONS --safe --without-K #-}
module ErasedWound where
open import Imperium.Protection
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
bad : Episode.damage sample 2 ≡ 0
bad = refl
