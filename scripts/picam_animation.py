#!/usr/bin/env python
import os
import time
import settings
import picamera


def cam_settings(camera):
    for k, param in getattr(settings, 'PICAM_PARAMS', None).items():
        setattr(camera, k, param)


def capture_animated_gif(capture):
    cwd = os.getcwd()
    images_dir = os.path.join(cwd, '..', 'images')

    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

    for the_file in os.listdir(images_dir):
        file_path = os.path.join(images_dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

    with picamera.PiCamera() as camera:
        cam_settings(camera)

        camera.start_preview()

        start = time.time()
        # let the camera warm up.
        time.sleep(capture['interval'])
        # capture 10 frames.
        camera.capture_sequence((
            '../images/image%04d.png' % i
            for i in range(capture['images'])
            ), use_video_port=True, format='png')
        fps = capture['images'] / (time.time() - start)
        print('Captured %s images at %.2ffps' % (capture['images'], fps))
        camera.stop_preview()

        os.system('convert -delay 30 ../images/*.png ../images/animation.gif')


if __name__ == '__main__':
    try:
        PICAM_CAPTURE = getattr(settings, 'PICAM_CAPTURE', None)
        capture_animated_gif(PICAM_CAPTURE)
    except Exception as e:
        print 'Error: %s' % e
