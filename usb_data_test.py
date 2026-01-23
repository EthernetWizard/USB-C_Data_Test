"""
USB-C / USB cable data transfer test for Windows
- Checks if the connected device appears as more than just a "charging" device
- Looks for typical data-capable USB device classes

Run this script BEFORE and AFTER plugging in the cable+device you want to test.
"""

import time
import sys
import subprocess
from datetime import datetime

try:
    import wmi
except ImportError:
    print("wmi module not found.")
    print("Please install it with:")
    print("    pip install wmi")
    sys.exit(1)


def get_usb_devices():
    """Get list of currently connected USB devices with basic info"""
    c = wmi.WMI()
    devices = []
    
    # Look at USB controllers + composite devices + hubs + storage + CDC devices etc.
    for dev in c.Win32_PnPEntity():
        if not dev.DeviceID:
            continue
        if "USB\\" not in dev.DeviceID.upper():
            continue
            
        name = dev.Name or "Unnamed"
        desc = dev.Description or ""
        status = dev.Status or "?"
        devid = dev.DeviceID
        
        # Try to get more readable vendor/product if possible
        vid_pid = ""
        if "VID_" in devid and "PID_" in devid:
            parts = devid.upper().split("\\")
            for part in parts:
                if "VID_" in part and "PID_" in part:
                    vid_pid = part
                    break
        
        devices.append({
            "name": name,
            "desc": desc,
            "status": status,
            "vid_pid": vid_pid,
            "device_id": devid
        })
    
    return devices


def print_devices(devices, title=""):
    if title:
        print(f"\n{title}")
        print("-" * 70)
    
    if not devices:
        print("No USB devices found.")
        return
    
    for d in sorted(devices, key=lambda x: x["name"] or ""):
        extra = ""
        if "COMPOSITE" in d["device_id"].upper():
            extra = "(composite)"
        elif "STORAGE" in d["device_id"].upper() or "DISK" in d["desc"].upper():
            extra = "← HAS DATA (MTP/SCSI/Mass Storage)"
        elif "CDC" in d["device_id"].upper() or "SERIAL" in d["desc"].upper():
            extra = "← HAS DATA (serial / modem / ECM)"
        elif "HUB" in d["desc"].upper():
            extra = "(hub)"
            
        line = f"{d['name'][:48]:<48} {d['vid_pid']:<18} {extra}"
        print(line)


def main():
    print("USB-C cable data transfer test")
    print("───────────────────────────────")
    print("1. Disconnect the cable/device you want to test")
    print("2. Run this script once (press Enter when ready)")
    input("   Press Enter to scan without the test device... ")
    
    before = get_usb_devices()
    print_devices(before, "Devices BEFORE connecting the cable/device:")
    
    print("\n" + "="*70)
    print("Now connect your USB-C cable + phone / drive / whatever you want to test")
    print("Wait 5–10 seconds until Windows finishes recognizing the device")
    input("Press Enter when the device is connected and recognized... ")
    
    after = get_usb_devices()
    print_devices(after, "Devices AFTER connecting:")
    
    print("\n" + "="*70)
    print("Comparison / Interpretation:")
    print()
    
    before_ids = {d["device_id"] for d in before}
    new_devices = [d for d in after if d["device_id"] not in before_ids]
    
    if not new_devices:
        print("→ No new USB devices detected!")
        print("  Most likely the cable is CHARGE-ONLY")
        return
    
    has_data_indicators = False
    
    for dev in new_devices:
        if any(x in dev["desc"].upper() for x in ["MTP", "MASS", "STORAGE", "DISK", "CDC", "SERIAL", "COMPOSITE", "ECM", "RNDIS"]):
            has_data_indicators = True
            print("→ FOUND DATA CAPABLE DEVICE:", dev["name"])
            print("  Description:", dev["desc"])
            print("  VID:PID   ", dev["vid_pid"])
            print()
    
    if has_data_indicators:
        print("CONCLUSION: This cable most likely SUPPORTS DATA TRANSFER")
    else:
        print("→ New device appeared, but no clear data-class detected")
        print("  → possibly charge-only cable with very limited identification")
        print("  → or unusual device that Windows doesn't recognize properly")
    
    print("\nTip: also check in File Explorer / This PC whether any new drive or phone appears")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped by user.")
    except Exception as e:
        print("Error:", str(e))
        print("Try running as Administrator if you get permission issues.")