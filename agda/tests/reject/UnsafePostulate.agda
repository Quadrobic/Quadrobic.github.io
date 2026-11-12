{-# OPTIONS --safe --without-K #-}
module UnsafePostulate where
open import Data.Empty using (⊥)
postulate bad : ⊥
