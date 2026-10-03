import os

# إنشاء الهيكلية الأساسية للمشروع
directories = [
    ".github/workflows",
    "config/rules",
    "desktop/assets",
    "frontend/src/app",
    "src/api",
    "src/audit",
    "src/core",
    "src/crm",
    "src/data_quality",
    "src/db",
    "src/engines",
    "src/models",
    "src/reporting",
    "src/security",
    "src/utils",
    "tests"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"Created directory: {directory}")

print("\nFRCS V5 Directory Structure Created Successfully.")