## import RPI.GPIO as GPIO
import tomli
import json
import RPi.GPIO as GPIO
# speakerID_list global  is better??

def load_setting_toml(toml_file_path: str) -> dict:
    """
    
    Parameters
    ----------
    toml_file_path: str
        toml file path.

    Returns
    -------
    toml_dict: dict
        dict about speaker ID and GPIO(BCM) relationship.

    Examples
    --------
    >>> toml_dict = toybox.load_setting_toml("setting.toml")
    
    Notes
    -----

    See Also
    --------
    https://pypi.org/project/tomli/
    """
    with open(toml_file_path, "rb") as f:
        toml_dict = tomli.load(f)
    return toml_dict

def make_BCM_list(dict_IDandBCM:dict) -> list:
    """

    Notes
    -----
    this is better than now code?
    >>> toml_dict = toybox.load_setting_toml(toml_file_path)
    >>> speakerID_list =  [i for i in toml_dict["SPEAKER_IDandBCM"].keys()]
    >>> speakerBCM_list = makeBCM_list(toml_dict, speakerID_list)
    >>> def make_BCM_list(toml_dict: dict, speakerID_list: list) -> list:
    >>>     speakerBCM_list = [toml_dict["SPEAKER_BCM"][j] for j in speakerID_list]
    >>>     return speakerBCM_list

    Examples
    --------
    >>> toml_dict = toybox.load_BCM("setting.toml")
    >>> IDandBCM = toml_dict["SPEAKER_IDandBCM"]
    >>> speakerBCM_list = make_BCM_list(IDandBCM)
    """
    
    #speakerID_list = ['speaker1', 'speaker2', 'speaker3', 'speaker4', 'speaker5', 'speaker6', 'speaker7', 'speaker8', 'speaker9', 'speaker10', 'speaker11':'speaker12', 'speaker13', 'speaker14', 'speaker15', 'speaker16', 'speaker17', 'speaker18']
    speakerID_list = [i for i in dict_IDandBCM.keys()]
    speakerBCM_list = [dict_IDandBCM[j] for j in speakerID_list] # you can [j for j in IDandBCM.values()] ??

    return speakerBCM_list

def BCM_available(speakerBCM_list: list, speakerid: int):
    if speakerid in speakerBCM_list:
        return True
    else:
        return False

def init_BCM(speakerBCM_list: list) -> None:
    for i in speakerBCM_list:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, 0)

def on_BCM(speakerBCM_id: int) -> None:
    GPIO.output(speakerBCM_id, 1)

def save_json(out_json_path: str, json_data) -> None:
    with open(out_json_path, mode="wt", encoding="utf-8") as f:
        json.dump(json_data, f)

def load_json(json_path: str) -> dict:
    with open(json_path, mode="rt", encoding="utf-8") as f:
        speaker_json = json.load(f)
    return speaker_json

def ID2BCM(speaker_id:int) -> int:
    BCM_num = speaker_id - 1
    return BCM_num
