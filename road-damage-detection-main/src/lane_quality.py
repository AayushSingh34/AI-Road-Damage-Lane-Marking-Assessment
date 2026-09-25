import cv2
import numpy as np

class LaneQualityEngine:
    """
    Evaluates lane marking surface degradation, continuity, 
    and contrast ratio aligned with IRC:35-2015 guidelines.
    """
    def __init__(self, camera_height=1.2, focal_length=800):
        self.camera_height = camera_height
        self.focal_length = focal_length

    def evaluate_marking_quality(self, frame_bgr, bbox_strip):
        x1, y1, x2, y2 = [int(v) for v in bbox_strip]
        roi = frame_bgr[y1:y2, x1:x2]
        if roi.size == 0 or roi.shape[0] < 10 or roi.shape[1] < 10:
            return {"wear_percentage": 0.0, "serviceability": "No ROI Available"}

        # 1. Convert to HLS & Grayscale for White / Yellow Marking Isolation
        hls = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        # White markings mask (High Luminance)
        _, white_mask = cv2.threshold(hls[:, :, 1], 190, 255, cv2.THRESH_BINARY)

        # Yellow markings mask (Hue 15-35, High Saturation)
        yellow_lower = np.array([15, 60, 90], dtype=np.uint8)
        yellow_upper = np.array([38, 255, 255], dtype=np.uint8)
        yellow_mask = cv2.inRange(hls, yellow_lower, yellow_upper)

        marking_mask = cv2.bitwise_or(white_mask, yellow_mask)

        # 2. Compute Wear Percentage
        total_roi_pixels = roi.shape[0] * roi.shape[1]
        marking_pixels = cv2.countNonZero(marking_mask)

        # Expected lane strip density within theoretical envelope (~28% of corridor)
        expected_envelope_pixels = max(1, int(total_roi_pixels * 0.28))
        wear_ratio = max(0.0, 1.0 - (marking_pixels / float(expected_envelope_pixels)))
        wear_percentage = round(min(100.0, wear_ratio * 100.0), 1)

        # 3. Compute Photometric Contrast (L_marking / L_asphalt)
        asphalt_mask = cv2.bitwise_not(marking_mask)
        mean_marking_lum = cv2.mean(gray, mask=marking_mask)[0] if marking_pixels > 0 else 0
        mean_asphalt_lum = cv2.mean(gray, mask=asphalt_mask)[0] if cv2.countNonZero(asphalt_mask) > 0 else 1

        contrast_ratio = round((mean_marking_lum + 1.0) / (mean_asphalt_lum + 1.0), 2)

        # 4. Continuity & Grade Determination (IRC:35-2015 Benchmarks)
        continuity_percentage = round(max(0.0, 100.0 - (wear_percentage * 1.1)), 1)

        if wear_percentage < 25.0 and contrast_ratio >= 3.0:
            serviceability = "Grade A: Optimal (Meets IRC:35 Highway Delineation)"
            action = "No intervention needed. Markings within serviceable life."
        elif wear_percentage < 50.0:
            serviceability = "Grade B: Moderate Fading / Abrasion"
            action = "Schedule thermoplastic re-striping within 60 days."
        else:
            serviceability = "Grade C: Structural Failure / Bare Asphalt Exposed"
            action = "Immediate Restriping Work Order Required (Warranty Non-Compliant)."

        return {
            "wear_percentage": wear_percentage,
            "continuity_percentage": continuity_percentage,
            "contrast_ratio": contrast_ratio,
            "serviceability": serviceability,
            "recommended_action": action,
            "irc_compliance": "Compliant" if wear_percentage < 35.0 else "Non-Compliant (Requires Maintenance)"
        }