{-# OPTIONS --safe --without-K #-}
module CompressionFree where
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (at-edge)
open import Imperium.Empire using (b)
open import Data.Sum using (inj₂)
open import Data.Product using (_,_)
open import Relation.Binary.PropositionalEquality using (refl)
bad : MayLeave (compress at-edge) b
bad = inj₂ (leave (compress at-edge) b , depart refl refl)
