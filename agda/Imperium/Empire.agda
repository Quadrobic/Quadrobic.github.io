{-# OPTIONS --safe --without-K #-}

module Imperium.Empire where

open import Data.Empty using (⊥)
open import Data.Unit using (⊤; tt)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_)

-- Опора, власть над чужим Руслом и полнота голоса — РАЗНЫЕ отношения.
-- Rules означает присвоенное право решать за чужое Русло, а не временное
-- распределение задач общего дела (§35).
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

-- Роль опоры не утверждает окончательного оттаивания (§32).
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

-- Эти поля задают обязательства модели. Конкретный экземпляр ниже
-- предъявляет доказательства их совместной выполнимости.
empireWith : (Three → Three → Set) → Empire
empireWith holds = record
  { Jiva = Three ; member = a ; Holds = holds
  ; Rules = λ _ _ → ⊥ ; no-throne = λ _ _ x → x
  ; Aspect = Three ; Voices = _≡_
  ; heard = λ j → j , refl ; no-whole-voice = missing
  }

threeEmpire : Empire
threeEmpire = empireWith H

-- Опора МОЖЕТ быть нетранзитивной. Это контрмодель универсальному
-- требованию транзитивности, а НЕ вывод нетранзитивности из отсутствия трона.
threeEmpire-not-transitive :
  ¬ (∀ x y z → Empire.Holds threeEmpire x y → Empire.Holds threeEmpire y z → Empire.Holds threeEmpire x z)
threeEmpire-not-transitive tr = tr a b c tt tt

-- И транзитивная опора совместима с отсутствием власти и целого голоса.
-- Даже возможность держать всех не даёт права решать за них.
allSupportEmpire : Empire
allSupportEmpire = empireWith (λ _ _ → ⊤)

allSupport-transitive : ∀ x y z → Empire.Holds allSupportEmpire x y →
  Empire.Holds allSupportEmpire y z → Empire.Holds allSupportEmpire x z
allSupport-transitive _ _ _ _ _ = tt

supports-all : ∀ j k → Empire.Holds allSupportEmpire j k
supports-all _ _ = tt

a-supports : EmperorRole threeEmpire a
a-supports = b , (λ ()) , tt

-- Есть получатель опоры, который сам не держит других. Сеть при этом
-- не пуста и не распалась: у каждой из трёх Джив есть другая опора.
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
