{-# OPTIONS --safe --without-K #-}
module IndividualVotes where
open import Imperium.DeathStar
open import Imperium.Checks using (mixed-state; mixed-a-free)
open import Imperium.Empire using (b)
bad : MayLeave mixed-state b
bad = mixed-a-free
