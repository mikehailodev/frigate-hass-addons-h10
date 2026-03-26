#!/bin/bash
# install_hailort_h10.sh — Upstream-ready HailoRT 5.2.0 installer
# Mirrors docker/main/install_hailort.sh but for Hailo-10H
#
# This would live at docker/main/install_hailort_h10.sh in the
# blakeblackshear/frigate repo and run during CI Docker build
# for the -h10 image variant.

set -euxo pipefail

hailo_version="5.2.0"

if [[ "${TARGETARCH}" == "amd64" ]]; then
    arch="x86_64"
elif [[ "${TARGETARCH}" == "arm64" ]]; then
    arch="aarch64"
fi

# These URLs would point to wherever the H10 packages are hosted
# (e.g., frigate-nvr/hailort GitHub releases, or a Hailo CDN)
wget -qO /tmp/hailort.deb "https://github.com/frigate-nvr/hailort/releases/download/v${hailo_version}/h10-hailort_${hailo_version}_${TARGETARCH}.deb"
dpkg -i /tmp/hailort.deb || apt-get install -f -y
rm /tmp/hailort.deb
ldconfig

wget -P /wheels/ "https://github.com/frigate-nvr/hailort/releases/download/v${hailo_version}/hailort-${hailo_version}-cp311-cp311-linux_${arch}.whl"
