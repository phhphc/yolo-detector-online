import tempfile
from django.shortcuts import redirect, render
from base64 import b64encode

from .forms import ImageForm
from yolo.yolo import predict_image

predict_extd = '.jpg'


def home_view(request):
    form = ImageForm()
    return render(
        request,
        'yolo_detector/index.html',
        {
            'form': form
        })
    
    
def detect_view(request):
    if request.method == "POST":
        input_file = request.FILES.get("image")
        if input_file is not None:
            # temporary save image to disk
            fp = tempfile.NamedTemporaryFile()
            for chunk in input_file.chunks():
                fp.write(chunk)
            # predict image
            success, buffer = predict_image(fp.name, predict_extd)
            # convert to base64
            if success:
                img_src = f"data:image/{predict_extd[1:]};base64, {b64encode(buffer).decode()}"

            return render(
                request,
                'yolo_detector/detect.html',
                {
                    'img_src': img_src,
                })
    
    return redirect('yolo_detector_home')
