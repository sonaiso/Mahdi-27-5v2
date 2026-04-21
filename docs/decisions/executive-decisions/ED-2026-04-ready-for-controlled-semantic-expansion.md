# قرار تنفيذي — Ready for Controlled Semantic Expansion (v1)

**التاريخ:** 2026-04-21  
**الحالة المعتمدة:** Architecturally Verified, Operationally Stable, and Ready for Controlled Semantic Expansion

## 1) قرارات المرحلة

1. **`reference_predication` تبقى مستقلة الآن**  
   - دون دمج مباشر داخل `MasterChain`  
   - عبر واجهة ثابتة  
   - مع Feature Flag  
   - ومع Trace واضح

2. **R4 وR12 مخففان تقنيًا ومفتوحان حوكميًا حتى اكتمال الإغلاق الرسمي**  
   - اختبارات الحواف والمخاطر  
   - تحديث وثائقي صريح  
   - CI Gate للنطاق المستهدف كـ required scoped gate

3. **تصنيف النوى الرسمي (بالترتيب المعتمد)**  
   - Language → **Core**  
   - Qiyas → **Core**  
   - Semantic Kernel → **Transitional**

4. **ترتيب baseline المرجعي-الإسنادي**  
   - Σ1 → G_i → I^(2)  
   - ثم مراجعة ختامية: **Ready for Controlled Semantic Expansion**

## 2) معيار الإغلاق الرسمي لـ R4 / R12

### أ) الاختبارات
- Edge cases
- Failure modes
- Threshold behavior
- Regression safety

### ب) الوثائق
- ما الذي اختُبر
- ما الذي لم يُختبر
- حدود الثقة
- المعايير المعتمدة

### ج) CI Gate
- نجاح suite المحددة للنطاق
- عدم تراجع التغطية في النطاق المستهدف (via coverage floor)
- منع الدمج عند فشل suite الخاصة بـ R4/R12 (required scoped status check)
- lint/type checks: غير متوفرة حاليًا في المشروع

## 3) تعريف النجاح في هذه الدورة

- R4 = Technically mitigated, governance-open pending formal evidence closure
- R12 = Technically mitigated, governance-open pending formal evidence closure
- `reference_predication` = مستقلة + واجهة ثابتة + Feature Flag + Trace
- تصنيف Language/Qiyas/Semantic Kernel = موثق ومعتمد
- جاهزية انتقال منضبط إلى التوسعة الدلالية

## 4) ملحق القرارات الحاسمة قبل التنفيذ

1. **`r4-r12-gate` بوابة مستقلة ومطلوبة على فرع الدمج الرئيسي**  
   - أي PR يمس نطاق: `arabic_engine/reference_predication/**` أو `tests/test_sigma2.py` أو وحدات العتبات أو اختبارات المخاطر لا يُقبل إلا بعد نجاح البوابة.
   - التفعيل الحوكمـي يتم عبر Branch Protection/Ruleset بتعيين check: `r4-r12-gate` كـ required.

2. **صيغة رسمية ثابتة لمصفوفة ربط المخاطر بالاختبارات**  
   - المرجع الرسمي: `docs/risks/risk-to-test-matrix_v1.md`
   - الأعمدة المعتمدة:  
     `Risk ID | Scope | Required Tests | Failure Modes Covered | Acceptance Criteria | Gate`

3. **جدول إنهاء `grammatical_factor` النصي legacy**  
   - الدورة الحالية: قبول legacy + تحويل داخلي + warning.  
   - الدورة التالية: منع أي استخدام داخلي مباشر للـ string form.  
   - نهاية الدورة التالية: منعه من الواجهة العامة إلا بطبقة adapter صريحة.  
   - بعد ذلك: إزالة الدعم القديم.  
   - **القاعدة المختصرة:** نافذة توافق = إصدار واحد كامل + دورة إزالة واحدة.

4. **اعتماد Threshold Bundle v1 قبل التطوير وعدم تغييره داخل الدورة**  
   - المرجع التنفيذي: `arabic_engine/reference_predication/thresholds.py`
   - الحالة: **v1 locked for this cycle**

5. **معيار المبرر التنفيذي الكافي لدمج `reference_predication` داخل `MasterChain`**  
   - لا دمج قبل تحقق الشروط الأربعة معًا:
     - Risk Closure
     - Baseline Stability
     - Contract Safety
     - Traceability
