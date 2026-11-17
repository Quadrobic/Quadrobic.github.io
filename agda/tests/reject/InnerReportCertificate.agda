{-# OPTIONS --safe --without-K #-}
module InnerReportCertificate where
open import Imperium.Witness
open import Relation.Binary.PropositionalEquality using (_≡_; refl)

-- An alive report does not certify that its underlying act is flowing.
inner-check : Feeling → Verdict
inner-check alive = flowing
inner-check stuck = binding

bad : inner-check (Observation.feeling hidden-grip) ≡ verdict (Observation.action hidden-grip)
bad = refl
