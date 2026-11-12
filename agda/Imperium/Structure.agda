{-# OPTIONS --safe --without-K #-}

module Imperium.Structure where

open import Data.Empty using (⊥)
open import Data.Unit using (⊤; tt)
open import Data.Nat using (ℕ)
open import Data.Maybe using (Maybe; just; nothing)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_)

-- §8: только структура трёх нитей. Connection — внешний параметр-свидетель
-- наличия связи, НЕ тип Истока и не содержимое голоса Хридаи.
-- Исток намеренно отсутствует в языке модели.
record Encounter (Riverbed Present Connection : Set) : Set where
  constructor encounter
  field
    riverbed : Riverbed
    present : Present
    connection : Connection

-- §10: снять стену — не стереть край. Типы обоих переданы извне.
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

-- §2: различаются способы удержания формы, не наличие движения.
data Mode : Set where
  repetition renewal : Mode

record MovingForm (Movement : Set) : Set where
  constructor form
  field
    movement : Movement
    mode : Mode

form-needs-movement : MovingForm ⊥ → ⊥
form-needs-movement = MovingForm.movement

-- §24: зверь и принадлежность тени — разные координаты.
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
  human : ℕ → ShadowItem -- отвергнутое человеческое чувство, не зверь

IsBeast : ShadowItem → Set
IsBeast (animal _ _) = ⊤
IsBeast (human _) = ⊥

shadow-not-only-beasts : ¬ (∀ x → IsBeast x)
shadow-not-only-beasts f = f (human 0)
