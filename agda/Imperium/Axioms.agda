{-# OPTIONS --safe --without-K #-}

module Imperium.Axioms where

open import Imperium.Core
open import Imperium.Signs
open import Imperium.Empire
open import Imperium.Roles
open import Imperium.Protection
open import Imperium.Structure
open import Imperium.DeathStar
open import Imperium.CollectiveExamples using (circle; shared-return; shared-capture)
open Gathering
open import Data.Nat using (ℕ)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_)
open import Relation.Nullary using (¬_)

-- A collection of obligations and a constructive instance, not a proof that
-- the doctrine is true. Failure to find a term does NOT establish a contradiction:
-- lemmas, assumptions, or a proof strategy may still be missing.
-- Representation equalities and explicit initial contracts.
-- Agda checks them, but they are not conclusions about the gathering's dynamics.
record ModelContracts : Set₁ where
  field
    ct-initial-access : ∀ C → OpenAccess (initial C)
    ct-decision-passage : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ inside →
      passage (resolve g outcome shape) p ≡ outcome-passage outcome
    ct-outside-passage : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ outside →
      passage (resolve g outcome shape) p ≡ unlocked
    ct-resolution-keeps-position : ∀ {C} (g : Gathering C) outcome shape p →
      position (resolve g outcome shape) p ≡ position g p
    ct-riverbed-by-representation : ∀ {C} (g h : Gathering C) p → bed g p ≡ bed h p
    ct-shadow-keeps-beast : ∀ b → Beast.identity (acknowledge b) ≡ Beast.identity b
    ct-wall-keeps-edge : ∀ {E W} (b : Boundary E W) →
      Boundary.edge (lower-wall b) ≡ Boundary.edge b

-- Consequences derived under these definitions and contracts.
-- Unlike ct-*, the target's safety is not a transition premise.
record Theorems : Set₁ where
  field
    ax1-thawing-extension : ∀ h n → Σ History (λ h′ → Agrees n h h′ × Siddha h′)
    ax1-no-cert : ∀ h n → Σ History (λ h′ → Agrees n h h′ × ¬ Siddha h′)
    ax-no-finite-cert : ∀ h n → ¬ Certifies n h
    ax-no-finite-condemnation : ∀ h n → ¬ Refutes n h
    ax-recognition-⇏-siddha : ¬ (∀ l s k → Recognized (Life.observed l) s k → Siddha (Life.acts l))
    ax-siddha-⇏-recognition : ¬ (∀ l s k → Siddha (Life.acts l) → Recognized (Life.observed l) s k)
    ax-emperor-⇏-siddha : ¬ (∀ E lives j s k → EmperorStatus E lives j s k → Siddha (Life.acts (lives j)))
    ax-siddha-⇏-emperor : ¬ (∀ E lives j s k → Siddha (Life.acts (lives j)) → EmperorStatus E lives j s k)
    ax-recognition-revocable : Σ Observations (λ o → Recognized o 0 1 × ¬ Recognized o 1 1)
    ax-status-revocable : Σ (Three → Life) (λ lives →
      EmperorStatus threeEmpire lives a 0 1 × ¬ EmperorStatus threeEmpire lives a 1 1)
    ax-no-empty-recognition : ∀ o s → ¬ Recognized o s 0
    -- A concrete model without a throne; NOT a claim that all support is nontransitive.
    ax-throneless : Σ Empire (λ E → ¬ (∀ x y z → Empire.Holds E x y → Empire.Holds E y z → Empire.Holds E x z))
    ax-protection-releases : ∀ (e : Episode) t → Problem.threat (Episode.problem e t) ≡ 0 → level e t ≡ 0
    thm-star-step-preserves : ∀ {C} {g h : Gathering C} (step : RawStep g h) →
      Admissible step → EscapeInvariant g → EscapeInvariant h
    thm-star-trace-preserves : ∀ {C} {g h : Gathering C} →
      Trace g h → EscapeInvariant g → EscapeInvariant h
    thm-star-run-preserves : ∀ {C} (r : Run C) → EscapeInvariant (Run.state r 0) →
      ∀ t → EscapeInvariant (Run.state r t)
    thm-compression-violates : ∀ {C} (g : Gathering C) p → position g p ≡ inside →
      ¬ EscapeInvariant (compress g)
    -- Definitional consequence of the admissibility policy, not an independent
    -- dynamical theorem. Its empty-pattern proof has only normative content.
    thm-compression-not-admissible : ∀ {C} (g : Gathering C) ready input
      (effective : EffectiveOutcome g input enclosure) →
      ¬ Admissible (compression-step g ready input effective)
    thm-raw-steps-can-fail : ∀ {C} (g : Gathering C) (ready : phase g ≡ brink) input
      (effective : EffectiveOutcome g input enclosure) → EscapeInvariant g →
      ¬ (∀ {h} → RawStep g h → EscapeInvariant g → EscapeInvariant h)
    thm-recovery-reopens : ∀ {C} (g : Gathering C) p (support : Support g p) →
      MayLeave (recover g p support) p
    thm-closed-circle-no-support : ∀ {C} (g : Gathering C) →
      (∀ q → passage g q ≡ shut) → ∀ p → ¬ Support g p
    thm-explosion-has-personal-step : ∀ {C} (g : Gathering C) input →
      EffectiveOutcome g input explosion →
      Σ (Circle.Person C) (λ p → position g p ≡ inside ×
        CollectiveRule.choice (Circle.rule C) input p ≡ reclaim)
    thm-explosion-frees-all : ∀ {C} (g : Gathering C) shape → EscapeInvariant (burst g shape)
    thm-one-shakti-can-free-all : EscapeInvariant shared-return
    thm-one-kashaya-can-trap-all : ∀ p → ¬ MayLeave shared-capture p

