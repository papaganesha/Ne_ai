"""
Processamento visual leve (V1).

Extrai apenas sinais básicos.
"""

def process_frame(event):
    """
    Converte um frame em features simples.
    """

    frame = event.data

    height, width, channels = frame.shape
    mean_pixel = float(frame.mean())

    return {
        "type": "visual_signal",
        "source": event.source,
        "features": {
            "width": width,
            "height": height,
            "channels": channels,
            "mean_pixel": mean_pixel
        },
        "confidence": event.confidence
    }
