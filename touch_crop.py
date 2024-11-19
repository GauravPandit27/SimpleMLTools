import cv2
import os

# Function to draw ROI and save or cancel
def manual_crop(image_path, save_path):
    img = cv2.imread(image_path)
    roi = None

    # Callback function for drawing the rectangle
    def select_roi(event, x, y, flags, param):
        nonlocal roi, img_copy
        if event == cv2.EVENT_LBUTTONDOWN:
            roi = [(x, y)]
        elif event == cv2.EVENT_LBUTTONUP:
            roi.append((x, y))
            cv2.rectangle(img_copy, roi[0], roi[1], (0, 255, 0), 2)
            cv2.imshow("Image", img_copy)

    img_copy = img.copy()

    # Use namedWindow to enable window resizing
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Image", img_copy)
    cv2.setMouseCallback("Image", select_roi)

    while True:
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            # Clear the ROI, redraw
            img_copy = img.copy()
            roi = None
            cv2.imshow("Image", img_copy)
        
        elif key == ord('a'):  # Press 'a' to skip the image
            print(f"Skipping: {image_path}")
            break

        elif key == ord('d'):  
            if roi:
                # Crop and save the image
                x1, y1 = roi[0]
                x2, y2 = roi[1]
                cropped_img = img[y1:y2, x1:x2]

                # Ensure save directory exists
                if not os.path.exists(save_path):
                    os.makedirs(save_path)

                save_file = os.path.join(save_path, os.path.basename(image_path))
                cv2.imwrite(save_file, cropped_img)
                print(f"Image saved at: {save_file}")
                break

        elif key == 27:  # Esc key to quit
            break

    cv2.destroyAllWindows()

# Function to process folders recursively
def process_folders(image_folder, save_folder):
    for root, dirs, files in os.walk(image_folder):
        # Get relative path to maintain folder structure
        rel_path = os.path.relpath(root, image_folder)
        save_dir = os.path.join(save_folder, rel_path)

        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):  # Add supported image formats
                img_path = os.path.join(root, file)
                print(f"Processing: {img_path}")
                manual_crop(img_path, save_dir)

# Example usage
image_folder = "/home/gpandit/Videos/glenmark/perfect_cap"       # Root folder containing images in subfolders
save_folder = "/home/gpandit/Videos/glenmark/perfect_cap/Ok_output"  # Root folder to save cropped images

# Process all images in the folder structure
process_folders(image_folder, save_folder)

