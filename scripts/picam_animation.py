#!/usr/bin/env python
import os
import time
import settings
import picamera


def cam_settings(camera):
    for k, param in getattr(settings, 'PICAM_PARAMS', None):
        setattr(camera, k, param)


def capture_animated_gif(capture):
    cwd = os.getcwd()
    if not os.path.exists(cwd+"/images"):
        os.makedirs(cwd+"/images")

    with picamera.PiCamera() as camera:
        cam_settings(camera)

        camera.start_preview()

        start = time.time()
        # let the camera warm up.
        time.sleep(capture['interval'])
        # capture 10 frames.
        camera.capture_sequence((
            'images/image%04d.png' % i
            for i in range(capture['images'])
            ), use_video_port=True, format='png')
        fps = capture['images'] / (time.time() - start)
        print('Captured 10 images at %.2ffps' % fps)
        camera.stop_preview()


if __name__ == '__main__':
    try:
        PICAM_CAPTURE = getattr(settings, 'PICAM_CAPTURE', None)
        capture_animated_gif(PICAM_CAPTURE)
    except Exception as e:
        print 'Error: %s' % e
