#!/usr/bin/env python3
"""
Patch Frigate's hailo8l.py detector plugin to add Hailo-10H support.

This script runs at Docker build time. It finds hailo8l.py inside the
Frigate image and applies targeted text replacements to:
  1. Add H10 default model constants
  2. Recognize HAILO10H architecture from hailortcli
  3. Update model selection logic for H10
"""

import os
import sys

# ── locate hailo8l.py ──────────────────────────────────────────────
SEARCH = [
    "/opt/frigate/frigate/detectors/plugins/hailo8l.py",
    "/usr/local/lib/python3.11/dist-packages/frigate/detectors/plugins/hailo8l.py",
]

target = None
for p in SEARCH:
    if os.path.exists(p):
        target = p
        break

if target is None:
    # broad search as fallback
    for root, _dirs, files in os.walk("/opt"):
        if "hailo8l.py" in files and "detectors" in root:
            target = os.path.join(root, "hailo8l.py")
            break

if target is None:
    print("ERROR: hailo8l.py not found – cannot patch", file=sys.stderr)
    sys.exit(1)

print(f"Patching {target} for Hailo-10H support …")

with open(target, "r") as fh:
    src = fh.read()

# keep original for comparison
original = src

# ── 1. Add H10 constants after the H8L ones ───────────────────────
OLD_CONSTANTS = (
    'H8L_DEFAULT_URL = "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/'
    'ModelZoo/Compiled/v2.14.0/hailo8l/yolov6n.hef"'
)
NEW_CONSTANTS = (
    'H8L_DEFAULT_URL = "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/'
    'ModelZoo/Compiled/v2.14.0/hailo8l/yolov6n.hef"\n'
    'H10_DEFAULT_MODEL = "yolov6n.hef"\n'
    'H10_DEFAULT_URL = "https://hailo-model-zoo.s3.eu-west-2.amazonaws.com/'
    'ModelZoo/Compiled/v2.15.0/hailo10h/yolov6n.hef"'
)
src = src.replace(OLD_CONSTANTS, NEW_CONSTANTS, 1)

# ── 2. Patch detect_hailo_arch() – recognise HAILO10H ─────────────
#       Must check HAILO10H *before* HAILO8 to avoid false match.
OLD_DETECT = '''\
                if "HAILO8L" in line:
                    return "hailo8l"
                elif "HAILO8" in line:
                    return "hailo8"'''
NEW_DETECT = '''\
                if "HAILO10H" in line or "HAILO10" in line:
                    return "hailo10h"
                elif "HAILO8L" in line:
                    return "hailo8l"
                elif "HAILO8" in line:
                    return "hailo8"'''
src = src.replace(OLD_DETECT, NEW_DETECT, 1)

# ── 3. Patch extract_model_name() ─────────────────────────────────
OLD_EXTRACT = '''\
            if ARCH == "hailo8":
                return H8_DEFAULT_MODEL
            else:
                return H8L_DEFAULT_MODEL'''
NEW_EXTRACT = '''\
            if ARCH == "hailo10h":
                return H10_DEFAULT_MODEL
            elif ARCH == "hailo8":
                return H8_DEFAULT_MODEL
            else:
                return H8L_DEFAULT_MODEL'''
src = src.replace(OLD_EXTRACT, NEW_EXTRACT, 1)

# ── 4. Patch check_and_prepare() download logic ───────────────────
OLD_PREPARE = '''\
                if ARCH == "hailo8":
                    self.download_model(H8_DEFAULT_URL, cached_model_path)
                else:
                    self.download_model(H8L_DEFAULT_URL, cached_model_path)'''
NEW_PREPARE = '''\
                if ARCH == "hailo10h":
                    self.download_model(H10_DEFAULT_URL, cached_model_path)
                elif ARCH == "hailo8":
                    self.download_model(H8_DEFAULT_URL, cached_model_path)
                else:
                    self.download_model(H8L_DEFAULT_URL, cached_model_path)'''
src = src.replace(OLD_PREPARE, NEW_PREPARE, 1)

# ── 5. Enable shared VDevice for parallel device access ────────────
#       Required so Frigate + VLM (or other Hailo apps) can share the
#       Hailo-10H concurrently.  Uses the standard Hailo constant "SHARED".
OLD_VDEVICE = '''        params = VDevice.create_params()
        params.scheduling_algorithm = HailoSchedulingAlgorithm.ROUND_ROBIN'''
NEW_VDEVICE = '''        params = VDevice.create_params()
        params.scheduling_algorithm = HailoSchedulingAlgorithm.ROUND_ROBIN
        params.group_id = "SHARED"'''
src = src.replace(OLD_VDEVICE, NEW_VDEVICE, 1)

# ── 6. Update HailoDetectorConfig docstring ────────────────────────
src = src.replace(
    "Hailo-8/Hailo-8L detector using HEF models and the HailoRT SDK",
    "Hailo-8/Hailo-8L/Hailo-10H detector using HEF models and the HailoRT SDK",
)
src = src.replace(
    'title="Hailo-8/Hailo-8L"',
    'title="Hailo-8/Hailo-8L/Hailo-10H"',
)

# ── verify changes were applied ────────────────────────────────────
if src == original:
    print("WARNING: No changes applied – plugin may have changed upstream",
          file=sys.stderr)
    sys.exit(1)

with open(target, "w") as fh:
    fh.write(src)

print("✓ hailo8l.py patched successfully")
