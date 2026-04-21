# قرار تنفيذي — Ready for Controlled Semantic Expansion (v1)

**التاريخ:** 2026-04-21  
**الحالة المعتمدة:** Architecturally Verified, Operationally Stable, and Ready for Controlled Semantic Expansion

## 1) قرارات المرحلة

1. **`reference_predication` تبقى مستقلة الآن**  
   - دون دمج مباشر داخل `MasterChain`  
   - عبر واجهة ثابتة  
   - مع Feature Flag  
   - ومع Trace واضح

2. **إغلاق R4 وR12 رسميًا مشروط بثلاثة عناصر معًا**  
   - اختبارات الحواف والمخاطر  
   - تحديث وثائقي صريح  
   - CI Gate للنطاق المستهدف

3. **تصنيف النوى الرسمي (بالترتيب المعتمد)**  
   - Language → **Core**  
   - Qiyas → **Core**  
   - Semantic Kernel → **Extension / Transitional Core Review**

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
- نجاح suite المطلوبة
- عدم تراجع التغطية في النطاق المستهدف (via coverage floor)
- منع الدمج عند فشل suite الخاصة بـ R4/R12
- lint/type checks: غير متوفرة حاليًا في المشروع

## 3) تعريف النجاح في هذه الدورة

- R4 = Closed (رسميًا)
- R12 = Closed (رسميًا)
- `reference_predication` = مستقلة + واجهة ثابتة + Feature Flag + Trace
- تصنيف Language/Qiyas/Semantic Kernel = موثق ومعتمد
- جاهزية انتقال منضبط إلى التوسعة الدلالية
