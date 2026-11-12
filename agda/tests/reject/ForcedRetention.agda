{-# OPTIONS --safe --without-K #-}
module ForcedRetention where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (shared-return)
open import Imperium.Empire using (b)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
bad : Captured shared-return b
bad = refl , refl , refl
