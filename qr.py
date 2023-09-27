import qrcode
from PIL import Image

# Sample product information
product_id = "12345"
status = "Shipped"

# Combine product information into a string
product_info = f"Product ID: {product_id}\nStatus: {status}"

# Generate a QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(product_info)
qr.make(fit=True)

# Create a QR code image
qr_img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code to a file (optional)
qr_img.save("product_qr.png")

# Display the QR code (optional)
qr_img.show()
