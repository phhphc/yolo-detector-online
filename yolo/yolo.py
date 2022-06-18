from audioop import avg
import cv2
import numpy as np
from sqlalchemy import false


# path to yolo required files
classes_path = 'yolo/yolov3.txt'
weights_path = 'yolo/yolov3.weights'
config_path = 'yolo/yolov3.cfg'


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

    return output_layers


def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = str(classes[class_id])
    color = COLORS[class_id]

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)  # box

    text = "{}: {:.4f}".format(label, confidence)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 1
    txt_color = (255, 255, 255) if avg(color, 3) < 128 else (0, 0, 0)

    text_w, text_h = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    outside = y - text_h >= 3
    cv2.rectangle(img,
                  (x, y),
                  (x + text_w, y - text_h - 3 if outside else y + text_h + 3),
                  color,
                  -1,
                  cv2.LINE_AA)  # filled
    cv2.putText(img,
                text,
                (x, y - 2 if outside else y + text_h + 2),
                font,
                font_scale,
                txt_color,
                font_thickness,
                lineType=cv2.LINE_AA)  # text


def predict_image(img_path, extd='.jpg'):
    # load our input image and grab its spatial dimensions
    image = cv2.imread(img_path)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    blob = cv2.dnn.blobFromImage(
        image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    # Thực hiện xác định bằng HOG và SVM
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(
        boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(
            x), round(y), round(x + w), round(y + h))

    return cv2.imencode(extd, image)


# load classes names
classes = None
with open(classes_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# create random colors for each label
COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

# load yolo network
net = cv2.dnn.readNet(weights_path, config_path)
