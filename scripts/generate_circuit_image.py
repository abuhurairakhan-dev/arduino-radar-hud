#!/usr/bin/env python3
"""
Generates high-resolution, clean circuit diagrams (Dark and Light themes)
for the Arduino Ultrasonic Scanning Radar & Alarm System with Google Gemini AI Assistant integration.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def get_font(name: str, size: int):
    candidates = [
        f"C:/Windows/Fonts/{name}.ttf",
        f"C:/Windows/Fonts/{name}.TTF",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_circuit(theme="dark", output_path="docs/circuit_diagram.png"):
    W, H = 2400, 1500
    
    if theme == "dark":
        bg_col = (11, 18, 30)
        panel_bg = (18, 28, 46)
        panel_border = (38, 56, 88)
        text_title = (0, 235, 255)
        text_bright = (240, 246, 255)
        text_dim = (140, 165, 195)
        text_badge = (255, 255, 255)
        bus_5v_bg = (55, 18, 26)
        bus_5v_line = (255, 60, 95)
        bus_gnd_bg = (14, 38, 62)
        bus_gnd_line = (0, 170, 255)
        arduino_bg = (8, 48, 68)
        arduino_chip = (10, 22, 34)
        arduino_border = (0, 210, 240)
        grid_dot = (25, 38, 60)
        table_hdr_bg = (24, 40, 68)
        ai_card_bg = (12, 34, 58)
        ai_card_border = (59, 130, 246)
        ai_glow = (96, 165, 250)
    else: # light
        bg_col = (248, 250, 252)
        panel_bg = (255, 255, 255)
        panel_border = (203, 213, 225)
        text_title = (14, 116, 144)
        text_bright = (15, 23, 42)
        text_dim = (100, 116, 139)
        text_badge = (255, 255, 255)
        bus_5v_bg = (254, 242, 242)
        bus_5v_line = (239, 68, 68)
        bus_gnd_bg = (238, 242, 255)
        bus_gnd_line = (37, 99, 235)
        arduino_bg = (224, 242, 254)
        arduino_chip = (30, 41, 59)
        arduino_border = (2, 132, 199)
        grid_dot = (226, 232, 240)
        table_hdr_bg = (241, 245, 249)
        ai_card_bg = (239, 246, 255)
        ai_card_border = (37, 99, 235)
        ai_glow = (29, 78, 216)

    # Wire Color Palette
    WIRE_5V = (244, 63, 94)      # Vibrant Rose/Red
    WIRE_GND = (56, 189, 248)    # Light Cyan/Sky Blue
    WIRE_TRIG = (234, 179, 8)    # Amber/Yellow (D2)
    WIRE_ECHO = (34, 197, 94)    # Emerald/Green (D3)
    WIRE_LED = (14, 165, 233)    # Bright Blue (D4)
    WIRE_BUZZ = (192, 132, 252)  # Purple (D5)
    WIRE_SERVO = (249, 115, 22)  # Orange (D6)
    WIRE_USB = (168, 85, 247)    # Purple/Violet for USB-AI link

    img = Image.new("RGBA", (W, H), bg_col)
    draw = ImageDraw.Draw(img)

    # Load typography
    font_main_title = get_font("segoeuib", 36)
    font_sub_title = get_font("segoeui", 19)
    font_section = get_font("segoeuib", 22)
    font_item_title = get_font("segoeuib", 20)
    font_body = get_font("segoeui", 16)
    font_mono = get_font("consola", 16)
    font_mono_bold = get_font("consolab", 18)
    font_badge = get_font("segoeuib", 15)
    font_micro = get_font("consola", 13)

    # 1. Subtle Background Blueprint Grid
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            draw.point((x, y), fill=grid_dot)

    # 2. Header Bar with Gemini AI Branding
    draw.rounded_rectangle([40, 22, W - 40, 95], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((65, 34), "NEXUS-7 // ARDUINO ULTRASONIC SCANNING RADAR & GEMINI AI SYSTEM", fill=text_title, font=font_main_title)
    draw.text((65, 74), "FULL HARDWARE CIRCUIT SCHEMATIC, BREADBOARD BUS RAILS & GOOGLE GEMINI AI TELEMETRY ARCHITECTURE", fill=text_dim, font=font_sub_title)
    draw.text((W - 380, 42), "CIRCUIT REV 2.5 // VERIFIED\nARDUINO UNO + HC-SR04 + GEMINI AI", fill=ai_glow, font=font_mono_bold, align="right")

    # 3. Top Power Distribution Rails (Breadboard 5V and GND)
    rail_x1, rail_y1, rail_x2, rail_y2 = 720, 115, W - 40, 205
    draw.rounded_rectangle([rail_x1, rail_y1, rail_x2, rail_y2], radius=10, fill=panel_bg, outline=panel_border, width=2)
    draw.text((rail_x1 + 20, rail_y1 + 8), "BREADBOARD COMMON POWER DISTRIBUTION BUS RAILS", fill=text_dim, font=font_mono_bold)

    # +5V Rail
    r5_y = rail_y1 + 35
    draw.rounded_rectangle([rail_x1 + 15, r5_y, rail_x2 - 15, r5_y + 22], radius=5, fill=bus_5v_bg, outline=bus_5v_line, width=1)
    draw.line([(rail_x1 + 25, r5_y + 11), (rail_x2 - 25, r5_y + 11)], fill=bus_5v_line, width=2)
    draw.text((rail_x1 + 30, r5_y + 3), "[ +5V POSITIVE POWER RAIL (VCC) ]", fill=bus_5v_line, font=font_mono_bold)

    # GND Rail
    rg_y = rail_y1 + 62
    draw.rounded_rectangle([rail_x1 + 15, rg_y, rail_x2 - 15, rg_y + 22], radius=5, fill=bus_gnd_bg, outline=bus_gnd_line, width=1)
    draw.line([(rail_x1 + 25, rg_y + 11), (rail_x2 - 25, rg_y + 11)], fill=bus_gnd_line, width=2)
    draw.text((rail_x1 + 30, rg_y + 3), "[ GND COMMON GROUND RETURN RAIL (0V) ]", fill=bus_gnd_line, font=font_mono_bold)

    # 4. Component Left: Arduino Uno R3 Board Representation
    uno_x1, uno_y1, uno_w, uno_h = 40, 115, 640, 1345
    uno_x2 = uno_x1 + uno_w
    uno_y2 = uno_y1 + uno_h
    draw.rounded_rectangle([uno_x1, uno_y1, uno_x2, uno_y2], radius=14, fill=arduino_bg, outline=arduino_border, width=3)
    draw.rounded_rectangle([uno_x1 + 8, uno_y1 + 8, uno_x2 - 8, uno_y2 - 8], radius=10, fill=panel_bg, outline=panel_border, width=1)

    # Arduino Title
    draw.text((uno_x1 + 25, uno_y1 + 22), "ARDUINO UNO R3", fill=text_title, font=font_section)
    draw.text((uno_x1 + 25, uno_y1 + 50), "Main MCU: ATmega328P @ 16 MHz (5.0V TTL Logic)", fill=text_dim, font=font_body)

    # Hardware elements on Arduino
    # USB Port
    usb_rect = [uno_x1 + 25, uno_y1 + 82, uno_x1 + 160, uno_y1 + 152]
    draw.rounded_rectangle(usb_rect, radius=6, fill=(71, 85, 105), outline=(148, 163, 184), width=2)
    draw.text((uno_x1 + 45, uno_y1 + 102), "USB PORT\n(PC Telemetry)", fill=(255, 255, 255), font=font_badge)

    # Power Barrel Jack
    draw.rounded_rectangle([uno_x1 + 25, uno_y1 + 168, uno_x1 + 160, uno_y1 + 248], radius=6, fill=(30, 41, 59), outline=(71, 85, 105), width=2)
    draw.ellipse([uno_x1 + 80, uno_y1 + 193, uno_x1 + 105, uno_y1 + 218], fill=(15, 23, 42), outline=(100, 116, 139), width=2)
    draw.text((uno_x1 + 45, uno_y1 + 223), "DC 7-12V JACK", fill=(148, 163, 184), font=font_micro)

    # ATmega328P DIP Chip
    chip_x1, chip_y1, chip_x2, chip_y2 = uno_x1 + 30, uno_y1 + 280, uno_x1 + 260, uno_y1 + 480
    draw.rounded_rectangle([chip_x1, chip_y1, chip_x2, chip_y2], radius=6, fill=arduino_chip, outline=arduino_border, width=2)
    draw.arc([chip_x1 + 90, chip_y1 - 10, chip_x1 + 140, chip_y1 + 20], 0, 180, fill=arduino_border, width=2)
    draw.text((chip_x1 + 35, chip_y1 + 65), "ATmega328P\nMICROCONTROLLER\n32KB FLASH\n2KB SRAM\n16.00 MHz CRYSTAL", fill=text_title if theme == "dark" else (255, 255, 255), font=font_mono, align="center")

    # Power Pins Header (Left side of board)
    p_hdr_x = uno_x1 + 30
    p_hdr_y = uno_y1 + 510
    draw.text((p_hdr_x, p_hdr_y), "POWER HEADER", fill=text_dim, font=font_mono_bold)
    power_pins = [
        ("5V", "Regulated 5.0V Output to Breadboard", WIRE_5V, True),
        ("GND", "Common Ground Reference (0V)", WIRE_GND, True),
        ("GND", "Secondary Ground", (100, 116, 139), False),
        ("3.3V", "3.3V Auxiliary Supply (Not Used)", (100, 116, 139), False),
        ("RESET", "Master Reset Line", (100, 116, 139), False),
        ("VIN", "Raw Input Voltage Pin", (100, 116, 139), False)
    ]
    pin_y = p_hdr_y + 26
    pin_anchor_5v = None
    pin_anchor_gnd = None

    for name, desc, col, active in power_pins:
        draw.rounded_rectangle([p_hdr_x, pin_y, p_hdr_x + 70, pin_y + 34], radius=6, fill=panel_bg, outline=col if active else panel_border, width=2 if active else 1)
        draw.ellipse([p_hdr_x + 10, pin_y + 10, p_hdr_x + 24, pin_y + 24], fill=col if active else (71, 85, 105))
        draw.text((p_hdr_x + 32, pin_y + 7), name, fill=text_bright if active else text_dim, font=font_mono_bold)
        draw.text((p_hdr_x + 85, pin_y + 9), desc, fill=col if active else text_dim, font=font_body)
        if name == "5V" and active and pin_anchor_5v is None:
            pin_anchor_5v = (p_hdr_x + 70, pin_y + 17)
        elif name == "GND" and active and pin_anchor_gnd is None:
            pin_anchor_gnd = (p_hdr_x + 70, pin_y + 17)
        pin_y += 44

    # Digital Pins Header (Right side of board)
    d_hdr_x = uno_x1 + 380
    d_hdr_y = uno_y1 + 82
    draw.text((d_hdr_x, d_hdr_y), "DIGITAL I/O HEADER", fill=text_dim, font=font_mono_bold)

    digital_pins = [
        ("D2", "TRIG (Ultrasonic 10us Trigger Pulse)", WIRE_TRIG, True),
        ("D3", "ECHO (Ultrasonic Pulse Width Duration)", WIRE_ECHO, True),
        ("D4", "LED (Active HIGH Visual Alarm Out)", WIRE_LED, True),
        ("D5", "BUZZER (PWM Tone Generator 2200Hz)", WIRE_BUZZ, True),
        ("D6", "SERVO (PWM Servo Angle Control)", WIRE_SERVO, True),
        ("D7", "Unused GPIO Pin", (100, 116, 139), False),
        ("D8", "Unused GPIO Pin", (100, 116, 139), False),
        ("D9", "Unused PWM Pin", (100, 116, 139), False),
        ("D10", "Unused PWM Pin", (100, 116, 139), False),
        ("D11", "Unused SPI MOSI Pin", (100, 116, 139), False),
        ("D12", "Unused SPI MISO Pin", (100, 116, 139), False),
        ("D13", "Onboard LED Pin", (100, 116, 139), False),
        ("GND", "Digital Ground Return", (100, 116, 139), False),
        ("AREF", "Analog Reference Voltage", (100, 116, 139), False)
    ]

    pin_anchors = {}
    d_pin_y = d_hdr_y + 28
    for name, desc, col, active in digital_pins:
        draw.rounded_rectangle([d_hdr_x, d_pin_y, d_hdr_x + 85, d_pin_y + 34], radius=6, fill=panel_bg, outline=col if active else panel_border, width=2 if active else 1)
        draw.ellipse([d_hdr_x + 10, d_pin_y + 10, d_hdr_x + 24, d_pin_y + 24], fill=col if active else (71, 85, 105))
        draw.text((d_hdr_x + 32, d_pin_y + 7), name, fill=text_bright if active else text_dim, font=font_mono_bold)
        if active:
            pin_anchors[name] = (d_hdr_x + 85, d_pin_y + 17)
            draw.text((d_hdr_x + 95, d_pin_y + 7), desc.split("(")[0].strip(), fill=col, font=font_badge)
        d_pin_y += 44

    # 4B. Dedicated GOOGLE GEMINI AI ASSISTANT & TELEMETRY HUB STATION (Lower Left)
    ai_box_x1, ai_box_y1 = uno_x1 + 25, uno_y1 + 800
    ai_box_x2, ai_box_y2 = uno_x2 - 25, uno_y2 - 25
    draw.rounded_rectangle([ai_box_x1, ai_box_y1, ai_box_x2, ai_box_y2], radius=10, fill=ai_card_bg, outline=ai_card_border, width=2)

    # Gemini AI Header
    draw.rounded_rectangle([ai_box_x1 + 10, ai_box_y1 + 10, ai_box_x2 - 10, ai_box_y1 + 55], radius=6, fill=table_hdr_bg, outline=ai_glow, width=1)
    draw.text((ai_box_x1 + 20, ai_box_y1 + 18), "GOOGLE GEMINI AI ASSISTANT // CO-PILOT & TELEMETRY HUB", fill=ai_glow, font=font_item_title)
    draw.text((ai_box_x1 + 20, ai_box_y1 + 68), "Bidirectional USB-UART Bridge @ 115200 Baud (8-N-1 Serial Stream)", fill=text_bright, font=font_mono_bold)

    # Gemini AI Feature Points
    ai_features = [
        ("• AI Hardware Co-Pilot:", "Code generation, pinout validation & circuit guidance."),
        ("• Telemetry Analytics:", "Live distance stream parsing & acoustic echo evaluation."),
        ("• Threat Assessment:", "Dynamic DEFCON 1-5 matrix scoring & alert monitoring."),
        ("• Procedural Audio FX:", "44.1 kHz NumPy synthesized sonar sweep & alarm pings."),
        ("• Sci-Fi HUD Visualizer:", "Pygame phosphor persistence sweep & target clustering.")
    ]
    cur_f_y = ai_box_y1 + 102
    for title, desc in ai_features:
        draw.text((ai_box_x1 + 20, cur_f_y), title, fill=text_title, font=font_mono_bold)
        draw.text((ai_box_x1 + 230, cur_f_y), desc, fill=text_dim, font=font_body)
        cur_f_y += 38

    # Status Pill Banner
    draw.rounded_rectangle([ai_box_x1 + 20, ai_box_y2 - 60, ai_box_x2 - 20, ai_box_y2 - 18], radius=6, fill=(16, 185, 129) if theme == "light" else (6, 78, 59), outline=(52, 211, 153), width=1)
    draw.text((ai_box_x1 + 35, ai_box_y2 - 47), "GEMINI AI INTEGRATION ACTIVE // FULL TELEMETRY LINKED", fill=(255, 255, 255), font=font_mono_bold)

    # Draw USB Cable connection from USB Port down to Gemini AI Box
    usb_pt_start = (uno_x1 + 92, uno_y1 + 152)
    usb_pt_end = (uno_x1 + 92, ai_box_y1)
    draw.line([usb_pt_start, usb_pt_end], fill=WIRE_USB, width=4)
    # Cable label
    draw.rounded_rectangle([uno_x1 + 45, uno_y1 + 260, uno_x1 + 140, uno_y1 + 295], radius=4, fill=panel_bg, outline=WIRE_USB, width=1)
    draw.text((uno_x1 + 52, uno_y1 + 268), "USB LINK", fill=WIRE_USB, font=font_badge)

    # 5. Component Box 1: HC-SR04 Ultrasonic Distance Sensor
    box1_x1, box1_y1, box1_x2, box1_y2 = 720, 230, 1530, 520
    draw.rounded_rectangle([box1_x1, box1_y1, box1_x2, box1_y2], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((box1_x1 + 25, box1_y1 + 18), "HC-SR04 ULTRASONIC RANGING MODULE", fill=text_title, font=font_item_title)
    draw.text((box1_x1 + 25, box1_y1 + 44), "Acoustic Sonar Transceiver // Range: 2cm - 400cm // 40 kHz Sound Wave Cones", fill=text_dim, font=font_body)

    # Transducer Cylinders
    # Transmit Transducer "T"
    cyl_t_center = (box1_x1 + 160, box1_y1 + 155)
    draw.ellipse([cyl_t_center[0] - 65, cyl_t_center[1] - 65, cyl_t_center[0] + 65, cyl_t_center[1] + 65], fill=(24, 38, 58), outline=(148, 163, 184), width=3)
    draw.ellipse([cyl_t_center[0] - 45, cyl_t_center[1] - 45, cyl_t_center[0] + 45, cyl_t_center[1] + 45], fill=(15, 23, 42), outline=WIRE_TRIG, width=2)
    draw.text((cyl_t_center[0] - 25, cyl_t_center[1] - 16), "TRANSMIT\n'T' (TRIG)", fill=WIRE_TRIG, font=font_mono_bold, align="center")

    # Acoustic wave cones radiating from T
    for r_wave in [85, 105, 125]:
        draw.arc([cyl_t_center[0] - r_wave, cyl_t_center[1] - r_wave, cyl_t_center[0] + r_wave, cyl_t_center[1] + r_wave], 230, 310, fill=WIRE_TRIG, width=2)

    # Receive Transducer "R"
    cyl_r_center = (box1_x1 + 380, box1_y1 + 155)
    draw.ellipse([cyl_r_center[0] - 65, cyl_r_center[1] - 65, cyl_r_center[0] + 65, cyl_r_center[1] + 65], fill=(24, 38, 58), outline=(148, 163, 184), width=3)
    draw.ellipse([cyl_r_center[0] - 45, cyl_r_center[1] - 45, cyl_r_center[0] + 45, cyl_r_center[1] + 45], fill=(15, 23, 42), outline=WIRE_ECHO, width=2)
    draw.text((cyl_r_center[0] - 25, cyl_r_center[1] - 16), "RECEIVE\n'R' (ECHO)", fill=WIRE_ECHO, font=font_mono_bold, align="center")

    # Inbound Echo wave cones into R
    for r_wave in [85, 105, 125]:
        draw.arc([cyl_r_center[0] - r_wave, cyl_r_center[1] - r_wave, cyl_r_center[0] + r_wave, cyl_r_center[1] + r_wave], 50, 130, fill=WIRE_ECHO, width=2)

    # Sensor Pin Headers at right of module
    sensor_pins = [
        ("VCC", "+5V Bus", WIRE_5V, box1_x1 + 540, box1_y1 + 90),
        ("TRIG", "Pin D2", WIRE_TRIG, box1_x1 + 540, box1_y1 + 140),
        ("ECHO", "Pin D3", WIRE_ECHO, box1_x1 + 540, box1_y1 + 190),
        ("GND", "GND Bus", WIRE_GND, box1_x1 + 540, box1_y1 + 240)
    ]
    hcsr04_anchors = {}
    for pname, pdesc, pcol, px, py in sensor_pins:
        draw.rounded_rectangle([px, py, px + 230, py + 38], radius=6, fill=panel_bg, outline=pcol, width=2)
        draw.ellipse([px + 10, py + 12, px + 24, py + 26], fill=pcol)
        draw.text((px + 32, py + 8), pname, fill=text_bright, font=font_mono_bold)
        draw.text((px + 90, py + 10), pdesc, fill=pcol, font=font_badge)
        hcsr04_anchors[pname] = (px, py + 19)

    # 6. Component Box 2: SG90 Micro Servo (Sweeper)
    box2_x1, box2_y1, box2_x2, box2_y2 = 1570, 230, W - 40, 520
    draw.rounded_rectangle([box2_x1, box2_y1, box2_x2, box2_y2], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((box2_x1 + 25, box2_y1 + 18), "SG90 MICRO SERVO (9g)", fill=WIRE_SERVO, font=font_item_title)
    draw.text((box2_x1 + 25, box2_y1 + 44), "Sweeps Ultrasonic Sensor: 15° to 165° back and forth continuously", fill=text_dim, font=font_body)

    # Servo Motor Illustration
    s_motor_center = (box2_x1 + 170, box2_y1 + 165)
    draw.rounded_rectangle([s_motor_center[0] - 90, s_motor_center[1] - 50, s_motor_center[0] + 90, s_motor_center[1] + 75], radius=8, fill=(14, 116, 144) if theme == "light" else (6, 78, 105), outline=WIRE_SERVO, width=2)
    draw.ellipse([s_motor_center[0] - 40, s_motor_center[1] - 40, s_motor_center[0] + 40, s_motor_center[1] + 40], fill=(226, 232, 240), outline=(71, 85, 105), width=2)
    draw.line([(s_motor_center[0] - 35, s_motor_center[1]), (s_motor_center[0] + 35, s_motor_center[1])], fill=WIRE_SERVO, width=4)
    draw.line([(s_motor_center[0], s_motor_center[1] - 35), (s_motor_center[0], s_motor_center[1] + 35)], fill=WIRE_SERVO, width=4)
    draw.ellipse([s_motor_center[0] - 10, s_motor_center[1] - 10, s_motor_center[0] + 10, s_motor_center[1] + 10], fill=WIRE_SERVO)
    draw.text((s_motor_center[0] - 55, s_motor_center[1] + 48), "15° <==> 165°", fill=(255, 255, 255), font=font_mono_bold)

    # Servo Ribbon Cable Pins
    servo_pins = [
        ("GND (Brown)", "GND Bus", WIRE_GND, box2_x1 + 440, box2_y1 + 100),
        ("5V (Red)", "+5V Bus", WIRE_5V, box2_x1 + 440, box2_y1 + 155),
        ("SIG (Orange)", "Pin D6 (PWM)", WIRE_SERVO, box2_x1 + 440, box2_y1 + 210)
    ]
    servo_anchors = {}
    for pname, pdesc, pcol, px, py in servo_pins:
        draw.rounded_rectangle([px, py, px + 310, py + 40], radius=6, fill=panel_bg, outline=pcol, width=2)
        draw.ellipse([px + 12, py + 13, px + 26, py + 27], fill=pcol)
        draw.text((px + 35, py + 10), pname, fill=text_bright, font=font_mono_bold)
        draw.text((px + 180, py + 12), pdesc, fill=pcol, font=font_badge)
        servo_anchors[pname] = (px, py + 20)

    # 7. Component Box 3: Visual Alarm Subsystem (Red LED + 300Ω Resistor)
    box3_x1, box3_y1, box3_x2, box3_y2 = 720, 545, 1530, 830
    draw.rounded_rectangle([box3_x1, box3_y1, box3_x2, box3_y2], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((box3_x1 + 25, box3_y1 + 18), "VISUAL PROXIMITY ALARM // 5mm RED LED & 300Ω RESISTOR", fill=WIRE_5V, font=font_item_title)
    draw.text((box3_x1 + 25, box3_y1 + 44), "Illuminates repeatedly when target distance < 30.0 cm", fill=text_dim, font=font_body)

    # 300 Ohm Resistor R1
    r1_x1, r1_y1 = box3_x1 + 50, box3_y1 + 110
    draw.rounded_rectangle([r1_x1 + 50, r1_y1, r1_x1 + 230, r1_y1 + 60], radius=8, fill=(217, 119, 6) if theme == "light" else (69, 39, 16), outline=(245, 158, 11), width=2)
    # Color Bands: Orange (3), Orange (3), Brown (x10), Gold (5%)
    draw.rectangle([r1_x1 + 80, r1_y1, r1_x1 + 95, r1_y1 + 60], fill=(234, 88, 12))  # Orange
    draw.rectangle([r1_x1 + 115, r1_y1, r1_x1 + 130, r1_y1 + 60], fill=(234, 88, 12)) # Orange
    draw.rectangle([r1_x1 + 150, r1_y1, r1_x1 + 165, r1_y1 + 60], fill=(120, 53, 15))  # Brown
    draw.rectangle([r1_x1 + 190, r1_y1, r1_x1 + 205, r1_y1 + 60], fill=(234, 179, 8))  # Gold
    draw.text((r1_x1 + 65, r1_y1 + 70), "R1: 300Ω (1/4W)\nLimits I to ~10mA", fill=text_bright, font=font_badge)

    led_in_anchor = (r1_x1 + 50, r1_y1 + 30)

    # Connection between R1 and LED Anode
    draw.line([(r1_x1 + 230, r1_y1 + 30), (r1_x1 + 330, r1_y1 + 30)], fill=WIRE_LED, width=4)
    draw.ellipse([r1_x1 + 225, r1_y1 + 25, r1_x1 + 235, r1_y1 + 35], fill=WIRE_LED)
    draw.ellipse([r1_x1 + 325, r1_y1 + 25, r1_x1 + 335, r1_y1 + 35], fill=WIRE_LED)

    # 5mm Red LED
    led_center = (r1_x1 + 400, r1_y1 + 30)
    draw.ellipse([led_center[0] - 38, led_center[1] - 38, led_center[0] + 38, led_center[1] + 38], fill=(225, 29, 72), outline=(255, 255, 255), width=2)
    draw.line([(led_center[0] + 34, led_center[1] - 25), (led_center[0] + 34, led_center[1] + 25)], fill=(255, 255, 255), width=4)
    draw.polygon([(led_center[0] - 15, led_center[1] - 18), (led_center[0] - 15, led_center[1] + 18), (led_center[0] + 12, led_center[1])], fill=(255, 255, 255))
    draw.line([(led_center[0] + 13, led_center[1] - 18), (led_center[0] + 13, led_center[1] + 18)], fill=(255, 255, 255), width=3)
    draw.line([(led_center[0] + 15, led_center[1] - 22), (led_center[0] + 32, led_center[1] - 38)], fill=WIRE_5V, width=2)
    draw.line([(led_center[0] + 25, led_center[1] - 16), (led_center[0] + 42, led_center[1] - 32)], fill=WIRE_5V, width=2)

    draw.text((led_center[0] - 80, led_center[1] + 48), "ANODE (+)\nPin D4 via R1", fill=WIRE_LED, font=font_mono_bold)
    draw.text((led_center[0] + 40, led_center[1] + 48), "CATHODE (-)\nGround Rail", fill=WIRE_GND, font=font_mono_bold)

    led_cathode_anchor = (led_center[0] + 38, led_center[1])
    draw.text((box3_x1 + 530, box3_y1 + 105), "ELECTRICAL CALCULATION:\n• Vcc = 5.0 V\n• V_forward (Red) ≈ 2.0 V\n• I_led = (5.0V - 2.0V) / 300Ω\n• I_led = 10.0 mA (Safe & Bright)", fill=text_dim, font=font_mono)

    # 8. Component Box 4: Acoustic Alarm Subsystem (Piezo Buzzer + 100Ω Resistor)
    box4_x1, box4_y1, box4_x2, box4_y2 = 1570, 545, W - 40, 830
    draw.rounded_rectangle([box4_x1, box4_y1, box4_x2, box4_y2], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((box4_x1 + 25, box4_y1 + 18), "ACOUSTIC ALARM // PASSIVE PIEZO BUZZER & 100Ω", fill=WIRE_BUZZ, font=font_item_title)
    draw.text((box4_x1 + 25, box4_y1 + 44), "Emits pulsating 2200 Hz tone pattern on proximity alert", fill=text_dim, font=font_body)

    # 100 Ohm Resistor R2
    r2_x1, r2_y1 = box4_x1 + 50, box4_y1 + 110
    draw.rounded_rectangle([r2_x1 + 50, r2_y1, r2_x1 + 230, r2_y1 + 60], radius=8, fill=(217, 119, 6) if theme == "light" else (69, 39, 16), outline=(245, 158, 11), width=2)
    # Color Bands: Brown (1), Black (0), Brown (x10), Gold (5%)
    draw.rectangle([r2_x1 + 80, r2_y1, r2_x1 + 95, r2_y1 + 60], fill=(120, 53, 15))  # Brown
    draw.rectangle([r2_x1 + 115, r2_y1, r2_x1 + 130, r2_y1 + 60], fill=(0, 0, 0))     # Black
    draw.rectangle([r2_x1 + 150, r2_y1, r2_x1 + 165, r2_y1 + 60], fill=(120, 53, 15))  # Brown
    draw.rectangle([r2_x1 + 190, r2_y1, r2_x1 + 205, r2_y1 + 60], fill=(234, 179, 8))  # Gold
    draw.text((r2_x1 + 65, r2_y1 + 70), "R2: 100Ω (1/4W)\nDamps Inductive Spikes", fill=text_bright, font=font_badge)

    buzzer_in_anchor = (r2_x1 + 50, r2_y1 + 30)

    # Connection from R2 to Buzzer (+)
    draw.line([(r2_x1 + 230, r2_y1 + 30), (r2_x1 + 310, r2_y1 + 30)], fill=WIRE_BUZZ, width=4)
    draw.ellipse([r2_x1 + 225, r2_y1 + 25, r2_x1 + 235, r2_y1 + 35], fill=WIRE_BUZZ)
    draw.ellipse([r2_x1 + 305, r2_y1 + 25, r2_x1 + 315, r2_y1 + 35], fill=WIRE_BUZZ)

    # Piezo Buzzer
    buzz_center = (r2_x1 + 380, r2_y1 + 30)
    draw.ellipse([buzz_center[0] - 45, buzz_center[1] - 45, buzz_center[0] + 45, buzz_center[1] + 45], fill=(30, 41, 59), outline=WIRE_BUZZ, width=3)
    draw.ellipse([buzz_center[0] - 22, buzz_center[1] - 22, buzz_center[0] + 22, buzz_center[1] + 22], fill=(15, 23, 42), outline=(148, 163, 184), width=2)
    draw.text((buzz_center[0] - 8, buzz_center[1] - 12), "♪", fill=WIRE_BUZZ, font=font_item_title)

    draw.text((buzz_center[0] - 80, buzz_center[1] + 52), "(+) Pin D5 via R2", fill=WIRE_BUZZ, font=font_mono_bold)
    draw.text((buzz_center[0] + 35, buzz_center[1] + 52), "(-) Ground Rail", fill=WIRE_GND, font=font_mono_bold)

    buzz_ground_anchor = (buzz_center[0] + 45, buzz_center[1])
    draw.text((box4_x1 + 470, box4_y1 + 105), "ACOUSTIC SPECIFICATIONS:\n• Frequency: 2200 Hz Square Wave\n• Drive Function: tone(5, 2200)\n• Series Resistor protects Arduino\n  pin from back-EMF spikes.", fill=text_dim, font=font_mono)

    # 9. Bottom Section: Master Interconnection Reference Table & Safety Checklist
    tbl_x1, tbl_y1, tbl_x2, tbl_y2 = 720, 855, W - 40, 1460
    draw.rounded_rectangle([tbl_x1, tbl_y1, tbl_x2, tbl_y2], radius=12, fill=panel_bg, outline=panel_border, width=2)
    draw.text((tbl_x1 + 25, tbl_y1 + 18), "COMPLETE SYSTEM INTERCONNECTION MATRIX & ELECTRICAL SPECIFICATIONS", fill=text_title, font=font_section)

    # Table Header Row
    th_y = tbl_y1 + 55
    draw.rectangle([tbl_x1 + 15, th_y, tbl_x2 - 15, th_y + 36], fill=table_hdr_bg)
    headers = [
        ("ARDUINO PIN", 30),
        ("COMPONENT", 220),
        ("COMPONENT PIN", 460),
        ("WIRE COLOR", 680),
        ("LOGIC / ELECTRICAL CHARACTERISTIC", 870),
        ("STATUS", 1370)
    ]
    for hname, hx in headers:
        draw.text((tbl_x1 + hx, th_y + 8), hname, fill=text_bright, font=font_mono_bold)

    matrix_rows = [
        ("Pin 5V", "Breadboard Power Bus", "(+) Rail (VCC)", "RED", "+5.0V Regulated DC Rail (Powers HC-SR04 & Servo)", "ACTIVE", WIRE_5V),
        ("Pin GND", "Breadboard Ground Bus", "(-) Rail (GND)", "BLACK", "System Common Ground Reference (0V Return)", "ACTIVE", WIRE_GND),
        ("Pin D2", "HC-SR04 Sensor", "TRIG Pin", "YELLOW", "10 microsecond Active-HIGH Ultrasonic Trigger Pulse", "ACTIVE", WIRE_TRIG),
        ("Pin D3", "HC-SR04 Sensor", "ECHO Pin", "GREEN", "Return Echo Flight Time Pulse Width (0.15ms to 25ms)", "ACTIVE", WIRE_ECHO),
        ("Pin D4", "Red LED Indicator", "Anode (+) via 300Ω", "BLUE", "Digital Output: 5V High when Distance < 30.0cm (10mA)", "ACTIVE", WIRE_LED),
        ("Pin D5", "Passive Piezo Buzzer", "Plus (+) via 100Ω", "PURPLE", "Tone Output: 2200Hz Square Wave Frequency on Alert", "ACTIVE", WIRE_BUZZ),
        ("Pin D6 (PWM)", "SG90 Micro Servo", "SIG Pin (Orange)", "ORANGE", "50Hz PWM Signal controlling sweep angle (15° to 165°)", "ACTIVE", WIRE_SERVO),
        ("USB Port", "Host PC / Gemini AI", "D- / D+ / VBUS", "PURPLE", "Bidirectional Serial Telemetry (115200 Baud) to Gemini AI Hub", "ACTIVE", WIRE_USB)
    ]

    r_y = th_y + 44
    for apin, comp, cpin, wcol, charact, stat, pcol in matrix_rows:
        draw.line([(tbl_x1 + 15, r_y), (tbl_x2 - 15, r_y)], fill=panel_border, width=1)
        draw.text((tbl_x1 + 30, r_y + 6), apin, fill=pcol, font=font_mono_bold)
        draw.text((tbl_x1 + 220, r_y + 6), comp, fill=text_bright, font=font_body)
        draw.text((tbl_x1 + 460, r_y + 6), cpin, fill=text_dim, font=font_body)
        draw.text((tbl_x1 + 680, r_y + 6), wcol, fill=pcol, font=font_mono_bold)
        draw.text((tbl_x1 + 870, r_y + 6), charact, fill=text_dim, font=font_body)
        draw.text((tbl_x1 + 1370, r_y + 6), stat, fill=(34, 197, 94), font=font_badge)
        r_y += 36

    # Bottom Formula Card
    bf_y = r_y + 16
    draw.rounded_rectangle([tbl_x1 + 20, bf_y, tbl_x2 - 20, tbl_y2 - 20], radius=8, fill=panel_bg, outline=arduino_border, width=1)
    draw.text((tbl_x1 + 40, bf_y + 10), "CRITICAL FORMULAS & TIMING RULES:", fill=text_title, font=font_mono_bold)
    draw.text((tbl_x1 + 40, bf_y + 34), "1. Distance (cm) = (Echo_us * 0.0343) / 2  [Speed of Sound in Air = 343.2 m/s @ 20°C]\n2. HC-SR04 Cycle Timing: Requires >= 60 ms between successive pings to avoid false echo reflections (Radar uses 70ms step).\n3. Power Isolation: SG90 Servo draws up to 250mA surge current. Powered safely via common 5V breadboard bus.", fill=text_dim, font=font_mono)

    # ================= WIRING TRACES (Orthogonal with Junction Dots) =================
    # Trace 1: Arduino 5V to +5V Rail
    p1 = pin_anchor_5v
    p2 = (p1[0] + 50, p1[1])
    p3 = (p2[0], rail_y1 + 46)
    p4 = (rail_x1 + 15, rail_y1 + 46)
    draw.line([p1, p2, p3, p4], fill=WIRE_5V, width=4)
    draw.ellipse([p1[0] - 5, p1[1] - 5, p1[0] + 5, p1[1] + 5], fill=WIRE_5V)
    draw.ellipse([p4[0] - 5, p4[1] - 5, p4[0] + 5, p4[1] + 5], fill=WIRE_5V)

    # Trace 2: Arduino GND to GND Rail
    g1 = pin_anchor_gnd
    g2 = (g1[0] + 80, g1[1])
    g3 = (g2[0], rail_y1 + 73)
    g4 = (rail_x1 + 15, rail_y1 + 73)
    draw.line([g1, g2, g3, g4], fill=WIRE_GND, width=4)
    draw.ellipse([g1[0] - 5, g1[1] - 5, g1[0] + 5, g1[1] + 5], fill=WIRE_GND)
    draw.ellipse([g4[0] - 5, g4[1] - 5, g4[0] + 5, g4[1] + 5], fill=WIRE_GND)

    # Trace 3: HC-SR04 VCC up to 5V Rail
    h_vcc = hcsr04_anchors["VCC"]
    h_vcc_mid = (h_vcc[0] - 25, h_vcc[1])
    h_vcc_up = (h_vcc_mid[0], rail_y1 + 46)
    draw.line([h_vcc, h_vcc_mid, h_vcc_up], fill=WIRE_5V, width=3)
    draw.ellipse([h_vcc[0] - 4, h_vcc[1] - 4, h_vcc[0] + 4, h_vcc[1] + 4], fill=WIRE_5V)
    draw.ellipse([h_vcc_up[0] - 5, h_vcc_up[1] - 5, h_vcc_up[0] + 5, h_vcc_up[1] + 5], fill=WIRE_5V)

    # Trace 4: HC-SR04 GND up to GND Rail
    h_gnd = hcsr04_anchors["GND"]
    h_gnd_mid = (h_gnd[0] - 45, h_gnd[1])
    h_gnd_up = (h_gnd_mid[0], rail_y1 + 73)
    draw.line([h_gnd, h_gnd_mid, h_gnd_up], fill=WIRE_GND, width=3)
    draw.ellipse([h_gnd[0] - 4, h_gnd[1] - 4, h_gnd[0] + 4, h_gnd[1] + 4], fill=WIRE_GND)
    draw.ellipse([h_gnd_up[0] - 5, h_gnd_up[1] - 5, h_gnd_up[0] + 5, h_gnd_up[1] + 5], fill=WIRE_GND)

    # Trace 5: D2 (TRIG) from Arduino to HC-SR04
    t_start = pin_anchors["D2"]
    t_end = hcsr04_anchors["TRIG"]
    t_mid_x = 690
    draw.line([t_start, (t_mid_x, t_start[1]), (t_mid_x, t_end[1]), t_end], fill=WIRE_TRIG, width=3)
    draw.ellipse([t_start[0] - 4, t_start[1] - 4, t_start[0] + 4, t_start[1] + 4], fill=WIRE_TRIG)
    draw.ellipse([t_end[0] - 4, t_end[1] - 4, t_end[0] + 4, t_end[1] + 4], fill=WIRE_TRIG)

    # Trace 6: D3 (ECHO) from Arduino to HC-SR04
    e_start = pin_anchors["D3"]
    e_end = hcsr04_anchors["ECHO"]
    e_mid_x = 705
    draw.line([e_start, (e_mid_x, e_start[1]), (e_mid_x, e_end[1]), e_end], fill=WIRE_ECHO, width=3)
    draw.ellipse([e_start[0] - 4, e_start[1] - 4, e_start[0] + 4, e_start[1] + 4], fill=WIRE_ECHO)
    draw.ellipse([e_end[0] - 4, e_end[1] - 4, e_end[0] + 4, e_end[1] + 4], fill=WIRE_ECHO)

    # Trace 7: D4 (LED) from Arduino to R1
    led_start = pin_anchors["D4"]
    led_end = led_in_anchor
    draw.line([led_start, (695, led_start[1]), (695, led_end[1]), led_end], fill=WIRE_LED, width=3)
    draw.ellipse([led_start[0] - 4, led_start[1] - 4, led_start[0] + 4, led_start[1] + 4], fill=WIRE_LED)
    draw.ellipse([led_end[0] - 4, led_end[1] - 4, led_end[0] + 4, led_end[1] + 4], fill=WIRE_LED)

    # Trace 8: LED Cathode to GND Rail
    c_start = led_cathode_anchor
    c_up = (c_start[0] + 40, c_start[1])
    c_rail = (c_up[0], rail_y1 + 73)
    draw.line([c_start, c_up, c_rail], fill=WIRE_GND, width=3)
    draw.ellipse([c_start[0] - 4, c_start[1] - 4, c_start[0] + 4, c_start[1] + 4], fill=WIRE_GND)
    draw.ellipse([c_rail[0] - 5, c_rail[1] - 5, c_rail[0] + 5, c_rail[1] + 5], fill=WIRE_GND)

    # Trace 9: D5 (BUZZER) from Arduino to R2
    bz_start = pin_anchors["D5"]
    bz_end = buzzer_in_anchor
    draw.line([bz_start, (685, bz_start[1]), (685, 840), (1555, 840), (1555, bz_end[1]), bz_end], fill=WIRE_BUZZ, width=3)
    draw.ellipse([bz_start[0] - 4, bz_start[1] - 4, bz_start[0] + 4, bz_start[1] + 4], fill=WIRE_BUZZ)
    draw.ellipse([bz_end[0] - 4, bz_end[1] - 4, bz_end[0] + 4, bz_end[1] + 4], fill=WIRE_BUZZ)

    # Trace 10: Buzzer Ground to GND Rail
    bg_start = buzz_ground_anchor
    bg_up = (bg_start[0] + 35, bg_start[1])
    bg_rail = (bg_up[0], rail_y1 + 73)
    draw.line([bg_start, bg_up, bg_rail], fill=WIRE_GND, width=3)
    draw.ellipse([bg_start[0] - 4, bg_start[1] - 4, bg_start[0] + 4, bg_start[1] + 4], fill=WIRE_GND)
    draw.ellipse([bg_rail[0] - 5, bg_rail[1] - 5, bg_rail[0] + 5, bg_rail[1] + 5], fill=WIRE_GND)

    # Trace 11: D6 (SERVO PWM) from Arduino to Servo SIG
    sv_start = pin_anchors["D6"]
    sv_end = servo_anchors["SIG (Orange)"]
    draw.line([sv_start, (675, sv_start[1]), (675, 532), (1550, 532), (1550, sv_end[1]), sv_end], fill=WIRE_SERVO, width=3)
    draw.ellipse([sv_start[0] - 4, sv_start[1] - 4, sv_start[0] + 4, sv_start[1] + 4], fill=WIRE_SERVO)
    draw.ellipse([sv_end[0] - 4, sv_end[1] - 4, sv_end[0] + 4, sv_end[1] + 4], fill=WIRE_SERVO)

    # Trace 12: Servo 5V (Red) to +5V Rail
    sv_5v = servo_anchors["5V (Red)"]
    sv_5v_mid = (sv_5v[0] - 20, sv_5v[1])
    sv_5v_up = (sv_5v_mid[0], rail_y1 + 46)
    draw.line([sv_5v, sv_5v_mid, sv_5v_up], fill=WIRE_5V, width=3)
    draw.ellipse([sv_5v[0] - 4, sv_5v[1] - 4, sv_5v[0] + 4, sv_5v[1] + 4], fill=WIRE_5V)
    draw.ellipse([sv_5v_up[0] - 5, sv_5v_up[1] - 5, sv_5v_up[0] + 5, sv_5v_up[1] + 5], fill=WIRE_5V)

    # Trace 13: Servo GND (Brown) to GND Rail
    sv_gnd = servo_anchors["GND (Brown)"]
    sv_gnd_mid = (sv_gnd[0] - 40, sv_gnd[1])
    sv_gnd_up = (sv_gnd_mid[0], rail_y1 + 73)
    draw.line([sv_gnd, sv_gnd_mid, sv_gnd_up], fill=WIRE_GND, width=3)
    draw.ellipse([sv_gnd[0] - 4, sv_gnd[1] - 4, sv_gnd[0] + 4, sv_gnd[1] + 4], fill=WIRE_GND)
    draw.ellipse([sv_gnd_up[0] - 5, sv_gnd_up[1] - 5, sv_gnd_up[0] + 5, sv_gnd_up[1] + 5], fill=WIRE_GND)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    print(f"Generated clean circuit diagram image: {output_path} ({W}x{H})")

if __name__ == "__main__":
    draw_circuit("dark", "docs/circuit_diagram.png")
    draw_circuit("light", "docs/circuit_diagram_light.png")
