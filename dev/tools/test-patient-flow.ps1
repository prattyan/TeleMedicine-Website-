# Test Patient Registration and Login Flow
Write-Host "Testing Patient Registration and Login Flow..." -ForegroundColor Green

# Test patient registration
Write-Host "`n1. Testing Patient Registration..." -ForegroundColor Yellow
$registerResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/auth/register/patient" -Method POST -ContentType "application/json" -Body '{"name":"Live Data Test","age":28,"gender":"female","village":"Test City","phone":"8888777666"}'
Write-Host "Registration Response:" -ForegroundColor Cyan
$registerResponse | ConvertTo-Json

# Test patient login
Write-Host "`n2. Testing Patient Login..." -ForegroundColor Yellow  
$loginResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/auth/login/patient" -Method POST -ContentType "application/json" -Body '{"phone":"8888777666"}'
Write-Host "Login Response:" -ForegroundColor Cyan
$loginResponse | ConvertTo-Json

# Test profile API
Write-Host "`n3. Testing Profile API..." -ForegroundColor Yellow
$token = $loginResponse.token
$headers = @{ "Authorization" = "Bearer $token" }
$profileResponse = Invoke-RestMethod -Uri "http://localhost:4000/api/me" -Method GET -Headers $headers
Write-Host "Profile Response:" -ForegroundColor Cyan
$profileResponse | ConvertTo-Json -Depth 3

Write-Host "`n✅ Test completed successfully!" -ForegroundColor Green
Write-Host "You can now use this token to test the patient-landing page:" -ForegroundColor Magenta
Write-Host "Token: $token" -ForegroundColor White