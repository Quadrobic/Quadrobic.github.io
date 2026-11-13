{-# OPTIONS --safe --without-K #-}

-- Empire / Quadrobic Jainism: the formal core, stage 0.
--
-- What is modeled here (section references point to the treatise):
-- * kriya: an action at a given time (§11), with or without kashaya (§9);
-- * a jiva's history: an infinite sequence of such actions;
-- * siddha (§31): ice stops accumulating; eventually no action involves grasping;
-- * finite observation (companions observe for years, not forever, §31–32).
--
-- What is proved:
-- thawing-extension (§11): no finite past rules out eventual thawing;
-- gripping-extension (§31): no finite past certifies eventual liberation.
--
-- Both use the same construction: extend the past with either ice or water.
-- ASSUMPTION: History permits arbitrary extensions; riverbed dynamics are unspecified.
-- This establishes possibility in the model, not that every future is accessible
-- to a particular participant. The Source is deliberately neither a type nor a postulate.

module Imperium.Core where

open import Data.Nat using (ℕ; _≤_; _<_; _⊔_; _<?_)
open import Data.Nat.Properties using (m≤m⊔n; m≤n⊔m; <⇒≱; ≤-trans)
open import Data.Empty using (⊥; ⊥-elim)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; sym; trans)
open import Relation.Nullary using (yes; no; ¬_)

------------------------------------------------------------------------
-- Actions and histories

data Act : Set where
  flow : Act      -- movement leaves experience without binding the next action
  grip : Act      -- kashaya hardens the trace and accumulates ice (asrava)

History : Set
History = ℕ → Act

-- Distinguish freedom from T onward from eventual permanent freedom.
-- The latter does not assert liberation at the time of observation.
SiddhaFrom : History → ℕ → Set
SiddhaFrom h T = ∀ t → T ≤ t → h t ≡ flow

EventuallySiddha : History → Set
EventuallySiddha h = Σ ℕ (SiddhaFrom h)

-- Compatibility alias for the original theorems; its precise meaning is EventuallySiddha.
Siddha : History → Set
Siddha = EventuallySiddha

siddha-from-later : ∀ h T U → T ≤ U → SiddhaFrom h T → SiddhaFrom h U
siddha-from-later h T U T≤U p t U≤t = p t (≤-trans T≤U U≤t)

-- Two histories agree on the finite past, strictly before n.
Agrees : ℕ → History → History → Set
Agrees n h h' = ∀ t → t < n → h t ≡ h' t

------------------------------------------------------------------------
-- Two extensions of the same past

thaw : ℕ → History → History          -- always flow from n onward
thaw n h t with t <? n
... | yes _ = h t
... | no  _ = flow

freeze : ℕ → History → History        -- always grip from n onward
freeze n h t with t <? n
... | yes _ = h t
... | no  _ = grip

agrees-thaw : ∀ n h → Agrees n h (thaw n h)
agrees-thaw n h t t<n with t <? n
... | yes _  = refl
... | no t≮n = ⊥-elim (t≮n t<n)

agrees-freeze : ∀ n h → Agrees n h (freeze n h)
agrees-freeze n h t t<n with t <? n
... | yes _  = refl
... | no t≮n = ⊥-elim (t≮n t<n)

thaw-late : ∀ n h t → n ≤ t → thaw n h t ≡ flow
thaw-late n h t n≤t with t <? n
... | yes p = ⊥-elim (<⇒≱ p n≤t)
... | no  _ = refl

freeze-late : ∀ n h t → n ≤ t → freeze n h t ≡ grip
freeze-late n h t n≤t with t <? n
... | yes p = ⊥-elim (<⇒≱ p n≤t)
... | no  _ = refl

grip≢flow : ¬ (grip ≡ flow)
grip≢flow ()

------------------------------------------------------------------------
-- Theorems

-- §11: even the tightest repetition leaves an opening.
-- Every finite past has an extension in which ice stops accumulating.
thawing-extension : ∀ h n → Σ History (λ h' → Agrees n h h' × Siddha h')
thawing-extension h n = thaw n h , agrees-thaw n h , (n , thaw-late n h)

-- §31: no certificate can be issued from within a single day.
-- Every finite past has an extension without eventual liberation.
-- Thus no finite observation certifies eventual liberation.
gripping-extension : ∀ h n → Σ History (λ h' → Agrees n h h' × ¬ Siddha h')
gripping-extension h n = freeze n h , agrees-freeze n h , not-siddha
  where
    not-siddha : ¬ Siddha (freeze n h)
    not-siddha (T , p) = grip≢flow (trans (sym (freeze-late n h t n≤t)) (p t T≤t))
      where
        t : ℕ
        t = T ⊔ n
        T≤t : T ≤ t
        T≤t = m≤m⊔n T n
        n≤t : n ≤ t
        n≤t = m≤n⊔m T n

------------------------------------------------------------------------
-- Consequences about certificates, beyond individual extension witnesses.

Certifies : ℕ → History → Set
Certifies n h = ∀ h′ → Agrees n h h′ → Siddha h′

Refutes : ℕ → History → Set
Refutes n h = ∀ h′ → Agrees n h h′ → ¬ Siddha h′

no-finite-certificate : ∀ h n → ¬ Certifies n h
no-finite-certificate h n cert with gripping-extension h n
... | h′ , same , never = never (cert h′ same)

no-finite-condemnation : ∀ h n → ¬ Refutes n h
no-finite-condemnation h n refute with thawing-extension h n
... | h′ , same , eventually = refute h′ same eventually
