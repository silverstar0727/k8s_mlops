import cv2
from flask import Flask, request, jsonify
import os, io
from PIL import Image

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    # 반환할 respose를 생성합니다.
    response = {'success': False}

    # 파일의 입력을 요청합니다.
    request.files.get('file')
    # 파일을 읽습니다.
    image_requested = request.files['file'].read()
    # 읽은 파일을 엽니다.
    image = Image.open(io.BytesIO(image_requested))
    # RGB로 변환하여 줍니다.
    rgb_image = image.convert('RGB')
    # "image.jpg"로 저장합니다.
    rgb_image.save('image.jpg')

    # opencv를 이용하여 파일을 읽어줍니다.
    img = cv2.imread('image.jpg')

    # cv2.dnn을 이용하여 pretrianed된 tensorflow 모델을 열어줍니다.
    # 이때 Dockerfile에서 정상적으로 다운이 되지 않았다면 작동하지 않습니다.
    cv_net = cv2.dnn.readNetFromTensorflow('./pretrained/faster_rcnn_resnet50_coco_2018_01_28/frozen_inference_graph.pb', 
                                        './pretrained/model.pbtxt')

    # 원본 이미지 배열 BGR을 RGB로 변환하여 배열 입력, Tensorflow Faster RCNN은 size를 고정할 필요가 없는 것으로 추정됩니다. 
    cv_net.setInput(cv2.dnn.blobFromImage(img, swapRB=True, crop=False))

    # Object Detection 수행하여 결과를 cvout으로 반환 합니다.
    cv_out = cv_net.forward().tolist()

    # response의 "cvout"에 결과를 저장하고 성공적으로 수행했다는 것을 success에 True로 바꿉니다.
    response['cvout'] = cv_out
    response['success'] = True

    # json형태로 반환합니다.
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))