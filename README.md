# USB-C Data Test

A Windows diagnostic that uses Python and Windows Management Instrumentation (WMI) to compare which USB devices Windows detects before and after you connect a cable and device. This detection step is called USB enumeration. The script does not transfer a test file, measure speed, certify a cable, or verify charging or power-delivery capabilities.

## Quick start

1. In Windows, open a terminal in the folder containing `usb_data_test.py`. Use a Python environment where the `python` command is available.
2. Install the WMI package and start the script:

   ```text
   python -m pip install wmi
   python usb_data_test.py
   ```

3. With the test device disconnected, press Enter to take the first snapshot.
4. Connect the cable and device, give Windows time to detect it, then press Enter to take the second snapshot. Avoid plugging in or unplugging other USB devices between snapshots.

## Interpret the result

- **A new device appears:** Windows detected a device on this setup. That is evidence of enumeration, not proof that files can be transferred or that the cable meets a particular speed or specification.
- **No new device appears:** the result is inconclusive, even if the script suggests the cable is charge-only. Try the same port and device with a known-good data cable, check the device's USB mode, or allow more time for Windows to detect it.
- **A device appears without a recognized data-class label:** Windows saw a device, but the script did not recognize a class it uses as a hint. Confirm the device's intended function separately.

To verify a file transfer, try copying a file using a device that supports it. That can confirm the transfer worked on that setup; it does not certify the cable. Use a separate benchmark to measure throughput.
