{-# OPTIONS --cubical --safe #-}

-- Two domains, not two ranks (§17, §31, §32).
-- Eventual liberation descends to action-history tails. Recognition is local
-- to a fixed finite observation window and does not descend to observation tails.
-- These are DIFFERENT quotients: no map from actions to accurate observations
-- is supplied. Signs.Life deliberately leaves the two components independent.
-- The result concerns the minimal Recognized predicate, not the Emperor's
-- complete support role, trust, psychology, or a certificate of actual liberation.

module Imperium.Levels where

open import Cubical.Foundations.Prelude
open import Cubical.HITs.SetQuotients as SQ using (_/_; [_]; eq/)

import Data.Nat as N
import Data.Nat.Properties as NP
import Data.Empty as E
import Data.Product as P
import Relation.Binary.PropositionalEquality as Eq

open import Imperium.Core using (History; Siddha; Agrees)
open import Imperium.Signs using
  (mkObs; Observations; Improving; Recognized; Life; flat
  ; interior-regression; interior-not-recognized
  ; recognition-⇏-siddha; siddha-⇏-recognition)
open import Imperium.Tail using
  (Tails; IsSiddha; Rel; SiddhaP; SiddhaP-respects
  ; prefix-allows-siddha; prefix-allows-not-siddha; siddha-classes-distinct)

------------------------------------------------------------------------
-- Observation tails, on the same fixed clock.

ObsRel : Observations → Observations → Type
ObsRel o o′ = P.Σ N.ℕ (λ T → ∀ t → T N.≤ t → o t Eq.≡ o′ t)

ObsTails : Type
ObsTails = Observations / ObsRel

improving-cong : ∀ {a a′ b b′} →
  a Eq.≡ a′ → b Eq.≡ b′ → Improving a b → Improving a′ b′
improving-cong Eq.refl Eq.refl x = x

recognition-window-local : ∀ (o o′ : Observations) (s k : N.ℕ) →
  (∀ t → s N.≤ t → t N.≤ s N.+ k → o t Eq.≡ o′ t) →
  Recognized o s k → Recognized o′ s k
recognition-window-local o o′ s k agree r = record
  { duration = Recognized.duration r
  ; steps = λ {i} i<k →
      improving-cong
        (agree (s N.+ i) (NP.m≤m+n s i)
          (NP.≤-trans (NP.+-monoʳ-≤ s (NP.n≤1+n i))
                      (NP.+-monoʳ-≤ s i<k)))
        (agree (s N.+ N.suc i) (NP.m≤m+n s (N.suc i))
          (NP.+-monoʳ-≤ s i<k))
        (Recognized.steps r i<k)
  }

------------------------------------------------------------------------
-- A concrete window cannot be recovered from an observation-tail class.

flat-obs : Observations
flat-obs _ = mkObs 0 0 0

agree-from-2 : ∀ t → 2 N.≤ t → flat-obs t Eq.≡ interior-regression t
agree-from-2 N.zero ()
agree-from-2 (N.suc N.zero) (N.s≤s ())
agree-from-2 (N.suc (N.suc n)) _ = Eq.refl

same-tail-class : [ flat-obs ] ≡ [ interior-regression ]
same-tail-class = eq/ {R = ObsRel} flat-obs interior-regression (2 P., agree-from-2)

flat-recognized : Recognized flat-obs 0 2
flat-recognized = record
  { duration = N.s≤s N.z≤n
  ; steps = λ _ → flat (mkObs 0 0 0)
  }

-- One counterexample at [0,2] refutes a uniform descent for all fixed windows.
-- This does not refute a different, explicitly eventual recognition predicate.
recognition-not-tail-local :
  (P.Σ (ObsTails → Type)
    (λ Q → ∀ o → (Recognized o 0 2 → Q [ o ]) P.×
                   (Q [ o ] → Recognized o 0 2))) → E.⊥
recognition-not-tail-local (Q P., iff) =
  interior-not-recognized
    (P.proj₂ (iff interior-regression)
      (subst Q same-tail-class (P.proj₁ (iff flat-obs) flat-recognized)))

------------------------------------------------------------------------
-- Every finite action prefix admits distinct eventual outcomes.

siddha-not-window-local : ∀ (h : History) (n : N.ℕ) →
  P.Σ History (λ h₁ → P.Σ History (λ h₂ →
    Agrees n h h₁ P.× Agrees n h h₂ P.×
    fst (IsSiddha [ h₁ ]) P.× (fst (IsSiddha [ h₂ ]) → E.⊥)))
siddha-not-window-local h n
  with prefix-allows-siddha h n | prefix-allows-not-siddha h n
... | h₁ P., (a₁ P., s₁) | h₂ P., (a₂ P., n₂) =
  h₁ P., (h₂ P., (a₁ P., (a₂ P., (s₁ P., n₂))))

-- The quotient remains nontrivial even after fixing any finite past.
prefix-has-distinct-tails : ∀ (h : History) (n : N.ℕ) →
  P.Σ History (λ h₁ → P.Σ History (λ h₂ →
    Agrees n h h₁ P.× Agrees n h h₂ P.× ([ h₁ ] ≡ [ h₂ ] → E.⊥)))
prefix-has-distinct-tails h n with siddha-not-window-local h n
... | h₁ P., (h₂ P., (a₁ P., (a₂ P., (s₁ P., n₂)))) =
  h₁ P., (h₂ P., (a₁ P., (a₂ P., siddha-classes-distinct s₁ n₂)))

-- The record collects proved consequences; it supplies no new contracts.
record TwoLevels : Type₁ where
  field
    siddha-tail-local : ∀ (h h′ : History) → Rel h h′ → SiddhaP h ≡ SiddhaP h′
    siddha-not-window-local-f : ∀ (h : History) (n : N.ℕ) →
      P.Σ History (λ h₁ → P.Σ History (λ h₂ →
        Agrees n h h₁ P.× Agrees n h h₂ P.×
        fst (IsSiddha [ h₁ ]) P.× (fst (IsSiddha [ h₂ ]) → E.⊥)))
    recognition-window-local-f : ∀ (o o′ : Observations) (s k : N.ℕ) →
      (∀ t → s N.≤ t → t N.≤ s N.+ k → o t Eq.≡ o′ t) →
      Recognized o s k → Recognized o′ s k
    recognition-not-tail-local-f :
      (P.Σ (ObsTails → Type)
        (λ Q → ∀ o → (Recognized o 0 2 → Q [ o ]) P.×
                       (Q [ o ] → Recognized o 0 2))) → E.⊥
    recognition-⇏-siddha-f :
      (∀ l s k → Recognized (Life.observed l) s k → Siddha (Life.acts l)) → E.⊥
    siddha-⇏-recognition-f :
      (∀ l s k → Siddha (Life.acts l) → Recognized (Life.observed l) s k) → E.⊥

levels : TwoLevels
levels = record
  { siddha-tail-local = SiddhaP-respects
  ; siddha-not-window-local-f = siddha-not-window-local
  ; recognition-window-local-f = recognition-window-local
  ; recognition-not-tail-local-f = recognition-not-tail-local
  ; recognition-⇏-siddha-f = recognition-⇏-siddha
  ; siddha-⇏-recognition-f = siddha-⇏-recognition
  }
