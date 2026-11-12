{-# OPTIONS --safe --without-K #-}
module ZeroWindow where
open import Imperium.Signs
open import Data.Nat using (s≤s; z≤n)
bad : Recognized (Life.observed calm-gripping) 0 0
bad = calm-gripping-recognized 0 1 (s≤s z≤n)
