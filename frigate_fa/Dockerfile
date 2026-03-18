# Frigate with Hailo-10H support
# Based on official Frigate image, replaces HailoRT 4.x with 5.2.0
ARG BUILD_FROM=ghcr.io/blakeblackshear/frigate:0.17.0
FROM ${BUILD_FROM}

ENV DEBIAN_FRONTEND=noninteractive

# Copy Hailo-10H packages
COPY packages/h10-hailort_5.2.0_arm64.deb /tmp/
COPY packages/hailort-5.2.0-cp311-cp311-linux_aarch64.whl /tmp/

# Remove existing HailoRT 4.x wheel and install 5.2.0
RUN pip3 uninstall -y hailort 2>/dev/null || true \
    && pip3 install --break-system-packages /tmp/hailort-5.2.0-cp311-cp311-linux_aarch64.whl \
    && rm /tmp/hailort-5.2.0-cp311-cp311-linux_aarch64.whl

# Install HailoRT 5.2.0 native libraries (overwrite 4.x)
RUN dpkg -i /tmp/h10-hailort_5.2.0_arm64.deb 2>/dev/null; \
    apt-get -qq install -f -y 2>/dev/null; \
    ldconfig; \
    rm /tmp/h10-hailort_5.2.0_arm64.deb

# Patch the Hailo detector plugin to support Hailo-10H
COPY hailo10h_patch.py /tmp/
RUN python3 /tmp/hailo10h_patch.py && rm /tmp/hailo10h_patch.py

# Labels
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION}
