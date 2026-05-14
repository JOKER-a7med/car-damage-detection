"""
========================================
  organize_data.py
  ترتيب الداتا في فولدرات حسب الفئة
========================================
بيقرأ via_project.json من train و val
وبيكوبي كل صورة في فولدر الفئة الخاصة بيها

الناتج:
  data_multiclass/
      train/  Scratch / Dent / Dislocation / Shatter
      val/    Scratch / Dent / Dislocation / Shatter
"""

import json, os, shutil
from collections import Counter

# ─── ✏️ عدّل المسارات دي بس ──────────────────────────────────
ARCHIVE_DIR = r'D:\Downloads\Compressed\archive_4'   # ← مسار archive_4
OUTPUT_DIR  = r'D:\car_damage_project\data_multiclass'  # ← الناتج
# ─────────────────────────────────────────────────────────────

CLASSES = ['Scratch', 'Dent', 'Dislocation', 'Shatter']


def organize_split(src_dir, dst_dir, split_name):
    json_path = os.path.join(src_dir, 'via_project.json')

    if not os.path.exists(json_path):
        print(f"  ⚠️  مفيش via_project.json في {src_dir} — بيتخطى")
        return {}

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)

    counters = Counter()
    missing  = []

    for key, info in data.items():
        filename = info['filename']
        regions  = info['regions']

        if not regions:
            continue

        # الفئة الغالبة في الصورة
        labels   = [r['region_attributes'].get('damage', '') for r in regions]
        dominant = Counter(labels).most_common(1)[0][0]

        if dominant not in CLASSES:
            continue

        class_dir = os.path.join(dst_dir, dominant)
        os.makedirs(class_dir, exist_ok=True)

        src = os.path.join(src_dir, filename)
        dst = os.path.join(class_dir, filename)

        if os.path.exists(src):
            shutil.copy2(src, dst)
            counters[dominant] += 1
        else:
            missing.append(filename)

    print(f"\n  ✅ {split_name}:")
    for cls in CLASSES:
        print(f"     {cls:15s}: {counters[cls]:3d} صورة")
    if missing:
        print(f"     ⚠️  مش موجودة: {missing[:5]}{'...' if len(missing)>5 else ''}")

    return counters


# ─── تنفيذ ────────────────────────────────────────────────────
print("=" * 50)
print("  تنظيم الداتا للـ Multi-Class Training")
print("=" * 50)

train_counts = organize_split(
    os.path.join(ARCHIVE_DIR, 'train'),
    os.path.join(OUTPUT_DIR,  'train'),
    'Train'
)

val_counts = organize_split(
    os.path.join(ARCHIVE_DIR, 'val'),
    os.path.join(OUTPUT_DIR,  'val'),
    'Validation'
)

print(f"\n✅ الداتا اتحفظت في: {OUTPUT_DIR}")
print(f"\nجاهز للتدريب! شغّل train_multiclass.py")
