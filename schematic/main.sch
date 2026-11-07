{
  "version": 1,
  "symbols": [
    {
      "id": "arduino_1",
      "type": "reg:arduino-uno",
      "ref": "U1",
      "x": 34,
      "y": 58,
      "rotation": 0,
      "mirror": false
    },
    {
      "id": "ultra_1",
      "type": "reg:hc-sr04",
      "ref": "U2",
      "x": 69,
      "y": 33,
      "rotation": 0,
      "mirror": false
    },
    {
      "id": "buzzer_1",
      "type": "reg:piezo-buzzer",
      "ref": "U3",
      "x": 113,
      "y": 21,
      "rotation": 0,
      "mirror": false
    },
    {
      "id": "led_1",
      "type": "led",
      "ref": "D1",
      "x": 113,
      "y": 38,
      "rotation": 0,
      "props": {
        "color": "red"
      },
      "mirror": false
    },
    {
      "id": "r_led_1",
      "type": "resistor",
      "ref": "R1",
      "x": 69,
      "y": 109,
      "rotation": 0,
      "value": "300",
      "mirror": false
    },
    {
      "id": "r_buz_1",
      "type": "resistor",
      "ref": "R2",
      "x": 69,
      "y": 90,
      "rotation": 0,
      "value": "100",
      "mirror": false
    },
    {
      "id": "servo_1",
      "type": "reg:servo-sg90",
      "ref": "U4",
      "x": 69,
      "y": 56,
      "rotation": 0,
      "mirror": false
    }
  ],
  "wires": [
    {
      "id": "bbs_w_0",
      "points": [
        {
          "x": 28,
          "y": 47
        },
        {
          "x": 18,
          "y": 47
        },
        {
          "x": 18,
          "y": 34
        },
        {
          "x": 63,
          "y": 34
        }
      ],
      "net": "N_D2"
    },
    {
      "id": "bbs_w_1",
      "points": [
        {
          "x": 28,
          "y": 49
        },
        {
          "x": 12,
          "y": 49
        },
        {
          "x": 12,
          "y": 23
        },
        {
          "x": 85,
          "y": 23
        },
        {
          "x": 85,
          "y": 32
        },
        {
          "x": 75,
          "y": 32
        }
      ],
      "net": "N_D3"
    },
    {
      "id": "bbs_w_2",
      "points": [
        {
          "x": 28,
          "y": 51
        },
        {
          "x": 12,
          "y": 51
        },
        {
          "x": 12,
          "y": 101
        },
        {
          "x": 69,
          "y": 101
        },
        {
          "x": 69,
          "y": 106
        }
      ],
      "net": "N_D4"
    },
    {
      "id": "bbs_w_3",
      "points": [
        {
          "x": 28,
          "y": 53
        },
        {
          "x": 15,
          "y": 53
        },
        {
          "x": 15,
          "y": 82
        },
        {
          "x": 69,
          "y": 82
        },
        {
          "x": 69,
          "y": 87
        }
      ],
      "net": "N_D5"
    },
    {
      "id": "bbs_w_4",
      "points": [
        {
          "x": 28,
          "y": 55
        },
        {
          "x": 18,
          "y": 55
        },
        {
          "x": 18,
          "y": 120
        },
        {
          "x": 94,
          "y": 120
        },
        {
          "x": 94,
          "y": 56
        },
        {
          "x": 75,
          "y": 56
        }
      ],
      "net": "N_D6"
    },
    {
      "id": "bbs_w_5",
      "points": [
        {
          "x": 40,
          "y": 55
        },
        {
          "x": 50,
          "y": 55
        },
        {
          "x": 50,
          "y": 32
        },
        {
          "x": 63,
          "y": 32
        }
      ],
      "net": "V5"
    },
    {
      "id": "bbs_w_6",
      "points": [
        {
          "x": 40,
          "y": 55
        },
        {
          "x": 63,
          "y": 55
        }
      ],
      "net": "V5"
    },
    {
      "id": "bbs_w_7",
      "points": [
        {
          "x": 40,
          "y": 61
        },
        {
          "x": 53,
          "y": 61
        },
        {
          "x": 53,
          "y": 46
        },
        {
          "x": 88,
          "y": 46
        },
        {
          "x": 88,
          "y": 34
        },
        {
          "x": 75,
          "y": 34
        }
      ],
      "net": "0"
    },
    {
      "id": "bbs_w_8",
      "points": [
        {
          "x": 40,
          "y": 61
        },
        {
          "x": 53,
          "y": 61
        },
        {
          "x": 53,
          "y": 46
        },
        {
          "x": 88,
          "y": 46
        },
        {
          "x": 88,
          "y": 12
        },
        {
          "x": 129,
          "y": 12
        },
        {
          "x": 129,
          "y": 21
        },
        {
          "x": 119,
          "y": 21
        }
      ],
      "net": "0"
    },
    {
      "id": "bbs_w_9",
      "points": [
        {
          "x": 40,
          "y": 61
        },
        {
          "x": 53,
          "y": 61
        },
        {
          "x": 53,
          "y": 46
        },
        {
          "x": 113,
          "y": 46
        },
        {
          "x": 113,
          "y": 41
        }
      ],
      "net": "0"
    },
    {
      "id": "bbs_w_10",
      "points": [
        {
          "x": 40,
          "y": 61
        },
        {
          "x": 53,
          "y": 61
        },
        {
          "x": 53,
          "y": 57
        },
        {
          "x": 63,
          "y": 57
        }
      ],
      "net": "0"
    },
    {
      "id": "bbs_w_11",
      "points": [
        {
          "x": 69,
          "y": 93
        },
        {
          "x": 69,
          "y": 98
        },
        {
          "x": 91,
          "y": 98
        },
        {
          "x": 91,
          "y": 21
        },
        {
          "x": 107,
          "y": 21
        }
      ],
      "net": "N1"
    },
    {
      "id": "bbs_w_12",
      "points": [
        {
          "x": 69,
          "y": 112
        },
        {
          "x": 69,
          "y": 117
        },
        {
          "x": 97,
          "y": 117
        },
        {
          "x": 97,
          "y": 30
        },
        {
          "x": 113,
          "y": 30
        },
        {
          "x": 113,
          "y": 35
        }
      ],
      "net": "N2"
    }
  ],
  "junctions": [
    {
      "id": "j_50_55",
      "x": 50,
      "y": 55
    },
    {
      "id": "j_40_61",
      "x": 40,
      "y": 61
    },
    {
      "id": "j_53_61",
      "x": 53,
      "y": 61
    },
    {
      "id": "j_53_46",
      "x": 53,
      "y": 46
    },
    {
      "id": "j_88_46",
      "x": 88,
      "y": 46
    },
    {
      "id": "j_88_34",
      "x": 88,
      "y": 34
    },
    {
      "id": "j_53_57",
      "x": 53,
      "y": 57
    }
  ],
  "netLabels": [
    {
      "id": "bbs_nl_0",
      "name": "N_D2",
      "x": 28,
      "y": 47,
      "owner": "arduino_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_1",
      "name": "N_D3",
      "x": 28,
      "y": 49,
      "owner": "arduino_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_2",
      "name": "N_D4",
      "x": 28,
      "y": 51,
      "owner": "arduino_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_3",
      "name": "N_D5",
      "x": 28,
      "y": 53,
      "owner": "arduino_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_4",
      "name": "N_D6",
      "x": 28,
      "y": 55,
      "owner": "arduino_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_5",
      "name": "V5",
      "x": 40,
      "y": 55,
      "owner": "arduino_1",
      "anchor": "start"
    },
    {
      "id": "bbs_nl_6",
      "name": "GND",
      "x": 40,
      "y": 61,
      "owner": "arduino_1",
      "anchor": "start"
    },
    {
      "id": "bbs_nl_7",
      "name": "N1",
      "x": 69,
      "y": 93,
      "owner": "r_buz_1",
      "anchor": "end"
    },
    {
      "id": "bbs_nl_8",
      "name": "N2",
      "x": 69,
      "y": 112,
      "owner": "r_led_1",
      "anchor": "end"
    }
  ],
  "probes": [],
  "directives": [],
  "breadboardSync": {
    "sourceHash": "9757:1174965402",
    "symbolIds": [
      "arduino_1",
      "ultra_1",
      "buzzer_1",
      "led_1",
      "r_led_1",
      "r_buz_1",
      "servo_1"
    ],
    "wireIds": [
      "bbs_w_0",
      "bbs_w_1",
      "bbs_w_2",
      "bbs_w_3",
      "bbs_w_4",
      "bbs_w_5",
      "bbs_w_6",
      "bbs_w_7",
      "bbs_w_8",
      "bbs_w_9",
      "bbs_w_10",
      "bbs_w_11",
      "bbs_w_12"
    ],
    "netLabelIds": [
      "bbs_nl_0",
      "bbs_nl_1",
      "bbs_nl_2",
      "bbs_nl_3",
      "bbs_nl_4",
      "bbs_nl_5",
      "bbs_nl_6",
      "bbs_nl_7",
      "bbs_nl_8"
    ]
  }
}