{-# OPTIONS --cubical --safe #-}

-- Histories modulo eventual pointwise equality (§11, §31).
-- The time indices stay fixed: this does NOT identify arbitrary time shifts,
-- arbitrary reorderings, or histories with infinitely many differing actions.
--
-- This adds no empirical contract to Core. Arbitrary classified continuations
-- remain a modelling assumption. Siddha is EventuallySiddha, not freedom now.
-- The quotient predicate forgets the cutoff witness by propositional truncation.
-- Two extension lemmas alone do not establish tail invariance: siddha-respects
-- proves it separately. Cubical univalence identifies equivalent propositions;
-- it does not identify all histories that satisfy the same predicate.

module Imperium.Tail where

open import Cubical.Foundations.Prelude
open import Cubical.Foundations.HLevels using (hProp; isSetHProp; TypeOfHLevel≡)
open import Cubical.Foundations.Univalence using (hPropExt)
open import Cubical.HITs.PropositionalTruncation as PT using (∥_∥₁; ∣_∣₁; squash₁)
open import Cubical.HITs.SetQuotients as SQ using (_/_; [_]; eq/)

import Data.Nat as N
import Data.Nat.Properties as NP
import Data.Empty as E
import Data.Product as P
import Relation.Binary.PropositionalEquality as Eq

open import Imperium.Core using
  (History; Siddha; Agrees; thawing-extension; gripping-extension)

------------------------------------------------------------------------
-- The relation retains a common clock and ignores only a finite beginning.

Rel : History → History → Type
Rel h h′ = P.Σ N.ℕ (λ T → ∀ t → T N.≤ t → h t Eq.≡ h′ t)

Rel-refl : ∀ h → Rel h h
Rel-refl h = 0 P., (λ _ _ → Eq.refl)

Rel-sym : ∀ {h h′} → Rel h h′ → Rel h′ h
Rel-sym (T P., p) = T P., (λ t T≤t → Eq.sym (p t T≤t))

Rel-trans : ∀ {h h′ h″} → Rel h h′ → Rel h′ h″ → Rel h h″
Rel-trans (T P., p) (U P., q) = (T N.⊔ U) P., λ t ge →
  Eq.trans (p t (NP.≤-trans (NP.m≤m⊔n T U) ge))
           (q t (NP.≤-trans (NP.m≤n⊔m T U) ge))

siddha-respects : ∀ {h h′} → Rel h h′ → Siddha h → Siddha h′
siddha-respects (T₂ P., r) (T₁ P., s) =
  (T₁ N.⊔ T₂) P., λ t ge →
    Eq.trans (Eq.sym (r t (NP.≤-trans (NP.m≤n⊔m T₁ T₂) ge)))
             (s t (NP.≤-trans (NP.m≤m⊔n T₁ T₂) ge))

------------------------------------------------------------------------
-- A set quotient and its proposition-valued predicate.

Tails : Type
Tails = History / Rel

SiddhaP : History → hProp ℓ-zero
SiddhaP h = ∥ Siddha h ∥₁ , squash₁

SiddhaP-respects : (h h′ : History) → Rel h h′ → SiddhaP h ≡ SiddhaP h′
SiddhaP-respects h h′ r =
  TypeOfHLevel≡ 1
    (hPropExt squash₁ squash₁
      (PT.rec squash₁ (λ s → ∣ siddha-respects r s ∣₁))
      (PT.rec squash₁ (λ s → ∣ siddha-respects (Rel-sym r) s ∣₁)))

IsSiddha : Tails → hProp ℓ-zero
IsSiddha = SQ.rec isSetHProp SiddhaP SiddhaP-respects

------------------------------------------------------------------------
-- Changing finitely many initial actions preserves the class.

prefix-invisible : ∀ (h h′ : History) (n : N.ℕ) →
  (∀ t → n N.≤ t → h t Eq.≡ h′ t) → [ h ] ≡ [ h′ ]
prefix-invisible h h′ n p = eq/ {R = Rel} h h′ (n P., p)

IsSiddha-computes : ∀ h → IsSiddha [ h ] ≡ SiddhaP h
IsSiddha-computes h = refl

prefix-allows-siddha : ∀ (h : History) (n : N.ℕ) →
  P.Σ History (λ h₁ → Agrees n h h₁ P.× fst (IsSiddha [ h₁ ]))
prefix-allows-siddha h n with thawing-extension h n
... | h₁ P., (agr P., sid) = h₁ P., (agr P., ∣ sid ∣₁)

isProp-⊥ : isProp E.⊥
isProp-⊥ ()

prefix-allows-not-siddha : ∀ (h : History) (n : N.ℕ) →
  P.Σ History (λ h₂ → Agrees n h h₂ P.× (fst (IsSiddha [ h₂ ]) → E.⊥))
prefix-allows-not-siddha h n with gripping-extension h n
... | h₂ P., (agr P., ns) = h₂ P., (agr P., PT.rec isProp-⊥ ns)

-- Sharing a finite past does not put the two futures in the same tail class.
siddha-classes-distinct : ∀ {h h′} →
  fst (IsSiddha [ h ]) → (fst (IsSiddha [ h′ ]) → E.⊥) →
  ([ h ] ≡ [ h′ ]) → E.⊥
siddha-classes-distinct yes no path = no (subst (λ q → fst (IsSiddha q)) path yes)
