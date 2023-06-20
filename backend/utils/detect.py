from collections import Counter
from typing import Dict, Union

import cv2
from ultralytics import YOLO

RU_GARBAGE_CLASSES = (
    "мусорные мешки",
    "картон",
    "крупногабаритный мусор",
    "стекло",
    "металл",
    "бумага",
    "пластик",
    "ветки"
)


class GarbageDetection:
    def __init__(self, model_pth: str):
        self.model = YOLO(model_pth)
        for class_gb in self.model.names:
            self.model.names[class_gb] = RU_GARBAGE_CLASSES[class_gb]

    def garbage_detection(self, img_pth: str, save_pth: str) -> Union[Dict, None]:
        try:
            results = self.model(source=img_pth, device="cpu")
            find_garbage = Counter((results[0].boxes.cls.short().tolist()))
            for item in set(find_garbage.keys()):
                find_garbage[RU_GARBAGE_CLASSES[item]] = find_garbage.pop(item)
            cv2.imwrite(save_pth, cv2.resize(results[0].plot(conf=False), (640, 480)))
            return dict(find_garbage)
        except:
            return None
