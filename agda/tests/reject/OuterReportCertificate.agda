{-# OPTIONS --safe --without-K #-}
module OuterReportCertificate where
open import Imperium.Witness
open import Relation.Binary.PropositionalEquality using (_≡_; refl)

-- The ideal decoder's theorem cannot classify an arbitrary encounter.
bad : Theorems.classify sample (Observation.reply hidden-grip) ≡ binding
bad = refl
