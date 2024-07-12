for file in `ls examples/`
do
  tesseract \
    examples/$file \
    detections-$file \
    hocr
done
