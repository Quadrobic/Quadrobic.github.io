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
    ct-decision-gate : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ inside →
      gate (resolve g outcome shape) p ≡ outcome-gate outcome
    ct-outside-gate : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ outside →
      gate (resolve g outcome shape) p ≡ unlocked
    ct-decision-authority : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ inside →
      authority (resolve g outcome shape) p ≡ outcome-authority outcome
    ct-outside-authority : ∀ {C} (g : Gathering C) outcome shape p → position g p ≡ outside →
      authority (resolve g outcome shape) p ≡ own
    ct-riverbed-by-representation : ∀ {C} (g h : Gathering C) p → bed g p ≡ bed h p
    ct-shadow-keeps-beast : ∀ b → Beast.identity (acknowledge b) ≡ Beast.identity b
    ct-wall-keeps-edge : ∀ {E W} (b : Boundary E W) →
      Boundary.edge (lower-wall b) ≡ Boundary.edge b

-- Consequences derived under these definitions and contracts.
-- Unlike ct-*, the target's safety is not a transition premise.
record Theorems : Set₁ where
  field
    ax1-thawing-extension : ∀ h n → Σ History (λ h′ → Agrees n h h′ × Liberated h′)
    ax1-no-cert : ∀ h n → Σ History (λ h′ → Agrees n h h′ × ¬ Liberated h′)
    ax-no-finite-cert : ∀ h n → ¬ Certifies n h
    ax-no-finite-condemnation : ∀ h n → ¬ Refutes n h
    ax-recognition-⇏-liberated : ¬ (∀ l s k → Recognized (Life.observed l) s k → Liberated (Life.acts l))
    ax-liberated-⇏-recognition : ¬ (∀ l s k → Liberated (Life.acts l) → Recognized (Life.observed l) s k)
    ax-emperor-⇏-liberated : ¬ (∀ E lives j s k → EmperorStatus E lives j s k → Liberated (Life.acts (lives j)))
    ax-liberated-⇏-emperor : ¬ (∀ E lives j s k → Liberated (Life.acts (lives j)) → EmperorStatus E lives j s k)
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
    thm-compression-not-admissible : ∀ {C} (g : Gathering C) ready input
      (effective : EffectiveOutcome g input enclosure) →
      ¬ Admissible (compression-step g ready input effective)
    thm-raw-steps-can-fail : ∀ {C} (g : Gathering C) (ready : phase g ≡ brink) input
      (effective : EffectiveOutcome g input enclosure) → EscapeInvariant g →
      ¬ (∀ {h} → RawStep g h → EscapeInvariant g → EscapeInvariant h)
    thm-recovery-reopens : ∀ {C} (g : Gathering C) p → MayLeave (recover g p) p
    thm-explosion-frees-all : ∀ {C} (g : Gathering C) shape → EscapeInvariant (burst g shape)
    thm-one-life-force-can-free-all : EscapeInvariant shared-return
    thm-one-grasping-force-can-trap-all : ∀ p → ¬ MayLeave shared-capture p

record Doctrine : Set₁ where
  field
    contracts : ModelContracts
    theorems : Theorems

model-contracts : ModelContracts
model-contracts = record
  { ct-initial-access = initial-access
  ; ct-decision-gate = resolve-inside-gate
  ; ct-outside-gate = resolve-outside-gate
  ; ct-decision-authority = resolve-inside-authority
  ; ct-outside-authority = resolve-outside-authority
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
  ; ax-recognition-⇏-liberated = recognition-⇏-liberated
  ; ax-liberated-⇏-recognition = liberated-⇏-recognition
  ; ax-emperor-⇏-liberated = emperor-⇏-liberated
  ; ax-liberated-⇏-emperor = liberated-⇏-emperor
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
  ; thm-explosion-frees-all = explosion-frees-all
  ; thm-one-life-force-can-free-all = Imperium.CollectiveExamples.single-life-force-frees-all
  ; thm-one-grasping-force-can-trap-all = Imperium.CollectiveExamples.single-grasping-force-traps
  }

imperium : Doctrine
imperium = record { contracts = model-contracts ; theorems = verified-theorems }
