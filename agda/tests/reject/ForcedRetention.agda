{-# OPTIONS --safe --without-K #-}
module ForcedRetention where
open import Imperium.DeathStar
open import Imperium.Checks using (returned-state)
open import Imperium.Empire using (b)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
bad : Captured returned-state b
bad = refl , refl , refl
