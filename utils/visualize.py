import cv2

def draw_bbox(image_path, stamp_bbox, sig_bbox, out_path):
    img = cv2.imread(image_path)

    if img is None:
        return

    # Draw stamp bbox (RED)
    if stamp_bbox:
        x1, y1, x2, y2 = stamp_bbox
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(
            img, "STAMP",
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 0, 255), 2
        )

    # Draw signature bbox (GREEN)
    if sig_bbox:
        x1, y1, x2, y2 = sig_bbox
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            img, "SIGNATURE",
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (0, 255, 0), 2
        )

    cv2.imwrite(out_path, img)
