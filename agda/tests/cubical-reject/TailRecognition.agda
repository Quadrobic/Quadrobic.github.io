{-# OPTIONS --safe --cubical #-}
module TailRecognition where
open import Imperium.Signs using (Recognized; interior-regression)
open import Imperium.Levels using (flat-recognized)
-- Equal observation tails do not preserve recognition of an early window.
bad : Recognized interior-regression 0 2
bad = flat-recognized
