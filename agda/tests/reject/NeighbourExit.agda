{-# OPTIONS --safe --without-K #-}
module NeighbourExit where
open import Imperium.DeathStar
open import Imperium.Checks using (a-left)
open import Imperium.Empire using (b)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
bad : Gathering.position a-left b ≡ outside
bad = refl
