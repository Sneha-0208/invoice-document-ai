from paddleocr import PaddleOCR

# Initialize OCR once (important for speed)
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",   # English + mixed text; Hindi often partially works
    show_log=False
)

def run_ocr(image_path):
    """
    Runs OCR on an image and returns list of dicts:
    {
        text: str,
        bbox: [[x1,y1], [x2,y2], [x3,y3], [x4,y4]],
        confidence: float
    }
    """
    result = ocr.ocr(image_path, cls=True)

    outputs = []
    if result and result[0]:
        for line in result[0]:
            bbox = line[0]
            text = line[1][0]
            conf = float(line[1][1])

            outputs.append({
                "text": text,
                "bbox": bbox,
                "confidence": conf
            })

    return outputs
