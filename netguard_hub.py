import ctypes
import numpy as np
from bidi.algorithm import get_display
from concurrent.futures import ThreadPoolExecutor
import socket

def ar_print(text):
    print(get_display(text))

# ربط المكتبات المحدثة
lib_c = ctypes.CDLL('./libnetguard.so')
import cryptomod

ar_print("\n=============================================")
ar_print(" 🛡️  NetGuard-Hub v2.8: مدمج بميزة المسار IP-Route")
ar_print("=============================================")

# 1. جلب بوابة الشبكة (Gateway) من موديول الـ C بدلاً من أوامر النظام المخترقة
gateway_buffer = ctypes.create_string_buffer(50)
if lib_c.get_default_gateway(gateway_buffer):
    detected_gateway = gateway_buffer.value.decode()
    ar_print(f"[+] مسار الشبكة المكتشف (IP Route Gateway): {detected_gateway}")
else:
    detected_gateway = "192.168.1.1"
    ar_print("[-] لم يتم جلب المسار الافتراضي، استخدام الافتراضي: 192.168.1.1")

# تحديد نطاق الشبكة ديناميكياً بناءً على الـ Gateway المكتشفة
ip_prefix = ".".join(detected_gateway.split(".")[:3]) + "."
ar_print(f"[*] جاري فحص النطاق تلقائياً: {ip_prefix}1 إلى {ip_prefix}254")

alive_devices = []

def scan_ip(ip_target):
    if lib_c.is_device_alive(ip_target.encode('utf-8')):
        return ip_target
    return None

# 2. اصطياد الأجهزة المتصلة
ar_print("\n[*] جاري البحث عن الأجهزة المتصلة بالشبكة...")
with ThreadPoolExecutor(max_workers=50) as executor:
    ips_to_scan = [f"{ip_prefix}{i}" for i in range(1, 255)]
    results = executor.map(scan_ip, ips_to_scan)
    for res in list(results):
        if res:
            alive_devices.append(res)
            ar_print(f"[+] جهاز نشط مكتشف: {res}")

if not alive_devices:
    alive_devices = [detected_gateway]

# 3. فحص كامل المنافذ (1-65535) للأجهزة النشطة
discovered_data = {}

def scan_single_port(args):
    ip, port = args
    if lib_c.check_port_status(ip.encode('utf-8'), port):
        return port
    return None

for device in alive_devices:
    ar_print(f"\n[*] جاري فحص كامل المنافذ (1-65535) للجهاز: {device}...")
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=500) as port_executor:
        port_tasks = [(device, p) for p in range(1, 65536)]
        port_results = port_executor.map(scan_single_port, port_tasks)
        for p_res in port_results:
            if p_res:
                open_ports.append(p_res)
                ar_print(f"    [!] منفذ مفتوح تم رصده: {p_res}")
                
    discovered_data[device] = open_ports

# 4. تشغيل محرك فورتراين العمودي (كودك الصافي المثالي)
ar_print("\n[*] ثالثاً: تشغيل محرك فك التجزئة الحسابي عبر Fortran العمودي الخارق...")
wordlist = ["test", "pass", "root", "hack"]
matrix = np.array([[ord(c) for c in w] for w in wordlist], dtype=np.int32)
target_hash = 452

found_idx = cryptomod.batch_crack(matrix.T, target_hash)

if found_idx > 0:
    actual_index = found_idx - 1
    ar_print(f"[+] محرك Fortran وجد الكلمة بنجاح في السطر: {found_idx}")
    ar_print(f"[+] الكلمة المخترقة هي: '{wordlist[actual_index]}'")
else:
    ar_print("[-] لم يتم العثور على أي تطابق الحسابات.")

# 5. بناء تقرير الـ HTML الموسع وحفظه مباشرة في الـ Download
html_sections = ""
for device, ports in discovered_data.items():
    ports_str = ", ".join(map(str, ports)) if ports else "لا توجد منافذ مفتوحة نشطة"
    html_sections += f"""
    <div style="background: #252525; padding: 15px; border-radius: 6px; margin-bottom: 15px; border-right: 4px solid #00ff66; text-align: right;">
        <h3 style="margin: 0 0 10px 0; color: #00ff66;">🖥️ الجهاز: {device}</h3>
        <p style="margin: 5px 0; color: #ccc;"><b>كامل المنافذ المفتوحة المكتشفة (1-65535):</b></p>
        <div style="background: #121212; padding: 10px; border-radius: 4px; font-family: monospace; word-wrap: break-word; color: #00ff66; direction: ltr;">
            {ports_str}
        </div>
    </div>
    """

html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تقرير فحص الشبكة والمسارات</title>
</head>
<body style="background-color: #121212; color: #ffffff; font-family: system-ui, sans-serif; margin: 0; padding: 15px;">
    <div style="max-width: 600px; margin: 0 auto; background: #1e1e1e; padding: 20px; border-radius: 8px;">
        <h2 style="color: #00ff66; border-bottom: 2px solid #333; padding-bottom: 10px; margin-top: 0;">🛡️ خريطة مسار الشبكة NetGuard</h2>
        <p style="color: #00ff66; font-size: 15px;"><b>البوابة الافتراضية المكتشفة (IP Route Gateway): {detected_gateway}</b></p>
        <hr style="border: 0; border-top: 1px solid #333; margin: 15px 0;">
        {html_sections}
    </div>
</body>
</html>"""

with open("/sdcard/Download/report.html", "w", encoding="utf-8") as f:
    f.write(html_content)

ar_print("\n[+] انتهى الفحص الكامل بنجاح!")
ar_print("[+] التقرير مدمجاً بمعلومات الـ Route بانتظارك في مجلد Download.")
ar_print("=============================================")
