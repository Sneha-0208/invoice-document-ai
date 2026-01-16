import cv2

def detect_stamp(image_path):
    """
    Detect stamp using contour density in bottom-right region
    Returns: (present: bool, bbox: [x1, y1, x2, y2] or None)
    """
    img = cv2.imread(image_path)
    if img is None:
        return False, None

    h, w, _ = img.shape

    # Bottom-right ROI
    roi = img[int(0.6*h):h, int(0.6*w):w]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:  # heuristic threshold
            x, y, bw, bh = cv2.boundingRect(cnt)

            # Convert bbox to original image coordinates
            x1 = int(0.6*w + x)
            y1 = int(0.6*h + y)
            x2 = x1 + bw
            y2 = y1 + bh

            return True, [x1, y1, x2, y2]

    return False, None


def detect_signature(image_path):
    """
    Detect signature using thin contour heuristic in bottom region
    Returns: (present: bool, bbox or None)
    """
    img = cv2.imread(image_path)
    if img is None:
        return False, None

    h, w, _ = img.shape

    # Bottom region (signature usually here)
    roi = img[int(0.65*h):h, int(0.1*w):int(0.9*w)]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)

        # Signature = long, thin region
        aspect_ratio = bw / float(bh)

        if area > 300 and aspect_ratio > 3 and bh < 120:
            x1 = int(0.1*w + x)
            y1 = int(0.65*h + y)
            x2 = x1 + bw
            y2 = y1 + bh

            return True, [x1, y1, x2, y2]

    return False, None
