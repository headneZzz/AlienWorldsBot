import pyotp
totp = pyotp.TOTP("Z4FOEYKOI3IYGXSE")
print("Current OTP:", totp.now())