record Doctrine : Set₁ where
  field
    contracts : ModelContracts
    theorems : Theorems

model-contracts : ModelContracts
model-contracts = record
  { ct-initial-access = initial-access
  ; ct-decision-passage = resolve-inside-passage
  ; ct-outside-passage = resolve-outside-passage
  ; ct-resolution-keeps-position = resolve-preserves-position
  ; ct-riverbed-by-representation = bed-by-representation
  ; ct-shadow-keeps-beast = beast-preserved
  ; ct-wall-keeps-edge = edge-preserved
  }

verified-theorems : Theorems
verified-theorems = record
  { ax1-thawing-extension = thawing-extension
  ; ax1-no-cert = gripping-extension
  ; ax-no-finite-cert = no-finite-certificate
  ; ax-no-finite-condemnation = no-finite-condemnation
  ; ax-recognition-⇏-siddha = recognition-⇏-siddha
  ; ax-siddha-⇏-recognition = siddha-⇏-recognition
  ; ax-emperor-⇏-siddha = emperor-⇏-siddha
  ; ax-siddha-⇏-emperor = siddha-⇏-emperor
  ; ax-recognition-revocable = revocable
  ; ax-status-revocable = revocable-status
  ; ax-no-empty-recognition = no-zero-window
  ; ax-throneless = threeEmpire , threeEmpire-not-transitive
  ; ax-protection-releases = released
  ; thm-star-step-preserves = admissible-preserves
  ; thm-star-trace-preserves = trace-preserves
  ; thm-star-run-preserves = run-preserves
  ; thm-compression-violates = compression-violates
  ; thm-compression-not-admissible = compression-not-admissible
  ; thm-raw-steps-can-fail = raw-preservation-false
  ; thm-recovery-reopens = recovery-reopens
  ; thm-closed-circle-no-support = closed-circle-no-support
  ; thm-explosion-has-personal-step = explosion-has-personal-step
  ; thm-explosion-frees-all = explosion-frees-all
  ; thm-one-shakti-can-free-all = Imperium.CollectiveExamples.single-shakti-frees-all
  ; thm-one-kashaya-can-trap-all = Imperium.CollectiveExamples.single-kashaya-traps
  }

imperium : Doctrine
imperium = record { contracts = model-contracts ; theorems = verified-theorems }
