{-# OPTIONS --safe --without-K #-}
module FiniteCertificate where
open import Imperium.Core
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
bad : Certifies 5 (λ _ → flow)
bad = λ _ _ → 0 , (λ _ _ → refl)
