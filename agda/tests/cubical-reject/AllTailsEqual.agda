{-# OPTIONS --safe --cubical #-}
module AllTailsEqual where
open import Cubical.Foundations.Prelude
open import Cubical.HITs.SetQuotients using ([_])
open import Imperium.Core using (flow; grip)
open import Imperium.Tail using (Tails)
bad : _≡_ {A = Tails} [ (λ _ → flow) ] [ (λ _ → grip) ]
bad = refl
