{-# OPTIONS --safe --without-K #-}

module Imperium.Roles where

open import Imperium.Core
open import Imperium.Signs
open import Imperium.Empire
open import Data.Nat using (ℕ; s≤s; z≤n)
open import Data.Product using (Σ; _×_; _,_; proj₁; proj₂)
open import Relation.Binary.PropositionalEquality using (refl)
open import Relation.Nullary using (¬_)

-- §32: роль включает реальную опору другим, не только видимые оценки.
-- Это ограниченная формальная версия признания; наблюдения не всеведущи.
EmperorStatus : (E : Empire) → (Empire.Jiva E → Life) → Empire.Jiva E → ℕ → ℕ → Set
EmperorStatus E lives j s k = EmperorRole E j × Recognized (Life.observed (lives j)) s k

emperor-⇏-siddha : ¬ (∀ E lives j s k → EmperorStatus E lives j s k → Siddha (Life.acts (lives j)))
emperor-⇏-siddha f = calm-gripping-not-siddha
  (f threeEmpire (λ _ → calm-gripping) a 0 1
    (a-supports , calm-gripping-recognized 0 1 (s≤s z≤n)))

-- Здесь наблюдения даже удовлетворяют критерию. Отсутствует именно роль
-- поддержки: не всякое собственное движение ведёт держать чужие Русла.
free-visible : Life
free-visible = record { acts = λ _ → flow ; observed = λ _ → mkObs 0 0 0 }

free-visible-siddha : Siddha (Life.acts free-visible)
free-visible-siddha = 0 , (λ _ _ → refl)

siddha-⇏-emperor : ¬ (∀ E lives j s k → Siddha (Life.acts (lives j)) → EmperorStatus E lives j s k)
siddha-⇏-emperor f = b-no-support-role
  (proj₁ (f receivingEmpire (λ _ → free-visible) b 0 1 free-visible-siddha))

-- Обратимо и признание роли целиком, даже если способность поддержать осталась.
revocable-status : Σ (Three → Life) (λ lives →
  EmperorStatus threeEmpire lives a 0 1 × ¬ EmperorStatus threeEmpire lives a 1 1)
revocable-status with revocable
... | o , initial , withdrawn =
  (λ _ → record { acts = λ _ → grip ; observed = o }) ,
  (a-supports , initial) , (λ status → withdrawn (proj₂ status))
