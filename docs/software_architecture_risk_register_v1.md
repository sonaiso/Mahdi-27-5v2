# سجل مخاطر المعمارية البرمجية v1
## Software Architecture Risk Register v1

> **Repository Path:** `docs/software_architecture_risk_register_v1.md`

---

## فهرس المحتويات

1. [الغرض](#الغرض)
2. [منهج التقييم](#منهج-التقييم)
3. [سجل المخاطر](#سجل-المخاطر)
4. [الأولويات التنفيذية](#الأولويات-التنفيذية)
5. [معايير الإغلاق](#معايير-الإغلاق)

---

## الغرض

هذه الوثيقة تسجل المخاطر المعمارية العليا في المشروع، وتحدد:

- موضع كل خطر
- أثره
- احتماله
- شدته
- مؤشرات ظهوره
- العلاج المقترح
- أولوية المعالجة

---

## منهج التقييم

### مقياس الاحتمال

| الدرجة | الوصف |
|--------|-------|
| 1 | منخفض |
| 2 | متوسط |
| 3 | عالٍ |

### مقياس الأثر

| الدرجة | الوصف |
|--------|-------|
| 1 | منخفض |
| 2 | متوسط |
| 3 | عالٍ |

### الشدة

$$
RiskScore = Probability \times Impact
$$

| النطاق | التصنيف |
|--------|---------|
| 1–2 | منخفض |
| 3–4 | متوسط |
| 6–9 | حرج |

---

## سجل المخاطر

| ID | الخطر | الوصف | الاحتمال | الأثر | الشدة | المؤشرات | العلاج |
|----|-------|-------|----------|-------|-------|----------|--------|
| R1 | تضخم `core` | تراكم enums/types/contracts/traces في مركز واحد حتى يفقد وضوحه الدلالي | 3 | 3 | 9 حرج | صعوبة التتبع، تكرار الأسماء، تضارب state models | تقسيم `core` إلى نوى فرعية: `core/gates`, `core/trace`, `core/judgement`, `core/singular`, `core/weight` |
| R2 | تعدد السلاسل | وجود أكثر من pipeline/chain/runtime path بلا Master Chain واضحة | 3 | 3 | 9 حرج | اختلاف معاني النجاح/الفشل/التعليق، trace متعددة | تعريف سلسلة سيادية واحدة، وتحويل البقية إلى adapters أو projections |
| R3 | فجوة تطبيق العقود | وجود contracts أقوى من التنفيذ الفعلي | 3 | 3 | 9 حرج | YAML غني لكن enforcement جزئي، mismatch غير مكتشف | تفعيل adjacency + invariants + runtime enforcement |
| R4 | عدم اكتمال الحواف والقيود | build_constraint_edges / validators / edge cases غير مغلقة | 3 | 3 | 9 حرج | نتائج صحيحة مركزيًا لكن غير ثابتة حدّيًا | بناء boundary suite + constraint edge audit + exception path tests |
| R5 | غياب تحرير المفرد | خلط التصور المفرد والمعلومة المفردة والمفهوم المفرد | 3 | 3 | 9 حرج | القفز من unicode إلى التركيب أو المفهوم | إنشاء `singular/` كنواة مستقلة بثلاث طبقات closure |
| R6 | غياب رتبة الوزن | الوزن يعامل كطبقة صرفية لا كشرط إمكان بنيوي | 3 | 3 | 9 حرج | فساد الاشتقاق، اضطراب built/inflected, noun/verb/particle legality | إنشاء `weight/` كنواة سيادية قبل composition |
| R7 | خلط التركيب بالتعيين | التركيب يعامل كتجميع أو parsing لا كتوزيع أدوار | 3 | 3 | 9 حرج | syntax labels بلا role-distribution semantics | إنشاء `composition/roles` + `relations/asnadi,tadmini,taqyidi` |
| R8 | القفز من القضية إلى الحكم | proposition closure تُعامل كأنها judgement | 2 | 3 | 6 حرج | أحكام بلا جهة أو معيار أو trace chain كاملة | فصل proposition/judgement transition بدستور ومحرك مستقل |
| R9 | trace غير مغلقة تمامًا | replay / hash / evidence / edge cases غير مكتملة | 2 | 3 | 6 حرج | mismatch غير مفسر، replay جزئي أو هش | توحيد trace model + replay tests + failure semantics |
| R10 | التوسع قبل الغلق | API/DB/AI integration قبل إغلاق القلب الرمزي | 3 | 2 | 6 حرج | أعمال كثيرة outward-facing مع قلب غير ثابت | منع أي توسعة تشغيلية قبل إغلاق singular + weight + composition + judgement |
| R11 | تضارب taxonomy | تعدد مفاهيم الحالة والقرار والانتقال دون mapping صارم | 2 | 3 | 6 حرج | SUSPEND/REJECT/INVALID/PENDING... بلا ربط واضح | Unified State Model + mapping tests |
| R12 | اختبارات عددية لا بنيوية | كثرة الاختبارات مع ضعف نسبي في النقاط الحرجة | 2 | 3 | 6 حرج | coverage مقبولة لكن الحواف ضعيفة | تحويل strategy من count-driven إلى risk-driven |

---

## الأولويات التنفيذية

### أولوية قصوى (الشدة 9)

| ID | الخطر |
|----|-------|
| R1 | تضخم `core` |
| R2 | تعدد السلاسل |
| R3 | فجوة تطبيق العقود |
| R5 | غياب تحرير المفرد |
| R6 | غياب رتبة الوزن |
| R7 | خلط التركيب بالتعيين |

### أولوية عالية (الشدة 6)

| ID | الخطر |
|----|-------|
| R4 | عدم اكتمال الحواف والقيود |
| R8 | القفز من القضية إلى الحكم |
| R9 | trace غير مغلقة تمامًا |
| R11 | تضارب taxonomy |

### أولوية متوسطة

| ID | الخطر |
|----|-------|
| R10 | التوسع قبل الغلق |
| R12 | اختبارات عددية لا بنيوية |

---

## معايير الإغلاق

لا يُعدّ الخطر مغلقًا إلا إذا تحقق الآتي:

### R1 — تضخم `core`

- [ ] تقسيم `core` إلى نوى فرعية واضحة
- [ ] اختفاء التكرار الدلالي
- [ ] وضوح domains الداخلية

### R2 — تعدد السلاسل

- [ ] وجود Master Chain واحدة
- [ ] البقية adapters فقط

### R3 — فجوة تطبيق العقود

- [ ] adjacency تعمل فعليًا
- [ ] invariants تُفحص فعليًا
- [ ] failures معللة ومفسرة

### R4 — عدم اكتمال الحواف والقيود

- [ ] boundary suite مكتمل
- [ ] constraint edge audit منفذ
- [ ] exception path tests موجودة

### R5 — غياب تحرير المفرد

- [ ] وجود `singular/perception.py`
- [ ] وجود `singular/information.py`
- [ ] وجود `singular/concept.py`
- [ ] اختبارات تمنع القفز من المفرد إلى التركيب

### R6 — غياب رتبة الوزن

- [ ] وجود `weight/mizan.py`
- [ ] وجود `weight/legality.py`
- [ ] منع أي composition من وحدة غير مقفلة وزنيًا

### R7 — خلط التركيب بالتعيين

- [ ] وجود role-distribution engine
- [ ] النسب الإسنادية/التضمينية/التقييدية ممثلة فعليًا

### R8 — القفز من القضية إلى الحكم

- [ ] فصل proposition/judgement transition بدستور واضح
- [ ] محرك مستقل للانتقال
- [ ] اختبارات تمنع القفز المباشر

### R9 — trace غير مغلقة تمامًا

- [ ] توحيد trace model
- [ ] replay tests ناجحة
- [ ] failure semantics واضحة

### R10 — التوسع قبل الغلق

- [ ] منع أي توسعة تشغيلية قبل إغلاق singular + weight + composition + judgement
- [ ] وثيقة بوابة (gate document) لأي integration خارجي

### R11 — تضارب taxonomy

- [ ] Unified State Model موثق
- [ ] mapping tests تثبت التوافق

### R12 — اختبارات عددية لا بنيوية

- [ ] تحويل strategy من count-driven إلى risk-driven
- [ ] تغطية الحواف الحرجة بأولوية

---

## التوصية النهائية

**ابدؤوا بهذه الوثيقة أولًا** لأنها تضبط **لماذا** نعيد التشكيل.
ثم انتقلوا إلى `docs/core_refactor_map_v1.md` التي تضبط **كيف** نعيده.

الخطوة التالية الأنسب: تحويل هاتين الوثيقتين إلى **خطة تنفيذ من 4 أسابيع** بأولويات أسبوعية واضحة.
