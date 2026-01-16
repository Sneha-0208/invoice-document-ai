import os
import json, time
from utils.ocr import run_ocr
from utils.confidence import compute_confidence
from utils.visualize import draw_bbox
from utils.stamp_signature import detect_stamp, detect_signature
from utils.extract_fields import (
    extract_model_name,
    extract_horse_power,
    extract_asset_cost,
    clean_model_name,
    extract_dealer_name
)


IMAGE_DIR = "sample_images"

if __name__ == "__main__":
    # images = os.listdir(IMAGE_DIR)
    images = [
        f for f in os.listdir(IMAGE_DIR)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    for img in images[:3]:      # change the number of times you want to run
        start = time.time()
        img_path = os.path.join(IMAGE_DIR, img)
        print(f"\n========== {img} ==========")

        ocr_results = run_ocr(img_path)

        dealer = extract_dealer_name(ocr_results)
        raw_model = extract_model_name(ocr_results)
        model = clean_model_name(raw_model)
        hp = extract_horse_power(ocr_results)
        cost = extract_asset_cost(ocr_results)
        stamp_present, stamp_bbox = detect_stamp(img_path)
        sig_present, sig_bbox = detect_signature(img_path)
        
        # uncomment this if you want to save stamp and signature boxed images to visuals folder
        # draw_bbox(
        #     img_path,
        #     stamp_bbox,
        #     sig_bbox,
        #     f"visuals/annotated_{img}"
        # )


        # print("DEALER:", dealer)
        # print("MODEL:", model)
        # print("HP:", hp)
        # print("COST:", cost)
        # print("STAMP :", stamp_present, stamp_bbox)
        # print("SIGN  :", sig_present, sig_bbox)


        result = {
            "doc_id": img,
            "fields": {
                "dealer_name": dealer,
                "model_name": model,
                "horse_power": hp,
                "asset_cost": cost,
                "signature": {
                    "present": sig_present,
                    "bbox": sig_bbox
                },
                "stamp": {
                    "present": stamp_present,
                    "bbox": stamp_bbox
                }
            },
            "confidence": compute_confidence(
                dealer, model, hp, cost, stamp_present, sig_present
            ),
            "processing_time_sec": round(time.time() - start, 2),
            "cost_estimate_usd": 0.002
        }

        print(json.dumps(result, indent=2))

