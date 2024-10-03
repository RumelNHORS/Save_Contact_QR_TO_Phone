from django.shortcuts import render
import qrcode
from io import BytesIO
from django.http import HttpResponse
import base64

def generate_qr_code(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        # Create a vCard format
        vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\nTEL:{phone}\nEMAIL:{email}\nEND:VCARD"

        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(vcard_data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save QR code image to in-memory file
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        # Encode the QR code image to base64
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Store the base64 string in the session
        request.session['qr_code'] = qr_code_base64

        # Return the QR code image for display
        return render(request, 'generate_qr.html', {'qr_code_generated': True})

    return render(request, 'generate_qr.html')

def download_qr_code(request):
    if 'qr_code' in request.session:
        response = HttpResponse(base64.b64decode(request.session['qr_code']), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename="qr_code.png"'
        return response
    else:
        return HttpResponse("No QR code found.")
