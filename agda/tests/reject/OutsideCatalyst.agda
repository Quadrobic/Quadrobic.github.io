{-# OPTIONS --safe --without-K #-}
module OutsideCatalyst where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (one-grasping-force)
open import Imperium.Checks using (all-left)
open import Imperium.Empire using (b)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
-- Someone who has left cannot act as an internal catalyst in an empty circle.
bad : EffectiveOutcome all-left one-grasping-force enclosure
bad = b , refl , refl
