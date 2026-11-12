{-# OPTIONS --safe --without-K #-}
module NoPrivateExitDuringCapture where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (shared-capture)
open import Imperium.Empire using (a)
open import Data.Sum using (inj₂)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
-- Своё намерение reclaim не отменяет общего заточения от чужой кашаи.
bad : MayLeave shared-capture a
bad = inj₂ (leave shared-capture a , depart refl refl)
