import cv2
from pyzbar.pyzbar import decode

def draw_barcode_info(frame, barcodes):
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Put text
        text = f'{barcode_data} ({barcode_type})'
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        
        # Also print on terminal
        print(f'Detected barcode: {barcode_data} (Type: {barcode_type})')

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Could not open webcam")
        return

    print("Scanning... Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect barcodes in the frame
        barcodes = decode(frame)

        if barcodes:
            draw_barcode_info(frame, barcodes)

        # Show live feed
        cv2.imshow("Barcode Scanner", frame)

        # Quit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
