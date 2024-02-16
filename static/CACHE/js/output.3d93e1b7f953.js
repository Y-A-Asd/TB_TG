function displayErrorMessage(message){const errorMessageElement=document.getElementById('errorMessage');errorMessageElement.textContent=message;}
function getToken(){return localStorage.getItem('JWT');}
function makeAuthenticatedRequest(url,method,context=null){const token=getToken();const headers={'Content-Type':'application/json',};if(token){headers['Authorization']=`JWT ${token}`;}
const options={method:method,headers:headers,body:context?JSON.stringify(context):null,};console.log(options)
return fetch(url,options).then(response=>{console.log(response)
if(response.ok){return response.json()}else{return response.json().then(errorJson=>{alert(JSON.stringify(errorJson))
throw new Error(JSON.stringify(errorJson));});}}).catch(error=>{displayErrorMessage(error);console.error('eeeeeee',error);});}
function verifyToken(){const token=getToken();if(token){const endpoint='/core/auth/jwt/verify/';makeAuthenticatedRequest(endpoint,'POST',context={token:token}).then(response=>{console.log(response);if(response.code==='token_not_valid'){console.log('Token not valid. User needs to log in.');}else{console.log('Token is valid. User is already logged in.');alert('Token is valid. User is already logged in.')
window.location.href='/';}}).catch(error=>{console.error('Error:',error);});}else{console.log('No token found. User needs to log in.');}}
window.onload=function(){verifyToken();};document.getElementById('loginForm').addEventListener('submit',function(event){event.preventDefault();let otp=document.getElementById('content')
let email=localStorage.getItem('email');console.log(otp.value)
console.log(email)
let endpoint='/core/verify-otp/';makeAuthenticatedRequest(endpoint,'POST',context={'email':email,'otp':otp.value}).then(data=>{if(data){console.log(data);alert('Your account is active now please login!')
window.location.href='/login';}}).catch(error=>{console.error('Error:',error);});});;