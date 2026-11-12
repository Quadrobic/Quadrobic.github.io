{-# OPTIONS --safe --without-K #-}
module OneRecoveryFreesAll where
open import Imperium.DeathStar
open import Imperium.Checks using (only-b-recovered)
open import Data.Sum using (inj₁)
open import Relation.Binary.PropositionalEquality using (refl)
bad : EscapeInvariant only-b-recovered
bad = λ _ → inj₁ refl
