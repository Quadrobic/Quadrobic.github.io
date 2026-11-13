{-# OPTIONS --safe --without-K #-}
module NegligenceIsSiddha where
open import Imperium.Core
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
-- No kashaya does not suffice when pramada continues forever.
bad : Siddha (λ _ → pramada)
bad = 0 , (λ _ _ → refl)
