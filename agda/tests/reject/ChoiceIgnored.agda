{-# OPTIONS --safe --without-K #-}
module ChoiceIgnored where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples
open import Imperium.Empire using (a; b; c)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
-- Changing the sole Shakti contributor's choice removes this explosion witness.
no-reclaim : Profile
no-reclaim a = contribution surrender shakti
no-reclaim b = contribution surrender quiet
no-reclaim c = contribution surrender quiet
bad : EffectiveOutcome at-edge no-reclaim explosion
bad = a , refl , (refl , refl)
