{-# OPTIONS --safe --without-K #-}

-- Inner immediacy and knowledge of form are different questions (§8, §22).
-- This module does NOT encode Svabhava, Hridaya, or mystical experience.
-- Feeling is a report about an act; Reply is a coarse encounter observation,
-- not the other person's judgment, the whole Riverbed, or a measure of harm.

module Imperium.Witness where

open import Imperium.Core using (Act; flow; grip; pramada)
open import Data.Empty using (⊥)
open import Data.Product using (_×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; cong; trans; sym)
open import Relation.Nullary using (¬_)

data Feeling : Set where
  alive stuck : Feeling

data Reply : Set where
  room no-room : Reply

-- A binding verdict does not identify grip with pramada.
-- Nor does flowing mean harmless: harm and its repair need a richer model.
data Verdict : Set where
  flowing binding : Verdict

verdict : Act → Verdict
verdict flow = flowing
verdict grip = binding
verdict pramada = binding

flowing≢binding : ¬ (flowing ≡ binding)
flowing≢binding ()

room≢no-room : ¬ (room ≡ no-room)
room≢no-room ()

-- CONTRACT: one idealized observation window where ice imitates living motion
-- internally, while a discriminating encounter response separates the acts.
-- These equalities do not describe all acts or all witnesses. In particular,
-- §§11, 16 allow imitation, not a law that grip is NEVER felt as tightness.
-- The outer equalities assume the very observational adequacy they specify;
-- they do not prove that every observer can supply such a response.
record Perception : Set where
  field
    inner : Act → Feeling
    outer : Act → Reply
    flow-feels-alive : inner flow ≡ alive
    grip-feels-alive : inner grip ≡ inner flow
    pramada-feels-alive : inner pramada ≡ inner flow
    flow-leaves-room : outer flow ≡ room
    grip-closes : outer grip ≡ no-room
    pramada-closes : outer pramada ≡ no-room

module Theorems (P : Perception) where
  open Perception P

  -- Every criterion of this aliased inner report gives the same verdict.
  -- This is not a theorem that solitude or self-reflection is always useless.
  no-inner-criterion-grip :
    ∀ (f : Feeling → Verdict) → f (inner flow) ≡ flowing →
      f (inner grip) ≡ flowing
  no-inner-criterion-grip f h = trans (cong f grip-feels-alive) h

  no-inner-criterion-pramada :
    ∀ (f : Feeling → Verdict) → f (inner flow) ≡ flowing →
      f (inner pramada) ≡ flowing
  no-inner-criterion-pramada f h = trans (cong f pramada-feels-alive) h

  outer-separates-grip : ¬ (outer flow ≡ outer grip)
  outer-separates-grip e =
    room≢no-room (trans (sym flow-leaves-room) (trans e grip-closes))

  outer-separates-pramada : ¬ (outer flow ≡ outer pramada)
  outer-separates-pramada e =
    room≢no-room (trans (sym flow-leaves-room) (trans e pramada-closes))

  classify : Reply → Verdict
  classify room = flowing
  classify no-room = binding

  reads-flow : classify (outer flow) ≡ flowing
  reads-flow = cong classify flow-leaves-room

  reads-grip : classify (outer grip) ≡ binding
  reads-grip = cong classify grip-closes

  reads-pramada : classify (outer pramada) ≡ binding
  reads-pramada = cong classify pramada-closes

-- INHABITANT: the stated contracts are jointly satisfiable.
-- An inhabitant establishes consistency of this representation, not that an
-- ideal observation window exists for every real encounter.
sample : Perception
sample = record
  { inner = λ { flow → alive ; grip → alive ; pramada → alive }
  ; outer = λ { flow → room ; grip → no-room ; pramada → no-room }
  ; flow-feels-alive = refl
  ; grip-feels-alive = refl
  ; pramada-feels-alive = refl
  ; flow-leaves-room = refl
  ; grip-closes = refl
  ; pramada-closes = refl
  }

-- LIMITS: ordinary reports have no built-in oracle. The general representation
-- deliberately does not identify room with freedom or no-room with bondage.
-- A restriction needed for protection, a delayed reply, an error, or a compliant
-- companion can defeat a one-bit reading. No causal account is encoded here.
record Observation : Set where
  constructor observed
  field
    action : Act
    feeling : Feeling
    reply : Reply
open Observation

free-with-room : Observation
free-with-room = observed flow alive room

hidden-grip : Observation
hidden-grip = observed grip alive room

noticed-grip : Observation
noticed-grip = observed grip stuck no-room

free-without-room : Observation
free-without-room = observed flow alive no-room

-- The ambiguous case does not exclude other cases of direct self-noticing.
self-noticing-possible : ¬ (feeling noticed-grip ≡ feeling free-with-room)
self-noticing-possible ()

same-reply-different-action :
  reply free-with-room ≡ reply hidden-grip ×
  ¬ (verdict (action free-with-room) ≡ verdict (action hidden-grip))
same-reply-different-action = refl , flowing≢binding

-- Neither one-bit report alone is a universally correct classifier. These
-- counterexamples depend on allowing the ordinary observations above.
ReadsAllInner : (Feeling → Verdict) → Set
ReadsAllInner f = ∀ o → f (feeling o) ≡ verdict (action o)

ReadsAllOuter : (Reply → Verdict) → Set
ReadsAllOuter f = ∀ o → f (reply o) ≡ verdict (action o)

no-universal-inner : ∀ f → ¬ ReadsAllInner f
no-universal-inner f reads =
  flowing≢binding (trans (sym (reads free-with-room)) (reads hidden-grip))

no-universal-outer : ∀ f → ¬ ReadsAllOuter f
no-universal-outer f reads =
  flowing≢binding (trans (sym (reads free-with-room)) (reads hidden-grip))

-- The ideal decoder must not be exported as a verdict on all encounters.
ideal-decoder-not-universal : ¬ ReadsAllOuter (Theorems.classify sample)
ideal-decoder-not-universal = no-universal-outer (Theorems.classify sample)

-- Both directions can fail outside the discriminating window.
ideal-decoder-false-positive :
  ¬ (Theorems.classify sample (reply hidden-grip) ≡ verdict (action hidden-grip))
ideal-decoder-false-positive ()

ideal-decoder-false-negative :
  ¬ (Theorems.classify sample (reply free-without-room) ≡ verdict (action free-without-room))
ideal-decoder-false-negative ()
