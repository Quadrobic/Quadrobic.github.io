{-# OPTIONS --safe --without-K #-}

module Imperium.Empire where

open import Data.Empty using (⊥)
open import Data.Unit using (⊤; tt)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_)

-- Support, authority over another riverbed, and completeness of voice are DISTINCT.
-- Rules means an appropriated right to decide for another riverbed, not temporary
-- task coordination in a shared undertaking (§35).
record Empire : Set₁ where
  field
    Jiva : Set
    member : Jiva
    Holds Rules : Jiva → Jiva → Set
    no-throne : ∀ j k → ¬ Rules j k
    Aspect : Set
    Voices : Jiva → Aspect → Set
    heard : ∀ a → Σ Jiva (λ j → Voices j a)
    no-whole-voice : ∀ j → Σ Aspect (λ a → ¬ Voices j a)

-- A support role does not assert eventual liberation (§32).
EmperorRole : (E : Empire) → Empire.Jiva E → Set
EmperorRole E j = Σ (Empire.Jiva E) (λ k → ¬ (j ≡ k) × Empire.Holds E j k)

data Three : Set where
  a b c : Three

H : Three → Three → Set
H a b = ⊤
H b c = ⊤
H c a = ⊤
H _ _ = ⊥

missing : ∀ j → Σ Three (λ k → ¬ (j ≡ k))
missing a = c , (λ ())
missing b = a , (λ ())
missing c = b , (λ ())

-- These fields specify model obligations. The concrete instance below
-- provides evidence that they can be satisfied together.
empireWith : (Three → Three → Set) → Empire
empireWith holds = record
  { Jiva = Three ; member = a ; Holds = holds
  ; Rules = λ _ _ → ⊥ ; no-throne = λ _ _ x → x
  ; Aspect = Three ; Voices = _≡_
  ; heard = λ j → j , refl ; no-whole-voice = missing
  }

threeEmpire : Empire
threeEmpire = empireWith H

-- Support MAY be nontransitive. This refutes a universal transitivity requirement;
-- it does NOT derive nontransitivity from the absence of a throne.
threeEmpire-not-transitive :
  ¬ (∀ x y z → Empire.Holds threeEmpire x y → Empire.Holds threeEmpire y z → Empire.Holds threeEmpire x z)
threeEmpire-not-transitive tr = tr a b c tt tt

-- Transitive support is also consistent with no authority and no complete voice.
-- Even supporting everyone gives no right to decide for them.
allSupportEmpire : Empire
allSupportEmpire = empireWith (λ _ _ → ⊤)

allSupport-transitive : ∀ x y z → Empire.Holds allSupportEmpire x y →
  Empire.Holds allSupportEmpire y z → Empire.Holds allSupportEmpire x z
allSupport-transitive _ _ _ _ _ = tt

supports-all : ∀ j k → Empire.Holds allSupportEmpire j k
supports-all _ _ = tt

a-supports : EmperorRole threeEmpire a
a-supports = b , (λ ()) , tt

-- One recipient supports no one else. The network is nevertheless nonempty
-- and connected by support: each of the three participants has another supporter.
ReceivingH : Three → Three → Set
ReceivingH a b = ⊤
ReceivingH a c = ⊤
ReceivingH c a = ⊤
ReceivingH _ _ = ⊥

receivingEmpire : Empire
receivingEmpire = empireWith ReceivingH

b-no-support-role : ¬ EmperorRole receivingEmpire b
b-no-support-role (k , distinct , impossible) = impossible

all-receive-support : ∀ j → Σ Three (λ k → ¬ (j ≡ k) × ReceivingH k j)
all-receive-support a = c , (λ ()) , tt
all-receive-support b = a , (λ ()) , tt
all-receive-support c = a , (λ ()) , tt
