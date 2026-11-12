{-# OPTIONS --safe --without-K #-}

module Imperium.Signs where

open import Imperium.Core
open import Data.Nat using (ℕ; zero; suc; _≤_; _<_; _+_; _*_; pred; z≤n; s≤s)
open import Data.Nat.Properties using (≤-refl)
open import Data.Empty using (⊥)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl)
open import Relation.Nullary using (¬_)

-- Условные порядковые оценки, НЕ измерение Свабхавы или голоса Хридаи.
record Obs : Set where
  constructor mkObs
  field
    gap recovery stakes : ℕ
open Obs

Observations : Set
Observations = ℕ → Obs

record Improving (before after : Obs) : Set where
  field
    gap-narrows      : gap after ≤ gap before
    recovery-shrinks : recovery after ≤ recovery before
    stakes-widen     : stakes before ≤ stakes after

-- Минимальное наблюдаемое основание признания, не полное определение
-- Императора. Не кодирует способность держать других или доверие спутников.
-- Положительная длина исключает «признание без наблюдения».
-- Проверяются ВСЕ соседние наблюдения окна, а не только его концы.
record Recognized (o : Observations) (s k : ℕ) : Set where
  field
    duration : 0 < k
    steps : ∀ {i} → i < k → Improving (o (s + i)) (o (s + suc i))

no-zero-window : ∀ o s → ¬ Recognized o s 0
no-zero-window o s r with Recognized.duration r
... | ()

-- Последовательность положительного числа окон; k — длина каждого.
-- Это всё ещё конечное наблюдение, не знание бесконечного будущего.
record Sustained (o : Observations) (s k count : ℕ) : Set where
  field
    nonempty : 0 < count
    windows : ∀ i → i < count → Recognized o (s + i * k) k

record Life : Set where
  field
    acts : History
    observed : Observations
-- acts и observed пока независимы: верность наблюдения не постулируется.

flat : ∀ x → Improving x x
flat x = record
  { gap-narrows = ≤-refl
  ; recovery-shrinks = ≤-refl
  ; stakes-widen = ≤-refl
  }

revocable : Σ Observations (λ o → Recognized o 0 1 × ¬ Recognized o 1 1)
revocable = o , initial , withdrawn
  where
    o : Observations
    o t = mkObs (pred t) 0 0

    initial : Recognized o 0 1
    initial = record { duration = s≤s z≤n ; steps = step }
      where
        step : ∀ {i} → i < 1 → Improving (o i) (o (suc i))
        step {zero} _ = flat (mkObs 0 0 0)
        step {suc i} (s≤s ())

    withdrawn : ¬ Recognized o 1 1
    withdrawn r with Improving.gap-narrows (Recognized.steps r {0} (s≤s z≤n))
    ... | ()

-- Регресс внутри окна больше нельзя спрятать равенством конечных оценок.
interior-regression : Observations
interior-regression zero = mkObs 0 0 0
interior-regression (suc zero) = mkObs 1 0 0
interior-regression (suc (suc _)) = mkObs 0 0 0

endpoints-agree : interior-regression 0 ≡ interior-regression 2
endpoints-agree = refl

interior-not-recognized : ¬ Recognized interior-regression 0 2
interior-not-recognized r with Improving.gap-narrows (Recognized.steps r {0} (s≤s z≤n))
... | ()

calm-gripping : Life
calm-gripping = record { acts = λ _ → grip ; observed = λ _ → mkObs 0 0 0 }

calm-gripping-recognized : ∀ s k → 0 < k → Recognized (Life.observed calm-gripping) s k
calm-gripping-recognized s k positive = record
  { duration = positive ; steps = λ _ → flat (mkObs 0 0 0) }

calm-gripping-sustained : ∀ s k count → 0 < k → 0 < count →
  Sustained (Life.observed calm-gripping) s k count
calm-gripping-sustained s k count k+ count+ = record
  { nonempty = count+
  ; windows = λ i _ → calm-gripping-recognized (s + i * k) k k+
  }

calm-gripping-not-siddha : ¬ Siddha (Life.acts calm-gripping)
calm-gripping-not-siddha (T , p) = grip≢flow (p T ≤-refl)

free-unseen : Life
free-unseen = record { acts = λ _ → flow ; observed = λ t → mkObs t 0 0 }

free-unseen-siddha : Siddha (Life.acts free-unseen)
free-unseen-siddha = 0 , (λ _ _ → refl)

free-unseen-not-recognized : ¬ Recognized (Life.observed free-unseen) 0 1
free-unseen-not-recognized r with Improving.gap-narrows (Recognized.steps r {0} (s≤s z≤n))
... | ()

-- НЕ «Император = наблюдаемые числа». Это независимость двух предикатов
-- в модели со свободными наблюдениями, а не доказательство психологии сиддхи.
recognition-⇏-siddha : ¬ (∀ l s k → Recognized (Life.observed l) s k → Siddha (Life.acts l))
recognition-⇏-siddha f = calm-gripping-not-siddha
  (f calm-gripping 0 1 (calm-gripping-recognized 0 1 (s≤s z≤n)))

siddha-⇏-recognition : ¬ (∀ l s k → Siddha (Life.acts l) → Recognized (Life.observed l) s k)
siddha-⇏-recognition f = free-unseen-not-recognized (f free-unseen 0 1 free-unseen-siddha)
