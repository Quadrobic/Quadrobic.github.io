{-# OPTIONS --safe --without-K #-}
module HiddenRegression where
open import Imperium.Signs
open import Data.Nat using (s≤s; z≤n)
bad : Recognized interior-regression 0 2
bad = record { duration = s≤s z≤n ; steps = λ _ → flat (mkObs 0 0 0) }
