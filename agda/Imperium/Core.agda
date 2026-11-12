{-# OPTIONS --safe --without-K #-}

-- Империя / Квадроберский Джайнизм — формальное ядро, этап 0.
--
-- Что здесь моделируется (§-ссылки на трактат):
--   * крия (§11) — действие в момент времени; в нём есть хватка (кашая, §9) или её нет;
--   * история Дживы — бесконечная последовательность таких действий;
--   * сиддха (§31) — «в Русле больше не нарастает лёд»: с некоторого момента хватки нет вовсе;
--   * конечное наблюдение (спутники смотрят годами, но не вечно, §31–32).
--
-- Что доказано:
--   щель             (§11) — никакое конечное прошлое не закрывает оттаивание;
--   нет-грамоты      (§31) — никакое конечное прошлое не удостоверяет сиддху.
--
-- Это одна и та же конструкция: прошлое можно продолжить и льдом, и водой.
-- ДОПУЩЕНИЕ: History допускает любое продолжение; динамика Русла пока не задана.
-- Поэтому это возможность в модели, а не доказательство доступности любого
-- будущего конкретной Дживе. Исток намеренно не вводится ни типом, ни постулатом.

module Imperium.Core where

open import Data.Nat using (ℕ; _≤_; _<_; _⊔_; _<?_)
open import Data.Nat.Properties using (m≤m⊔n; m≤n⊔m; <⇒≱; ≤-trans)
open import Data.Empty using (⊥; ⊥-elim)
open import Data.Product using (Σ; _×_; _,_)
open import Relation.Binary.PropositionalEquality using (_≡_; refl; sym; trans)
open import Relation.Nullary using (yes; no; ¬_)

------------------------------------------------------------------------
-- Крия и история

data Act : Set where
  flow : Act      -- действие из движения: оставляет опыт, не связывает следующее
  grip : Act      -- действие из хватки: след твердеет, нарастает наледь (асрава)

History : Set
History = ℕ → Act

-- Различаем «свободна начиная с T» и «когда-нибудь окончательно свободна».
-- Второе не говорит, что Джива уже сиддха в наблюдаемый момент.
SiddhaFrom : History → ℕ → Set
SiddhaFrom h T = ∀ t → T ≤ t → h t ≡ flow

EventuallySiddha : History → Set
EventuallySiddha h = Σ ℕ (SiddhaFrom h)

-- Совместимое имя для исходных теорем; точный смысл — EventuallySiddha.
Siddha : History → Set
Siddha = EventuallySiddha

siddha-from-later : ∀ h T U → T ≤ U → SiddhaFrom h T → SiddhaFrom h U
siddha-from-later h T U T≤U p t U≤t = p t (≤-trans T≤U U≤t)

-- Две истории совпадают на конечном прошлом (до момента n, не включая).
Agrees : ℕ → History → History → Set
Agrees n h h' = ∀ t → t < n → h t ≡ h' t

------------------------------------------------------------------------
-- Два продолжения одного и того же прошлого

thaw : ℕ → History → History          -- после n всегда «flow»
thaw n h t with t <? n
... | yes _ = h t
... | no  _ = flow

freeze : ℕ → History → History        -- после n всегда «grip»
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
-- Теоремы

-- §11 «Даже в самом тесном повторении остаётся щель»:
-- каким бы ни было конечное прошлое, существует продолжение, где лёд перестаёт нарастать.
shchel : ∀ h n → Σ History (λ h' → Agrees n h h' × Siddha h')
shchel h n = thaw n h , agrees-thaw n h , (n , thaw-late n h)

-- §31 «Изнутри одного дня не выдают грамоты»:
-- каким бы ни было конечное прошлое, существует продолжение, где Джива НЕ сиддха.
-- Значит, никакое конечное наблюдение не удостоверяет сиддху.
net-gramoty : ∀ h n → Σ History (λ h' → Agrees n h h' × ¬ Siddha h')
net-gramoty h n = freeze n h , agrees-freeze n h , not-siddha
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
-- Следствия о сертификатах, не только примеры продолжений.

Certifies : ℕ → History → Set
Certifies n h = ∀ h′ → Agrees n h h′ → Siddha h′

Refutes : ℕ → History → Set
Refutes n h = ∀ h′ → Agrees n h h′ → ¬ Siddha h′

no-finite-certificate : ∀ h n → ¬ Certifies n h
no-finite-certificate h n cert with net-gramoty h n
... | h′ , same , never = never (cert h′ same)

no-finite-condemnation : ∀ h n → ¬ Refutes n h
no-finite-condemnation h n refute with shchel h n
... | h′ , same , eventually = refute h′ same eventually
