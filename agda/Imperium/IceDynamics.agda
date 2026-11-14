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

-- State after t classified actions of this very history. Classification is
-- supplied by discernment outside the model: accounting is not its cause.
iceAt : ℕ → History → ℕ → ℕ
iceAt initial h zero = initial
iceAt initial h (suc t) = step (iceAt initial h t) (h t)

-- Once permanent flow begins, the actual accumulated finite ice clears.
flow-tail-clears : ∀ initial h T →
  (∀ t → T Data.Nat.≤ t → h t ≡ flow) →
  ∀ n → iceAt initial h (T + n) ≡ run n (iceAt initial h T) (λ _ → flow)
flow-tail-clears initial h T free zero rewrite Data.Nat.Properties.+-identityʳ T = refl
flow-tail-clears initial h T free (suc n)
  rewrite +-suc T n | free (T + n) (Data.Nat.Properties.m≤m+n T n)
        | flow-tail-clears initial h T free n = advance n (iceAt initial h T)
  where
    advance : ∀ n ice → step (run n ice (λ _ → flow)) flow ≡ run (suc n) ice (λ _ → flow)
    advance zero ice = refl
    advance (suc n) ice = advance n (pred ice)

siddha-clears-ice : ∀ initial h → Siddha h →
  Data.Product.Σ ℕ (λ T → ∀ n → iceAt initial h (T + n) ≡ zero)
siddha-clears-ice initial h (T , free) = T + iceAt initial h T , cleared
  where
    cleared : ∀ n → iceAt initial h ((T + iceAt initial h T) + n) ≡ zero
    cleared n rewrite Data.Nat.Properties.+-assoc T (iceAt initial h T) n
      | flow-tail-clears initial h T free (iceAt initial h T + n) = drain (iceAt initial h T) n
      where
        drain : ∀ ice n → run (ice + n) ice (λ _ → flow) ≡ zero
        drain zero n = flow-keeps-clear n
        drain (suc ice) n = drain ice n

-- Width is the number of available responses, represented by one plus slack.
-- Binding narrows down to one; attentive flow expands. This floor is an
-- explicit axiom of representation, not an empirical accessibility claim.
widthStep : ℕ → Act → ℕ
widthStep slack flow = suc slack
widthStep slack grip = pred slack
widthStep slack pramada = pred slack

slackAt : ℕ → History → ℕ → ℕ
slackAt initial h zero = initial
slackAt initial h (suc t) = widthStep (slackAt initial h t) (h t)

width : ℕ → History → ℕ → ℕ
width initial h t = suc (slackAt initial h t)

opening-remains : ∀ initial h t → 0 Data.Nat.< width initial h t
opening-remains initial h t = Data.Nat.s≤s Data.Nat.z≤n
