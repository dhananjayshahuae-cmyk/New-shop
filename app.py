from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# HTML और CSS फ़्रंटएंड टेम्पलेट
HTML_STORE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Shoe Store</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f0f12; color: #ffffff; text-align: center; padding: 20px; margin: 0; }
        .store-card { max-width: 360px; margin: 40px auto; background: #1a1a24; padding: 24px; border-radius: 12px; box-shadow: 0 8px 30px rgba(0,0,0,0.5); border: 1px solid #2a2a3a; }
        .shoe-image { width: 100%; border-radius: 12px; height: 220px; object-fit: cover; }
        h1 { color: #ffffff; font-size: 28px; margin-bottom: 5px; }
        h2 { margin: 15px 0 5px 0; font-size: 24px; color: #ffd757; }
        .price-tag { font-size: 22px; color: #2ed573; font-weight: bold; margin: 10px 0; }
        
        /* Payment Form Styling */
        .payment-form { display: flex; flex-direction: column; gap: 12px; margin-top: 20px; text-align: left; }
        .input-group { display: flex; flex-direction: column; gap: 5px; }
        label { font-size: 12px; color: #a4b0be; text-transform: uppercase; font-weight: bold; }
        input { background: #252532; border: 1px solid #3b3b4f; padding: 12px; border-radius: 6px; color: white; font-size: 14px; outline: none; }
        input:focus { border-color: #ffd757; }
        .row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
        
        .checkout-btn { background: #ff4757; color: white; border: none; padding: 14px; width: 100%; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; margin-top: 10px; }
        .checkout-btn:hover { background: #ff2a3b; }
        .secure-notice { font-size: 11px; color: #a4b0be; margin-top: 15px; display: block; text-align: center; }
    </style>
</head>
<body>

    <h1>Premium Shoe Store</h1>
    <p style="color: #a4b0be;">Direct 2D Card Checkout (No OTP Required)</p>

    <div class="store-card">
        <!-- डमी शू इमेज (Unsplash से) -->
        <img src="https://unsplash.com" alt="Running Shoes" class="shoe-image">
        <h2>Speed Runner Pro</h2>
        <div class="price-tag">$149.00</div>

        <!-- 2D Payment Gateway Form -->
        <form id="paymentForm" class="payment-form">
            <div class="input-group">
                <label>Cardholder Name</label>
                <input type="text" id="cardName" placeholder="John Doe" required>
            </div>
            
            <div class="input-group">
                <label>Card Number</label>
                <input type="text" id="cardNumber" placeholder="4111 2222 3333 4444" maxlength="19" required>
            </div>

            <div class="row">
                <div class="input-group">
                    <label>Expiry Date</label>
                    <input type="text" id="cardExpiry" placeholder="MM/YY" maxlength="5" required>
                </div>
                <div class="input-group">
                    <label>CVV (2D Auth)</label>
                    <input type="password" id="cardCvv" placeholder="123" maxlength="3" required>
                </div>
            </div>

            <button type="submit" class="checkout-btn">Pay Now $149.00</button>
            <span class="secure-notice">🔒 Secure 2D API Merchant Server Connection</span>
        </form>
    </div>

    <!-- AJAX Script से बिना पेज रीलोड किए पेमेंट रिस्पांस दिखाने के लिए -->
    <script>
        document.getElementById('paymentForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const payload = {
                name: document.getElementById('cardName').value,
                number: document.getElementById('cardNumber').value,
                expiry: document.getElementById('cardExpiry').value,
                cvv: document.getElementById('cardCvv').value,
                amount: 149.00
            };

            // सर्वर के 2D API एंडपॉइंट पर डेटा भेजना
            const response = await fetch('/process-2d-payment', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            
            if(result.status === "SUCCESS") {
                alert(`🎉 Payment Successful!\\nTransaction ID: ${result.transaction_id}\\nStatus: 2D Auth Passed.`);
            } else {
                alert(`❌ Payment Failed: ${result.message}`);
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_STORE)

# 2D Payment Gateway API Logic
@app.route('/process-2d-payment', []'POST'])
def process_payment():
    data = request.get_json()
    
    card_number = data.get('number', '').replace(' ', '')
    cvv = data.get('cvv', '')
    expiry = data.get('expiry', '')
    amount = data.get('amount')

    # असली 2D गेटवे में यहाँ मर्चेंट (जैसे Stripe, Authorize.Net, या कोई इंटरनेशनल मर्चेंट) की API पर बिना OTP के डायरेक्ट हिट मारी जाती है।
    # सुरक्षा के लिए यहाँ एक बेसिक वैलिडेशन लॉजिक लगाया गया है:
    if len(card_number) >= 15 and len(cvv) == 3 and '/' in expiry:
        return jsonify({
            "status": "SUCCESS",
            "message": "Charge successful via 2D Gateway",
            "transaction_id": "TXN_2D_984321074",
            "amount_charged": amount
        }), 200
    else:
        return jsonify({
            "status": "FAILED",
            "message": "Invalid Card Details or 2D Authentication Declined"
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
