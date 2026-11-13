{-# OPTIONS --safe --without-K #-}

module Imperium.Protection where

open import Data.Nat using (ℕ; zero; suc; _≤_; _+_; z≤n; s≤s)
open import Data.Nat.Properties using (≤-refl; n≤0⇒n≡0)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; subst; trans; sym)
open import Relation.Nullary using (¬_)

-- Threat, residual harm, restriction, and inflicted injury are distinct quantities.
-- Numbers form an abstract scale here, not the treatise's definition of harm.
record Problem : Set₁ where
  field
    Action : Set
    threat : ℕ
    restriction residual wound : Action → ℕ
    idle : Action
    idle-level : restriction idle ≡ 0
    idle-residual : residual idle ≡ threat
    idle-wound : wound idle ≡ 0
open Problem

Adequate : (p : Problem) → Action p → Set
Adequate p a = residual p a ≡ 0

-- Minimality is relative to the available sufficient actions.
-- Do not equate incomparable threat and restriction scales.
record Proportionate (p : Problem) (a : Action p) : Set where
  field
    adequate : Adequate p a
    least : ∀ b → Adequate p b → restriction p a ≤ restriction p b
    -- Among equally restrictive actions, do not choose a greater injury.
    least-wound : ∀ b → Adequate p b → restriction p b ≡ restriction p a → wound p a ≤ wound p b

released-choice : ∀ p a → Proportionate p a → threat p ≡ 0 → restriction p a ≡ 0
released-choice p a justified clear = n≤0⇒n≡0
  (subst (restriction p a ≤_) (idle-level p)
    (Proportionate.least justified (idle p) (trans (idle-residual p) clear)))

released-no-new-wound : ∀ p a → Proportionate p a → threat p ≡ 0 → wound p a ≡ 0
released-no-new-wound p a justified clear = n≤0⇒n≡0
  (subst (wound p a ≤_) (idle-wound p)
    (Proportionate.least-wound justified (idle p) (trans (idle-residual p) clear)
      (trans (idle-level p) (sym (released-choice p a justified clear)))))

-- An episode retains consequences after restrictions are lifted.
record Episode : Set₁ where
  field
    problem : ℕ → Problem
    choice : ∀ t → Action (problem t)
    justified : ∀ t → Proportionate (problem t) (choice t)
    damage : ℕ → ℕ
    accounted : ∀ t → damage t + wound (problem t) (choice t) ≤ damage (suc t)
    retained : ∀ t → damage t ≤ damage (suc t)
open Episode

level : Episode → ℕ → ℕ
level e t = restriction (problem e t) (choice e t)

released : ∀ e t → threat (problem e t) ≡ 0 → level e t ≡ 0
released e t = released-choice (problem e t) (choice e t) (justified e t)

-- A nontrivial finite choice: restriction 1 stops threat 3.
-- Protection's injury is recorded separately; sufficiency does not make it zero.
data Response : Set where
  wait hold crush : Response

scenario : ℕ → Problem
scenario danger = record
  { Action = Response ; threat = danger
  ; restriction = λ { wait → 0 ; hold → 1 ; crush → 2 }
  ; residual = λ { wait → danger ; hold → 0 ; crush → 0 }
  ; wound = λ { wait → 0 ; hold → 1 ; crush → 2 }
  ; idle = wait ; idle-level = refl ; idle-residual = refl ; idle-wound = refl
  }

hold-proportionate : Proportionate (scenario 3) hold
hold-proportionate = record { adequate = refl ; least = least ; least-wound = least-wound }
  where
    least : ∀ b → Adequate (scenario 3) b → restriction (scenario 3) hold ≤ restriction (scenario 3) b
    least wait ()
    least hold _ = ≤-refl
    least crush _ = s≤s z≤n

    least-wound : ∀ b → Adequate (scenario 3) b →
      restriction (scenario 3) b ≡ restriction (scenario 3) hold →
      wound (scenario 3) hold ≤ wound (scenario 3) b
    least-wound wait ()
    least-wound hold _ _ = ≤-refl
    least-wound crush _ ()

wait-proportionate : Proportionate (scenario 0) wait
wait-proportionate = record
  { adequate = refl ; least = λ _ _ → z≤n ; least-wound = λ _ _ _ → z≤n }

proportional-is-not-equality : ¬ (restriction (scenario 3) hold ≡ threat (scenario 3))
proportional-is-not-equality ()

necessary-wound : wound (scenario 3) hold ≡ 1
necessary-wound = refl

sample : Episode
sample = record
  { problem = λ { zero → scenario 3 ; (suc _) → scenario 0 }
  ; choice = λ { zero → hold ; (suc _) → wait }
  ; justified = λ { zero → hold-proportionate ; (suc _) → wait-proportionate }
  ; damage = λ { zero → 0 ; (suc _) → 1 }
  ; accounted = λ { zero → ≤-refl ; (suc _) → ≤-refl }
  ; retained = λ { zero → z≤n ; (suc _) → ≤-refl }
  }

sample-released : level sample 1 ≡ 0
sample-released = released sample 1 refl

wound-not-erased : damage sample 2 ≡ 1
wound-not-erased = refl
