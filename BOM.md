# Bill of Materials (BOM) - KozbenSal Eye Tracking System

**Project:** KozbenSal - Assistive Eye-Tracking Glasses  
**Version:** 1.0  
**Date:** July 14, 2026  
**Author:** Nurtas Ulagat (nurtasulagat@gmail.com)

---

## Hardware Components

| Component | Quantity | Description | Estimated Cost (USD) | Purpose | Source/Model |
|-----------|----------|-------------|---------------------|---------|--------------|
| **PS3 Eye Camera** | 1 | USB webcam with 640x480@60fps, wide FOV | $5-10 | Eye tracking capture | Sony PlayStation Eye |
| **Raspberry Pi 4** | 1 | 4GB RAM model (or higher) | $35-45 | Main processing unit | Raspberry Pi Foundation |
| **MicroSD Card** | 1 | 32GB+ Class 10 | $8-12 | OS and software storage | SanDisk/Samsung |
| **Power Bank** | 1 | 10,000mAh, USB-C output | $15-20 | Portable power supply | Anker/Xiaomi |
| **USB Cable** | 1 | USB-A to mini-USB (for PS3 Eye) | $3-5 | Camera connection | Generic |
| **3D Printed Frame** | 1 | Glasses frame to mount camera | $5-10 (filament) | Wearable mounting | Custom design (PLA) |
| **Velcro Straps** | 1 set | Adjustable head strap | $3-5 | Secure fit on head | Generic |
| **Mini HDMI Cable** (optional) | 1 | For external display | $5-8 | Debug/setup display | Generic |

**Total Hardware Cost:** ~$80-120 USD

---

## Software Components

| Software | Version | License | Purpose |
|----------|---------|---------|---------|
| **Python** | 3.8+ | PSF License | Core runtime |
| **OpenCV** | 4.8.0+ | Apache 2.0 | Video processing, CV pupil detection |
| **MediaPipe** | 0.10.0+ | Apache 2.0 | Face mesh and eye landmark detection |
| **Pygame** | 2.5.0+ | LGPL | GUI rendering and canvas |
| **NumPy** | 1.24.0+ | BSD | Mathematical operations |
| **SciPy** | 1.11.0+ | BSD | Homography transforms |
| **Pillow** | 10.0.0+ | HPND | Image processing |
| **Raspbian OS** | Bullseye+ | Various | Operating system |

**Total Software Cost:** $0 (all open source)

---

## Development Tools

| Tool | Purpose | Cost |
|------|---------|------|
| **VS Code** | Code editor | Free |
| **Git/GitHub** | Version control | Free |
| **Python pip** | Package management | Free |
| **Fusion 360** (optional) | 3D modeling for frame | Free (student) |

---

## Performance Specifications

| Metric | Value |
|--------|-------|
| Camera Resolution | 640x480 @ 30fps |
| Processing Latency | ~50-55ms |
| Power Consumption | ~10W (Raspberry Pi + Camera) |
| Battery Life | 8-10 hours (with 10,000mAh power bank) |
| Operating System | Raspberry Pi OS (Debian-based) |
| Storage Required | 4GB+ for OS and software |

---

## Assembly Notes

### 1. Camera Mounting
- PS3 Eye camera mounts on front of 3D-printed glasses frame
- Camera positioned ~15-20cm from user's eyes
- Adjustable angle for optimal face capture

### 2. Processing Unit
- Raspberry Pi can be worn on belt/pocket or mounted on back of head
- Connect via USB cable (recommend 1-2m length for flexibility)
- Power bank in pocket or belt pouch

### 3. Calibration
- One-time 9-point calibration per user
- Sits at comfortable distance from screen (40-60cm)
- Well-lit environment recommended

---

## Cost Comparison

| Solution | Cost | Notes |
|----------|------|-------|
| **KozbenSal (DIY)** | $80-120 | Open source, customizable |
| **Tobii Eye Tracker 5** | $230 | Desktop-only, not wearable |
| **EyeTech TM5** | $2,500+ | Professional grade |
| **Tobii Dynavox** | $15,000+ | Full AAC system |

**Cost Advantage:** 125-187x cheaper than professional assistive devices

---

## Scalability & Manufacturing

### Prototype (Current)
- Hand-assembled components
- 3D printed frame
- ~$100 per unit

### Small Batch (10-50 units)
- Bulk component purchase
- Improved 3D print quality
- ~$70-80 per unit

### Mass Production (1000+ units)
- Custom PCB with integrated camera
- Injection-molded frame
- Estimated ~$40-50 per unit

---

## Required Skills for Assembly

- Basic soldering (if custom wiring needed)
- 3D printing operation
- Software installation via command line
- Basic Linux/Raspberry Pi knowledge

**Estimated Assembly Time:** 2-3 hours for first build, 1 hour for subsequent builds

---

## Maintenance & Lifecycle

- **Camera lifespan:** 5+ years
- **Raspberry Pi lifespan:** 5-7 years
- **Battery replacement:** Every 2-3 years
- **Software updates:** Free, community-maintained

---

## Future Component Upgrades

### Planned Improvements
- [ ] Raspberry Pi 5 (better performance, lower latency)
- [ ] IR camera for low-light operation
- [ ] Custom PCB to reduce size
- [ ] Lighter frame materials (carbon fiber)
- [ ] Bluetooth connectivity for wireless operation

---

## Safety & Compliance

- ⚠️ Not a medical device (assistive tool only)
- Non-invasive, no contact with eyes
- Low-power components (safe voltage)
- No wireless emissions (USB connection only)

---

## Contact & Support

**Developer:** Nurtas Ulagat  
**Email:** nurtasulagat@gmail.com  
**Repository:** https://github.com/ulacoder/KozbenSal  
**License:** Open Source

---

## References

- [Raspberry Pi Official](https://www.raspberrypi.org/)
- [PS3 Eye Camera Specs](https://en.wikipedia.org/wiki/PlayStation_Eye)
- [MediaPipe Documentation](https://google.github.io/mediapipe/)
- [OpenCV Documentation](https://opencv.org/)

---

*Last Updated: July 14, 2026*
