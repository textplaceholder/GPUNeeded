from ultralytics import YOLO


image_directory = 'C:/Users/ADMIN/Downloads/projects/projects/face-recog/dataset/1'
output_directory = 'C:/Users/ADMIN/Downloads/projects/projects/face-recog/dataset/annotate/1'
model = YOLO('trained_model.pt')


model.train(
    data='data.yaml',
    epochs=200,                
    imgsz=640,                 
    batch=50,                  
    name='trained_model'
)

"""
for filename in os.listdir(image_directory):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        image_path = os.path.join(image_directory, filename)
        
        # Perform inference
        results = model(image_path)

        # Save the annotated image
        annotated_image_path = os.path.join(output_directory, f'annotated_{filename}')
        results[0].save(annotated_image_path)

        # Save the annotations in YOLO format
        annotation_path = os.path.join(output_directory, f'{os.path.splitext(filename)[0]}.txt')
        with open(annotation_path, 'w') as f:
            for result in results[0].boxes:
                # Get class (0 for person) and bounding box
                class_id = int(result.cls[0])  # assuming class_id 0 is for humans
                x_center = result.xyxy[0][0] + (result.xyxy[0][2] - result.xyxy[0][0]) / 2  # x_center
                y_center = result.xyxy[0][1] + (result.xyxy[0][3] - result.xyxy[0][1]) / 2  # y_center
                width = result.xyxy[0][2] - result.xyxy[0][0]  # width
                height = result.xyxy[0][3] - result.xyxy[0][1]  # height

                # Normalize the coordinates
                x_center /= results[0].orig_shape[1]  # normalize x_center
                y_center /= results[0].orig_shape[0]  # normalize y_center
                width /= results[0].orig_shape[1]  # normalize width
                height /= results[0].orig_shape[0]  # normalize height

                f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

print("Annotation complete.")
"""