import asyncio
from bleak import BleakScanner, BleakClient

# ============================
# Standard BLE UUIDs
# ============================

HEART_RATE_SERVICE = "0000180d-0000-1000-8000-00805f9b34fb"
HEART_RATE_CHAR = "00002a37-0000-1000-8000-00805f9b34fb"

BATTERY_SERVICE = "0000180f-0000-1000-8000-00805f9b34fb"
BATTERY_CHAR = "00002a19-0000-1000-8000-00805f9b34fb"


# ============================
# Manual fallback
# ============================

def manual_fill(data):
    print("\n⚠️ Some health metrics are not available via Bluetooth.")
    print("Please enter missing values manually (press Enter to skip):\n")

    prompts = {
        "spo2": "Blood Oxygen SpO₂ (%)",
        "sleep_hours": "Sleep duration (hours)",
        "stress_level": "Stress level (low / medium / high)",
        "steps": "Steps walked today",
        "distance_km": "Distance walked (km)",
        "calories": "Calories burned"
    }

    for key, label in prompts.items():
        if data[key] is None:
            val = input(f"{label}: ").strip()
            data[key] = val if val else None

    return data


# ============================
# Main BLE Logic
# ============================

async def main():
    print("\n🔍 Scanning for nearby BLE devices (10 seconds)...\n")
    devices = await BleakScanner.discover(timeout=10)

    if not devices:
        print("❌ No Bluetooth devices found.")
        return

    print("📡 Found Devices:\n")
    for i, d in enumerate(devices):
        print(f"[{i}] {d.name or 'BLE Device (Name Hidden)'} | {d.address}")

    try:
        idx = int(input("\nSelect device number: "))
        device = devices[idx]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    print(f"\n🔗 Connecting to {device.name or 'Selected BLE Device'}...\n")

    health_data = {
        "device_name": device.name or "Unknown BLE Device",
        "heart_rate": None,
        "battery": None,
        "spo2": None,
        "sleep_hours": None,
        "stress_level": None,
        "steps": None,
        "distance_km": None,
        "calories": None,
        "source": "ble/manual"
    }

    try:
        # ----------------------------
        # CONNECT & KEEP ALIVE
        # ----------------------------
        async with BleakClient(device.address) as client:
            await client.connect()

            if not client.is_connected:
                print("❌ Bluetooth connection failed.")
                return

            print("✅ Bluetooth connected successfully.\n")

            # ----------------------------
            # DISCOVER SERVICES
            # ----------------------------
            services = await client.get_services()
            service_uuids = [s.uuid.lower() for s in services]

            print("🔍 Discovered Services:")
            for s in service_uuids:
                print(" -", s)
            print()

            # ----------------------------
            # HEART RATE
            # ----------------------------
            if HEART_RATE_SERVICE in service_uuids:
                try:
                    raw = await client.read_gatt_char(HEART_RATE_CHAR)
                    health_data["heart_rate"] = raw[1]
                    print(f"❤️ Heart Rate (BLE): {health_data['heart_rate']} bpm")
                except Exception as e:
                    print("⚠️ Heart rate read failed:", e)
            else:
                print("ℹ️ Heart Rate service not supported.")

            # ----------------------------
            # BATTERY LEVEL
            # ----------------------------
            if BATTERY_SERVICE in service_uuids:
                try:
                    raw = await client.read_gatt_char(BATTERY_CHAR)
                    health_data["battery"] = raw[0]
                    print(f"🔋 Battery Level (BLE): {health_data['battery']} %")
                except Exception as e:
                    print("⚠️ Battery read failed:", e)
            else:
                print("ℹ️ Battery service not supported.")

            # ----------------------------
            # INFO
            # ----------------------------
            print("\nℹ️ SpO₂, sleep, stress, steps, distance, calories")
            print("   are not exposed via standard BLE on most smartwatches.")

            # ----------------------------
            # KEEP CONNECTION ALIVE
            # ----------------------------
            print("\n🔒 Bluetooth connection is ACTIVE.")
            print("Press ENTER when you want to disconnect...\n")

            # Wait for user input without blocking event loop
            await asyncio.get_event_loop().run_in_executor(None, input)

            print("\n🔌 Disconnecting from device...")

    except Exception as e:
        print("❌ BLE communication error:", e)

    # ----------------------------
    # Manual fallback
    # ----------------------------
    health_data = manual_fill(health_data)

    # ----------------------------
    # Final Output
    # ----------------------------
    print("\n📊 FINAL HEALTH DATA USED\n")
    for k, v in health_data.items():
        print(f"{k}: {v}")

    print("\n⚠️ Disclaimer: This system is NOT a medical diagnostic tool.\n")


# ============================
# Entry Point
# ============================

if __name__ == "__main__":
    asyncio.run(main())
