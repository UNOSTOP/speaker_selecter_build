#! /usr/bin/env python3
import sys
import json
import tomli

import RPi.GPIO as GPIO
from flask import Flask, request, jsonify

# toybox has handmade modules
import toybox

GPIO.setmode(GPIO.BCM)
app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health():
    return "ok(^^)b"

@app.route("/speaker", methods=["GET"])
def get_speaker_num():
    speaker_json = toybox.load_json("speaker_nowON.json")
    return jsonify(speaker_json)

@app.route("/speaker", methods=["PUT"])
def put_speaker_num():
    if request.json is None:
        msg = f"Error: request body is invalid"
        print(msg, file=sys.stderr)
        return jsonify({"message": msg}), 400

    if not "speaker_num" in request.json:
        msg = f"Error: request body is invalid"
        print(msg, file=sys.stderr)
        return jsonify({"message": msg}), 400


    #speaker_num = request.json["speaker_num"]
    speaker_num = request.json["speaker_num"]
    # Error process
    if (speaker_num < 1) or (speaker_num > 18):
        msg = f"Error: speaker_num must be in 1-18, got: {speaker_num}"
        print(msg, file=sys.stderr)
        return jsonify({"message": msg}), 400

    # speaker select process
    print(f"Present speaker number ... {speaker_num}", file=sys.stderr)
    # init pin (BCM)
    toybox.init_BCM(speakerBCM_list)
    # Turn ON the GPIO pin use "GPIO.output(speakerBCM, 1)
    toybox.on_BCM(speakerBCM_list[toybox.ID2BCM(speaker_num)])
    # make "ON GPIO pin history .json file"
    toybox.save_json("speaker_nowON.json", request.json)

    # Success message
    msg = f"speaker_num changed to {speaker_num}"
    print(msg, file=sys.stderr)
    return jsonify({"message": msg})

if __name__ == "__main__":
    #GPIO.setmode(GPIO.BCM)
    #setting_file_path = "./setting.toml"
    setting_file_path = "/home/pi/speaker_selecter/ver4/setting.toml"
    setting_dict = toybox.load_setting_toml(setting_file_path)
    speakerBCM_list = toybox.make_BCM_list(setting_dict["SPEAKER_IDandBCM"])
    
    # init BCM. Speaker1 is ON at first
    toybox.init_BCM(speakerBCM_list)
    toybox.on_BCM(speakerBCM_list[0])
    toybox.save_json("speaker_nowON.json", {"speaker_num": speakerBCM_list[0]})
    
    # run server
    app.run(host="0.0.0.0", port=80)
    GPIO.cleanup()
