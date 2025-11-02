from setuptools import setup, find_packages

# هذا الملف بيساعد خدمات النشر (مثل Render/Heroku) إنها تعرف وين مكان ملفات المشروع الرئيسية
# ويخليها تشوف ملف requirements.txt صح.

setup(
    name='car_tracker_system',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        # بيتم استيراد كل المتطلبات من ملف requirements.txt
    ],
    # تحديد مسار المشروع ليكون داخل Car_Tracker
    package_dir={'': 'Car_Tracker'},
)
