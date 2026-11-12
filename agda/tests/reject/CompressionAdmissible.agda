{-# OPTIONS --safe --without-K #-}
module CompressionAdmissible where
open import Imperium.DeathStar
open import Imperium.Checks using (bad-step)
open import Relation.Binary.PropositionalEquality using (refl)
bad : Admissible bad-step
bad = allow-explosion
