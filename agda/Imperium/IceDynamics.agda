{-# OPTIONS --safe --without-K #-}

module Imperium.IceDynamics where

open import Imperium.Core using (Act; flow; grip; pramada; History; Siddha)
open import Data.Nat using (ℕ; zero; suc; pred; _+_)
open import Data.Nat.Properties using (+-suc; ≤-refl)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; trans)
open import Data.Product using (_,_ )
open import Relation.Nullary using (¬_)

-- MODEL CONTRACT (§11): a unit scale for the abstract persistence of a trace.
-- Grasping and heedless repetition add one unit; attentive flow removes at most
-- one. These rates are a convention, not empirical psychology, karmic particles,
-- a measure of suffering, or a complete account of classical bandha causes.
step : ℕ → Act → ℕ
step ice flow = pred ice
step ice grip = suc ice
step ice pramada = suc ice

-- A finite run reads successive actions; no relation to rebirth is postulated.
run : ℕ → ℕ → History → ℕ
run zero ice h = ice
run (suc count) ice h = run count (step ice (h zero)) (λ t → h (suc t))

-- Derived multi-step consequences of the chosen update contract.
-- Absence of kashaya alone does not imply absence of accretion.
pramada-grows : ∀ count ice → run count ice (λ _ → pramada) ≡ count + ice
pramada-grows zero ice = refl
pramada-grows (suc count) ice = trans (pramada-grows count (suc ice)) (+-suc count ice)

grip-grows : ∀ count ice → run count ice (λ _ → grip) ≡ count + ice
grip-grows zero ice = refl
grip-grows (suc count) ice = trans (grip-grows count (suc ice)) (+-suc count ice)

-- Clearing old ice takes a finite sequence, not one privileged experience.
-- The bound uses unit rates and available flow actions; it is NOT a promise
-- that a real person can complete recovery in a prescribed number of acts.
flow-clears : ∀ ice → run ice ice (λ _ → flow) ≡ zero
flow-clears zero = refl
flow-clears (suc ice) = flow-clears ice

flow-keeps-clear : ∀ count → run count zero (λ _ → flow) ≡ zero
flow-keeps-clear zero = refl
flow-keeps-clear (suc count) = flow-keeps-clear count

pramada≢flow : ¬ (pramada ≡ flow)
pramada≢flow ()

-- The refined Siddha predicate rules out heedless repetition as well as grip.
-- This counterexample prevents the old "no grip implies liberation" shortcut.
heedless-not-siddha : ¬ Siddha (λ _ → pramada)
heedless-not-siddha (T , free) = pramada≢flow (free T ≤-refl)
