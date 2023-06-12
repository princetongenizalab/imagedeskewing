import os

from groundingdino.util.inference import load_model, load_image, predict, annotate

def find_images(directory, extension):
    """Returns the abs path to all files with a specified extension in a parent directory"""
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                images.append(file_path)
    return images

def main():
    model_config_path = "/scratch/gpfs/eh0560/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py"
    model_weight_path = "/scratch/gpfs/eh0560/imagedeskewing/models/grounding_dino_models/groundingdino_swint_ogc.pth"
    model = load_model(model_config_path, model_weight_path)

    tif_image_paths = find_images("/scratch/gpfs/RUSTOW/htr_deskewing_image_dataset/NEED_DESKEWING", ".tif")
    image_path = tif_image_paths[10]
    image_source, image = load_image(image_path)

    TEXT_PROMPT = "document"
    BOX_TRESHOLD = 0.35
    TEXT_TRESHOLD = 0.25

    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )

    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)

if __name__ == "__main__":
    main()
