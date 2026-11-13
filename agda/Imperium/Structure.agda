{-# OPTIONS --safe --without-K #-}

module Imperium.Structure where

open import Data.Empty using (⊥)
open import Data.Unit using (⊤; tt)
open import Data.Nat using (ℕ)
open import Data.Maybe using (Maybe; just; nothing)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_)

-- §8: only the three-thread structure. Connection is an external witness parameter
-- for the presence of a connection, NOT a Source type or the content of the inner voice.
-- The Source is deliberately absent from the model's language.
record Encounter (Riverbed Present Connection : Set) : Set where
  constructor encounter
  field
    riverbed : Riverbed
    present : Present
    connection : Connection

-- §10: removing a wall does not erase a boundary. Both types are external parameters.
record Boundary (Edge Wall : Set) : Set where
  constructor boundary
  field
    edge : Edge
    wall : Maybe Wall

lower-wall : ∀ {E W} → Boundary E W → Boundary E W
lower-wall b = boundary (Boundary.edge b) nothing

edge-preserved : ∀ {E W} (b : Boundary E W) →
  Boundary.edge (lower-wall b) ≡ Boundary.edge b
edge-preserved b = refl

wall-removed : ∀ {E W} (b : Boundary E W) → Boundary.wall (lower-wall b) ≡ nothing
wall-removed b = refl

-- §2: modes of maintaining form differ; both require movement.
data Mode : Set where
  repetition renewal : Mode

record MovingForm (Movement : Set) : Set where
  constructor form
  field
    movement : Movement
    mode : Mode

form-needs-movement : MovingForm ⊥ → ⊥
form-needs-movement = MovingForm.movement

-- §24: beast identity and membership in shadow are distinct coordinates.
data Recognition : Set where
  rejected acknowledged : Recognition

record Beast : Set where
  constructor beast
  field
    identity : ℕ
    recognition : Recognition

InShadow : Beast → Set
InShadow b = Beast.recognition b ≡ rejected

acknowledge : Beast → Beast
acknowledge b = beast (Beast.identity b) acknowledged

beast-preserved : ∀ b → Beast.identity (acknowledge b) ≡ Beast.identity b
beast-preserved b = refl

acknowledged-not-shadow : ∀ b → ¬ InShadow (acknowledge b)
acknowledged-not-shadow b ()

data ShadowItem : Set where
  animal : (b : Beast) → InShadow b → ShadowItem
  human : ℕ → ShadowItem -- a rejected human feeling, not a beast

IsBeast : ShadowItem → Set
IsBeast (animal _ _) = ⊤
IsBeast (human _) = ⊥

shadow-not-only-beasts : ¬ (∀ x → IsBeast x)
shadow-not-only-beasts f = f (human 0)
