{-# OPTIONS --safe --without-K #-}
module UnanimityRequired where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (Contribution; one-shakti)
open import Imperium.Empire using (b)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
-- Общий взрыв уже осуществлён; из этого нельзя вывести единодушие b.
bad : Contribution.intention (one-shakti b) ≡ reclaim
bad = refl
