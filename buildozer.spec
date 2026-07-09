[app]
title = 4K Upscaler Free
package.name = upscaler
package.domain = com.bossmyapp
source.dir = .
source.include_exts = py,png,jpg
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.1.1,Pillow,opencv-python,numpy
orientation = portrait
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES,READ_MEDIA_VIDEO
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2
warn_on_root = 1
